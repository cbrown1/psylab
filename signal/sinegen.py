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

def sinegen(f, fs, **kwargs):
    '''Generates pure tones
        
        Parameters
        ----------
        f: scalar/array
            Frequency info. If f is a scalar, then a pure tone of fixed 
            frequency is created. If f is a 2-element array, the values will be 
            the start and end frequecies of a linear frequency sweep. If f is 
            an array of length > 2, the values will be the instantaneous 
            frequency of an arbitrary (but nonetheless pure) waveform. In this 
            case, dur will be ignored, and the output array will be the same 
            length (the same number of samples) as input f. 
        fs: scalar
            The sampling frequency.
        
        Kwargs
        ------
        dur : scalar
            The duration in ms.
        amp : scalar/array
            Amplitude values less than or equal to 0 are treated as dB (re: 
             +-1), and values greater than 0 are used to scale the waveform 
             peak linearly. default is 1
        phase : scalar
            The starting phase in degrees. default is 0
        
        Returns
        -------
        y : array
            The specified signal.
     
        Notes
        -----
        Examples:
        
        # Generate a 1000-Hz pure tone, with a sample rate of 22050, a 
        # duration of 1s, an amplitude of +-.9, and a cosine starting phase
        tone = sinegen(1000, 44100, dur=1000, amp=.9, phase=180);
        
        # Generate a tone with an amplitude that is 3 dB down from peak (+-1.0)
        tone = sinegen(1000, 44100, dur=1000, amp=-3);
        
        # Generate a linear tone sweep starting at 200 Hz and ending at 750 Hz
        tone = sinegen((200, 750), 44100, dur=1000, amp=-3);
        
        # Generate 2-Hz FM (with 50 Hz mod depth), on a 500-Hz carrier 
        fm = sinegen(sinegen(2, 44100, dur=1000) * 25 + 500, 44100);
        
    '''
    
    dur = kwargs.get('dur');
    amp = kwargs.get('amp', 1);
    phase = kwargs.get('phase', 0);
#    if not 'amp' in kwargs:
#        kwargs['amp'] = 1.;
#    if not 'phase' in kwargs:
#        kwargs['phase'] = 0.;

    f = np.array(np.float32(f));
    fs = np.float32(fs);
    amp = np.array(np.float32(amp));
    phase = np.float32(phase)*np.pi/180.;
    
    if f.size == 2:
        dur = np.round((np.float32(dur) / 1000.) * fs);
        freq = np.linspace(f[0], f[1], dur);
    elif f.size == 1:
        dur = np.round((np.float32(dur) / 1000.) * fs);
        freq = np.ones(dur) * f;
    else:
        dur = f.size;
        freq = f;
    
    if amp.size == 2:
        if not amp[0] > 0 or not amp[1] > 0:
            raise Exception, 'When generating amplitude sweeps, linear scaling must be used (ie., .01 < amp < 1.0';
        amp1 = np.linspace(amp[0], amp[1], dur);
    elif amp.size == 1:
        if amp <= 0:
            amp1 = np.ones(dur) * 10. ** (amp / 20.);
        else:
            amp1 = np.ones(dur) * amp;
    else:
        amp1 = amp;
    
    return amp1 * np.sin(phase + (2. * np.pi * np.cumsum(freq) / fs));
