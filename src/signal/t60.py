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
