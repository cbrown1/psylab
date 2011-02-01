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

import numpy as np

def lts(sig, wsize, overlap=0, window=None):
    """Computes a long-term spectrum of a signal
    
        lts computes a long-term spectrum of a signal by breaking it up
        into a number of chunks of size wsize, applying a window, and then
        averaging the fft of each windowed chunk. Recall that the fft function 
        will simply truncate the signal if you set the fftsize to be less 
        than the length of the signal. 
       
       Parameters
       ----------
       sig : array
          The input signal
       wsize : scalar
          The width of the window. Should be a power of 2
       wtype : string
          The type of window:
            'flat' [no window]
            'hanning' [default]
            'hamming'
            'bartlett'
            'blackman'
        overlap : scalar
          The number of samples to overlap each window [default = 0]
        
        Returns
        -------
        y : array
            The averaged fft of the signal. The length will be wsize/2.
            
    """
    
    siglen = len(sig)    
    pt = 0
    newpt = pt + wsize
    n = 0
    ltfft = np.zeros(wsize/2+1)

    if window == None:
        window = 'hanning'
    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is one of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"
    
    if window == 'flat': #no window
        w=np.ones(wsize,'d')
    else:
        w=eval('np.%s(%i)' % (window, wsize))
    
    while siglen > newpt:
        thissig = sig[pt:newpt] * w
        ltfft += np.real(np.fft.rfft(thissig))
        pt = newpt + 1 - overlap
        newpt = pt + wsize
        n += 1
    if window == 'flat': #no window
        w=np.ones(siglen-pt,'d')
    else:
        w=eval('np.%s(%i)' % (window, siglen-pt))
    
    ltfft += np.real(np.fft.rfft(sig[pt:]*w,wsize))
    return np.abs(ltfft / (n+1))
