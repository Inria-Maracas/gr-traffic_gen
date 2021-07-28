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
import struct
from gnuradio import gr
import socket
import threading

class trigger(gr.sync_block):
    """
    docstring for block trigger
    """
    def __init__(self, ip_addr, port, tag_name, margin):
        gr.sync_block.__init__(self,
            name="trigger",
            in_sig=[np.complex64, ],
            out_sig=[np.complex64, ])


        self.ip_addr = ip_addr
        self.port = port
        self.tag_name = tag_name
        self.margin = margin
        self.message_port_register_out(pmt.intern("resamp"))
        self.message_port_register_out(pmt.intern("freq"))

        self.pack_start = False
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
            self.samples_to_send = int(recieved[0] + self.margin)
            self.resamp_ratio = recieved[1]
            self.freq_shift = recieved[2]
            self.pack_start = True
            print(f"Transmitting packet len = {self.samples_to_send}")

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        if self.pack_start:
            print("sending",self.samples_to_send)
            a = pmt.make_dict()
            a = pmt.dict_add(a, pmt.intern("resamp_ratio"), pmt.from_float(self.resamp_ratio))
            self.message_port_pub(pmt.intern("resamp"),a)
            self.add_item_tag(0, self.nitems_written(0), pmt.intern("resamp_ratio"), pmt.from_float(self.resamp_ratio))
            self.add_item_tag(0, self.nitems_written(0), pmt.intern(self.tag_name), pmt.to_pmt(int(self.samples_to_send/self.resamp_ratio)))
            self.pack_start = False

        to_copy = min(self.samples_to_send, in0.shape[0])

        out[:to_copy] = in0[:to_copy]
        self.samples_to_send -= to_copy

        return to_copy
