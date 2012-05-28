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
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# Comments and/or additions are welcome. Send e-mail to: cbrown1@pitt.edu.
#

import numpy as np
from scipy.signal import lfilter

# Encodings of the referenced polynomials as binary digits in a hexadecimal.
# For a given k in "taps", the argument to np.uint32 is determined by sum([2**i for i in taps[k]])
mls_bintaps = {2 : np.uint32(3),     # taps = [1, 0]
               3 : np.uint32(5),            # [2, 0]
               4 : np.uint32(9),            # [3, 0]
               5 : np.uint32(18),           # [4, 1]
               6 : np.uint32(33),           # [5, 0]
               7 : np.uint32(65),           # [6, 0]
               8 : np.uint32(177),          # [7, 5, 4, 0]
               9 : np.uint32(264),          # [8, 3]
               10 : np.uint32(516),         # [9, 2]
               11 : np.uint32(1026),        # [10, 1]
               12 : np.uint32(2124),        # [11, 6, 3, 2]
               13 : np.uint32(4109),        # [12, 3, 2, 0]
               14 : np.uint32(11265),       # [13, 11, 10, 0]
               15 : np.uint32(16385),       # [14, 0]
               16 : np.uint32(32790),       # [15, 4, 2, 1]
               17 : np.uint32(65540),       # [16, 2]
               18 : np.uint32(131076),      # [17, 2]
               19 : np.uint32(262193),      # [18, 5, 4, 0]
               20 : np.uint32(524292),      # [19, 2]
               21 : np.uint32(1048578),     # [20, 1]
               22 : np.uint32(2097153),     # [21, 0]
               23 : np.uint32(4194320),     # [22, 4]
               24 : np.uint32(8388621),     # [23, 3, 2, 0]
               25 : np.uint32(16777220),    # [24, 2]
               26 : np.uint32(33554625),    # [25, 7, 6, 0]
               27 : np.uint32(67109057),    # [26, 7, 6, 0]
               28 : np.uint32(134217732),   # [27, 2]
               29 : np.uint32(268435458),   # [28, 1]
               30 : np.uint32(536920065),   # [29, 15, 14, 0]
               31 : np.uint32(1073741828),  # [30, 2]
               32 : np.uint32(2348810241)   # [31, 27, 26, 0]
              }

pink_B = np.array((0.049922035, -0.095993537, 0.050612699, -0.004408786));
pink_A = np.array((1, -2.494956002, 2.017265875, -0.522189400));
pink_nT60 = np.round(np.log(1000)/(1-np.max(np.abs(np.roots(pink_A))))); # T60 est.


def hcomplex(f, fs, **kwargs):
    '''Generates harmonic complexes

        Parameters
        ----------
        f :  scalar
            fundamental frequency
        fs : scalar
            sampling frequency

        Kwargs
        ------
        dur : scalar
            duration in ms
        amp : scalar
            amplitude values less than or equal to 0 are treated as dB (re:
            +-1), and values greater than 0 are used to scale the waveform
            peak linearly. default is 1
        ncomponents : scalar
            number of harmonic components
        offset : scalar
            offset in Hz. Eg., offset = 2 would yield 202, 302, 402, etc.

        Returns
        -------
        y : array
            The waveform
    '''
    if not 'amp' in kwargs:
        kwargs['amp'] = 1.;
    if not 'offset' in kwargs:
        kwargs['offset'] = 0.;
    f = np.float32(f);
    fs = np.float32(fs);
    dur = np.round((np.float32(kwargs['dur']) / 1000.) * fs);
    amp = np.float32(kwargs['amp']);
    nc = np.float32(kwargs['ncomponents']);
    offset = np.float32(kwargs['offset']);

    if amp <= 0:
        amp = 10. ** (amp / 20.);

    comp = np.linspace(f, f*nc, nc) + offset;
    y = np.zeros(dur);
    for i in range(nc):
        buff = np.ones(dur) * comp[i];
        y = y + (amp * np.sin(2 * np.pi * np.cumsum(buff) / fs));
    return y;


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
            The noise.
    '''
    dd = dur/1000.;
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


def mls(n, rand_seed=False):
    '''Generates maximum-length sequences

        Implements a Galois-configuration linear feedback shift register
        to generate maximum-length sequences, which are pseudorandom noises
        useful for acoustic measurements.

        Maximum-length sequences are nice because they have a flat frequency
        spectrum, but are comprised of only 1's and -1's. Gaussian noise,
        on the other hand, does have a flat spectrum, but is normally
        distributed around zero, meaning many of the instantaneous values are
        close to zero. So, if both noises are normalized to +/-1, the MLS is
        louder. This is advantageous when, e.g., estimating reverberation
        times, because you usually want the loudest noise you can get, since
        your likely going to have to extrapolate down to -60 dB (RT60) anyway.

        When using for reverb measurements, you want the noise to be at least
        as long as your reverb time is, so that you reach a steady-state by
        the time the noise turns off.

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
        Careful! Longer bit lengths will take a very long time to process!

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
        print "n must be an integer in the interval [2, 32]."

    seqlen = 2**n - 1;

    def generate_lfsr(n, use_rand_seed):
        toggle_mask = mls_bintaps[n]
        if use_rand_seed:
            lfsr = np.uint32(np.random.randint(1, (2**n - 1)))
        else:
            lfsr = np.uint32(1)

        while 1:
            lsb = lfsr & np.uint32(1)
            yield lsb
            lfsr = (lfsr >> np.uint32(1)) ^ (np.uint32(0) - (lfsr & np.uint32(1)) & toggle_mask)

    # Initialize the linear feedback shift register, val = 1 for all indices.
    lfsr = generate_lfsr(n, rand_seed)

    #mls = np.ones(n, dtype=np.int32)
    def zero_to_neg_one(x):
        if x == 0:
            return -1
        else:
            return 1
    zero_to_neg_one = lambda x: x
    return np.array([zero_to_neg_one(lfsr.next()) for i in xrange(seqlen)], np.int32)


