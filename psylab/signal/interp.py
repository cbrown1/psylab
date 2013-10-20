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
from scipy import interpolate

def interp(sig, n, kind='linear'):
    '''Returns y interpolated to n points using specified interpolation
     
        This is just a convenience function that wraps scipy's interp1d.

        Parameters
        ----------
        sig : array
            The input signal.
        n : scalar
            The number of points to interpolate to.
        kind: str or int
            The type of interpolation to use. This gets passed as is to the 
            'kind' parameter of scipy.interpolate.interp1d. Can be 'zero' 
            (completely aliased), 'lin', and so on. Consult the scipy 
            function's docstring for more info.
        
        Returns
        -------
        y : array
            The interpolated signal.
'''

    x = np.linspace(0,sig.size,sig.size)
    xx = np.linspace(0,sig.size,n)
    f = interpolate.interp1d(x,sig)
    yy = f(xx)

    return(yy)
