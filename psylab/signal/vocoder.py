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
from scipy.signal import filter_design as filters, lfilter, filtfilt
import scipy.signal
from .tone import tone
from .peakpick import pick_peaks
from .zeropad import zeropad
from .filter import filter_bank, freqs_logspace

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

    ret = np.zeros((len(signal),channels))
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
#        ret[:,i] = Sig_sub.copy()
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
#    return ret
    if sumchannels:
        return carriers * ( np.sqrt(np.mean(signal**2)) / np.sqrt(np.mean(carriers**2)) )
    else:
        return carriers

def vocoder_vect(signal, fs, channels, inlo, inhi, **kwargs):
    """A 'vectorized' vocoder implementation
    
        This is vectorized as much as possible. But it probably isn't much 
        of an improvement on speed, since the filtering is still in a 
        loop. 
    
    """
    outlo = kwargs.get('outlo', inlo)
    outhi = kwargs.get('outhi', inhi)
    envfilter = kwargs.get('envfilter', 400)
    noise = kwargs.get('noise', False)
    sumchannels = kwargs.get('sumchannels', True)
    order = kwargs.get('order', 6)
    compression_ratio = kwargs.get('compression_ratio', 1)
    gate = kwargs.get('gate', None)
    ace = kwargs.get('ace', None)
    nyq = fs/2.
    
    #try:
    #    # This is actually pretty slow
    #    #raise Exception
    #    import brian
    #    import brian.hears as bh
    #    def bp_filt_bank(signal, fs, cfs):
    #        filterbank = bh.Butterworth(bh.Sound(signal,fs*brian.Hz), cfs.size-1, order, cfs, 'bandpass')
    #        out = filterbank.process()
    #        return out
    #except:
        
    # Compute cutoff frequencies
    cfs_in = freqs_logspace(inlo, inhi, channels)
    cfs_out= freqs_logspace(outlo, outhi, channels)
    
    # Analysis filterbank
    sig_fb = filter_bank(signal, fs, order, cfs_in)
    
    # Extract envelope
    env_cfs = np.concatenate (( np.zeros(1), np.minimum((cfs_out[1:] - cfs_out[:-1])/2, envfilter) ))
    envelopes = filter_bank(np.maximum(sig_fb,0), fs, order, env_cfs, btype='low')

    # Generate carriers
    if noise:
        carrier = np.random.randn(signal.size)
        carrier = carrier/np.max(np.abs(carrier))
        carriers = filter_bank(carrier,fs,order,cfs_out)
    else:
        fcarriers = (cfs_out[1:]+cfs_out[:-1]) / 2.
        carriers = np.sin(2*np.pi * np.cumsum(np.ones((signal.size,channels))*fcarriers,axis=0) / fs)
    
    if ace:
        wsize = np.round((.02)*fs) # 20ms analysis window
        peaks,rms = pick_peaks(voc, ace, wsize) 
        carriers, peaks, rms = zeropad(carriers,peaks,rms)
        # Generate 1-d index array
        indices = peaks.ravel() + np.repeat(range(0, carriers.shape[1]*carriers.shape[0], carriers.shape[1]), peaks.shape[1])
        # Pull out the carriers, atten
        out = rms.ravel()[indices] * carriers.ravel()[indices]
        # Back to 2-d
        voc = out.reshape(peaks.shape)
        
    else:
        # Modulate
        voc = carriers * envelopes
        
        # Post filter
        voc = filter_bank(voc, fs, order, cfs_out)
        
        # Equate each channel
        voc *= np.sqrt(np.mean(sig_fb**2.,axis=0)) / np.sqrt(np.mean(voc**2.,axis=0))
        
        
        
    # Equate overal signal
    voc *= np.sqrt(np.mean(signal**2)) / np.sqrt(np.mean(voc.sum(axis=1)**2))

    if sumchannels:
        voc = voc.sum(axis=1)

    return voc


def vocoder_overlap(signal, fs, channel_n, channel_width, flo, fhi):
    '''Prototype vocoder where channel width is independent of channel spacing

        That is, channels are not necessarily contiguous

        The channel_width parameter is in octaves, and channel cfs are
        logarithmically spaced from flo to fhi

        E.g., the following set of parameters would yield contiguous bands from 88 to 11314 Hz:
        psylab.signal.vocoder_overlap(sig,fs,6,1,125,8000)

        vocoder_overlap(signal, fs, channel_n, channel_width, flo, fhi)
    '''
    signal = signal - np.mean(signal)
    cfs = np.float32(np.round(np.linspace(flo,fhi,channel_n)))
    cfs = freqs_logspace(flo, fhi, channel_n)

    cw = np.float32(channel_width/2.)
    nyq=np.float32(fs/2.)
    envfilter = 400.
    print("Channel width: {:} Oct".format(channel_width))
    noisecarrier = np.random.randn(len(signal))
    noisecarrier = noisecarrier/max(np.abs(noisecarrier))
    summed_carriers = np.zeros(len(signal))

    for cf in cfs:
        lo = np.round(cf*(2.**-cw))
        hi = np.round(cf*(2.**cw))

        print("  lo {:}; cf {:}; hi {:}".format(lo,cf,hi))

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
    
