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
from scipy.stats import linregress

def cumr2(x, y):

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

def t60(data, fs, toplot=False):
    '''Estimates reverberation time
        
        Generates an integrated impulse decay curve, and uses it to estimate
        reverberation time as T60, or the time it takes for the reverberant 
        energy to decay by 60 dB.
    
        Parameters
        ----------
        data : ndarray
            The input array. Pass only the segment of the IR after the offset 
            of the impulse
        fs : scalar
            The sampling frequency
        toplot : bool
            True to return slope and y-intercept values (useful if you plan 
            to plot the iidc along with a line for visual inspection)
        
        Returns
        -------
        t : scalar
            The estimated T60 (reverberation time), in ms
        y : array
            The iidc
        slope : scalar [optional]
            The slope of the line used to estimate T60
        intercept : scalar [optional]
            The y-intercept of the line used to estimate T60

        Notes
        -----
        Reference: Schroeder, M.R. (1965). New method of measuring reverberation
        time. Journal of the Acoustical Society of America, 37, 409-412.
        
        Example
        -------
        rt,iidc = t60(signal,fs)
        rt,iidc,slope,intercept = t60(signal,fs,True)
        xtime = numpy.linspace(0,float(len(iidc))/fs,len(iidc))
        plot(xtime,iidc,'b-')
        plot((0,-60),(0,intercept),'r-')
    '''
    
    y = np.flipud( np.cumsum( np.flipud( data**2 ) ) ) ; # time-reverse, integrate, reverse again
    y = 10 * np.log10( y / np.max( np.abs( y ) ) ); # Convert to dB
    xtime = np.linspace( 0, ( len( y ) / ( fs / 1000. ) ), len( y ) ) ;
    begin = np.round( fs * .05 ); # Assume slope extends to at least 50 ms (adjust as necessary
    r2 = cumr2( xtime[ begin: ], y[ begin: ] ) ; # Get cumulative r2's
    r2max = np.nonzero( r2[ 2: ] == np.max( r2[ 2: ] ) ) ; # Find all of the points along slope where r2 is max
    stop = begin + 2 + r2max[ -1 ] ; # Use index of the max(r2) that is furthest down the slope
    slope, intercept, r, prob, stderr = linregress( xtime[ begin:stop[ 0 ] ], y[ begin:stop[ 0 ] ] ) ;
    rt = np.round( np.abs( 60. / slope ) - intercept ) ;
    if toplot:
        ret = rt, y, slope, intercept
    else:
        ret = rt, y
      
    return ret
