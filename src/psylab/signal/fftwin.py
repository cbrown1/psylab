# -*- coding: utf-8 -*-

import numpy as np

def fftwin(sig, fftsize, window=None, overlap=0):

    if not wtype in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is one of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

    if window in ['flat', None]:
        w=np.ones(fftsize,'d')
    else:
        w=eval('np.'+window+'(fftsize)')

    siglen = len(sig)
    n = 1.
    i1 = 0
    i2 = fftsize
    ltfft = np.zeros(fftsize/2+1)
    while siglen > i2:
        thissig = sig[i1:i2] * w
        ltfft += np.real(np.fft.rfft(thissig))
        i1 = i2 + 1 - overlap
        i2 = i1 + fftsize
        n += 1.
    wsize = len(sig)-i1-overlap
    w = eval('np.' + window + '(wsize)')
    ltfft += np.real(np.fft.rfft(sig[i1-overlap:]* w,fftsize))
    return ltfft / n
