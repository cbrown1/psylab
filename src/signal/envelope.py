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
from scipy.signal import filter_design as filters, filtfilt, hilbert

def envelope(signal,fs,use_hilbert=False,env_cutoff=16.,env_order=4.):
    '''Extracts the amplitude envelope from a signal
    
        If use_hilbert is False, half-wave rectification and low-pass 
        filtering is used (default cutoff frequency is 16 Hz, default 
        filter order is 6. If usehilbert is True, the Hilbert transform
        is used.
        
        Parameters
        ----------
        signal : array
            The signal to extract the amplitude envelope from. 
        fs : scalar
            The sampling frequency.
        use_hilbert : bool
            True to use hilbert method [env_cutoff and env_order are ignored]
            False to use half-wave rectification and low-pass filtering
        env_cutoff : scalar
            The envelope cutoff frequency [default=16 Hz].
        env_order : scalar
            The order of the envelope filter [must be even number; default=6].
        
        Returns
        -------
        env : array
            The amplitude envelope of the input signal.
    '''
    if use_hilbert:
        h = np.imag(hilbert(signal))
        env = np.sqrt((signal**2) + h**2)
        # finestructure = np.arctan(h/signal)
    else:
        env = np.maximum(signal,0)
        env_b,env_a = filters.butter(env_order/2.,np.float32(env_cutoff)/(np.float32(fs)/2.))
        env = filtfilt(env_b,env_a,env)

    return env
