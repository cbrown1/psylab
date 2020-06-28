# -*- coding: utf-8 -*-

# Copyright (c) 2010-2020 Christopher Brown
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
# contributions are welcome. Go to https://github.com/cbrown1/psylab/
# for more information and to contribute. Or send an e-mail to: 
# cbrown1@pitt.edu.
#

import numpy as np
from scipy.signal import filter_design as filters, filtfilt, hilbert

def envelope(signal, fs, env_cutoff=16., env_order=4., full_rect=False):
    '''Extracts the amplitude envelope from a signal using rectification and low-pass filtering
    
        Parameters
        ----------
        signal : array
            The signal to extract the amplitude envelope from
        fs : scalar
            The sampling frequency
        env_cutoff : scalar
            The envelope cutoff frequency [default=16 Hz]
        env_order : scalar
            The order of the envelope filter [must be even number; default=6]
        full_rect : bool
            True for full-wave rectification [default=half-wave rectification]
        
        Returns
        -------
        env : array
            The amplitude envelope of the input signal
    '''
    signal = signal - np.mean(signal) # Remove DC component

    if full_rect:
        rect = np.absolute(signal)
    else:
        rect = np.maximum(signal,0)
    env_b,env_a = filters.butter(env_order/2.,np.float32(env_cutoff)/(np.float32(fs)/2.))
    env = filtfilt(env_b,env_a,rect)

    return env


def env_hilbert(signal, return_tfs=False):
    """Computes the Hilbert envelope (and tfs) of a signal

        Parameters
        ----------
        signal : array
            The original signal 
        return_tfs : bool
            True to also return the reconstructed temporal fine structure [default=False]

        Returns
        -------
        ret : array or tuple of arrays

            If return_tfs == True, then ret is a 2-element tuple: env,tfs. Otherwise, just env

    """

    signal = signal - np.mean(signal) # Remove DC component
    z = hilbert(signal)               # form the analytical signal
    env = np.abs(z)                   # envelope extraction

    if not return_tfs:
        return env
    else:
        inst_phase = np.unwrap(np.angle(z))             # inst phase
        inst_freq = np.diff(inst_phase)/(2*np.pi)*fs    # inst frequency

        # Regenerate the carrier from the instantaneous phase
        tfs = np.cos(inst_phase)
        return env,tfs

    #h = np.imag(hilbert(signal))
    #env = np.sqrt((signal**2) + h**2)
    # finestructure = np.arctan(h/signal)

