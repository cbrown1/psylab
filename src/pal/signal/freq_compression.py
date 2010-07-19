import numpy as np
from numpy.fft import fft, ifft
import interp

def sola_dumb(x, window, overlap):
    """Cheap SOLA implementation that doesn't attempt any overlap matching.

    x : ndarray
        Time-domain representation of the signal.
    window : ndarray
        Shape to ramp the summed timeslices of the signal.
    overlap : int
         Samples of overlap for each pair of summed windows.
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


def freq_compress(signal, semitones, window, interp_func=interp.interp_lin):
    """Performs frequency compression on a signal
    
        Uses the synchronous-overlap-add (SOLA) method

    Parameters:
    -----------
    signal : numpy.ndarray
        Array of samples

    semitones : int
        Number of semitones by which to compress the pitch.

    window : array
        The sampling window, impacts quality. 

    interp_func : function
        An interpolation functin to use.
    """
    ws = len(window)
    length = signal.size
    resample_factor = (2.0)**(float(semitones)/12)
    #print "1/resample_factor", 1./resample_factor
    over = (1 - 1./resample_factor) * ws
    return sola_dumb(interp_func(signal, int(length * resample_factor)),
                     window, over)[:length]
