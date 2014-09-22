# -*- coding: utf-8 -*-

# Copyright (c) 2003, Stephen McGovern; All rights reserved.
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

# Start meshgrid
def meshgrid(*xi,**kwargs):
    """
    Return coordinate matrices from one or more coordinate vectors.

    Make N-D coordinate arrays for vectorized evaluations of
    N-D scalar/vector fields over N-D grids, given
    one-dimensional coordinate arrays x1, x2,..., xn.

    Parameters
    ----------
    x1, x2,..., xn : array_like
        1-D arrays representing the coordinates of a grid.
    indexing : 'xy' or 'ij' (optional)
        cartesian ('xy', default) or matrix ('ij') indexing of output
    sparse : True or False (default) (optional)
         If True a sparse grid is returned in order to conserve memory.
    copy : True (default) or False (optional)
        If False a view into the original arrays are returned in order to
        conserve memory

    Returns
    -------
    X1, X2,..., XN : ndarray
        For vectors `x1`, `x2`,..., 'xn' with lengths ``Ni=len(xi)`` ,
        return ``(N1, N2, N3,...Nn)`` shaped arrays if indexing='ij'
        or ``(N2, N1, N3,...Nn)`` shaped arrays if indexing='xy'
        with the elements of `xi` repeated to fill the matrix along
        the first dimension for `x1`, the second for `x2` and so on.

    See Also
    --------
    index_tricks.mgrid : Construct a multi-dimensional "meshgrid"
                     using indexing notation.
    index_tricks.ogrid : Construct an open multi-dimensional "meshgrid"
                     using indexing notation.

    Examples
    --------
    >>> x = np.linspace(0,1,3)   # coordinates along x axis
    >>> y = np.linspace(0,1,2)   # coordinates along y axis
    >>> xv, yv = meshgrid(x,y)   # extend x and y for a 2D xy grid
    >>> xv
    array([[ 0. ,  0.5,  1. ],
           [ 0. ,  0.5,  1. ]])
    >>> yv
    array([[ 0.,  0.,  0.],
           [ 1.,  1.,  1.]])
    >>> xv, yv = meshgrid(x,y, sparse=True)  # make sparse output arrays
    >>> xv
    array([[ 0. ,  0.5,  1. ]])
    >>> yv
    array([[ 0.],
           [ 1.]])

    >>> meshgrid(x,y,sparse=True,indexing='ij')  # change to matrix indexing
    [array([[ 0. ],
           [ 0.5],
           [ 1. ]]), array([[ 0.,  1.]])]
    >>> meshgrid(x,y,indexing='ij')
    [array([[ 0. ,  0. ],
           [ 0.5,  0.5],
           [ 1. ,  1. ]]),
     array([[ 0.,  1.],
           [ 0.,  1.],
           [ 0.,  1.]])]

    >>> meshgrid(0,1,5)  # just a 3D point
    [array([[[0]]]), array([[[1]]]), array([[[5]]])]
    >>> map(np.squeeze,meshgrid(0,1,5))  # just a 3D point
    [array(0), array(1), array(5)]
    >>> meshgrid(3)
    array([3])
    >>> meshgrid(y)      # 1D grid; y is just returned
    array([ 0.,  1.])

    `meshgrid` is very useful to evaluate functions on a grid.

    >>> x = np.arange(-5, 5, 0.1)
    >>> y = np.arange(-5, 5, 0.1)
    >>> xx, yy = meshgrid(x, y, sparse=True)
    >>> z = np.sin(xx**2+yy**2)/(xx**2+yy**2)
    """
    copy = kwargs.get('copy',True)
    args = np.atleast_1d(*xi)
    if not isinstance(args, list):
        if args.size>0:
            return args.copy() if copy else args
        else:
            raise TypeError('meshgrid() take 1 or more arguments (0 given)')

    sparse = kwargs.get('sparse',False)
    indexing = kwargs.get('indexing','xy') # 'ij'


    ndim = len(args)
    s0 = (1,)*ndim
    output = [x.reshape(s0[:i]+(-1,)+s0[i+1::]) for i, x in enumerate(args)]

    shape = [x.size for x in output]

    if indexing == 'xy':
        # switch first and second axis
        output[0].shape = (1,-1) + (1,)*(ndim-2)
        output[1].shape = (-1, 1) + (1,)*(ndim-2)
        shape[0],shape[1] = shape[1],shape[0]

    if sparse:
        if copy:
            return [x.copy() for x in output]
        else:
            return output
    else:
        # Return the full N-D matrix (not only the 1-D vector)
        if copy:
            mult_fact = np.ones(shape,dtype=int)
            return [x*mult_fact for x in output]
        else:
            return np.broadcast_arrays(*output)