def pink(t):
    '''Generates pink noise

        Pink noise has equal energy per octave.

        Parameters
        ----------
        n : scalar
            A number of samples.

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
    '''

    v = np.random.randn(t+pink_nT60); # Gaussian white noise: N(0,1)
    x = lfilter(pink_B,pink_A,v);    # Apply 1/F roll-off to PSD
    return x[pink_nT60:];    # Skip transient response


def tone(f, fs, dur, **kwargs):
    '''Generates pure tones

        Parameters
        ----------
        f: scalar/array
            Frequency info. If f is a scalar, then a pure tone of fixed
            frequency is created. If f is a 2-element array, the values will be
            the start and end frequecies of a linear frequency sweep. If f is
            an array of length > 2, the values will be the instantaneous
            frequency of an arbitrary (but nonetheless pure) waveform. In this
            case, dur will be ignored, and the output array will be the same
            length (the same number of samples) as input f.
        fs: scalar
            The sampling frequency.
        dur : scalar
            The duration in ms.

        Kwargs
        ------
        amp : scalar/array
            Amplitude values less than or equal to 0 are treated as dB (re:
             +-1), and values greater than 0 are used to scale the waveform
             peak linearly. default is 1
        phase : scalar
            The starting phase in degrees. default is 0

        Returns
        -------
        y : array
            The specified signal.

        Notes
        -----
        Examples:

        # Generate a 1000-Hz pure tone, with a sample rate of 22050, a
        # duration of 1s, an amplitude of +-.9, and a cosine starting phase
        t = tone(1000, 44100, 1000, amp=.9, phase=180);

        # Generate a tone with an amplitude that is 3 dB down from peak (+-1.0)
        t = tone(1000, 44100, 1000, amp=-3);

        # Generate a linear tone sweep starting at 200 Hz and ending at 750 Hz
        t = tone((200, 750), 44100, 1000, amp=-3);

        # Generate 2-Hz FM (with 50 Hz mod depth), on a 500-Hz carrier
        fm = tone(tone(2, 44100, 1000) * 25 + 500, 44100);

    '''

    amp = kwargs.get('amp', 1);
    phase = kwargs.get('phase', 0);

    f = np.array(np.float32(f));
    fs = np.float32(fs);
    dur = np.float32(dur);
    amp = np.array(np.float32(amp));
    phase = np.float32(phase)*np.pi/180.;

    if f.size == 2:
        dur = np.round((dur / 1000.) * fs);
        freq = np.linspace(f[0], f[1], dur);
    elif f.size == 1:
        dur = np.round((dur / 1000.) * fs);
        freq = np.ones(dur) * f;
    else:
        dur = f.size;
        freq = f;

    if amp.size == 2:
        if not amp[0] > 0 or not amp[1] > 0:
            raise Exception, 'When generating amplitude sweeps, linear scaling must be used (ie., .01 < amp < 1.0';
        amp1 = np.linspace(amp[0], amp[1], dur);
    elif amp.size == 1:
        if amp <= 0:
            amp1 = np.ones(dur) * 10. ** (amp / 20.);
        else:
            amp1 = np.ones(dur) * amp;
    else:
        amp1 = amp;

    return amp1 * np.sin(phase + (2. * np.pi * np.cumsum(freq) / fs));
