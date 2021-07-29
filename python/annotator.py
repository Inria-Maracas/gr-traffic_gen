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

class annotator(gr.sync_block):
    """
    docstring for block annotator
    """
    def __init__(self, ip_addr, port, tag_name, delay):
        gr.sync_block.__init__(self,
            name="annotator",
            in_sig=[np.complex64, ],
            out_sig=[np.complex64, ])

        self.ip_addr = ip_addr
        self.port = port
        self.tag_name = tag_name
        self.delay = delay

        print("Init")
        self.socket_thread = threading.Thread(target=self.handle_packet)
        self.socket_thread.daemon = True
        self.socket_thread.start()

    def set_delay(self, new_delay):
        self.delay = new_delay

    def handle_packet(self):
        # initialize a socket, think of it as a cable
        # SOCK_DGRAM specifies that this is UDP
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.s.bind((self.ip_addr,self.port))
        print("Listening")
        while 1:
            data = self.s.recv(100)
            recieved = np.fromstring(data, dtype=np.float64)
            self.modulation = int(recieved[0])
            self.samples_to_send = int(recieved[1])
            self.resamp_ratio = recieved[2]
            self.freq_shift = recieved[3]
            print(f"Transmitting packet len = {self.samples_to_send}")

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>

        self.add_item_tag(0, self.nitems_written(0)+self.delay, pmt.intern(self.tag_name), pmt.from_float(self.resamp_ratio))
        out[:] = in0
        return len(output_items[0])
