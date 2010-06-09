# -*- coding: utf-8 -*-

# Copyright (c) 2008-2010 Christopher Brown; All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
#    * Redistributions of source code must retain the above copyright 
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright 
#      notice, this list of conditions and the following disclaimer in 
#      the documentation and/or other materials provided with the distribution
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
#
# Comments and/or additions are welcome (send e-mail to: c-b@asu.edu).
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
