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
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# Comments and/or additions are welcome. Send e-mail to: cbrown1@pitt.edu.
#

import numpy as np

def zeropad( *args ):
    '''Zero pads two or more arrays to be the same length
        
        Ensures two or more arrays are the same length using zero-padding 
        if necessary. Input arrays can be 1- or 2-dimensional, but the 
        function always works along the first dimension of all arrays. 
    
        Parameters
        ----------
        args: tuple of arrays
            Function takes any number of 1- or 2-dimensional input arrays. 

        Returns
        -------
        args : tuple of arrays
            The input tuple of arrays is returned.
            
        Example
        -------
        # Assume a, b, and c are arrays, possibly of varying length 
        a,b,c = zeropad(a,b,c) # The first dimension of all three are now same length
    '''
    length = 0
    out = list(args)
    for arg in args:
        if arg.shape[0] > length:
            length = arg.shape[0]

    for n in range(0, len(args)):
        if length > args[n].shape[0]:
            if args[n].ndim == 1:
                out[n] = np.concatenate((args[n], np.zeros(length-args[n].shape[0])))
            else:
                out[n] = np.concatenate((args[n], np.zeros((length-args[n].shape[0],args[n].shape[1]))))
                
    return tuple(out)
