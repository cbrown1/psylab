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
signal - A collection of functions generally useful for psychoacoustics-based
signal processing.

Functions include:

atten - Attenuates input array by a dB value
compensate - Shapes the input array in the frequency domain [UNTESTED]
envelope - Extracts the amplitude envelope from a signal
equate - Equates wavefiles in rms
erbs2f - Converts erb numbers to frequency values
f2erbs - Converts frequency values to erb numbers
f2place - Converts a frequency (Hz) to a basilar membrane place (mm)
f2oct - Calculates the distance in octaves between two frequencies
fconv - Convolves two signals using FFT-based fast convolution
filterbank - Filters the input array with a bank of filters [UNTESTED]
f0 - Estimates the fundamental frequency of a signal
gammatone - Computes the filter coefficients for a bank of Gammatone filters [UNTESTED]
hcomplex - Generates harmonic complexes
interp_lin - Interpolates a signal using linear interpolation
interp_spline - Interpolates a signal using cubic spline interpolation
magspec - Computes the magnitude spectrum of a signal
mls - Generates maximum-length sequences
ms2samp - Converts milliseconds to samples
normalize - Normalizes wavefiles, so that the overall peak is 1
oct2f - Calculates frequencies from octaves
pink - Generates pink noise
place2f - Converts a basilar membrane place (mm) to a frequency (Hz)
ramps - Applies ramps to the onsets and/or offsets of a signal
rir - Generates room impulse responses
rms - Computes the root-mean-square of a signal
samp2ms - Converts samples to milliseconds
sinegen - Generates pure tones
smooth - Smooths a signal using windowing
specgram - Plots a nice spectrogram
specplot - Plots magnitude spectra
t60 - Estimates reverberation time
vocoder - Implements an envelope vocoder
wavplay - Plays a signal using the soundcard
wavread - Reads wavefiles
wavwrite - Writes wavefiles
zeropad - Zero pads the shorter of two or more arrays

Dependencies:

numpy, scipy
'''

# A few imports for convenience
from numpy.random import randn, rand
from numpy.fft import fft, ifft
from time import sleep
from scipy.signal import filter_design as filters, lfilter, filtfilt

#import audiere

from atten import atten
from compensate import compensate
from envelope import envelope
from equate import equate
from frequency import f2oct, oct2f, f2erbs, erbs2f, place2f, f2place
from f0 import f0
from gammatone import gammatone, filterbank
from hcomplex import hcomplex
from interp import interp_bad, interp_lin, interp_spline
from irn import irn
from magspec import magspec
from mix import mix
from mls import mls
from ms2samp import ms2samp
from normalize import normalize
from pink import pink
from ramps import ramps
from rir import rir, fconv
from samp2ms import samp2ms
from smooth import smooth
from specgram import specgram
from specplot import specplot
from t60 import t60
from tone import tone
from vocoder import vocoder
from waveio import wavread, wavwrite
#from wavplay import wavplay
from zeropad import zeropad
