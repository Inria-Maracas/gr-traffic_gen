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
import pmt
from gnuradio import gr
import socket
import threading

class trigger(gr.sync_block):
    """
    docstring for block trigger
    """
    def __init__(self, ip_addr, port, tag_name, margin, modulation_name, modulation_id, samp_rate):
        gr.sync_block.__init__(self,
            name="trigger",
            in_sig=[np.complex64, ],
            out_sig=[np.complex64, ])

        self.ip_addr = ip_addr
        self.port = port + modulation_id
        self.tag_name = tag_name
        self.margin = margin
        self.mod_name = modulation_name
        self.mod_id = modulation_id
        self.samp_rate = samp_rate
        self.message_port_register_out(pmt.intern("resamp"))
        self.message_port_register_out(pmt.intern("freq"))

        self.pack_start = False
        self.mod_to_send = 0
        self.samples_to_send = 0
        self.resamp_ratio = 1
        self.freq_shift = 1

        print("Init")
        self.socket_thread = threading.Thread(target=self.handle_packet)
        self.socket_thread.daemon = True
        self.socket_thread.start()

    def set_margin(self, new_marg):
        self.margin = new_marg

    def handle_packet(self):
        # initialize a socket, think of it as a cable
        # SOCK_DGRAM specifies that this is UDP
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.s.bind((self.ip_addr,self.port))
        print("Listening")
        while 1:
            data = self.s.recv(100)
            recieved = np.fromstring(data, dtype=np.float64)
            self.mod_to_send = recieved[3]
            if self.mod_to_send == self.mod_id:
                self.resamp_ratio = recieved[1]
                self.freq_shift = recieved[2]
                self.samples_to_send = int((recieved[0] + 2*self.margin) * self.resamp_ratio)
                self.pack_start = True
                print(f"Trigger : WANTED {self.mod_name} packet len = {recieved[0]}, resamp={self.resamp_ratio} \n")

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        if self.pack_start:
            print("Trigger start sending",self.samples_to_send)
            a = pmt.make_dict()
            a = pmt.dict_add(a, pmt.intern("resamp_ratio"), pmt.from_float(self.resamp_ratio))
            self.message_port_pub(pmt.intern("resamp"),a)
            b = pmt.make_dict()
            b = pmt.dict_add(b, pmt.intern("freq"), pmt.from_float(self.freq_shift * (self.samp_rate/2)))
            self.message_port_pub(pmt.intern("freq"),b)
            self.add_item_tag(0, self.nitems_written(0), pmt.intern("resamp_ratio"), pmt.from_float(self.resamp_ratio))
            self.add_item_tag(0, self.nitems_written(0), pmt.intern(self.tag_name), pmt.from_uint64((self.samples_to_send)))
            self.add_item_tag(0, self.nitems_written(0), pmt.intern("mod_name"), pmt.intern(self.mod_name))
            self.add_item_tag(0, self.nitems_written(0), pmt.intern("freq_shift"), pmt.from_float(self.freq_shift))
            # self.add_item_tag(0, self.nitems_written(0), pmt.intern("burst"), pmt.to_pmt(True))
            # self.add_item_tag(0, self.nitems_written(0)+int(self.samples_to_send-1), pmt.intern("burst"), pmt.to_pmt(False))
            self.pack_start = False

        to_copy = min(self.samples_to_send, len(in0))
        

        out[:to_copy] = in0[:to_copy]
        self.samples_to_send -= to_copy
        self.consume(0, to_copy)

        #if (to_copy != 0) :
        #    print("Trigger - sending : ",to_copy, " - remain : ", self.samples_to_send, " - inpt length : ", len(in0))

        return to_copy