def ndgrid(*args,**kwargs):
    """
    Same as calling meshgrid with indexing='ij' (see meshgrid for
    documentation).
    """
    kwargs['indexing'] = 'ij'
    return meshgrid(*args,**kwargs)
## End meshgrid

def fconv(x, h):
    '''Convolves two signals using FFT-based fast convolution

        Parameters
        ----------
        x: array
            First array
        h: array
            Second array

        Returns
        -------
        y : array
            x convolved with h
    '''
    def nextpow2(i):
        n = 2 
        while n < i: 
            n *= 2
        return n 

    ly = len(x) + len(h) - 1
    ly2 = 2**(nextpow2(ly))

    m = max(abs(x))
    x = np.fft(x, ly2)
    h = np.fft(h, ly2)

    y = x * h

    y = np.real(np.ifft(y, ly2)) # Inverse fast Fourier transform
    y = y[:ly]
    m = m/max(abs(y))
    y = m*y

    return y
    


def rir(fs, rm, src, mic, n, r):
    '''Generates room impulse responses

        Parameters
        ----------
        fs: scalar
            Sampling frequency 
        rm: list
            [x y z] dimensions of room ( in meters )
        src: list
            [x y z] coords of sound source
        mic: list
            [x y z] coords of receiver ( microphone )
        n: scalar
            program accounts  for (2*n+1)^3 virtual sources
        r: scalar
            reflection coefficient of surfaces. (-1 < r < 1)
        
        Returns
        -------
        y : array
            The impulse response
            
        Notes
        -----
        You can use fconv for fast convolution of the generated ir with a waveform
        Derived from Matlab code written by Stephen McGovern. 
        Copyright (c) 2003, Stephen McGovern; All rights reserved. 
        
        Examples
        --------
        fs = 44100; n = 12; r = .968; 
        rm = [4.59, 6.64, 2.6];  src = [1.43, 6.25, 1.3];  mic = [2.8, 2.5, 1.3];
        ir = rir(fs, rm, src, mic, n, r);
        
    '''
    
    nn = np.array(range(-n, n+1))
    rms = nn + 0.5 - 0.5*(-1.)**nn
    srcs = (-1.)**nn

    xi = srcs*src[0] + rms*rm[0]-mic[0]
    yj = srcs*src[1] + rms*rm[1]-mic[1]
    zk = srcs*src[2] + rms*rm[2]-mic[2]
    
    i,j,k = meshgrid(xi,yj,zk,indexing="ij")

    d = np.sqrt(i**2 + j**2 + k**2)
    time = np.round(fs*d/343) + 1

    e,f,g = meshgrid(nn, nn, nn, indexing="ij")
    c = r**(np.abs(e) + np.abs(f) + np.abs(g))
    e = c/d

    # Equivalent to Matlab: h = full(sparse(time(:),1,e(:)))
    h = np.zeros(int(time.flatten().max()))
    timeflat = time.flatten()  # Memoize
    eflat = e.flatten()  # Memoize
    for i in xrange(len(timeflat)):
        h[int(timeflat[i])-1] = eflat[i]

    return h/np.max(np.abs(h))
