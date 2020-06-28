# -*- coding: utf-8 -*-

# Copyright (c) 2010-2013 Christopher Brown
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
from numpy.fft import fft, ifft
from . import interp

def tdhs(x, window, overlap):
    """Time-scale modification algorithm using overlap-add and windowing for
    smooth transitions. The window size should be pre-aligned to the period
    of the signal's fundamental frequency to be true TDHS after Mal79.

    References
    ----------
    [Mal79] D. Malah. Time-domain algorithms for harmonic bandwidth reduction
    and time scaling of speech signals. IEEE Transactions on ASSP, ASSP-27:121-
    133, April 1979.

    Parameters
    ----------
    x : ndarray
        Time-domain representation of the signal.
    window : ndarray
        Shape to ramp the summed timeslices of the signal.
    overlap : int
         Samples of overlap for each pair of summed windows.

    Returns:
    --------
    y : ndarray
        The time-scaled source signal.
    """
    assert overlap <= len(window)

    y = np.zeros(x.size)

    i = 0
    j = 0
    window_size = len(window)
    while j+window_size < x.size:
        y[i:i+window_size] += window * x[j:j+window_size]
        i += window_size - overlap
        j += window_size
    return y

def solafs_offline(x, w_ov, s_s, s_a, k_max):
    """Time-domain scaling using the SOLAFS algorithm.
    
    The compression ratio is determined by alpha = s_s / s_a.
    
    alpha > 1 implies time-domain expansion,
    alpha < 1 implies time-domain compression.
    
    Currently very low-performance due to lots of inefficient
    arithmetic operations occurring at the Python level. 
    
    Parameters
    ----------
    x : ndarray
        Source signal to be scaled.
        
    w_ov : int
        Window overlap in samples.
        
    s_s : int
        Synthesis distance in samples.
        
    s_a : int
        Analysis distance in samples.

    k_max : int
        Maximum window offset for the next window to add.
    """
    alpha = float(s_s)/s_a
    beta = np.linspace(1,0,w_ov)

    w = s_s + w_ov

    y = np.zeros(int(x.size * alpha))

    for m in xrange(0, ((y.size - w) / s_s)):
        x_m = np.zeros(w)

        r = np.zeros(k_max+1)
        for k in xrange(0, k_max+1):
            a = np.sum([x[m*s_a + k + n] * y[m * s_s + n] for n in xrange(0, w_ov)])
            b = np.sum([x[m*s_a + k + n]**2 for n in xrange(0, w_ov)])
            c = np.sum([y[m*s_s + n] for n in xrange(0, w_ov)])
            r[k] = a / (np.sqrt(b) * np.sqrt(c))

        k_m = 0
        k_m_corr = r[0]
        if np.isnan(k_m_corr):
            k_m_corr = 0
        for k in xrange(1, r.size):
            if np.isfinite(r[k]):
                if r[k] > k_m_corr:
                    k_m = k
                    k_m_corr = r[k]

        for n in xrange(0, w):
            i = m * s_a + k_m + n
            if i < x.size:
                x_m[n] = x[i]

        for n in xrange(0, w_ov):
            y[m * s_s + n] = beta[n]*y[m * s_s + n] + (1-beta[n])*x_m[n]
        for n in xrange(w_ov, w):
            y[m * s_s + n] = x_m[n]

    return y

def freq_compress(x, semitones, 
                  window=400,
                  tdsalg="tdhs",
                  k_max = 100):
    """Performs frequency compression on a signal in the time domain.
    
    Parameters
    ----------
    x : numpy.ndarray
        Array of samples
    
    semitones : int
        Number of semitones by which to compress the pitch.
    
    window : scalar
        The size of the sampling window, impacts quality for t.
    
    tdsalg : str
        What algorithm to use in performing time-domain scaling.
        Permissible values are "tdhs" and "solafs".
    
    k_max : int
        Search distance for the next overlapping window for SOLAFS.
        Not used if tdsalg == "tdhs".
    
    Returns
    -------
    y : ndarray
        The frequency-compressed signal.
    
    Examples
    --------
    >>>
    """
    w = np.hanning(window)
    alpha = (2.0)**(float(semitones)/12)
    w_ov = (1 - 1./alpha) * window
    if tdsalg == "tdhs":
        y = tdhs(x, w, w_ov)
        y = interp.interp(y, int(x.size * alpha))[:x.size]
        return y
    elif tdsalg == "solafs":
        y = solafs_offline(x, int(w_ov), window, int(window*alpha), k_max)
        y = interp.interp(y, int(x.size))
        return y
    else:
        raise ValueError("`tdsalg` must be 'tdhs' or 'solafs'.")

