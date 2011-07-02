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

import numpy as np
from scipy.signal import filter_design as filters, lfilter, filtfilt
from tone import tone

def vocoder(signal, fs, channels, inlo, inhi, **kwargs):
    '''Implements an envelope vocoder

        Vocodes the input signal using specified parameters.

        You can specify a different frequency range for both input
        (analysis) and output, for a given number of channels (the output
        frequency range values default to input values). Both input and output
        channels are distributed contiguously on a log scale across the
        respective frequency ranges. Carriers can be pure tones (at the
        arithmetic center of each band) or noise bands (which are as wide as
        the output channel). The envelope cutoff frequency defaults to 400 Hz,
        but is never more than half the output-channel bandwidth.

        Parameters
        ----------
        signal : array
            The input signal
        fs : scalar
            The sampling frequency
        channels : scalar
            The number of vocoder channels
        inlo : scalar
            Low-side (start) frequency of the analysis channels
        inhi : scalar
            High-side (end) frequency of the analysis channels

        Kwargs
        ------
        outlo : scalar
            Low-side (start) frequency of the output channels [ default = inlo ]
        outhi : scalar
            High-side (end) frequency of the output channels [ default = inhi ]
        compression_ratio : scalar
            Compression ration: input / output [ default = 1 ]
        gate : scalar
            A gate to apply to each envelope. Values below gate are set to 0 [ default = 0 ]
        envfilter : scalar
            Low-pass cutoff frequency of the envelope extraction filter [ default = 400 ]
        noise : bool
            False for sinusoidal carriers [ default ]
            True for noise band carriers
        sumchannels : bool
            False to return a 2-d array in which each output channel is a column
            True to return a 1-d array containing the summed output channels. The rms
            will be equated to the rms of the input [ default ]
        order : int
            The filter order to use [ default = 3 ]

        Returns
        -------
        y : array
            The vocoded signal

        Notes
        -----
        Depends on tone.py
'''

    outlo = kwargs.get('outlo', inlo) 
    outhi = kwargs.get('outhi', inhi) 
    envfilter = kwargs.get('envfilter', 400) 
    noise = kwargs.get('noise', False) 
    sumchannels = kwargs.get('sumchannels', True) 
    ord = kwargs.get('order', 3) 
    compression_ratio = kwargs.get('compression_ratio', 1) 
    gate = kwargs.get('gate', None)

    if noise:
        noisecarrier = np.random.randn(len(signal))
        noisecarrier = noisecarrier/max(np.abs(noisecarrier))
    signal = signal - np.mean(signal)
    nyq=np.float32(fs/2.)
    ininterval=np.log10(np.float32(inhi)/np.float32(inlo))/np.float32(channels)
    outinterval=np.log10(np.float32(outhi)/np.float32(outlo))/np.float32(channels)
    if sumchannels:
        carriers = np.zeros(len(signal))
    else:
        carriers = np.zeros((len(signal), channels))

    for i in range(channels):
        # Estimate filters
        finhi=np.float32(inlo)*10.**(ininterval*(i+1))
        finlo=np.float32(inlo)*10.**(ininterval*i)
        fouthi=np.float32(outlo)*10.**(outinterval*(i+1))
        foutlo=np.float32(outlo)*10.**(outinterval*i)
        fcarrier=.5*(fouthi+foutlo)
        [b_sub_hp,a_sub_hp]=filters.butter(ord,(finlo/nyq),btype='high')
        [b_sub_lp,a_sub_lp]=filters.butter(ord,(finhi/nyq))

        [b_env,a_env]=filters.butter(2,min((.5*(fouthi-foutlo)), envfilter)/nyq)
        [b_out_hp,a_out_hp]=filters.butter(ord,(foutlo/nyq),btype='high')
        [b_out_lp,a_out_lp]=filters.butter(ord,(fouthi/nyq))

        ## Filter input
        Sig_sub = lfilter(b_sub_hp, a_sub_hp, signal)
        Sig_sub = lfilter(b_sub_lp, a_sub_lp, Sig_sub)
        rms_Sig_sub = np.sqrt(np.mean(Sig_sub**2))
        Sig_env_sub = lfilter(b_env,a_env,np.maximum(Sig_sub,0))
        peak = Sig_env_sub.max()
        Sig_env_sub /= compression_ratio
        Sig_env_sub += peak-Sig_env_sub.max()
        if gate is not None:
            db = 20*np.log10(Sig_env_sub/peak)
            Sig_env_sub[db<gate] = 0
        if noise:
            Mod_carrier = filtfilt(b_out_hp, a_out_hp, noisecarrier)
            Mod_carrier = filtfilt(b_out_lp, a_out_lp, Mod_carrier)*Sig_env_sub
        else:
            Mod_carrier = tone(np.ones(len(signal))*fcarrier,fs,1)*Sig_env_sub

        ## Filter output
        Mod_carrier_filt = lfilter(b_out_hp, a_out_hp, Mod_carrier)
        Mod_carrier_filt = lfilter(b_out_lp, a_out_lp, Mod_carrier_filt)
        if sumchannels:
            carriers += Mod_carrier_filt/np.sqrt(np.mean(Mod_carrier_filt**2))*rms_Sig_sub
        else:
            carriers[:,i] = Mod_carrier_filt/np.sqrt(np.mean(Mod_carrier_filt**2))*rms_Sig_sub
    if sumchannels:
        return carriers * ( np.sqrt(np.mean(signal**2)) / np.sqrt(np.mean(carriers**2)) )
    else:
        return carriers

