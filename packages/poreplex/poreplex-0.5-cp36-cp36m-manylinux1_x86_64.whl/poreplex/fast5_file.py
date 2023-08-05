#!/usr/bin/env python3
#
# Copyright (c) 2019 Institute for Basic Science
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import h5py
import numpy as np
import pandas as pd
from scipy.signal import medfilt
from functools import lru_cache
import os.path

__all__ = ['get_read_ids', 'Fast5Reader', 'DuplicatedReadError']

class DuplicatedReadError(Exception):
    pass


def get_read_ids(filename, basedir):
    if basedir is not None:
        fast5path = os.path.join(basedir, filename)
    else:
        fast5path = filename

    with h5py.File(fast5path, 'r') as f5file:
        if 'UniqueGlobalKey' in f5file:
            # Single-read FAST5
            try:
                first_read = next(iter(f5file['Raw/Reads'].values()))
                return [(filename, first_read.attrs['read_id'].decode())]
            except KeyError:
                return []

        # Multi-read FAST5
        reads = []
        for node in f5file:
            if node.startswith('read_'):
                reads.append((filename, node[5:]))

        return reads


class Fast5Reader:

    RAWSIGNAL_PREFILTER_SIZE = 5 # applied only when loading events from guppy

    def __init__(self, path, read_id):
        self.path = path
        self.read_id = read_id
        self.handle = h5py.File(path, 'r')

        self.is_multiread = 'UniqueGlobalKey' not in self.handle
        if self.is_multiread:
            self.read_node = 'read_{}/Raw'.format(read_id)
            self.channel_node = 'read_{}/channel_id'.format(read_id)
            self.tracking_node = 'read_{}/tracking_id'.format(read_id)
            self.analyses_node = 'read_{}/Analyses'.format(read_id)
        else:
            first_read_name = next(iter(self.handle['Raw/Reads'].keys()))

            self.read_node = 'Raw/Reads/' + first_read_name
            self.channel_node = 'UniqueGlobalKey/channel_id'
            self.tracking_node = 'UniqueGlobalKey/tracking_id'
            self.analyses_node = 'Analyses'

        self.load_metadata()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def close(self):
        if self.handle is not None:
            self.handle.close()
            self.handle = None

    def load_metadata(self):
        # Raw/Reads/Read_*
        sigattrs = self.handle[self.read_node].attrs
        self.duration = int(sigattrs['duration'])
        self.start_time = int(sigattrs['start_time'])
        file_read_id = sigattrs['read_id'].decode()
        if self.read_id is None:
            self.read_id = file_read_id
        elif file_read_id != self.read_id:
            raise ValueError('Unexpected read {} found in {}'.format(
                             file_read_id, self.path))

        # UniqueGlobalKey/channel_id
        chanattrs = self.handle[self.channel_node].attrs
        self.channel_number = chanattrs['channel_number'].decode()
        self.digitization = float(chanattrs['digitisation'])
        self.offset = float(chanattrs['offset'])
        self.range = float(chanattrs['range'])
        self.sampling_rate = float(chanattrs['sampling_rate'])

        # UniqueGlobalKey/tracking_id
        trackattrs = self.handle[self.tracking_node].attrs
        self.run_id = trackattrs['run_id'].decode()
        self.sample_id = trackattrs['sample_id'].decode()

    def get_raw_data(self, start=None, end=None):
        rawsignode = self.handle[self.read_node + '/Signal']
        if end is None or end > len(rawsignode):
            end = len(rawsignode)
        if start is None:
            start = 0
        rawsignal = rawsignode[start:end]

        return np.array(self.range / self.digitization * (rawsignal + self.offset),
                        dtype=np.float32)

    def get_basecall(self, analysis_group='Basecall_1D'):
        try:
            analnode = self.handle[self.analyses_node]
        except KeyError:
            return

        analgroups = [name for name in analnode.keys() if name.startswith(analysis_group)]
        if len(analgroups) < 1:
            return

        analyses = analnode[max(analgroups)]
        groupno = analyses.name.rsplit('_', 1)[-1]
        segattrs = analnode['Segmentation_{}/Summary/segmentation'.format(groupno)].attrs
        summary = {}

        # Sequence and quality scores
        fastqenc = analyses['BaseCalled_template/Fastq'][()].decode().split('\n')
        summary['sequence'] = fastqenc[1]
        summary['qstring'] = fastqenc[3]

        # Basecall stats
        summaryattrs = analyses['Summary/{}_template'.format(analysis_group.lower())].attrs
        summary['block_stride'] = int(summaryattrs.get('block_stride', 15))
        summary['sequence_length'] = int(summaryattrs['sequence_length'])
        summary['mean_qscore'] = float(summaryattrs['mean_qscore'])
        summary['num_events'] = int(segattrs['num_events_template'])
        summary['first_sample_template'] = int(segattrs['first_sample_template'])

        # Events mapping
        summary['events'] = self.load_events(analyses, summary)

        return summary

    def load_events(self, analyses, summary):
        if 'BaseCalled_template/Events' in analyses:
            # `Events' is available in guppy < 2.3.7 and albacore
            evdf = pd.DataFrame(analyses['BaseCalled_template/Events'][()])
        elif 'BaseCalled_template/Move' in analyses:
            # `Move' is available in guppy >= 2.3.7
            evdf = self.construct_events_from_moves(analyses, summary)
        else:
            raise Exception("Neither `Events' or `Move' table found in the basecall.")

        if len(evdf.columns) <= 3 and 'move' in evdf.columns: # ONT Guppy
            return self.convert_events_guppy(evdf, summary)
        elif len(evdf.columns) == 14: # ONT albacore >= 2.3.0
            return evdf
        else:
            raise Exception('Unsupported event table found.')

    def construct_events_from_moves(self, analyses, summary):
        moves = analyses['BaseCalled_template/Move'][()]
        pos = moves.cumsum() - 1
        kmer_size = len(summary['sequence']) - int(moves.sum()) + 1
        revseq = summary['sequence'][::-1].replace('U', 'T')
        qual = 1 - 10 ** -((np.frombuffer(summary['qstring'].encode(), 'B') - 33) / 10)

        if kmer_size == 5: # Guppy old models
            posshift = 2
        elif kmer_size == 1: # Guppy flip-flop models
            # Translate the 1-mer frames to 5-mer's for compatibility
            revseq = '__' + revseq + '__'
            posshift = 0
        else:
            raise Exception("Move table is encoded with an unknown kmer-size.")

        kmergetter = lambda x: revseq[int(x):int(x) + 5]
        seqgetter = lru_cache(3)(kmergetter)

        qualgetter = lru_cache(3)(lambda x, p=posshift: qual[int(x) + posshift])

        return pd.DataFrame({
            'model_state': np.vectorize(seqgetter)(pos),
            'p_model_state': np.vectorize(qualgetter)(pos),
            'move': moves
        })

    def convert_events_guppy(self, events, summary):
        first_sample = summary['first_sample_template']
        block_stride = summary['block_stride']
        last_sample = first_sample + block_stride * len(events) # non-inclusive

        events['start'] = np.arange(first_sample, last_sample, block_stride)

        rawdata = self.get_raw_data(first_sample, last_sample)
        rawdata = medfilt(rawdata, self.RAWSIGNAL_PREFILTER_SIZE)
        if len(rawdata) % block_stride > 0:
            rawdata = np.pad(rawdata, [0, block_stride - len(rawdata) % block_stride],
                             'constant', constant_values=[np.nan, np.nan])
        if len(rawdata) // block_stride != len(events):
            raise Exception('Numbers of events and raw data strides does not match.')

        sigbyevents = rawdata.reshape([len(events), block_stride])
        events['mean'] = sigbyevents.mean(axis=1)
        events['stdv'] = sigbyevents.std(axis=1)
        events['length'] = block_stride

        return events

    def copyto(self, dstfile):
        nodepath = 'read_' + self.read_id

        if self.is_multiread:
            try:
                dstfile.copy(self.handle[nodepath], dstfile, nodepath)
                return
            except RuntimeError as exc:
                if 'destination object already exists' in exc.args[0]:
                    raise DuplicatedReadError(exc.args[0])
                raise

        if nodepath in dstfile:
            raise DuplicatedReadError("Duplicated read '{}' found.".format(self.read_id))

        try:
            dstgrp = dstfile.create_group(nodepath)
        except ValueError as exc:
            raise Exception("Failed to create read '{}'.".format(self.read_id))

        dstgrp.attrs['run_id'] = self.run_id

        # Copy Raw signal to new file
        dstgrp.copy(self.handle[self.read_node], 'Raw')

        # Copy UniqueGlobalKey to new file
        for grpname, grpobj in self.handle['UniqueGlobalKey'].items():
            dstgrp.copy(grpobj, dstgrp, grpname)

        # Copy other groups
        for grpname, grpobj in self.handle.items():
            if grpname not in ("Raw", "UniqueGlobalKey"):
                dstgrp.copy(grpobj, grpname)

