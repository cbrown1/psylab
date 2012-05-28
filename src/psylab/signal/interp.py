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
from scipy import interpolate

def interp_bad(y, n):
    '''Returns y interpolated to n points using bad interpolation
        (completely aliased)
     
        BROKEN!

        Parameters
        ----------
        sig : array
            The input signal.
        n : scalar
            The number of points to interpolate to.
        
        Returns
        -------
        y : array
            The interpolated signal.
'''
    x = np.arange(0,len(y))
    new_x = np.linspace(0,len(y)-1,n)
    f = interpolate.interp1d(x, y)
    new_y = f(new_x) 
    return np.floor(new_y)

def interp_lin(y, n):
    '''Interpolates a signal using linear interpolation
        
        Returns y interpolated to n points using linear interpolation
        
        Parameters
        ----------
        sig : array
            The input signal.
        n : scalar
            The number of points to interpolate to.
        
        Returns
        -------
        y : array
            The interpolated signal.
    '''
    x = np.arange(0,len(y))
    new_x = np.linspace(0,len(y)-1,n)
    f = interpolate.interp1d(x, y)
    new_y = f(new_x) 
    return new_y

def interp_spline(y, n):
    '''Interpolates a signal using cubic spline interpolation
        
        Returns y interpolated to n points using cubic spline interpolation
        
        Parameters
        ----------
        sig : array
            The input signal.
        n : scalar
            The number of points to interpolate to.
        
        Returns
        -------
        y : array
            The interpolated signal.
    '''
    from scipy import interpolate
    x = np.arange(0,len(y))
    new_x = np.linspace(0,len(y)-1,n)
    tck = interpolate.splrep(x,y)
    new_y = interpolate.splev(new_x, tck)
    return new_y
