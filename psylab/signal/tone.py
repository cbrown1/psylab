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

def tone(f, fs, dur, **kwargs):
    '''Generates pure tones

        Parameters
        ----------
        f: scalar/array
            Frequency info. If f is a scalar, then a pure tone of fixed
            frequency is created. If f is a 2-element array, the values will be
            the start and end frequecies of a linear frequency sweep. If f is
            an array of length > 2, the values will be the instantaneous
            sinusoidal frequency of the resulting signal. In this case, dur will 
            be ignored, and the output signal will be the same length (the same 
            number of samples) as input f.
        fs: scalar
            The sampling frequency.
        dur : scalar
            The duration in ms. 

        Kwargs
        ------
        amp : scalar/array
            The amplitude of the signal. If amp is a scalar, the entire signal 
            is scaled to amp. If it is an array, it must be the same length as 
            the resulting signal, and the elements of amp will be the 
            instantaneous amplitude of the resulting signal. Amplitude values 
            less than or equal to 0 are assumed to be in units of dB (re:+-1), 
            and values greater than 0 are used to scale the waveform peak 
            linearly. [default is 1]
        phase : scalar/array
            The phase of the signal, in degrees. If phase is a scalar, it is the 
            starting phase of the signal. If it is an array, it must be the same 
            length as the resulting signal, and the elements of phase will be 
            the instantaneous phase of the signal. [default = 0]

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

    amp = kwargs.get('amp', 1.)
    phase = kwargs.get('phase', 0.)

    f = np.array(np.float64(f))
    fs = np.float64(fs)
    dur = np.float64(dur)
    amp = np.array(np.float64(amp))
    phase = np.float64(phase)*np.pi/180.

    if f.size == 2:
        dur = np.round((dur / 1000.) * fs)
        freq = np.linspace(f[0], f[1], dur)
    elif f.size == 1:
        dur = np.round((dur / 1000.) * fs)
        freq = np.ones(dur) * f
    else:
        dur = f.size
        freq = f

    if amp.size == 2:
        if not amp[0] > 0 or not amp[1] > 0:
            raise Exception('When generating amplitude sweeps, linear scaling must be used (ie., .01 < amp < 1.0')
        amp1 = np.linspace(amp[0], amp[1], dur)
    elif amp.size == 1:
        if amp <= 0:
            amp1 = np.ones(dur) * 10. ** (amp / 20.)
        else:
            amp1 = np.ones(dur) * amp
    else:
        amp1 = amp

    return amp1 * np.sin(phase + (2. * np.pi * np.cumsum(freq) / fs))
