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
from toptek import Toptek

class toptek_control(gr.basic_block):
    """
    Control Toptek Amplifier
    """
    def __init__(self, serial_port:str='/dev/ttyAmplifier', pa:bool=False, lna:bool=False, da:bool=False, tx_pwr:int=0, verbose:bool=False):
        gr.basic_block.__init__(self,
            name="Toptek Control",
            in_sig=None,
            out_sig=None)
        self.verbose = verbose
        self.amp = Toptek(serial_port)
        self.message_port_register_in(pmt.intern('pa'))
        self.message_port_register_in(pmt.intern('da'))
        self.message_port_register_in(pmt.intern('lna'))
        self.message_port_register_in(pmt.intern('tx_pwr'))
        self.message_port_register_in(pmt.intern('ptt'))
        self.set_msg_handler(pmt.intern('pa'), self.pa_handler)
        self.set_msg_handler(pmt.intern('da'), self.da_handler)
        self.set_msg_handler(pmt.intern('lna'), self.lna_handler)
        self.set_msg_handler(pmt.intern('tx_pwr'), self.tx_pwr_handler)
        self.set_msg_handler(pmt.intern('ptt'), self.ptt)
        self.set_pa(pa)
        self.set_lna(lna)
        self.set_da(da)
        if tx_pwr != 0:
            self.set_tx_pwr(tx_pwr)
        self.log = gr.logger(self.alias())
    
    def __del__(self):
        self.set_pa(False)
        self.set_lna(False)
        self.set_da(False)
    
    def set_pa(self, pa:bool):
        self.amp.pa_on() if pa else self.amp.pa_off()
    
    def set_lna(self, lna:bool):
        self.amp.lna_on() if lna else self.amp.lna_off()
    
    def set_da(self, da:bool):
        self.amp.da_on_fast() if da else self.amp.da_off_fast()
    
    def set_tx_pwr(self, pwr:int):
        try:
            self.amp.set_tx_power(pwr)
            self.log.info(f"tx power set: {pwr}")
        except (ValueError, RuntimeError) as e:
            self.log.warn(f"{e}")

    def pa_handler(self, msg):
        try:
            state = pmt.to_bool(pmt.cdr(msg))
            if state:
                self.amp.pa_on()
                if self.verbose:
                    self.log.info("PA set on")
            else:
                self.amp.pa_off()
                if self.verbose:
                    self.log.info("PA set off")
        except ValueError:
            pass
    
    def da_handler(self, msg):
        try:
            state = pmt.to_bool(pmt.cdr(msg))
            if state:
                self.amp.da_on_fast()
                if self.verbose:
                    self.log.info("DA set on")
            else:
                self.amp.da_off_fast()
                if self.verbose:
                    self.log.info("DA set off")
        except ValueError:
            pass
    
    def lna_handler(self, msg):
        try:
            state = pmt.to_bool(pmt.cdr(msg))
            if state:
                self.amp.lna_on()
                if self.verbose:
                    self.log.info("LNA set on")
            else:
                self.amp.lna_off()
                if self.verbose:
                    self.log.info("LNA set off")
        except ValueError:
            pass
    
    def tx_pwr_handler(self, msg):
        try:
            pwr = pmt.to_long(pmt.cdr(msg))
        except ValueError:
            return
        try:
            self.amp.set_tx_power(pwr)
            self.log.info(f"tx power set: {pwr}")
        except (ValueError, RuntimeError) as e:
            self.log.warn(f"{e}")
    
    def ptt(self, msg):
        try:
            enable = pmt.to_bool(pmt.cdr(msg))
            if enable:
                self.amp.da_on_fast()
            else:
                self.amp.da_off_fast()
        except:
            pass

    def forecast(self, noutput_items, ninputs):
        return 0

    def general_work(self, input_items, output_items):
        self.consume_each(0)
        return 0
