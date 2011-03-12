# -*- coding: utf-8 -*-

# Copyright (c) 2010-2011 Christopher Brown; All Rights Reserved.
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

"""
    wg1 - functions to control TDT WG1 waveform generators

    Functions
    ---------
    set_shape(dev, shape, port='COM1')
        Selects the waveform shape on the specified device.

    set_amp(dev, amp, port='COM1')
        Sets the output waveform amplitude on the specified device.

    set_freq(dev, freq, port='COM1')
        Sets the sinewave frequency on the specified device.

    clear(dev, port='COM1')
        Clears the specified WG1 and resets it to the factory default setup.

    set_onoff(dev, on=False, port='COM1')
        Starts or stops the specified WG1.

    get_status(dev, port='COM1')
        Gets the status of the specified WG1

    Notes
    -----
    To access TDT modules via the serial port, set both jumpers on
    the back of the OI1 to the RIGHT (can be accessed from the front
    of the XBUS rack). Jumpers to the left for AP2 control.

    Tested on windows and linux.

    Depends on pyserial (http://sourceforge.net/projects/pyserial/)
"""

import serial

class wg1():
    class __command__():
        def __init__(self):
            self.data = [0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x20]
            self.keys = ['ON','OFF','CLEAR','AMP', 'FREQ', 'SWEEP', 'PHASE', 'DCSHIFT', 'SHAPE', 'DUR', 'RF', 'STATUS']
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

    class __shape__():
        def __init__(self):
            self.data = [1, 2, 3, 4]
            self.keys = ['GAUSS','UNIFORM','SINE','WAVE']
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

    class __status__():
        def __init__(self):
            self.data = [0, 1, 2, 3]
            self.keys = ['OFF','ON','RISING','FALLING']
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
    shape = __shape__()
    status = __status__()
    SUCESS = '\xc3'

    def set_shape(self, dev, shape, port='COM1'):
        '''Selects the WG1 waveform shape on the specified device.

            Parameters
            ----------
            dev : int
                The device ID. Device 1 is the first module in the first
                xbus, etc.

            shape : str
                One of:
                    `GAUSS` : White noise sampled from a Gaussian distribution
                    `UNIFORM` : White noise sampled from a Uniform distribution
                    `SINE` : A pure tone

            port : str
                The serial port to use. Default is 'COM1'. On my linux
                box, it is '/dev/ttyS0'

            Returns
            -------
            None. Raises exception on access error.
        '''
        d = chr(3+dev)
        b = chr(0x40 + 4)      # Number of bytes to follow (including checksum)
        c = chr(self.command('SHAPE'))
        if shape in self.shape.keys:
            shapeval = self.shape(shape)

        lo,hi = lohibytes(shapeval)
        cs,j = lohibytes(ch+lo+hi)
        command = d + b + c + chr(hi) + chr(lo) + chr(cs)

        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(command)
        ret = s.readline()
        s.close()
        if ret != self.SUCCESS:
            raise Exception, 'Error accessing hardware'

    def set_amp(self, dev, amp, port='COM1'):
        '''Sets the output waveform amplitude on the specified device.

            Parameters
            ----------
            dev : int
                The device ID. Device 1 is the first module in the first
                xbus, etc.

            amp : int
                The amplitude of the output waveform. Should be 0 <= 99.9

            port : str
                The serial port to use. Default is 'COM1'. On my linux
                box, it is '/dev/ttyS0'

            Returns
            -------
            None. Raises exception on access error.
        '''
        d = chr(3+dev)         # device ID's start at 4
        b = chr(0x40 + 4)      # Number of bytes to follow (including checksum)
        c = chr(self.command('AMP'))
        if amp >9.99:
            amp_clipped = 9.99
        elif amp < 0:
            amp_clipped = 0.
        else:
            amp_clipped = float(amp)

        lo,hi = lohibytes(amp_clipped)
        cs,j = lohibytes(ch+lo+hi)
        command = d + b + c + chr(hi) + chr(lo) + chr(cs)

        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(command)
        ret = s.readline()
        s.close()
        if ret != self.SUCCESS:
            raise Exception, 'Error accessing hardware'

    def set_freq(self, dev, freq, port='COM1'):
        '''Sets the sinewave frequency on the specified device.

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
        c = chr(self.command('FREQ'))
        if freq >20000:
            freq_clipped = 20000
        elif freq < 0:
            freq_clipped = 0.
        else:
            freq_clipped = float(freq)

        lo,hi = lohibytes(freq_clipped)
        cs,j = lohibytes(ch+lo+hi)
        command = d + b + c + chr(hi) + chr(lo) + chr(cs)

        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(command)
        ret = s.readline()
        s.close()
        if ret != self.SUCCESS:
            raise Exception, 'Error accessing hardware'

    def clear(self, dev, port='COM1'):
        '''Clears the specified WG1 and resets it to the factory default setup.

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
        ch = chr(self.command('CLEAR'))
        command = d + ch

        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(command)
        ret = s.readline()
        s.close()
        if ret != self.SUCCESS:
            raise Exception, 'Error accessing hardware'

    def set_onoff(self, dev, on = False, port='COM1'):
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
        if on:
            ch = chr(self.command('ON'))
        else:
            ch = chr(self.command('OFF'))
        command = d + ch

        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(command)
        ret = s.readline()
        s.close()
        if ret != self.SUCCESS:
            raise Exception, 'Error accessing hardware'

    def find(self, port='COM1'):
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
        c = chr(self.command('STATUS'))
        s = serial.Serial(port, baudrate=38400, timeout=.1)
        for dev in range(1,33):
            s.write(chr(3+dev) + c)
            ret = s.readline()
            if ret != '' and ret[0] == self.SUCCESS:
                devlist.append(dev)

        s.close()
        return devlist

    def get_status(self, dev, port='COM1'):
        '''Gets the status of the specified device.

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
            status : float
                The the status of the device.
        '''
        d = chr(3+dev)
        c = chr(self.command('STATUS'))
        command = d + c

        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(command)
        ret = s.readline()
        s.close()
        if ret == '' or ret[0] != self.SUCCESS:
            raise Exception, 'Error accessing hardware'
        return (ord(ret[2]) + ord(ret[1]) * 256) / 10.

    def lohibytes(self, val):
        ha = hex(int(val))
        bytes = ha[2:].zfill(4)
        lo = int('0x%s' % bytes[2:4],16)
        hi = int('0x%s' % bytes[0:2],16)
        return lo,hi
