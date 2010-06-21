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

'''
frequency.py - A collection of functions for various frequency conversions. 

Functions include:

f2oct - Calculates octaves from frequencies
oct2f - Calculates frequencies from octaves
f2erbs - Converts frequency values to erb numbers
erbs2f - Converts erb numbers to frequency values
f2place - Converts a frequency (Hz) to a basilar membrane place (mm)
place2f - Converts a basilar membrane place (mm) to a frequency (Hz)

Dependencies:

numpy
'''

import numpy as np

def oct2f(cf, oct):
    '''Calculates frequencies from octaves
        
        Returns a tuple containing the upper and lower frequencies that 
        are the specified number of octaves away from the center frequency
        
        Parameters
        ----------
        cf : scalar
            A center frequency. 
        oct : scalar
            The distance, in octaves, to be computed.
        
        Returns
        -------
        lo : scalar
            The frequency that is oct octaves below cf.
        hi : scalar
            The frequency that is oct octaves above cf.
    '''
    lo = np.round(cf*(2.**np.float32(-oct)));
    hi = np.round(cf*(2.**np.float32(oct)));
    return lo,hi

def f2oct(f1, f2):
    '''Calculates the distance in octaves between two frequencies
        
        Parameters
        ----------
        f1 : scalar
            The first frequency value. 
        f2 : scalar
            The second frequency.
        
        Returns
        -------
        oct : scalar
            The distance, in octaves, between f1 and f2.
    '''
    return np.log2(np.float32(f2)/np.float32(f1))

def f2erbs(f):
    '''Converts frequency values to erb numbers

        converts an array of frequencies (in Hz) to the corresponding 
        values on the ERB-rate scale on which the human ear has 
        roughly constant resolution as judged by psychophysical 
        measurements of the cochlear filters.
        
        Parameters
        ----------
        f : scalar or array
            Frequencies, in Hz.
        
        Returns
        -------
        erb : scalar or array
            Equivalent rectangular bandwidth (ERB) values.
    '''
    return 21.4 * ( np.log10( 229 + f ) - 2.36 );

def erbs2f(erbs):
    '''Converts erb numbers to frequency values

        converts a vector of ERB-rate values
        to the corresponding frequencies in Hz.

        Note that erb values must not exceed 42.79

        Parameters
        ----------
        erb : scalar or array
            Equivalent rectangular bandwidth (ERB) values.
        
        Returns
        -------
        f : scalar or array
            Frequencies, in Hz.
    '''
    return ( 10 ** ( erbs/21.4 + 2.36)  ) - 229;

def f2place(x):
    '''Converts a frequency (Hz) to a basilar membrane place (mm)
        
        Takes a frequency (Hz), and computes a basilar membrane place (mm), 
        using the Greenwood equation, and constants suitable for human ears.

        Parameters
        ----------
        x : scalar
            A frequency, in Hz.
        
        Returns
        -------
        f : scalar
            A basilar membrane distance, in mm.
    '''
    return np.log10((x/165.4)+.88)/.06
    
def place2f(x):
    '''Converts a basilar membrane place (mm) to a frequency (Hz)
        
        Takes a basilar membrane place (mm), and computes a frequency (Hz), 
        using the Greenwood equation, and constants suitable for human ears.

        Parameters
        ----------
        x : scalar
            A basilar membrane place, in mm.
        
        Returns
        -------
        f : scalar
            A frequency, in Hz.
    '''
    return 165.4*(10**(.06*x)-.88)