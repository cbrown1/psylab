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

'''
frequency.py - A collection of functions for various frequency conversions. 

Functions include:

f_logspace - Calculates a frequency range in logspace
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


def f_logspace(start, stop, n):
    '''Calculates a frequency range in logspace
        
        Returns a number frequencies within the specified range, in log space.
        The array returns will have a length of n + 1.
    
        Parameters
        ----------
        start : scalar
            The start frequency frequency. 
        stop : scalar
            The end frequency.
        n : scalar
            The number of frequencies to compute.
        
        Returns
        -------
        freqs : array
            An array of frequencies.
    '''
    n_arr = np.arange(n+1)
    interval = np.log10(stop/float(start))/float(n)
    freqs = start*10.**(interval*n_arr)
    return freqs


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
