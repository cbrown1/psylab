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
# along with Psylab.  If not, see <http://www.gnu.org/licenses/>.
#
# Bug reports, bug fixes, suggestions, enhancements, or other 
# contributions are welcome. Go to http://code.google.com/p/psylab/ 
# for more information and to contribute. Or send an e-mail to: 
# cbrown1@pitt.edu.
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
        raise ValueError("Window is one of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")
    
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
