# -*- coding: utf-8 -*-

import numpy as np

def fftwin(sig, fftsize, window=None):
    siglen = len(sig)    
    pt = 0
    newpt = pt + fftsize
    n = 0
    ltfft = np.zeros(fftsize/2+1)
    if window == None:
        window = np.hamming(fftsize)
    while siglen > newpt:
        thissig = sig[pt:newpt] # * window
        ltfft += np.real(np.fft.rfft(thissig))
        pt = newpt + 1
        newpt = pt + fftsize
        n += 1
    ltfft += np.real(np.fft.rfft(sig[pt:],fftsize)) # * window)
    return ltfft / (n+1)
