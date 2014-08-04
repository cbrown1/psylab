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
from .window import sliding_window

def rms(sig):
    '''Computes the root-mean-square of a signal
        
        Returns the root-mean-square of an array of numbers, working along the 
        first dimension. 
        
        Parameters
        ----------
        sig : array
            The input signal.
        
        Returns
        -------
        y : scalar
            The root-mean-square of the input.
    '''
    return np.sqrt(np.mean(sig**2.,axis=0))

def rms_win(sig, window_size):
    '''Slides a window through the signal and computes an rms, with no overlap

        Parameters
        ----------
        sig : array
            The input signal.
        window_size : int
            The size of the analysis window
        
        Returns
        -------
        y : array
            The root-mean-square values of the windowed input signal.
            
        Notes
        -----
        Depends on window

    '''
    if len(data.shape) < 2:
        ws = window_size
    else:
        ws = (window_size,data.shape[1])
    return np.sqrt(np.mean(sliding_window(sig,ws)**2,axis=1))
