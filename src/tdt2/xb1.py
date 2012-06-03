# -*- coding: utf-8 -*-

# Copyright (c) 2010-2011 Christopher Brown
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
# along with Psylab.  If not, see <http://www.gnu.org/licenses/>.
#
# Bug reports, bug fixes, suggestions, enhancements, or other 
# contributions are welcome. Go to http://code.google.com/p/psylab/ 
# for more information and to contribute. Or send an e-mail to: 
# cbrown1@pitt.edu.
#

"""
    pa4 - functions to control TDT PA4 programmable attenuators

    Functions
    ---------
    set_atten(device, atten, com='COM1')
        Sets the specified attenuation level on the specified device.

    get_atten(device, com='COM1')
        Gets the current attenuation level on the specified device.

    set_mute(device, mute=False, com='COM1')
        Sets the mute for the specified device. mute arg is a bool.

    find_pa4(com='COM1')
        Scans the first 32 device IDs, looking for PA4s.

    Notes
    -----
    To access TDT modules via the serial port, set both jumpers on
    the back of the OI1 to the RIGHT (can be accessed from the front
    of the XBUS rack). Jumpers to the left for AP2 control.

    These functions are based on C code from the House Ear Institute,
    provided by John Wygonski.

    Tested on windows and linux.

    Depends on pyserial (http://sourceforge.net/projects/pyserial/)
"""

import serial

class xb1():

    class __device__():
        def __init__(self):
            self.data = [ 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15]
            self.keys = ['PA4','SW2','CG1','SD1','ET1','PI1','UI1','WG1','PF1','TG6','PI2','WG2','DA1','AD1','DD1','DA2','AD2','AD3']
            self.index = 0
        def __call__(self, key=None):
            if key in self.keys:
                return self.data[self.keys.index(key)]
            else:
                return None
        def __iter__(self):
            return self
        def next(self):
            if self.index == len(self.data):
                raise StopIteration
            else:
                val = self.data[self.index]
                self.index += 1
                return val
        def key(self, ind):
            if ind in self.data:
                return self.keys[self.data.index(ind)]
            else:
                return None
        def keys(self):
            return self.keys

    device = __device__()
    SUCCESS = '\xc3'
    IDENT_REQUEST = 0x08
    SNOP = 0x00
    GTRIG = 0xD3
    VER_REQUEST = 0xD4
    ERR_ACK = 0xC2

    def xb1flush(self, port):
        s = serial.Serial(port, baudrate=38400, timeout=1)
        for i in range(20):
            s.write(chr(self.ERR_ACK))
        for i in range(20):
            s.write(chr(self.SNOP))


    def xb1version(self, rackn, port):
        '''Sets the specified attenuation level on the specified device.

            Parameters
            ----------
            dev : int
                The device ID. Device 1 is the first module in the first
                xbus, etc.

            atten : int
                The amount of attenuation, in dB. Should be 0 <= 99.9

            port : str
                The serial port to use. Default is 'COM1'. On my linux
                box, it is '/dev/ttyS0'

            Returns
            -------
            None. Raises exception on access error.
        '''
        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(chr(self.VER_REQUEST))
        s.write(chr(rackn))
        ret = s.readline()
        s.close()
        if ret != None or ret != '':
            return unicode(ord(ret))
        else:
            return ''


    def xb1flush(self, port):
        s = serial.Serial(port, baudrate=38400, timeout=1)
        for i in range(20):
            s.write(chr(self.ERR_ACK))
        for i in range(20):
            s.write(chr(self.SNOP))


    def xb1gtrig(self, port):
        '''Sets the specified attenuation level on the specified device.

            Parameters
            ----------
            dev : int
                The device ID. Device 1 is the first module in the first
                xbus, etc.

            atten : int
                The amount of attenuation, in dB. Should be 0 <= 99.9

            port : str
                The serial port to use. Default is 'COM1'. On my linux
                box, it is '/dev/ttyS0'

            Returns
            -------
            None. Raises exception on access error.
        '''
        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(chr(self.GTRIG))
        s.close()

    def xb1devname(self, dev, port):
        '''Scans the first 32 device IDs, looking for PA4s.

            Parameters
            ----------
            port : str
                The serial port to use. Default is 'COM1'. On my linux
                box, it is '/dev/ttyS0'

            Returns
            -------
            devs : list
                A list of PA4 device IDs

        '''
        c = chr(self.IDENT_REQUEST)
        s = serial.Serial(port, baudrate=38400, timeout=.1)
        s.write(chr(3+dev) + c)
        ret = s.readline()
        if ret != '':
            ret_dev = unicode(self.device.key(ord(ret)))
        else:
            ret_dev = unicode('')

        s.close()
        return ret_dev

    def lohibytes(val):
        ha = hex(int(val))
        bytes = ha[2:].zfill(4)
        lo = int('0x%s' % bytes[2:4],16)
        hi = int('0x%s' % bytes[0:2],16)
        return lo,hi