def vocoder_overlap(signal, fs, channel_n, channel_width, flo, fhi):
    '''Prototype vocoder where channel width is independent of channel spacing
        
        That is, channels are not necessarily contiguous
    
        vocoder_overlap(signal, fs, channel_n, channel_width, flo, fhi)
    '''
    signal = signal - np.mean(signal)
    cfs = np.round(np.linspace(flo,fhi,channel_n))
    cw = np.float32(channel_width/2.)
    nyq=np.float32(fs/2.)
    envfilter = 400
    
    noisecarrier = np.random.randn(len(signal))
    noisecarrier = noisecarrier/max(np.abs(noisecarrier))
    summed_carriers = np.zeros(len(signal))

    for cf in cfs:
        lo = np.round(cf*(2.**-cw))
        hi = np.round(cf*(2.**cw))
        
        [b_band_hp,a_band_hp]=filters.butter(3,(lo/nyq),btype='high')
        [b_band_lp,a_band_lp]=filters.butter(3,(hi/nyq))

        [b_wind_hp,a_wind_hp]=filters.butter(1,(cf/nyq),btype='high')
        [b_wind_lp,a_wind_lp]=filters.butter(1,(cf/nyq))
        
        [b_env,a_env]=filters.butter(2,min((.5*(hi-lo)), envfilter)/nyq)
        
        # Filter signal into sub-band
        Sig_band = lfilter(b_band_hp, a_band_hp, signal)
        Sig_band = lfilter(b_band_lp, a_band_lp, Sig_band)
        
        # Apply window to shape band
        Sig_band = lfilter(b_wind_hp, a_wind_hp, Sig_band)
        Sig_band = lfilter(b_wind_lp, a_wind_lp, Sig_band)
        
        # Extract envelope
        rms_Sig_band = np.sqrt(np.mean(Sig_band**2))
        Sig_env_band = lfilter(b_env,a_env,np.maximum(Sig_band,0))
        
        # Prefilter, modulate carrier
        Mod_carrier = filtfilt(b_band_hp, a_band_hp, noisecarrier)
        Mod_carrier = filtfilt(b_band_lp, a_band_lp, Mod_carrier)*Sig_env_band
        
        # Post filter
        Mod_carrier_filt = lfilter(b_band_hp, a_band_hp, Mod_carrier)
        Mod_carrier_filt = lfilter(b_band_lp, a_band_lp, Mod_carrier_filt)
        summed_carriers += Mod_carrier/np.sqrt(np.mean(Mod_carrier**2))*rms_Sig_band
    return summed_carriers * ( np.sqrt(np.mean(signal**2)) / np.sqrt(np.mean(summed_carriers**2)) )
    