# -*- coding: utf-8 -*-

# Copyright (c) John Vinyard, Christopher Brown
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
from numpy.lib.stride_tricks import as_strided
from itertools import product

def sliding_window(sig, ws, ss = None, flatten = True):
    '''Return a sliding window over a in any number of dimensions
    
        Parameters
        ----------
        sig : array
            The n-dimensional input signal
        ws : int or tuple
            an int (a is 1D) or tuple (a is 2D or greater) representing the 
            size of each dimension of the window
        ss : int or tuple
            an int (a is 1D) or tuple (a is 2D or greater) representing the 
            amount to slide the window in each dimension. If not specified, it
            defaults to ws.
        flatten : bool
            if True, all slices are flattened, otherwise, there is an extra 
            dimension for each dimension of the input.
         
        Returns
        -------
        y : array
            an array containing each n-dimensional window from a
            
        Notes
        -----
        This code was retrieved on 2014-07-24 from:
        http://www.johnvinyard.com/blog/?p=268
        
        Edits include:
          * Removed dependency to custom function norm_shape, which no longer 
            appears necessary with modern numpy versions
          * Renamed some variables for clarity
          * Improved docstrings
          * Other minor cleanup
    '''
    
    if isinstance(ws, (int,float)):
        ws = (ws,)
    if None is ss:
        ss = ws
    elif isinstance(ss, (int,float)):
        ss = (ss,)
    
    # convert ws, ss, and a.shape to numpy arrays so that we can do math in every
    # dimension at once.
    ws = np.array(ws)
    ss = np.array(ss)
    shape = np.array(sig.shape)
        
    # ensure that ws, ss, and a.shape all have the same number of dimensions
    ls = [len(shape),len(ws),len(ss)]
    if 1 != len(set(ls)):
        raise ValueError(\
        'sig.shape, ws and ss must all have the same length. They were %s' % str(ls))
    
    # ensure that ws is smaller than a in every dimension
    if np.any(ws > shape):
        raise ValueError(\
        'ws cannot be larger than a in any dimension.\
        sig.shape was %s and ws was %s' % (str(sig.shape),str(ws)))
    
    # how many slices will there be in each dimension?
    newshape = tuple(((shape - ws) // ss) + 1)
    # the shape of the strided array will be the number of slices in each dimension
    # plus the shape of the window (tuple addition)
    newshape += tuple(ws)
    # the strides tuple will be the array's strides multiplied by step size, plus
    # the array's strides (tuple addition)
    newstrides = tuple(np.array(sig.strides) * ss) + sig.strides
    strided = as_strided(sig,shape = newshape,strides = newstrides)
    if not flatten:
        return strided
    
    # Collapse strided so that it has one more dimension than the window.  I.e.,
    # the new array is a flat list of slices.
    meat = len(ws) if ws.shape else 0
    firstdim = (np.product(newshape[:-meat]),) if ws.shape else ()
    dim = firstdim + (newshape[-meat:])
    # remove any dimensions with size 1
    dim = filter(lambda i : i != 1,dim)
    return strided.reshape(dim)
    
