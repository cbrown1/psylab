# -*- coding: utf-8 -*-

# Copyright (c) 2014 Christopher Brown
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
import scipy.signal

def pre_emphasis(signal, fs, hp=50):
    """Applies a pre-emphasis filter to a signal
        
        Applies a 6 dB per octave highpass filter to the specified signal. 
    
        Parameters
        ----------
        signal : 1-d array
            The input signal
        fs : scalar
            The sampling frequency
        hp : scalar
            The high-pass cutoff frequency to use [default = 50 Hz]
            
        Notes
        -----
        The formula for alpha was taken from PRAAT.
    """
    alpha = np.exp(-2 * np.pi * hp / fs) # PRAAT
    sig = np.insert(signal,0,0)
    return sig[1:] - alpha * sig[:-1]
    

def filter_bank(signal, fs, order, cfs, btype='band'):
    """Filters the input array with a bank of filters
        
        Filters a signal with the cutoff frequencies specified in cfs. 
        
        Note: The returned array will be 2-d with one fewer column (dim=1) 
        than len(cfs). cfs[:-1] will be used as highpass cutoff frequencies, 
        and cfs[1:] will be used as lowpass cutoff frequencies. 
        
        The signal can either be 1-d, or 2-d where shape[1]==len(cfs)-1 
        (ie., it can already have been filter_banked; eg., bandpass 
        filtering followed by envelope extraction, which is the usecase 
        that this function was written for). 
        
        Parameters
        ----------
        signal : 1- or 2-d array
            The input signal
        fs : scalar
            The sampling frequency
        order : scalar
            The filter order to use
        cfs : array
            An array of cutoff frequencies
        btype : str
            The type of filter to implement ['band','low','high']
            
        Returns
        -------
        y : 2-d array
            The filtered signal, with the output of each filter along dim 1
    """

    if len(signal.shape) == 1:
        out = np.tile(signal,(cfs.size-1,1)).T
    else:
        out = signal
    if isinstance(order, (int,float)) == 1:
        order = np.tile(order,(cfs.size,)).T

    nyq = fs/2.
    for i in range(len(cfs)-1):
        if btype in ['high', 'band']:
            b_hp,a_hp=scipy.signal.filter_design.butter(order[i],(cfs[i]/nyq),btype='high')
            out[:,i] = scipy.signal.lfilter(b_hp,a_hp,out[:,i])
        if btype in ['low','band']:
            b_lp,a_lp=scipy.signal.filter_design.butter(order[i],(cfs[i+1]/nyq))
            out[:,i] = scipy.signal.lfilter(b_lp,a_lp,out[:,i])
    if len(cfs) == 2:
        out = out.flatten()
    return out


def freqs_logspace(start, stop, n):
    """Compute frequencies equally spaced in log space
    
        Computes n frequencies between start and stop that are evenly spaced 
        in log space. 
        
        The output of this function is useful as the cfs input to filter_bank, 
        when you want to create a bank of bandpass filters.
        
        Parameters
        ----------
        start : scalar
            The start frequency, in Hz
        stop : scalar
            The end frequency, in Hz
        n : scalar
            The number of 'channels' to compute. That is, the return array 
            will be length n+1
    
        Returns
        -------
        y : array
            The frequency values, ready to be input to filter_bank
    """
    n_arr = np.arange(n+1)
    interval = np.log10(stop/float(start))/float(n)
    freqs = start*10.**(interval*n_arr)
    return freqs
