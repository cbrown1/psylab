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
from scipy.signal import filter_design as filters, filtfilt, hilbert

def envelope(signal,fs,use_hilbert=False,env_cutoff=16.,env_order=6.):
    '''Extracts the amplitude envelope from a signal
    
        If use_hilbert is False, half-wave rectification and low-pass 
        filtering is used (default cutoff frequency is 16 Hz, default 
        filter order is 6. If usehilbert is True, the Hilbert transform
        is used.
        
        Parameters
        ----------
        signal : array
            The signal to extract the amplitude envelope from. 
        fs : scalar
            The sampling frequency.
        use_hilbert : bool
            True to use hilbert method [env_cutoff and env_order are ignored]
            False to use half-wave rectification and low-pass filtering
        env_cutoff : scalar
            The envelope cutoff frequency [default=16 Hz].
        env_order : scalar
            The order of the envelope filter [must be even number; default=6].
        
        Returns
        -------
        env : array
            The amplitude envelope of the input signal.
    '''
    if use_hilbert:
        h = np.imag(hilbert(signal))
        env = np.sqrt((signal**2) + h**2)
        # finestructure = np.arctan(h/signal)
    else:
        env = np.maximum(signal,0)
        env_b,env_a = filters.butter(env_order/2.,np.float32(env_cutoff)/(np.float32(fs)/2.))
        env = filtfilt(env_b,env_a,env)

    return env
