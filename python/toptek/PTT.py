#!/usr/bin/env python
# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2024 Swarnava Ghosh
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#


import numpy
from gnuradio import gr
import pmt
import time
import sys

class PTT(gr.sync_block):
    """
    docstring for block PTT
    """
    def __init__(self, baud_rate=9600, padding_nbytes=0, delay_s=0, extra_s=0):
        gr.sync_block.__init__(self,
            name="PTT",
            in_sig=None,
            out_sig=None)
        self.baud_rate = baud_rate
        self.padding_nbytes = padding_nbytes
        self.delay = delay_s
        self.extra = extra_s
        self.message_port_register_in(pmt.intern('tx_msg'))
        self.message_port_register_out(pmt.intern('tx_amp'))
        self.message_port_register_out(pmt.intern('tx_vga_gain'))
        self.message_port_register_out(pmt.intern('pa'))
        self.message_port_register_out(pmt.intern('da'))
        self.message_port_register_out(pmt.intern('lna'))
        self.set_msg_handler(pmt.intern('tx_msg'), self.handle_msg)
        self.message_port_pub(
            pmt.intern('pa'),
            pmt.cons(pmt.PMT_NIL, pmt.PMT_T))
        self.message_port_pub(
            pmt.intern('lna'),
            pmt.cons(pmt.PMT_NIL, pmt.PMT_T))

    def handle_msg(self, msg):
        msg = pmt.cdr(msg)
        msg = pmt.u8vector_elements(msg)
        length = (len(msg)+self.padding_nbytes)*8
        tx_time = length/self.baud_rate + self.extra
        time.sleep(self.delay)
        # self.amp.da_on()
        self.message_port_pub(
            pmt.intern('da'),
            pmt.cons(pmt.PMT_NIL, pmt.PMT_T))
        # self.message_port_pub(
        #    pmt.intern("tx_amp"),
        #    pmt.cons(pmt.intern("tx_amp"), pmt.PMT_T))
        # self.message_port_pub(
        #    pmt.intern("tx_vga_gain"),
        #    pmt.cons(pmt.intern("tx_vga_gain"), pmt.to_pmt(47)))
        time.sleep(tx_time)
        self.message_port_pub(
            pmt.intern('da'),
            pmt.cons(pmt.PMT_NIL, pmt.PMT_F))
        # self.amp.da_off()
        #self.message_port_pub(
        #    pmt.intern("tx_amp"),
        #    pmt.cons(pmt.intern("tx_amp"), pmt.PMT_F))
        #self.message_port_pub(
        #    pmt.intern("tx_vga_gain"),
        #    pmt.cons(pmt.intern("tx_vga_gain"), pmt.to_pmt(0)))

    def work(self, input_items, output_items):
        return 0

