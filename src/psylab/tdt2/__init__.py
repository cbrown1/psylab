# -*- coding: utf-8 -*-

# Copyright (c) 2011 Christopher Brown
#
# This file is part of Psylab.
#
# Psylab is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Psylab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# Comments and/or additions are welcome. Send e-mail to: cbrown1@pitt.edu.
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
