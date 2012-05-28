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
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# Comments and/or additions are welcome. Send e-mail to: cbrown1@pitt.edu.
#

"""
    pa4 - functions to control TDT PA4 programmable attenuators

    Functions
    ---------
    set_atten(device, atten, port)
        Sets the specified attenuation level on the specified device.

    get_atten(device, port)
        Gets the current attenuation level on the specified device.

    set_mute(device, mute, port)
        Sets the mute for the specified device. mute arg is a bool.

    find_pa4(port)
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

class pa4():

    class __command__():
        def __init__(self):
            self.data = [0x15, 0x16, 0x18, 0x20]
            self.keys = ['MUTE','NOMUTE','READ','ATTEN']
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

    command = __command__()
    SUCCESS = '\xc3'
    IDENT_REQUEST = 0x08
    SNOP = 0x00
    PA4_CODE = 0x01

    def pa4atten(self, dev, atten, port):
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
        d = chr(3+dev)         # device ID's start at 4
        b = chr(0x40 + 4)      # Number of bytes to follow (including checksum)
        c = chr(self.command('ATTEN'))
        lo,hi = self.lohibytes(atten * 10)
        cs,j = self.lohibytes(self.command('ATTEN') + (atten * 10))
        command = d + b + c + chr(hi) + chr(lo) + chr(cs)

        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(command)
        ret = s.readline()
        s.close()
        if ret[0] != self.SUCCESS:
            raise Exception, 'Hardware error: %s' % ret[1:-2]

    def pa4read(self, dev, port):
        '''Gets the current attenuation level on the specified device.

            Parameters
            ----------
            dev : int
                The device ID. Device 1 is the first module in the first
                xbus, etc.

            port : str
                The serial port to use. Default is 'COM1'. On my linux
                box, it is '/dev/ttyS0'

            Returns
            -------
            atten : float
                The amount of attenuation, in dB. Will be 0 <= 99.9
        '''
        d = chr(3+dev)
        c = chr(self.command('READ'))
        command = d + c

        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(command)
        ret = s.readline()
        s.close()
        if ret == '' or ret[0] != self.SUCCESS:
            raise Exception, 'Error accessing hardware'
        return (ord(ret[2]) + ord(ret[1]) * 256) / 10.

    def pa4find(self, port):
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
        devlist = []
        c = chr(self.IDENT_REQUEST)
        s = serial.Serial(port, baudrate=38400, timeout=.1)
        for dev in range(1,33):
            s.write(chr(3+dev)+c)
            ret = s.readline()
            if ret != '' and ret == chr(self.PA4_CODE):
                devlist.append(dev)

        s.close()
        return devlist

    def pa4mute(self, dev, mute, port):
        '''Sets the mute for the specified device. mute is a bool.

            Parameters
            ----------
            dev : int
                The device ID. Device 1 is the first module in the first
                xbus, etc.
            mute : bool
                True to mute device, False to unmute it.

            port : str
                The serial port to use. Default is 'COM1'. On my linux
                box, it is '/dev/ttyS0'

            Returns
            -------
            None.
        '''
        d = chr(3+dev)
        if mute:
            ch = chr(self.command('MUTE'))
        else:
            ch = chr(self.command('NOMUTE'))
        command = d + ch

        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(command)
        ret = s.readline()
        s.close()
        if ret[0] != self.SUCCESS:
            raise Exception, 'Hardware error: %s' % ret[1:-2]

    def lohibytes(self, val):
        ha = hex(int(val))
        bytes = ha[2:].zfill(4)
        lo = int('0x%s' % bytes[2:4],16)
        hi = int('0x%s' % bytes[0:2],16)
        return lo,hi
