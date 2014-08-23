# -*- coding: utf-8 -*-

# Copyright (c) 2014, Christopher Brown
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
from .window import sliding_window

def pick_peaks(sig, n, window_size):
    """ A peak picking strategy
        Slides an rms window through the channels of signal, then picks n 
        peaks. Assumes a 2d array with data along axis 0, channels on axis 1.
        Returns a tuple containing an array of channel indexes, and an array 
        of corresponding rms values.
        
        Parameters
        ----------
        sig : array
            The input signal it should be a 2-dimensional array, where the 
            signal data is along axis 0, and the channels are along axis 1
        n : scalar
            The number of peaks to select in each window. Useful for 
            implementing an 'n of m' strategy, where m is the total number 
            of channels (specified by axis 1 of the input array)
        window_size : scalar
            The size of the analysis window, in samples

        Returns
        -------
        ch : array
            The array of peaks. the length will be sig.length / window_size
            and the width (axis=1) will be equal to sig
        rms : array
            The array of windowed rms values

        Notes
        -----
        The order of each output array is from lowest to highest rms, not 
        from lowest to highest channel
        
        Depends on sliding_window, a vectorized windowing function
        
        Example
        -------
        n = 2 # number of peaks to return
        m = 3 # total number of channels
        
        window_size = 2 # in samples
        
        # Create a small array of length 10, with m channels
        signal = np.random.randn(10,m)
        signal[:,1] *= 1.2 # make 2nd channel slightly higher on average
        
        ch,rms = pick_peaks(signal, n, window_size)
    """
    # Number of channels is set by axis 1 of sig (sig must be 2d)
    if len(sig.shape) != 2:
        raise ValueError("Sig must be 2d")
    m = sig.shape[1]
    # Compute rms in each window in each channel
    # (overlap is not used here, but it's available in the function)
    rms = np.sqrt(np.mean(sliding_window(sig,(window_size,m))**2,axis=1))
    # Sort & take last n indexes, along dim 1
    peak_channels = np.argsort(rms,1)[:,-n:]
    peak_channels.sort(axis=1)
    
    peak_channels = peak_channels.repeat(window_size, axis=0)
    rms = rms.repeat(window_size,axis=0)
    
    indices = peak_channels.ravel() + np.repeat(range(0, rms.shape[1]*rms.shape[0], rms.shape[1]), peak_channels.shape[1])
    peak_rms = rms.ravel()[indices]
    peak_rms = peak_rms.reshape(peak_channels.shape)
    
#    # Do the same for rms
#    rms.sort()
#    peak_rms = rms[:,-n:]
    
    return peak_channels,peak_rms
