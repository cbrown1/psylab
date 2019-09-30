# -*- coding: utf-8 -*-

# Copyright (c) 2010 Christopher Brown
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

def cumr2(x, y):
    '''Computes cumulative r**2 values
        
        Computes cumulative r**2 values on the two input vectors. This type 
        of function can be useful for finding the straight part of a line. 
        
        
        Parameters
        ----------
        x : array
            The first array
        y : array
            The second array
        
        Returns
        -------
        r2 : array
            Cumulative r2 values. The first value is nan, the second is 1.
            
    '''
    last = len(x);
    r2 = np.zeros(last);
    sampsize = np.linspace(1,last,last);
    Exy2 = (np.cumsum(x * y) - ((np.cumsum(x) * np.cumsum(y)) / sampsize))**2;
    Ex2 = np.cumsum(x**2) - ((np.cumsum(x)**2) / sampsize);
    totss = np.cumsum(y**2) - ((np.cumsum(y)**2) / sampsize);
    regss = Exy2[1:] / Ex2[1:];
    r2[0] = np.nan;
    r2[1:] = regss / totss[1:];

    return r2
