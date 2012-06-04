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

def compensate(y, fs, compensation):
    '''Shapes the input array in the frequency domain

        The input array y will be compensated in the frequency domain
        according to the values in compensation, which should contain 
        pairs of frequency (in Hz), and attenuation (in dB) values.

        This is useful for compensating for the frequency response of
        headphones, etc.
        
        Parameters
        ----------
        y : array
            Array containing waveform(s) to shape. 
        fs : scalar
            The sampling frequency.
        dB : array
            A 2d array, containing pairs of values. Each pair should consist
            of a frequency value in Hz, and an attenuation value, in dB 
            (negative values mean more attenuation).
            
        Returns
        -------
        data : array
            The input array, attenuated.
        
        Notes
        -----
        Example 1:  
        To read the compensation data from a file, if it has the format:
        500 -4
        1000 -2
        2000 -5
            
        ...using:
        >>>compdata = np.loadtxt('compfile.txt')
        
        Example 2:
        You can specify the compensation data from the command line like this:
        >>> compdata = np.array(((100, -5),(200,-3),(1000, -6)))
        >>> compdata
        array([[ 100,   -5],
               [ 200,   -3],
               [1000,   -6]])

        Then, you just call compensate:
        >>>shapedsignal = compensate(signal, fs, compdata)
    '''

    nsamples = y.shape[0]
    ExtendedCMdB = np.zeros(nsamples)

    CMn = np.round(compensation[:, 0] * nsamples / fs);    # Hz --> Sample position
    CMdB = compensation[:, 1];
    if CMn[0] > 2:
        CMn = np.hstack((2, CMn))
        CMdB = np.hstack((0, CMdB))
    else:
        CMn[0] = 2;

    if CMn.max() < nsamples/2.:
        CMn = np.hstack((CMn, nsamples/2.))
        CMdB = np.hstack((CMdB, 0))

    for i in range(len(CMn)-1):
        b = (CMdB[i+1]*CMn[i]-CMdB[i]*CMn[i+1])/(CMn[i]-CMn[i+1]);
        k = (CMdB[i]-CMdB[i+1])/(CMn[i]-CMn[i+1]);
        for j in range(int(CMn[i]),int(CMn[i+1])):
            ExtendedCMdB[j] =  k * j + b;
            ExtendedCMdB[nsamples - j + 1] =  k * j + b;

    if y.ndim > 1:
        passes = y.shape[1]
        out = np.zeros((nsamples, passes))
        for i in range(passes):
            fftout = np.fft.fft(y);
            Amp = np.abs(fftout);
            Phs = np.angle(fftout);
            AdjustedAmp = Amp * 10 ** (ExtendedCMdB/20.);
            out[:, i] = np.real(np.fft.ifft(AdjustedAmp * np.exp(1j*Phs)))  # compose time-domain signal
    else:
        fftout = np.fft.fft(y);
        Amp = np.abs(fftout);
        Phs = np.angle(fftout);
        AdjustedAmp = Amp * 10 ** (ExtendedCMdB/20.);
        out = np.real(np.fft.ifft(AdjustedAmp * np.exp(1j*Phs)))  # compose time-domain signal

    return out
