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
        rf = np.concatenate((r, r[::-1]))
    else:
        raise Exception("shape not recognized")
    
    f_ramp = np.ones(data.shape[0])
    if set in ['on', 'onoff']:
        f_ramp[0:dur] = rf[0:dur]
    if set in ['off', 'onoff']:
        durp1 = dur-1
        f_ramp[-(durp1):] = rf[-(durp1):]

#    if len(data.shape) == 2:
#        f_ramp_1d = rf.copy()
#        for c in range(data.shape[1]-1):
#            f_ramp = np.column_stack((f_ramp, f_ramp_1d))

    return (data.T * f_ramp).T
#    y = data
#    if set in ['on', 'onoff']:
#        y[0:dur,] = y[0:dur,]*rf[0:dur,]
#    if set in ['off', 'onoff']:
#        durp1 = dur-1
#        y[-(durp1):,] = y[-(durp1):,]*rf[-(durp1):,]
#    return y
