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

def compensate(y, fs, compensation):
    '''Shapes the input array in the frequency domain

        The input array y will be compensated in the frequency domain
        according to the values in compensation, which should contain 
        pairs of frequency (in Hz), and attenuation (in dB) values.

        This is useful for compensating for the frequency response of
        headphones, etc..
        
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
    else:
        passes = 1

    out = np.zeros((nsamples, passes))
    for i in range(passes):
        fftout = np.fft.fft(y);
        Amp = np.abs(fftout);
        Phs = np.angle(fftout);
        AdjustedAmp = Amp * 10 ** (ExtendedCMdB/20.);
        out[:, i] = np.real(np.fft.ifft(AdjustedAmp * np.exp(1j*Phs)))  # compose time-domain signal
    return out
