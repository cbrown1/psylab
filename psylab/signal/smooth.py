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

def smooth(x, wsize=10, wtype='hanning'):
    '''Smooths a signal using windowing
        
       Smooths the input signal using a window with specified size and type.

       This method is based on the convolution of a scaled window with the signal.
       The signal is prepared by introducing reflected copies of the signal 
       (with the window size) in both ends so that transient parts are minimized
       in the begining and end part of the output signal.
    
       Parameters
       ----------
       x : array
          The input signal.
       wsize : scalar
          The width of the smoothing window
       wtype : string
          The type of window:
            'flat' [Unweighted moving average]
            'hanning'
            'hamming'
            'bartlett'
            'blackman'
        
        Returns
        -------
        y : array
            The smoothed signal.
        
        Notes
        -----
       example:

       t=linspace(-2,2,0.1)
       x=sin(t)+randn(len(t))*0.1
       y=smooth(x)
    
       source:
       http://www.scipy.org/Cookbook/SignalSmooth
    
       see also: 
       
       numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
       scipy.signal.lfilter
 
       TODO: the window parameter could be the window itself if an array instead of a string.
    '''
    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < wsize:
        raise ValueError("Input vector needs to be bigger than window size.")

    if wsize<3:
        return x

    if not wtype in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is one of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s=np.r_[2*x[0]-x[wsize:1:-1],x,2*x[-1]-x[-1:-wsize:-1]]
    #print(len(s))
    if wtype == 'flat': #moving average
        w=np.ones(wsize,'d')
    else:
        w=eval('np.'+wtype+'(wsize)')

    y = np.convolve(w/w.sum(),s,mode='same')
    return y[wsize-1:-wsize+1]
