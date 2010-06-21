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

def smooth(x, wsize=10, wtype='hanning'):
    '''Smooths a signal using windowing
        
       Smooths the input signal using a window with specified size and type.

       This method is based on the convolution of a scaled window with the signal.
       The signal is prepared by introducing reflected copies of the signal 
       (with the window size) in both ends so that transient parts are minimized
       in the begining and end part of the output signal.
    
       Parameters
       ----------
       x : array
          The input signal.
       wsize : scalar
          The width of the smoothing window
       wtype : string
          The type of window:
            'flat' [Unweighted moving average]
            'hanning'
            'hamming'
            'bartlett'
            'blackman'
        
        Returns
        -------
        y : array
            The smoothed signal.
        
        Notes
        -----
       example:

       t=linspace(-2,2,0.1)
       x=sin(t)+randn(len(t))*0.1
       y=smooth(x)
    
       source:
       http://www.scipy.org/Cookbook/SignalSmooth
    
       see also: 
       
       numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
       scipy.signal.lfilter
 
       TODO: the window parameter could be the window itself if an array instead of a string.
    '''
    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < wsize:
        raise ValueError, "Input vector needs to be bigger than window size."

    if wsize<3:
        return x

    if not wtype in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is one of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

    s=np.r_[2*x[0]-x[wsize:1:-1],x,2*x[-1]-x[-1:-wsize:-1]]
    #print(len(s))
    if wtype == 'flat': #moving average
        w=np.ones(wsize,'d')
    else:
        w=eval('np.'+wtype+'(wsize)')

    y = np.convolve(w/w.sum(),s,mode='same')
    return y[wsize-1:-wsize+1]
