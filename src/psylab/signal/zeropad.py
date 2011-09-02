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
