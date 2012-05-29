# -*- coding: utf-8 -*-

# Copyright (c) 2009 by Julius O. Smith III
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
from scipy.signal import lfilter

def pink(N):
    '''Generates pink noise

    Parameters
    ----------
    n : scalar
        A number of samples.
    
    Returns
    -------
    y : array
        The pink noise.
    
    Notes
    -----
    Adapted from: 
    https://ccrma.stanford.edu/~jos/sasp/Example_Synthesis_1_F_Noise.html
    Citation:
    Smith, Julius O. Spectral Audio Signal Processing, October 2008 Draft,
    http://ccrma.stanford.edu/~jos/sasp/, online book, accessed May 2009.
    '''

    B = np.array((0.049922035, -0.095993537, 0.050612699, -0.004408786));
    A = np.array((1, -2.494956002, 2.017265875, -0.522189400));
    nT60 = np.round(np.log(1000)/(1-np.max(np.abs(np.roots(A))))); # T60 est.
    v = np.random.randn(N+nT60); # Gaussian white noise: N(0,1)
    x = lfilter(B,A,v);    # Apply 1/F roll-off to PSD
    return x[nT60+1:];    # Skip transient response
