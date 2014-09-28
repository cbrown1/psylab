# -*- coding: utf-8 -*-

# Copyright (c) 2010-2014 Christopher Brown
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
signal - A collection of functions for psychoacoustics-based signal processing. 
Some are pedagogical in nature, others might actually be useful. 

Functions include:

atten - Attenuates input array by a dB value
compensate - Shapes the input array in the frequency domain
compress - Applies simple, single-channel compression to input signal signal
envelope - Extracts the amplitude envelope from a signal
equate - Equates wavefiles in rms
erbs2f - Converts erb numbers to frequency values
f0 - Estimates the fundamental frequency of a signal
f2erbs - Converts frequency values to erb numbers
f2place - Converts a frequency (Hz) to a basilar membrane place (mm)
f2oct - Calculates the distance in octaves between two frequencies
fconv - Convolves two signals using FFT-based fast convolution
filter_bank - Filters the input array with a bank of filters
freq_compress - Performs frequency compression on a signal
freqs_logspace - Computes a range of frequencies evenly spaced in log space
gso - Varies the inter-aural correlation of a stereo signal
hcomplex - Generates harmonic complexes
hrtf_data - Helper class for handling hrtf data
ild - Applies an interaural level difference to a signal
interp - Interpolates a signal to a specified number of points
itd - Applies an interaural time difference to a signal
lts - Computes a long-term spectrum of a signal
magspec - Computes the magnitude spectrum of a signal
mix - Mixes [adds] signals, zero padding as needed and at specified offsets
mls - Generates maximum-length sequences
ms2samp - Converts milliseconds to samples
normalize - Normalizes wavefiles, so that the overall peak is 1
oct2f - Calculates frequencies from octaves
pick_peaks - Finds rms peaks in signals
pink - Generates pink noise
place2f - Converts a basilar membrane place (mm) to a frequency (Hz)
pre_emphasis - Applies a pre-emphasis filter to a signal
ramps - Applies ramps to the onsets and/or offsets of a signal
rir - Generates room impulse responses
rms - Computes the root-mean-square of a signal
samp2ms - Converts samples to milliseconds
sliding_window - Apply a sliding window to a signal for vectorized processing
smooth - Smooths a signal using windowing
specgram - Plots a nice spectrogram
specplot - Plots magnitude spectra
t60 - Estimates reverberation time
tone - Generates pure tones
vocoder - Implements an envelope vocoder
white - Generates white noise
zeropad - Zero pads the shorter of two or more arrays

Dependencies:

numpy, scipy
'''

from numpy.random import randn, rand
from numpy.fft import fft, ifft
from time import sleep
from scipy.signal import filter_design as filters, lfilter, filtfilt
from .atten import atten
from .binaural import apply_itd, apply_ild, gso
from .compensate import compensate
from .compression import compress
from .envelope import envelope
from .equate import equate
from .f0 import f0
from .filter import freqs_logspace, filter_bank, pre_emphasis
from .freq_compression import freq_compress
from .frequency import f2oct, oct2f, f2erbs, erbs2f, place2f, f2place
from .hcomplex import hcomplex, hcomplex_old
from .hrtf import convolve, hrtf_data
from .interp import interp
from .mix import mix
from .noise import pink, white, irn, mls
from .normalize import normalize
from .peakpick import pick_peaks
from .ramps import ramps
from .rir import rir, fconv
from .rms import rms
from .samp import samp2ms, ms2samp
from .smooth import smooth
from .spec import lts, magspec, specgram, specplot
from .spl import spl2sp, spl2si, sp2spl, si2spl
from .tone import tone
from .t60 import t60
from .vocoder import vocoder, vocoder_vect, vocoder_overlap
from .window import sliding_window
from .zeropad import zeropad
