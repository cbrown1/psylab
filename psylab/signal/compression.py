# -*- coding: utf-8 -*-

# Copyright (c) 2009 Ian Wiggins 
# Copyright (c) 2014 Christopher Brown
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

def compress(sig, fs, threshold, comp_ratio, attack, release, ref_spl=110, delay_audio=False, make_up=False, return_gain_function=False):
    """Applies simple, single-channel compression to input signal sig in the
        time domain. Optionally returns the gain control signal in addition to
        the compressed signal.   
        
        The gain control signal is determined using a peak detector algorithm
        (cf Kates 2008, p233). Note that the peak detector operates on the
        instantaneous full-wave rectified input signal.
        
        Absolute levels are in reference to the measured SPL of a cal tone, 
        played at full volume (+- 1 v) on your system. 
        
        Attack and release time are specified in milliseconds and correspond to
        the 1/e time constants of the peak detector. Note that the observed
        attack and release time of the compressor system (measured in
        accordance with ANSI S3.22 / IEC 60118-2) will be different, as these 
        depend on other factors (compression ratio, threshold, amount of
        overshoot, etc) in a complicated way - cf Kates 1995. 
        
        The compression rule is linear amplification below threshold,
        compressive amplification (in accordance with compression ratio) above
        threshold. Note that there is no constraint on negative gain (ie
        attenuation) occurring at high input levels.
        
        If delay_audio is true, the audio signal is delayed by half the
        attack time. This reduces the amount of overshoot seen when the input
        level increases abruptly (cf Stone & Moore 2004). Warning: if the input
        signal does not contain enough trailing silence to accommodate the
        delay, the end of the signal will be truncated! (Note also that this
        delay length may not be optimal and may introduce other side-effects,
        eg "preshoot".) 
        
        If the make_up option is true, make-up gain is applied automatically
        such that the overall rms level of the compressed signal is equal to
        that of the input signal.
        
        Parameters
        ----------
        sig : array
            The input signal to be compressed (mono)
        fs : scalar
            The sampling frequency
        threshold : scalar
            The compression threshold (ie lower kneepoint) in dB SPL
        comp_ratio : scalar
            The compression ratio (eg a value of 2 gives 2:1 compression
            above the compression threshold)
        attack : scalar
            The attack time constant in ms (see note above)
        release :
            The release time constant in ms (see note above)
        ref_spl : scalar
            The measured SPL, in dB, of a tone at 1 v peak-to-peak. This is 
            used as the reference for compression threshold
        delay_audio : bool
            if true, audio signal is delayed by half the
            attack time [default = False]
        make_up : bool
            If true, make-up gain is applied [default = False]
        return_gain_function : bool
            If True, the returned array is the gain control signal
            If False, the returned array is the input signal with gc applied [default]
        
        Returns
        -------
        y : array
            Either the compressed output signal or the sample-by-sample gain 
            (in dB) applied by the compressor (Note: the effect of the 
            delay_audio option is not accounted for in the returned gain control 
            signal)

        Notes
        -----
        Adapted from Matlab code provided by Ian Wiggins, Institute of Hearing 
        Research, Nottingham
        
        """
        
    # Attenuate the rms (.707) of a tone of +-1 v (the loudest possible) by 
    # the dB difference between the ref_spl, and the threshold spl
    thresh_peff = 0.70710678118654757 * np.exp((threshold-ref_spl)/8.6860)

    # calculate attack and release coefficients based on specified attack and
    # release times (corresponding to 1/e time constants of the peak detector)
    alpha = np.exp(-1. / ((attack/1000.)*fs))
    beta = np.exp(-1. / ((release/1000.)*fs))
    aConst = (1-alpha)

    if delay_audio:
       ndelay = np.round((attack/1000.)*fs/2)
    if make_up:
       sig_rms = np.sqrt(np.mean(sig**2))

    d = np.zeros_like(sig)
    # loop to calculate peak detector output over the duration of the signal
    # (note that first sample of peak detector output is always zero here)
    for thisPtr in range( 1, len( sig ) ):
        prevPtr = thisPtr - 1
        if ( sig[ thisPtr] < d[prevPtr] ):
            d[  thisPtr] = d[prevPtr] * beta
        else:
            d[  thisPtr] = d[prevPtr] * alpha + ( sig[thisPtr] * aConst )

    # calculate peak detector output level in dB SPL
    d_dB = threshold + 20.*np.log10(d / thresh_peff)

    # calculate gain using a simple compression rule
    gain = np.zeros_like(d_dB)   # set gain to zero throughout as a first step.  
                                 # If the peak detector output level is below
                                 # the compression threshold, the gain is to
                                 # remain at zero for that sample 

    # find where the peak detector output is above threshold
    idx = np.where(d_dB > threshold)[0]
    
    # apply the compression rule to give the gain to be applied at these samples
    gain[idx] = (threshold + (d_dB[idx] - threshold) / comp_ratio) - d_dB[idx]
    
    if return_gain_function:
        return gain
    
    # if required, delay the audio signal before applying the gain signal
    if delay_audio:
       sig = np.roll(sig, ndelay)
       sig[:ndelay] = 0   # replace wrapped values at start with zeros

    # apply the compressor gain signal to the audio
    sigout = sig * (10.**(gain/20.))

    # apply make-up gain if required
    if make_up:
       make_up_gain = sig_rms - np.sqrt(np.mean(sigout**2))
       sigout = sigout*make_up_gain
       gain +=make_up_gain
    
    return sigout


def compression_apply(signal, gain):
    """Applies a predetermined gain function to the input signal. `gain`
        should have been generated previously using the `compress` function.
        
        Parameters
        ----------
        signal : array
            The input signal to be compressed (mono)
        gain : array
            The gain function, generated by `compress`

        Returns
        -------
        sigout : array
            The input signal with the gain function applied

        Notes
        -----
        There is no in-built facility using this function to delay the audio 
        signal relative to the gain control signal (to reduceovershoot 
        effects), which is an option in the compress function.
    
        Adapted from Matlab code provided by Ian Wiggins, Institute of Hearing 
        Research, Nottingham
    """
    # convert sample-by-sample gain in dB to array of linear scale factors
    lin_gain = 10.**(gain/20.)
    
    # apply gain
    sigout = signal * lin_gain
    return sigout
