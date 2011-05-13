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
