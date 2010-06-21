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
from scipy.signal import filter_design as filters, lfilter, filtfilt

def f0(sig,fs,noisegate=15):
    '''Estimates the fundamental frequency of a signal
        
        Returns an array of estimated instantaneous fundamental frequency 
        (F0) values based on zeros crossings in the input signal. 
        
        Parameters
        ----------
        sig : array
            The input signal.
        fs : array
            The sampling frequency.
        
        Returns
        -------
        y : array
            The pitch track.
    '''
    
    # Low-pass at 270 Hz (above most F0's)
    b,a = filters.butter(4,270./(fs/2.))
    fsig = filtfilt(b,a,sig)
    b,a = filters.butter(4,60./(fs/2.),btype='high')
    fsig = filtfilt(b,a,fsig)
    # Get zero crossings
    zc = np.array(np.where(np.sign(fsig[1:]) != np.sign(fsig[:-1]))).transpose()[:,0]
    # Compute period at each crossing 
    # (actually half-period, since a full period is 2 zero crossings)
    zc2 = np.concatenate((zc,np.zeros((1))))
    zc3 = np.concatenate((np.zeros((1)),zc))
    p = zc2 - zc3
    p[-1] = p[-2]
    # Create new array of periods @ fs
    pfs = np.zeros(fsig.shape)
    # Resample period data (aliased)
    for k in range(zc.shape[0]-1):
        pfs[zc[k]:zc[k+1]] = p[k]
    pfs[0:zc[0]] = p[0]
    pfs[zc[-1]:] = p[-2]
    # Convert instantaneous period data to instantaneous frequency data
    ps = ((pfs / (fs/1000.)) / 1000.)
    # The 2 here corrects for the half-period issue above
    f = (1./ps)/2.
    # Smooth the F0 track
    b,a = filters.butter(1,16./(fs/2.))
    f = filtfilt(b,a,f)
    
    # Voicing
    env = envelope(fsig,fs)
    env = env/np.max(np.abs(env))
    # Noise gate
    env[20*np.log10(env)<-noisegate] = 0
    env[env>0] = 1
#    env2 = env
#    vonsets = array(where(sign(env[1:]) < sign(env[:-1]))).transpose()[:,0]
#    print vonsets
#    print vonsets + vdelay - 1
#    skip = True
#    for k in range(vonsets.shape[0]):
#        if (skip):
#            env2[vonsets[k]:vonsets[k] + vdelay - 1] = 0
#            skip = False
#        else:
#            skip = True
    # Smooth the transitions
    b,a = filters.butter(1,16./(fs/2.))
    envf = filtfilt(b,a,env)

    return f * np.maximum(envf,0)
    #return f, np.maximum(env,0), np.maximum(env2,0)
    #return maximum(envf,0)
