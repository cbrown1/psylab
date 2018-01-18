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
import numpy.polynomial.polynomial as poly

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

def angle2f(x, stakhovskaya=True):
    '''Takes an angle into the cochlea, in degrees, and estimates a frequency in Hz
        
        if stakhovskaya = True [default], then polynomial coefficients derived from 
        a least-squares fit to the data in [1] will be used. Otherwise, the 
        mathmatical formula proposed in [2] will be used, which assumes that each 
        90 degrees represents a 1-octave change.

        [1] Stakhovskaya, O., Sridhar, D., Bonham, B., Leake, P. (2007). Frequency Map 
        for the Human Cochlear Spiral Ganglion: Implications for Cochlear Implants. 
        J Assoc Res Otolaryngol. 2007 June ; 8(2): 220–233.

        [2] Kang Cheng, Vivien Cheng and Chang-Hua Zou, (2008). A Logarithmic Spiral 
        Function to Plot a Cochleaogram. Trends in Medical Research, 3: 36-40.

        Parameters
        ----------
        x : scalar
            An angle, in degrees.
        stakhovskaya : Bool
            Whether to make the estimate based on Stakhovskaya's data.
        
        Returns
        -------
        f : scalar
            A frequency, in Hz.
    '''
    if stakhovskaya:
        stakh_coeffs = np.array([  1.71238469e+04,  -1.72587384e+02,  -2.29043020e-02,
                                1.67009544e-02,  -1.69880138e-04,   8.55464402e-07,
                               -2.48892410e-09,   4.10578945e-12,  -2.78555293e-15,
                               -2.34625856e-18,   6.41128833e-21,  -5.05875380e-24,
                                1.46471401e-27])
        ffit = poly.Polynomial(stakh_coeffs)
        return ffit(x)
    else:
        return 2048. * (2.**((360.-x)/90.))
    
def f2angle(f, stakhovskaya=True):
    '''Takes a frequency in Hz and estimates an angle into the cochlea, in degrees
        
        if stakhovskaya = True [default], then polynomial coefficients derived from 
        a least-squares fit to the data in [1] will be used. Otherwise, the 
        methematical formula proposed in [2] will be used, which assumes that each 
        90 degrees represents a 1-octave change.

        [1] Stakhovskaya, O., Sridhar, D., Bonham, B., Leake, P. (2007). Frequency Map 
        for the Human Cochlear Spiral Ganglion: Implications for Cochlear Implants. 
        J Assoc Res Otolaryngol. 2007 June ; 8(2): 220–233.

        [2] Kang Cheng, Vivien Cheng and Chang-Hua Zou, (2008). A Logarithmic Spiral 
        Function to Plot a Cochleaogram. Trends in Medical Research, 3: 36-40.
        
        The function assumes that each 90 degrees represents a 1-octave change.

        Parameters
        ----------
        f : scalar
            A frequency, in Hz.
        stakhovskaya : Bool
            Whether to make the estimate based on Stakhovskaya's data.
        
        Returns
        -------
        x : scalar
            An angle, in degrees.
    '''

    if stakhovskaya:
        stakh_coeffs = np.array([ 7.65812568e+02,  -7.80101136e-01,   4.12282815e-04,
                               -3.64080739e-08, -5.97333469e-11,   3.14151231e-14,
                               -7.83824139e-18,  1.18105511e-21,  -1.14512584e-25,
                                7.20438529e-30, -2.84655168e-34,   6.42398815e-39,
                               -6.31973435e-44])
        ffit = poly.Polynomial(stakh_coeffs)
        return ffit(f)
    else:
        return 1350. - ((np.log2(f)/11.)*990)

