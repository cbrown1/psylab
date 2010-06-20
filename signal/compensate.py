# -*- coding: utf-8 -*-

import numpy as np
from os.path import isfile

def compensate(y, fs, compensation):
    '''Shapes the input array in the frequency domain

        The input array y will be compensated in the frequency domain
        according to the values in compensation, which should contain a
        column of frequency values (Hz), and a column of attenuation
        values (dB),

        This is useful for compensating for the frequency response of
        headphones, etc..

    '''

    if isinstance(compensation, np.ndarray):
        compdata = compensation
    elif isfile(compensation):
        compdata = np.loadtxt('comp')
    else:
        pass;
        # Throw error, wrong comp type

    nsamples = y.shape[0]
    ExtendedCMdB = np.zeros(nsamples)

    CMn = np.round(compdata[:, 0] * nsamples / fs);    # Hz --> Sample position
    CMdB = compdata[:, 1];
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
        for j in range(CMn[i],CMn[i+1]):
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
