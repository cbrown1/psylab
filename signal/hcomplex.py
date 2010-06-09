# -*- coding: utf-8 -*-

# Copyright (c) 2008-2010 Christopher Brown; All Rights Reserved.
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
