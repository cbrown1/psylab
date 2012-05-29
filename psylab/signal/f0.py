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
