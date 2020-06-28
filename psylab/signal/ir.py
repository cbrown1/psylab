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
# contributions are welcome. Go to https://github.com/cbrown1/psylab/
# for more information and to contribute. Or send an e-mail to: 
# cbrown1@pitt.edu.
#

import numpy as np


def next_power_of_two(n):
    # Returns next power of two following n
    return np.int32(np.power(2, np.ceil(np.log2(n))))


def mag_spectrum(x, fs, win=None):
    N = len(x)  # Length of input sequence

    if win is None:
        win = np.ones(x.shape)
    if len(x) != len(win):
            raise ValueError('Signal and window must be of the same length')
    x = x * win

    # Calculate x (frequency)
    freq = np.arange((N / 2) + 1) / (float(N) / fs)
    # Calculate y (real FFT)
    sp = np.fft.rfft(x)

    # Scale the magnitude of FFT by window and factor of 2,
    # because we are using half of FFT spectrum.
    s_mag = np.abs(sp) * 2 / np.sum(win)

    # Convert to dBFS
    s_dbfs = 20 * np.log10(s_mag) #/s_mag.max())

    return freq, s_dbfs


def compute_recording_delay(hardware_delay, playback_distance, sos=343, fs=44100):
    
    """Convenience function to compute the total system delay during play/record 
        (hardware delay plus wave propagation time)
        
        Parameters
        ----------
        hardware_delay : int
            The delay, in samples, between playback, and recording on a system.
            This value can be obtained using a loopback setup, in which a 
            soundcard output (playback) channel is directly connected to an input 
            (record) channel, and play/record is initiated, say, of a click. On my 
            system, this value is 6126.
        playback_distance : float
            The distance, in meters, between the source (loudspeaker) and 
            receiver (microphone), in your setup during recording of impulse 
            responses. On my system, this is 1.6.
        sos : float
            The speed of sound, in meters/second in your system. Default is in
             air, and at sea level.
        fs : int
            The sampling frequency used for play/record.
            
        Returns
        -------
        total_delay : int
            The total delay, in samples, of your system.
            

    """
    total_delay = np.int32(((playback_distance / sos) * fs) + hardware_delay)
    return total_delay


def gen_sweep(f1=50, f2=18000, fs=44100, dur=5):
    
    """Generates an exponentially-swept pure tone useful for acoustic measurements
    
        A tuple is returned, containing the sweep and its inverse filter. 
        Record the sweep in an acoustic context, then convolve the inverse filter
        with the recording to obtain the impulse response of that context.
    
        Parameters
        ----------
        f1: float
            The frequency, in Hz, at which to start the sweep
        f2: float
            The frequency, in Hz, at which to end the sweep
        fs : int
            The sampling frequency of the sweep
        dur : float
            The duration of the sweep, in seconds
        
        Returns
        -------
        sweep : array
            The sweep
        inv_filter : array
            The inverse filter of the sweep, which is simply the time-reversed 
            sweep with an exponentially decaying envelope applied

    """
    t = np.arange(0, dur*fs)/fs
    R = np.log(f2/f1)

    # ESS generation
    sweep = np.sin((2*np.pi*f1*dur/R)*(np.exp(t*R/dur)-1))
    # Inverse filter
    k = np.exp(t*R/dur)
    inv_filter = sweep[::-1]/k
    
    return sweep, inv_filter


def get_level_difference(ir_1, ir_2):
    """Convenience function to compute the dB RMS difference between 2 arrays

        Intended use case is when you are making binaural IR recordings.
        Sometimes the two mics are not matched in output level, and this
        while show up as an ILD. Pass identical IR recordings from both 
        mics such that both recordings would be expected to be identical. Eg.,
        hold both mics next to each other and the same distance away from a 
        loudspeaker, then play/record a noise. The level returned here is the 
        dB difference bewteen the two, which can be assumed to be physical 
        sensitivity differences between the mics. Negative values means 
        ir_1 is > ir_2. Then, use apply_level_difference to actually do 
        the compensation to all binaural pairs 

    """

    rms_1 = np.sqrt(np.mean(np.square(ir_1)))
    rms_2 = np.sqrt(np.mean(np.square(ir_2)))
    return 20 * np.log10(rms_2/rms_1)


def apply_level_difference(ir_1, ir_2, db):
    """Attenuates one or another array as specified by dB
        
        Intended to be used with get_level_difference to adjust the level 
        of binaural IRs to compensate for sensitivity differences 
        across microphones 

    """

    if db < 0:
        out_1 = ir_1 * np.exp(np.float32(db)/8.6860)
        out_2 = ir_2
    else:
        out_1 = ir_1
        out_2 = ir_2 * np.exp(np.float32(-db)/8.6860)

    return out_1, out_2


def get_ir(recording, source, fs=44100, system_delay=0, ir_length=512, ir_prebuff=30, ir_ref_mag=1):
    
    """Generates an impulse response using FFT-based convolution
    
        Parameters
        ----------
        recording: array
            Recorded stimulus. Can be 1- or 2-d.
        source: array
            The stimulus that was recorded. Should be the stimulus you used to 
            record, time-reversed and equalized in amplitude with an 
            exponential decay.
        fs : int
            The sampling frequency
        system_delay : int
            The delay, in samples, between playback and recording of your system.
        ir_length : int
            Length of the impulse response to return in samples. Default is 512
            after Gardner and Martin.
        ir_prebuff : int
            Number of samples to take before the actual IR starts. Default is
            30, after Gardner and Martin.
        ir_ref_mag : float
            A reference magnitude, used for scaling the ir. Default is 1, which 
            means no scaling. But if you are using the associated gen_sweep 
            function, one option is to use the peak magnitude of the 'ideal' 
            ir, which can be obtained by passing to this function the sweep as 
            the recording:
                
                >>> sweep,inv_filter = gen_sweep()
                >>> ref_mag = np.max(get_ir(sweep, inv_filter))
            
            For default parameters (as written above), this reference magnitude 
            is 18677.3.
            
            I am not sure if this is the best way to scale the ir, but the 
            advantages are that (1) it leads to reasonable ir magnitudes for 
            actual recorded signals, (2) it ensures that 0 >= ir >= 1, and (3) 
            it preserves magnitude differences across recordings.
            
        Returns
        -------
        ir : array
            The impulse response. Shape will be [ir_length, recording.shape[1]]
    """

    rec = np.atleast_2d(recording)
    if rec.shape[0] == 1: rec = rec.T # when rec is 1d, atleast prepends dim
    out=np.zeros((ir_length, rec.shape[1]))

    n = next_power_of_two(rec.shape[0])

    # The IR will start here; subtract prebuff to start taking early
    ir_start = np.int32((source.shape[0]) + system_delay - ir_prebuff)
    if ir_start < 0: ir_start = 0
#    ir_start = np.int32((source.shape[0]/2) + total_delay - ir_prebuff) # For fftconvolve

    for i in np.arange(rec.shape[1]):

        y = np.concatenate((rec[:,i], np.zeros(n - rec.shape[0])))
        f = np.concatenate((source, np.zeros(n - source.shape[0])))
        #f /= np.sum(f)
        ir = np.real(np.fft.ifft( np.fft.fft(y) * np.fft.fft(f) ) )
        out[:,i] = ir[ir_start:ir_start+ir_length] / ir_ref_mag

    return out

