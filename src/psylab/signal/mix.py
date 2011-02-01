# -*- coding: utf-8 -*-

# Copyright (c) 2010-2011 Christopher Brown; All Rights Reserved.
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
from zeropad import zeropad

def mix( *args, **kwargs ):
    '''Mixes [adds] signals at specified offsets, zero padding as needed

        This function may be useful when you need to combine two or more signals
        that may be of varying lengths, or when some amout of delay is needed in
        one or more of the signals.

        Parameters
        ----------
        args : tuple of 1-d arrays
            A number of arrays to be combined.

        offsets : list of scalars
            An optional list of offset values, in samples. Should be either
            ommitted or set to `None` for no offsets. The list will be zero-
            padded If it is shorter in length than the number of input arrays,
            and truncated if it is longer.

        Returns
        -------
        out : array
            The input arrays combined

        Examples
        --------

        >>>import numpy as np
        >>>a = np.ones(3)  # 3 one's: array([ 1.,  1.,  1.])
        >>>b = np.ones(5)*4  # 5 four's
        >>>c = np.ones(10)*-3  # 10 negative three's
        >>>mix(a,b)
        array([ 3.,  3.,  3.,  2.,  2.])
        >>>mix(a,b,offsets=[1]) # offset a by 1
        array([ 2.,  3.,  3.,  3.,  2.])
        >>>mix(a,b,c,offsets=[0,5]) # offset a by 0 and b by 5
        array([-2., -2., -2., -3., -3.,  1.,  1.,  1.,  1.,  1.])

    '''
    out = np.zeros(1)

    if kwargs.has_key('offsets') and kwargs['offsets'] is not None:
        offsets_a = np.array(kwargs['offsets'])
        if len(offsets_a) < len(args):
            offsets_a = np.hstack((offsets_a,np.zeros(len(args)-len(offsets_a))))
        elif len(offsets_a) > len(args):
            offsets = offsets_a[:len(args)]
        offsets = list(offsets_a)
    else:
        offsets = list(np.zeros(len(args)))

    for sig,off in zip(args,offsets):
        prepad = np.zeros(off)
        this = np.hstack((prepad, sig))
        this,out = zeropad(this,out)
        out = out + this
    return out
