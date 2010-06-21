# -*- coding: utf-8 -*-

# Copyright (c) 2009 by Julius O. Smith III
# Copyright (c) 2009-2010 Christopher Brown; All Rights Reserved.
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
