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
signal - A collection of functions generally useful for psychoacoustics-based
signal processing.

Functions include:

atten - Attenuates input array by a dB value
compensate - Shapes the input array in the frequency domain
envelope - Extracts the amplitude envelope from a signal
equate - Equates wavefiles in rms
erbs2f - Converts erb numbers to frequency values
f0 - Estimates the fundamental frequency of a signal
f2erbs - Converts frequency values to erb numbers
f2place - Converts a frequency (Hz) to a basilar membrane place (mm)
f2oct - Calculates the distance in octaves between two frequencies
fconv - Convolves two signals using FFT-based fast convolution
filterbank - Filters the input array with a bank of filters [UNTESTED]
freq_compress - Performs frequency compression on a signal
hcomplex - Generates harmonic complexes
interp_lin - Interpolates a signal using linear interpolation
interp_spline - Interpolates a signal using cubic spline interpolation
lts - Computes a long-term spectrum of a signal
magspec - Computes the magnitude spectrum of a signal
mix - Mixes [adds] signals at specified offsets, zero padding as needed
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
tone - Generates pure tones
vocoder - Implements an envelope vocoder
zeropad - Zero pads the shorter of two or more arrays

Dependencies:

numpy, scipy
'''

# A few imports for convenience
from numpy.random import randn, rand
from numpy.fft import fft, ifft
from time import sleep
from scipy.signal import filter_design as filters, lfilter, filtfilt
from .atten import atten
from .compensate import compensate
from .envelope import envelope
from .equate import equate
from .frequency import f2oct, oct2f, f2erbs, erbs2f, place2f, f2place
from .f0 import f0
from .freq_compression import freq_compress
from .interp import interp_bad, interp_lin, interp_spline
from .lts import lts
from .magspec import magspec
from .mix import mix
from .ms2samp import ms2samp
from .normalize import normalize
from .ramps import ramps
from .rir import rir, fconv
from .rms import rms
from .samp2ms import samp2ms
from .smooth import smooth
from .specgram import specgram
from .specplot import specplot
from .tone import tone
from .t60 import t60
from .vocoder import vocoder, vocoder_overlap
from .zeropad import zeropad
