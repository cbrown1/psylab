# -*- coding: utf-8 -*-

# Copyright (c) 2009 by Julius O. Smith III
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
# contributions are welcome. Go to https://github.com/cbrown1/psylab/
# for more information and to contribute. Or send an e-mail to:
# cbrown1@pitt.edu.
#

import numpy as np
from scipy.signal import lfilter

def white(n, channels=None):
    """Generates white noise

        The noise is normalized (peak == 1)

        Parameters
        ----------
        n : scalar
            A number of samples (dim 0)
        channels : scalar
            A number of channels (dim 1)

        Returns
        -------
        y : array
            The white noise.
    """
    if channels:
        out = np.random.randn(np.int(n), np.int(channels))
    else:
        out = np.random.randn(np.int(n))
    return out/np.max(np.abs(out), axis=0)


def pink(n, channels=None):
    """Generates pink noise

        The noise is normalized (peak == 1)

        Parameters
        ----------
        n : scalar
            A number of samples (dim 0)
        channels : scalar
            A number of channels (dim 1)

        Returns
        -------
        y : array
            The pink noise.

        Notes
        -----
        Adapted from:
        https://ccrma.stanford.edu/~jos/sasp/Example_Synthesis_1_F_Noise.html
        Citation:
        Smith, Julius O. Spectral Audio Signal Processing, October 2008 Draft,
        http://ccrma.stanford.edu/~jos/sasp/, online book, accessed May 2009.
    """

    b = np.array((0.049922035, -0.095993537, 0.050612699, -0.004408786))
    a = np.array((1, -2.494956002, 2.017265875, -0.522189400))
    nT60 = np.round(np.log(1000)/(1-np.max(np.abs(np.roots(a))))) # T60 est.
    if channels:
        v = np.random.randn(np.int(n+nT60), np.int(channels)) # Gaussian white noise: N(0,1)
        x = np.zeros_like(v)
        for i in np.arange(channels):
            x[:,i] = lfilter(b,a,v[:,i])   # Apply 1/F roll-off to PSD
        out = x[np.int(nT60):,:]                 # Skip transient response
    else:
        v = np.random.randn(np.int(n+nT60)) # Gaussian white noise: N(0,1)
        x = lfilter(b,a,v)                 # Apply 1/F roll-off to PSD
        out = x[np.int(nT60):]                   # Skip transient response
    return out/np.max(np.abs(out), axis=0)


def irn(dur, fs, delay, gain, its, type=1):
    '''Generates iterated rippled noise

        Generates iterated rippled noise, or noise with a rippled spectrum, by
        implementing a delay-attenuate-add method.

        Parameters
        ----------
        dur : scalar
            Duration of the noise, in s.
        fs : scalar
            The sample frequency.
        delay : scalar
            The delay, in ms. The F0 of the pitch will be 1/delay.
        gain : scalar
            The attenuation. The strength of the pitch is set by the gain.
        its : scalar
            The number of iterations.
        type : scalar
            1 = IRNO; 2 = IRNS.

        Returns
        -------
        y : array
            The rippled noise.
    '''
    dd = np.int(dur/1000.);
    wbn = np.random.randn(fs);
    rip = wbn;

    if type == 1:
        for it in range(its):
            rip[:fs-delay] = rip[delay:fs];
            rip = ( rip * gain ) + wbn;

    elif type == 2:
        for it in range(its):
            rip1 = rip;
            rip[:fs-delay] = rip[delay:fs];
            rip = rip + ( gain * rip1 );

    rip = rip / np.max(np.abs(rip))
    return rip[:np.round(dd * fs)];

# MLS stuff here

# Encodings of primitive polynomials for use as tap values,
# decremented to account for mapping onto zero-indexed arrays.
mls_taps = {2 : [1, 0],
        3 : [2, 0],
        4 : [3, 0],
        5 : [4, 1],
        6 : [5, 0],
        7 : [6, 0],
        8 : [7, 5, 4, 0],
        9 : [8, 3],
        10 : [9, 2],
        11 : [10, 1],
        12 : [11, 6, 3, 2],
        13 : [12, 3, 2, 0],
        14 : [13, 11, 10, 0],
        15 : [14, 0],
        16 : [15, 4, 2, 1],
        17 : [16, 2],
        18 : [17, 2],
        19 : [18, 5, 4, 0],
        20 : [19, 2],
        21 : [20, 1],
        22 : [21, 0],
        23 : [22, 4],
        24 : [23, 3, 2, 0],
        25 : [24, 2],
        26 : [25, 7, 6, 0],
        27 : [26, 7, 6, 0],
        28 : [27, 2],
        29 : [28, 1],
        30 : [29, 15, 14, 0],
        31 : [30, 2],
        32 : [31, 27, 26, 0]
       }

# Encodings of the above polynomials as binary digits in a hexadecimal representation.
# For a given k in "taps", the argument to np.int64 is determined by sum([2**i for i in taps[k]])
mls_bintaps = {2 : 3,
           3 : 5,
           4 : 9,
           5 : 18,
           6 : 33,
           7 : 65,
           8 : 177,
           9 : 264,
           10 : 516,
           11 : 1026,
           12 : 2124,
           13 : 4109,
           14 : 11265,
           15 : 16385,
           16 : 32790,
           17 : 65540,
           18 : 131076,
           19 : 262193,
           20 : 524292,
           21 : 1048578,
           22 : 2097153,
           23 : 4194320,
           24 : 8388621,
           25 : 16777220,
           26 : 33554625,
           27 : 67109057,
           28 : 134217732,
           29 : 268435458,
           30 : 536920065,
           31 : 1073741828,
           32 : 2348810241
          }

def generate_lfsr(n, use_rand_seed=False):
    toggle_mask = mls_bintaps[n]
    if use_rand_seed:
        lfsr = np.random.randint(1, (2**n - 1))
    else:
        lfsr = 1

    while 1:
        lsb = lfsr & 1
        yield lsb
        lfsr = (lfsr >> np.int64(1)) ^ (np.int64(0) - (lfsr & np.int64(1)) & toggle_mask)

def mls(n, rand_seed=False):
    '''Generates maximum-length sequences

        Implements a Galois-configuration linear feedback shift register
        to generate maximum-length sequences, which are pseudorandom noises
        useful for acoustic measurements.

        Parameters
        ----------
        n : scalar
            The number of starting bits.
        rand_seed : bool
            True to begin with a sequence of all ones (repeatable).
            False to begin with a random sequence.

        Returns
        -------
        y : array
            The maximum-length sequence, which is 2^(n-1) in length.

        Notes
        -----
        Further information at:
        http://www.newwaveinstruments.com/resources/articles/m_sequence_linear_feedback_shift_register_lfsr.htm
        http://www.cfn.upenn.edu/aguirre/wiki/public:m_sequences
        Primitive binary polynomials obtained from:
          Stahnke, W. (1973). "Primitive binary polynomials," Mathematics of Computation, 27:977-980.
'''

    try:
        assert type(n) == type(1) # Ensure 'n' is an int
        assert 2 <= n <= 32
    except:
        print("n must be an integer in the interval [2, 32].")

    seqlen = 2**n - 1

    # Initialize the linear feedback shift register, val = 1 for all indices.
    lfsr = generate_lfsr(n, rand_seed)

    #mls = np.ones(n, dtype=np.int32)
    def zero_to_neg_one(x):
        if x == 0:
            return -1
        else:
            return 1
#    zero_to_neg_one = lambda x: x
    return np.array([zero_to_neg_one(next(lfsr)) for i in np.arange(seqlen)], np.float64)
