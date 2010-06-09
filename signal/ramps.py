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
from scipy import hanning, hamming

def ramps(data, fs, duration=10, shape='raisedcosine', set='onoff'):
    '''Applies ramps to the onsets and/or offsets of a signal
        
        Parameters
        ----------
        sig : array
            The input signal.
        fs : scalar
            The sampling frequency.
        duration : scalar
            The duration of each ramp, in ms [default = 10].
        shape : string
            Specifies the shape of the ramp. Possibilities include:
              'raisedcosine' [default]
              'hanning'
              'hamming'
              'linear'
        set : string
            Specifies where to apply ramps:
              'on' : apply to onset of signal only
              'off' : apply to offest only
              'onoff' : apply to both
        
        Returns
        -------
        y : array
            The ramped signal.
        
        Notes
        -----
        TODO: Change dur,shape,set to kwargs
        TODO: Make it work for n-dimensional input
    '''
    dur = np.round(np.float32(duration)*(np.float32(fs)/1000.))
    wspace=np.round(2.*dur)

    if shape is 'raisedcosine':
        rf = np.power((((np.cos(np.pi+2*np.pi*np.arange(0,wspace-1)/(wspace-1)))*.5)+.5),2)
    elif shape is 'hanning':
        rf = hanning(wspace)
    elif shape is 'hamming':
        rf = hamming(wspace)
    elif shape is 'linear':
        r = np.linspace(0, 1, dur)
        rf = np.concatenate((r, r[::-1]),1)
    else:
        raise Exception, "shape not recognized";

    y = data
# This used to work for multi-dimension data:
#    for i in range(0,ndim(data)):
#        if set in ['on', 'onoff']:
#            data[0:dur,i] = data[0:dur,i]*rf[0:dur]
#        if set in ['off', 'onoff']:
#            durp1 = dur-1
#            data[-(durp1):,i] = data[-(durp1):,i]*rf[-(durp1):]
    if set in ['on', 'onoff']:
        y[0:dur] = y[0:dur]*rf[0:dur]
    if set in ['off', 'onoff']:
        durp1 = dur-1
        y[-(durp1):] = y[-(durp1):]*rf[-(durp1):]
    return y
