#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 gr-traffic_gen author.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#


import numpy as np
from gnuradio import gr
import pmt
from sigmf import SigMFFile, sigmffile
import os
import collections as col

class labelisator(gr.sync_block):
    """
    docstring for block labelisator
    """
    def __init__(self, file_name, tag_name, head_margin, number_of_samples):
        gr.sync_block.__init__(self,
            name="labelisator",
            in_sig=[np.complex64, ],
            out_sig=None)

        self.m_file_name = file_name
        self.m_tag_name = tag_name
        self.m_head_margin = head_margin
        self.m_number_of_samples = number_of_samples

        self.m_dict_annotation = []

        self.m_data_sigmf_file = "%s.sigmf-data" % (self.m_file_name)
        self.count = 0



    def write_sigmf_meta(self):
        meta = SigMFFile(
            data_file='%s.sigmf-data' % (self.m_file_name), # extension is optional
            global_info = {
                SigMFFile.DATATYPE_KEY: 'cf32_le',
                SigMFFile.SAMPLE_RATE_KEY: 1
            }
        )

        meta.add_capture(0, metadata={
            SigMFFile.START_INDEX_KEY: 0,
            SigMFFile.LENGTH_INDEX_KEY: self.m_number_of_samples,
            SigMFFile.FREQUENCY_KEY: 0
        })

        for annotation in self.m_dict_annotation:
            meta.add_annotation(annotation["sample_start"], annotation["sample_count"], metadata = {
                    SigMFFile.FLO_KEY: annotation["freq_low"],
                    SigMFFile.FHI_KEY: annotation["freq_up"],
                    SigMFFile.DESCRIPTION_KEY: annotation["mod"],
                })

        meta.validate()
        meta.tofile(self.m_file_name)

    def work(self, input_items, output_items):
        self.count += len(input_items[0])
        input_items[0].tofile(self.m_data_sigmf_file)
        tags = self.get_tags_in_window(0, 0, len(input_items[0]))
        
        if len(tags) >= 4 :

            bw = 0
            freq_shift = 0
            sample_count = 0
            modulation = None
            
            for tag in tags:
                key = pmt.to_python(tag.key) 
                value = pmt.to_python(tag.value)
                offset = tag.offset
                

                if key == self.m_tag_name :
                    sample_count = value
                elif key == "resamp_ratio":
                    bw = value
                elif key == "mod_name":
                    modulation = value
                elif key == "freq_shift":
                    freq_shift = value
                else:
                    print("Label : Unknown label - {key} / {value} \n")
            
            freq_low = 0 + freq_shift - (bw / 2)
            freq_up = 0 + freq_shift + (bw / 2)
            sample_start = self.nitems_read(0) + offset + self.m_head_margin
            if sample_start + sample_count <= self.m_number_of_samples:
                sample_count = self.m_number_of_samples - sample_start

            self.m_dict_annotation.append({"freq_low" : freq_low, "freq_up" : freq_up, "sample_start" : sample_start, "sample_count" : sample_count, "mod" : modulation})
            print("Label : TAG annotation received \n")

        for tag in tags:
            if pmt.to_python(tag.key) == "end":
                self.write_sigmf_meta()
                print("Meta data generated")

        self.consume(0,len(input_items[0]))

        return 0

