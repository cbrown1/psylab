# -*- coding: utf-8 -*-

# Copyright (c) 2010 Christopher Brown; All Rights Reserved.
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
    wg1 - functions to control TDT WG1 waveform generators using the serial port

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
    To access pa4 modules via the serial port, set both jumpers on
    the back of the OI1 to the RIGHT (jumpers to the left for AP2
    control).

    These functions are based on C code from the House Ear Institute,
    provided by John Wygonski.

    Tested on windows and linux.

    Depends on pyserial (http://sourceforge.net/projects/pyserial/)
"""

import serial

class wg1():

    ON      = 0x11
    OFF     = 0x12
    CLEAR   = 0x13
    AMP     = 0x14
    FREQ    = 0x15
    SWEEP   = 0x16
    PHASE   = 0x17
    DCSHIFT = 0x18
    SHAPE   = 0x19
    DUR     = 0x1A
    RF      = 0x1B
    STATUS  = 0x20
    
    OFF     = 0
    ON      = 1
    RISING  = 2
    FALLING = 3
    
    SHAPE = {
    'GAUSS': 1,
    'UNIFORM': 2,
    'SINE': 3,
    'WAVE': 4,
    }

    success = '\xc3'

    def set_shape(dev, shape, port='COM1'):
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
        d = chr(3+dev)
        ch = chr(SHAPE[shape])
        command = d + ch

        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(command)
        ret = s.readline()
        s.close()
        if ret != success:
            raise Exception, 'Error accessing hardware'

    def set_amp(dev, amp, port='COM1'):
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
        ch = AMP
        c = chr(ch)
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
        if ret != success:
            raise Exception, 'Error accessing hardware'

    def set_freq(dev, freq, port='COM1'):
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
        ch = FREQ
        c = chr(ch)
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
        if ret != success:
            raise Exception, 'Error accessing hardware'

    def clear(dev, port='COM1'):
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
        ch = chr(CLEAR)
        command = d + ch

        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(command)
        ret = s.readline()
        s.close()
        if ret != success:
            raise Exception, 'Error accessing hardware'

    def set_onoff(dev, on = False, port='COM1'):
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
            ch = chr(ON)
        else:
            ch = chr(OFF)
        command = d + ch

        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(command)
        ret = s.readline()
        s.close()
        if ret != success:
            raise Exception, 'Error accessing hardware'

    def find(port='COM1'):
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
        ch = commands['READ']
        c = chr(ch)
        s = serial.Serial(port, baudrate=38400, timeout=.1)
        for dev in range(1,33):
            s.write(chr(3+dev) + c)
            ret = s.readline()
            if ret != '' and ret[0] == success:
                devlist.append(dev)

        s.close()
        return devlist

    def get_status(dev, port='COM1'):
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
        ch = STATUS
        c = chr(ch)
        command = d + c

        s = serial.Serial(port, baudrate=38400, timeout=1)
        s.write(command)
        ret = s.readline()
        s.close()
        if ret == '' or ret[0] != success:
            raise Exception, 'Error accessing hardware'
        return (ord(ret[2]) + ord(ret[1]) * 256) / 10.

    def lohibytes(val):
        ha = hex(int(val))
        bytes = ha[2:].zfill(4)
        lo = int('0x%s' % bytes[2:4],16)
        hi = int('0x%s' % bytes[0:2],16)
        return lo,hi
