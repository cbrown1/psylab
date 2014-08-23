# -*- coding: utf-8 -*-

# Copyright (c) 2003, Stephen McGovern; All rights reserved.
# Copyright (c) 2010-2014 Christopher Brown
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

import numpy as np

def convolve(x, h):
    '''Convolves two signals using FFT-based fast convolution
        
        If either x or h is 2-d, each column is treated as a channel, 
        and convolution is applied to each. In this case, h can be 1-d, 
        in which case the same h is convolved with each channel of x, or 
        it can be 2-d and have the same number of columns (channels) as x. 
        Alternately, x can be 1-d and h can be 2-d, and you get the idea...

        Parameters
        ----------
        x: array
            First array. Can be 1- or 2-d
        h: array
            Second array. Can be 1- or 2-d

        Returns
        -------
        y : array
            x convolved with h.
            
        Notes
        -----
        This is slower than np.convolve. My performance test (using 3s of 
        audio @ 44.1k) shows it is about half the speed of np.convolve with 
        1-d arrays, and the speed difference decreases as the number of 
        channels increases (performance was about .75 that of np.convolve when 
        x had 32-channels).
    '''
    def nextpow2(x):  
        return 2**(x-1).bit_length()
    
    # If x is 2d & h is 1d, tile h
    if len(x.shape) > len(h.shape):
        # Assume h.shape==(n,)
        h = np.tile(h,(x.shape[1],1)).T
    # Same for when h is 2d and x is 1d
    elif len(x.shape) < len(h.shape):
        x = np.tile(x,(h.shape[1],1)).T

    ly = x.shape[0] + h.shape[0] - 1
    ly2 = nextpow2(ly)

    m = np.max(np.abs(x),axis=0)
    x = np.fft.fft(x, ly2, axis=0)
    h = np.fft.fft(h, ly2, axis=0)

    y = x * h

    y = np.real(np.fft.ifft(y, ly2, axis=0))
    y = y[:ly,]
    m = m/np.max(np.abs(y), axis=0)
    y = m*y

    return y
