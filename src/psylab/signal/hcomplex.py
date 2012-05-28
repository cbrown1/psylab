# -*- coding: utf-8 -*-

# Copyright (c) 2010-2012 Christopher Brown
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

import numpy as np

def hcomplex(f, fs, **kwargs):
    '''Generates harmonic complexes
        
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
    f = np.float32(f);
    fs = np.float32(fs);
    dur = np.round((np.float32(kwargs['dur']) / 1000.) * fs);
    amp = np.float32(kwargs['amp']);
    nc = np.float32(kwargs['ncomponents']);
    offset = np.float32(kwargs['offset']);
    
    if amp <= 0:
        amp = 10. ** (amp / 20.);

    comp = np.linspace(f, f*nc, nc) + offset;
    y = np.zeros(dur);
    for i in range(nc):
        buff = np.ones(dur) * comp[i];
        y = y + (amp * np.sin(2 * np.pi * np.cumsum(buff) / fs));
    return y;
