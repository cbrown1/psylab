# -*- coding: utf-8 -*-

# Copyright (c) 2011 Christopher Brown; All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the distribution
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Comments and/or additions are welcome (send e-mail to: c-b@asu.edu).
#

'''
tdt2 - Control Tucker Davis Technologies System 2 hardware from the serial port

Modules include:

wg1 - functions to control TDT WG1 waveform generators
pa4 - functions to control TDT PA4 programmable attenuators

Notes
-----
To access TDT modules via the serial port, set both jumpers on
the back of the OI1 to the RIGHT (can be accessed from the front
of the XBUS rack). Jumpers to the left for AP2 control.

Tested on windows and linux.

Depends on pyserial (http://sourceforge.net/projects/pyserial/)
'''

import serial

__version__ = '0.2'

def scan_ports():
    """scan for available ports. return a list"""
    available = []
    for i in range(256):
        try:
            s = serial.Serial(i)
            available.append( s.portstr )
            s.close()   # explicit close 'cause of delayed GC in java
        except serial.SerialException:
            pass
    return available

port = scan_ports()[0]

from xb1 import xb1
from pa4 import pa4
from wg1 import wg1
xb1 = xb1()
pa4 = pa4()
wg1 = wg1()

def xb1_flush():
    global port
    xb1.xb1flush(port)

def xb1_version(rackn):
    global port
    ret = xb1.xb1version(rackn, port)
    return ret

def xb1_gtrig():
    global port
    xb1.xb1gtrig(port)

def xb1_device_name(dev):
    global port
    ret = xb1.xb1devname(dev, port)
    return ret

def wg1_shape(dev, shape):
    global port
    wg1.wg1shape(dev, shape, port)

def wg1_amp(dev, amp):
    global port
    wg1.wg1amp(dev, amp, port)

def wg1_swrt(dev, swrt):
    global port
    wg1.wg1swrt(dev, swrt, port)

def wg1_dc(dev, dc):
    global port
    wg1.wg1dc(dev, dc, port)

def wg1_rf(dev, rf):
    global port
    wg1.wg1amp(dev, rf, port)

def wg1_freq(dev, freq):
    global port
    wg1.wg1freq(dev, freq, port)

def wg1_clear(dev):
    global port
    wg1.wg1clear(dev, port)

def wg1_on(dev, on = False):
    global port
    wg1.wg1on(dev, on, port)

def wg1_find():
    global port
    ret = wg1.wg1find(port)
    return ret

def wg1_status(dev):
    global port
    ret = wg1.wg1status(dev, port)
    return ret

def pa4_set_atten(dev, atten):
    global port
    pa4.pa4atten(dev, atten, port)

def pa4_get_atten(dev):
    global port
    ret = pa4.pa4read(dev, port)
    return ret

def pa4_find():
    global port
    ret = pa4.pa4find(port)
    return ret

def pa4_mute(dev, mute = False):
    global port
    pa4.pa4mute(dev, mute, port)