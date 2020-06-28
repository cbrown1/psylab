# -*- coding: utf-8 -*-

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
# contributions are welcome. Go to https://github.com/cbrown1/psylab/
# for more information and to contribute. Or send an e-mail to: 
# cbrown1@pitt.edu.
#

import collections
import numpy as np

def hcomplex_old(f, fs, **kwargs):
    '''Generates harmonic complexes
        
        This is the unvectorized, lame version which might have some 
        value as it may be easier to see what's going on.         
        
        Parameters
        ----------
        f :  scalar
            fundamental frequency
        fs : scalar
            sampling frequency
        
        Kwargs
        ------
        dur : scalar
            duration in ms
        amp : scalar
            amplitude values less than or equal to 0 are treated as dB (re: 
            +-1), and values greater than 0 are used to scale the waveform 
            peak linearly. default is 1
        ncomponents : scalar
            number of harmonic components
        offset : scalar
            offset in Hz. Eg., offset = 2 would yield 202, 302, 402, etc.
          
        Returns
        -------
        y : array
            The waveform
    '''
    if not 'amp' in kwargs:
        kwargs['amp'] = 1.;
    if not 'offset' in kwargs:
        kwargs['offset'] = 0.;
    f = np.float32(f)
    fs = np.float32(fs)
    dur = np.int(np.round((np.float32(kwargs['dur']) / 1000.) * fs))
    amp = np.float32(kwargs['amp'])
    nc = np.float32(kwargs['ncomponents'])
    offset = np.float32(kwargs['offset'])
    
    if amp <= 0:
        amp = 10. ** (amp / 20.)

    comp = np.linspace(f, f*nc, nc) + offset
    y = np.zeros(dur)
    for i in range(nc):
        buff = np.ones(dur) * comp[i]
        y = y + (amp * np.sin(2 * np.pi * np.cumsum(buff) / fs))
    return y

def tcomplex(f, fs, dur, amp=1, ncomponents=100, offset=0):
    '''Generates tone complexes
        
        Parameters
        ----------
        f :  scalar or array-like
            If scalar, the fundamental frequency of a harmonic complex, and 
            use ncomponents and offset to specify components. Or pass an 
            array to specify component frequencies of a generic tone complex
            (ncomponents and offset arguments are ignored).
        fs : scalar
            sampling frequency
        dur : scalar
            duration in ms
        amp : scalar
            amplitude values less than or equal to 0 are treated as dB (re: 
            +-1), and values greater than 0 are used to scale the waveform 
            peak linearly. default is 1 (array of length f allows setting 
            amp of each component separately) default = 1
        ncomponents : scalar
            number of harmonic components. Ignored if f is an array. default = 100
        offset : scalar
            offset in Hz. Eg., offset = 2 would yield 102, 202, 302, 402, etc.
             Ignored if f is an array. (array of length f allows setting 
             offset of each component separately) default = 0
        Returns
        -------
        y : array
            The waveform
    '''    
    if amp <= 0:
        amp = 10. ** (amp / 20.)
    dur = np.int(np.round((dur / 1000.) * fs))
    if isinstance(f, (collections.Sequence, np.ndarray)):
        fh = f
        ncomponents = fh.size
    else:
        fh = ((np.arange(ncomponents) + 1) * f) + offset
    out = np.sin(2*np.pi * np.cumsum(np.ones((dur,ncomponents))*fh,axis=0) / fs) * amp
    return out.sum(axis=1)
    