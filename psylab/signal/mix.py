# -*- coding: utf-8 -*-

# Copyright (c) 2010-2013 Christopher Brown
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
from .zeropad import zeropad

def mix( *args, **kwargs ):
    '''Mixes [adds] signals at specified offsets, zero padding as needed

        This function may be useful when you need to combine two or more 
        signals that may be of varying lengths, or when some amout of delay is 
        needed in one or more of the signals. The reason for the existence of 
        this function is that doing this kind of thing by hand is actually a 
        pain in the ass with numpy, which makes working with both 1-d and 2-d 
        arrays tedious (eg., look at all the if statements in the code). 

        Parameters
        ----------
        args : tuple of 1-d arrays
            A number of arrays to be combined.
        offsets : list of scalars
            An optional list of offset values, in samples. Should be either
            ommitted or set to `None` for no offsets. The list will be zero-
            padded if it is shorter in length than the number of input arrays,
            and truncated if it is longer.
        as_channels : bool
            True to combine signals along dim 1 (ie., as separate audio 
            channels), False to sum all signals into a single channel 
            [default = False]

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
    out = np.zeros((1,))

    if 'offsets' in kwargs and kwargs['offsets'] is not None:
        offsets_a = np.array(kwargs['offsets'])
        if len(offsets_a) < len(args):
            offsets_a = np.hstack((offsets_a,np.zeros(len(args)-len(offsets_a))))
        elif len(offsets_a) > len(args):
            offsets = offsets_a[:len(args)]
        offsets = list(offsets_a)
    else:
        offsets = list(np.zeros(len(args)))
        
    if 'as_channels' in kwargs and kwargs['as_channels'] is not None:
        as_channels = kwargs['as_channels']
    else:
        as_channels = False

    for sig,off in zip(args,offsets):
        if len(sig.shape) == 1:
            prepad = np.zeros((off,))
        else:
            prepad = np.zeros((off,sig.shape[1]))
        this = np.concatenate((prepad, sig))
        this,out = zeropad(this,out)
        if as_channels:
            out = np.vstack((out.T,this.T)).T
        else:
            out = out + this
    if as_channels:
        out = out[:,1:] # Channel 1 is all zeros (from instantiation), so remove
    return out
