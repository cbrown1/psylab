# -*- coding: utf-8 -*-

# Copyright (c) John Vinyard, Christopher Brown
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
# contributions are welcome. Go to https://github.com/cbrown1/psylab/
# for more information and to contribute. Or send an e-mail to:
# cbrown1@pitt.edu.
#

import numpy as np
from numpy.lib.stride_tricks import as_strided
from itertools import product


def win_attack(ws, rs, ramp_fun=np.bartlett):
    """generates a window of length ws that is ramped (ramp
        length of rs) from 0 to 1, where 0 is ommitted. ramp_fun
        is the name of the windowing function to use to specify
        the shape of ramp (can be np.hanning, np.bartlett, etc).

        If rs is shorter than ws, then the rest of the window
        will be ones. 
        
           1 |   _________
        A    |  /
        m    | /
        p  0 |/
             +------------->
                |        |
               rs       ws

        If rs is longer than ws, then the value of the last
        element will be less than one. Eg., if ws is half of rs, 
        the window will be length ws, and the last element will 
        be .5.

          1 |
            |
            |
        A   |       
        m   |    /  
        p   |   / 
            |  /
            | /
          0 |/
            +------------>
                 |     |  
                ws    rs


        Parameters
        ----------
        ws : int
            window size in samples
        rs : int
            ramp size in samples
        ramp_fun : function
            The windowing function to use to shape the ramp.
            default is np.bartlett, which yeilds a linear ramp.

        Returns
        -------
        win : array
            The window

        Examples
        --------
        >>> win_attack(5, 2)
        [0.5 1.  1.  1.  1. ]

        >>> win_attack(5, 10)
        [0.1 0.2 0.3 0.4 0.5]

        Notes
        -----
        Handles gracefully cases where the ramp is longer than the win
        (ie., long attack time constants), which is the particular
        usecase this was written for.

        Also note that 0 (starting amp) does not appear in the win.
        Rather, the first value in the window will be the first
        interpolated amplitude between 0 and 1 given rs. This allows
        this function to be easily used along with sliding_window to
        allow amplitude changes over time with smooth transitions
        from one window to the next (consider rs the time constant
        of the amplitude change). Ie., to smoothly change amplitudes
        over time, use sliding window to window your data, then for
        each window, set amp_prev to be the ending amp from the
        previous window, and amp_cur to be the target amp for the
        current window. Then simply compute:

            # this_win is a window of data from sliding_window
            # attwin is the output of this function
            this_win *= (attwin * (amp_cur - amp_prev)) + amp_prev

    """
    win = np.ones(ws)
    ramp = ramp_fun((rs*2)+1)[:rs+1]
    rs_clipped = np.minimum(rs, ws)
    win[:rs_clipped] = ramp[1:rs_clipped+1]
    return win


def sliding_window(sig, ws, ss = None, flatten = True):
    '''Return a sliding window over an array in any number of dimensions

        Parameters
        ----------
        sig : array
            The n-dimensional input signal
        ws : int or tuple
            an int (a is 1D) or tuple (a is 2D or greater) representing the
            size of each dimension of the window
        ss : int or tuple
            an int (a is 1D) or tuple (a is 2D or greater) representing the
            amount to slide the window in each dimension. If not specified, it
            defaults to ws.
        flatten : bool
            if True, all slices are flattened, otherwise, there is an extra
            dimension for each dimension of the input.

        Returns
        -------
        y : array
            an array containing each n-dimensional window from a

        Notes
        -----
        This code was retrieved on 2014-07-24 from:
        http://www.johnvinyard.com/blog/?p=268

        Edits include:
          * Removed dependency to custom function norm_shape, which no longer
            appears necessary with modern numpy versions
          * Renamed some variables for clarity
          * Improved docstrings
          * Other minor cleanup
    '''

    if isinstance(ws, (int,float)):
        ws = (ws,)
    if None is ss:
        ss = ws
    elif isinstance(ss, (int,float)):
        ss = (ss,)

    # convert ws, ss, and a.shape to numpy arrays so that we can do math in every
    # dimension at once.
    ws = np.array(ws)
    ss = np.array(ss)
    shape = np.array(sig.shape)

    # ensure that ws, ss, and a.shape all have the same number of dimensions
    ls = [len(shape),len(ws),len(ss)]
    if 1 != len(set(ls)):
        raise ValueError(\
        'sig.shape, ws and ss must all have the same length. They were {}'.format(str(ls)))

    # ensure that ws is smaller than a in every dimension
    if np.any(ws > shape):
        raise ValueError(\
        'ws cannot be larger than a in any dimension.\
        sig.shape was {} and ws was {}'.format(str(sig.shape),str(ws)))

    # how many slices will there be in each dimension?
    newshape = tuple(((shape - ws) // ss) + 1)
    # the shape of the strided array will be the number of slices in each dimension
    # plus the shape of the window (tuple addition)
    newshape += tuple(ws)
    # the strides tuple will be the array's strides multiplied by step size, plus
    # the array's strides (tuple addition)
    newstrides = tuple(np.array(sig.strides) * ss) + sig.strides
    strided = as_strided(sig,shape = newshape,strides = newstrides)
    if not flatten:
        return strided

    # Collapse strided so that it has one more dimension than the window.  I.e.,
    # the new array is a flat list of slices.
    meat = len(ws) if ws.shape else 0
    firstdim = (np.product(newshape[:-meat]),) if ws.shape else ()
    dim = firstdim + (newshape[-meat:])
    # remove any dimensions with size 1
    dim = list(filter(lambda i : i != 1,dim)) # Added list for py3 compat; py3 filter returns generator
    return strided.reshape(dim)
