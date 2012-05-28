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
    wg1 - functions to control TDT WG1 waveform generators

    Functions
    ---------
    set_shape(dev, shape, port)
        Selects the waveform shape on the specified device.

    set_amp(dev, amp, port)
        Sets the output waveform amplitude on the specified device.

    set_freq(dev, freq, port)
        Sets the sinewave frequency on the specified device.

    clear(dev, port)
        Clears the specified WG1 and resets it to the factory default setup.

    on(dev, on, port)
        Starts or stops the specified WG1.

    get_status(dev, port)
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
            self.data = [0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x20]
            self.keys = ['ON','OFF','CLEAR','AMP', 'FREQ', 'SWEEP', 'PHASE', 'DCSHIFT', 'SHAPE', 'DUR', 'RF', 'TRIG', 'STATUS']
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

    class __trigger__():
        def __init__(self):
            self.data = [1, 2, 3, 4, 5]
            self.keys = ['POS_EDGE','NEG_EDGE','POS_ENABLE','NEG_ENABLE', 'NONE']
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
    SUCCESS = '\xc3'
    IDENT_REQUEST = 0x08
    SNOP = 0x00
    WG1_CODE = 0x08

    def wg1shape(self, dev, shape, port):
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
        if shape in self.shape.keys:
            shapeval = self.shape(shape)
        else:
            raise Exception, '`shape` must be one of %r' % self.shape.keys
        d = chr(3+dev)         # device ID's start at 4
        b = chr(0x40 + 4)      # Number of bytes to follow (including checksum)
        c = chr(self.command('SHAPE'))
        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(d)
        s.write(b)
        s.write(c)
        s.write(chr(shapeval))
        s.write(chr(shapeval >> 8))
        s.write(chr(self.command('SHAPE') + shapeval))
        ret = s.readline()
        s.close()
        if ret[0] != self.SUCCESS:
            raise Exception, '%s' % ret[1:-2]

    def wg1trig(self, dev, tcode, port):
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
        if tcode in self.trigger.keys:
            tval = self.trigger(tcode)
        else:
            raise Exception, '`shape` must be one of %r' % self.trigger.keys
        d = chr(3+dev)         # device ID's start at 4
        b = chr(0x40 + 4)      # Number of bytes to follow (including checksum)
        c = chr(self.command('TRIG'))
        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(d)
        s.write(b)
        s.write(c)
        s.write(chr(tval))
        s.write(chr(tval >> 8))
        s.write(chr(self.command('TRIG') + tval))
        ret = s.readline()
        s.close()
        if ret[0] != self.SUCCESS:
            raise Exception, '%s' % ret[1:-2]

    def wg1amp(self, dev, amp, port):
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
            amp_clipped = 999
        elif amp < 0:
            amp_clipped = 0
        else:
            amp_clipped = int(amp*100)
        lo,hi = self.lohibytes(amp_clipped)
        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(d)
        s.write(b)
        s.write(c)
        s.write(chr(lo))
        s.write(chr(hi))
        cs_lo,cs_hi = self.lohibytes(self.command('AMP') + lo + hi)
        s.write(chr(cs_lo))
        ret = s.readline()
        s.close()
        if ret[0] != self.SUCCESS:
            raise Exception, '%s' % ret[1:-2]

    def wg1dc(self, dv, amp, port):
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
        c = chr(self.command('DC'))
        if amp >9.99:
            amp_clipped = 999
        elif amp < 0:
            amp_clipped = 0
        else:
            amp_clipped = int(amp*100)
        lo,hi = self.lohibytes(amp_clipped)
        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(d)
        s.write(b)
        s.write(c)
        s.write(chr(lo))
        s.write(chr(hi))
        cs_lo,cs_hi = self.lohibytes(self.command('DC') + lo + hi)
        s.write(chr(cs_lo))
        ret = s.readline()
        s.close()
        if ret[0] != self.SUCCESS:
            raise Exception, '%s' % ret[1:-2]

    def wg1swrt(self, dev, swrt, port):
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
        c = chr(self.command('SWRT'))
        if swrt >9999:
            swrt_clipped = 9999
        elif swrt < 10:
            swrt_clipped = 10
        else:
            swrt_clipped = int(swrt)
        lo,hi = self.lohibytes(swrt_clipped)
        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(d)
        s.write(b)
        s.write(c)
        s.write(chr(lo))
        s.write(chr(hi))
        cs_lo,cs_hi = self.lohibytes(self.command('AMP') + lo + hi)
        s.write(chr(cs_lo))
        ret = s.readline()
        s.close()
        if ret[0] != self.SUCCESS:
            raise Exception, '%s' % ret[1:-2]

    def wg1freq(self, dev, freq, port):
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
            freq_clipped = 0
        else:
            freq_clipped = int(freq)
        lo,hi = self.lohibytes(freq_clipped)
        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(d)
        s.write(b)
        s.write(c)
        s.write(chr(lo))
        s.write(chr(hi))
        cs_lo,cs_hi = self.lohibytes(self.command('FREQ') + lo + hi)
        s.write(chr(cs_lo))
        ret = s.readline()
        s.close()
        if ret[0] != self.SUCCESS:
            raise Exception, '%s' % ret[1:-2]

    def wg1dur(self, dev, dur, port):
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
        c = chr(self.command('DUR'))
        if dur >30000:
            dur_clipped = 30000
        elif dur < 0:
            dur_clipped = 0
        else:
            dur_clipped = int(dur)
        lo,hi = self.lohibytes(dur_clipped)
        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(d)
        s.write(b)
        s.write(c)
        s.write(chr(lo))
        s.write(chr(hi))
        cs_lo,cs_hi = self.lohibytes(self.command('DUR') + lo + hi)
        s.write(chr(cs_lo))
        ret = s.readline()
        s.close()
        if ret[0] != self.SUCCESS:
            raise Exception, '%s' % ret[1:-2]

    def wg1rf(self, dev, rf, port):
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
        c = chr(self.command('RF'))
        reliable_rfs = [ .1,  .2,  .3,  .4,  .5,  .6,  .7,  .8,  .9,
                         1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9.,
                        10., 20., 30., 40., 50., 60., 70., 80., 90., ]
        if rf not in reliable_rfs:
            raise Exception, "Specified rf will not produce reliable results"

        rf_adj = int(rf * 10)
        lo,hi = self.lohibytes(rf_adj)
        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(d)
        s.write(b)
        s.write(c)
        s.write(chr(lo))
        s.write(chr(hi))
        cs_lo,cs_hi = self.lohibytes(self.command('RF') + lo + hi)
        s.write(chr(cs_lo))
        ret = s.readline()
        s.close()
        if ret[0] != self.SUCCESS:
            raise Exception, '%s' % ret[1:-2]

    def wg1clear(self, dev, port):
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
        if ret[0] != self.SUCCESS:
            raise Exception, '%s' % ret[1:-2]

    def wg1on(self, dev, on, port):
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
        if ret[0] != self.SUCCESS:
            raise Exception, '%s' % ret[1:-2]

    def wg1find(self, port):
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
            if ret != '' and ret == chr(self.WG1_CODE):
                devlist.append(dev)

        s.close()
        return devlist


    def wg1status(self, dev, port):
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
        if ret == '':
            raise Exception, 'Error Accessing Hardware'
        elif ret[0] != self.SUCCESS:
            raise Exception, '%s' %  ret[1:-2]
        return ord(ret[1])

    def lohibytes(self, val):
        ha = hex(int(val))
        bytes = ha[2:].zfill(4)
        lo = int('0x%s' % bytes[2:4],16)
        hi = int('0x%s' % bytes[0:2],16)
        return lo,hi
