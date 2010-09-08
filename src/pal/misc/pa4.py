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
    pa4 - functions to control TDT PA4 attenuators using the serial port

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

commands = { 'MUTE':   0x15,
             'NOMUTE': 0x16,
             'READ':   0x18,
             'ATTEN':  0x20,
           }

success = '\xc3'

def set_atten(dev, atten, port='COM1'):
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
    ch = commands['ATTEN'] # command for set atten
    c = chr(ch)
    lo,hi = lohibytes(atten * 10)
    cs,j = lohibytes(ch+lo+hi)
    command = d + b + c + chr(hi) + chr(lo) + chr(cs)

    s = serial.Serial(port, baudrate=38400, timeout=1)
    s.write(command)
    ret = s.readline()
    s.close()
    if ret != success:
        raise Exception, 'Error accessing hardware'

def find_pa4(port='COM1'):
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


def get_atten(dev, port='COM1'):
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
    ch = commands['READ']
    c = chr(ch)
    command = d + c

    s = serial.Serial(port, baudrate=38400, timeout=1)
    s.write(command)
    ret = s.readline()
    s.close()
    if ret == '' or ret[0] != success:
        raise Exception, 'Error accessing hardware'
    return (ord(ret[2]) + ord(ret[1]) * 256) / 10.

def set_mute(dev, mute=False, port='COM1'):
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
        ch = chr(commands['MUTE'])
    else:
        ch = chr(commands['NOMUTE'])
    command = d + ch

    s = serial.Serial(port, baudrate=38400, timeout=1)
    s.write(command)
    ret = s.readline()
    s.close()
    if ret != success:
        raise Exception, 'Error accessing hardware'


def lohibytes(val):
    ha = hex(int(val))
    bytes = ha[2:].zfill(4)
    lo = int('0x%s' % bytes[2:4],16)
    hi = int('0x%s' % bytes[0:2],16)
    return lo,hi
