# -*- coding: utf-8 -*-
"""
vocoder-overlap.py

"""

import numpy as np
from scipy.signal import filter_design as filters, lfilter, filtfilt


def vocoder_overlap(signal, fs, channel_n, channel_width, flo, fhi):
    '''Prototype vocoder where channel width is independent of channel spacing
        
        That is, channels are not necessarily contiguous
    
    '''
    signal = signal - np.mean(signal);
    cfs = np.round(np.linspace(flo,fhi,channel_n))
    cw = np.float32(channel_width/2.)
    nyq=np.float32(fs/2.);
    envfilter = 400;
    
    noisecarrier = np.random.randn(len(signal));
    noisecarrier = noisecarrier/max(np.abs(noisecarrier));
    summed_carriers = np.zeros(len(signal));
    
    for cf in cfs:
        lo = np.round(cf*(2.**-cw));
        hi = np.round(cf*(2.**cw));
        
        [b_band_hp,a_band_hp]=filters.butter(3,(lo/nyq),btype='high');
        [b_band_lp,a_band_lp]=filters.butter(3,(hi/nyq));

        [b_wind_hp,a_wind_hp]=filters.butter(1,(cf/nyq),btype='high');
        [b_wind_lp,a_wind_lp]=filters.butter(1,(cf/nyq));
        
        [b_env,a_env]=filters.butter(2,min((.5*(hi-lo)), envfilter)/nyq);
        
        # Filter signal into sub-band
        Sig_band = lfilter(b_band_hp, a_band_hp, signal);
        Sig_band = lfilter(b_band_lp, a_band_lp, Sig_band);
        
        # Apply window to shape band
        Sig_band = lfilter(b_wind_hp, a_wind_hp, Sig_band);
        Sig_band = lfilter(b_wind_lp, a_wind_lp, Sig_band);
        
        # Extract envelope
        rms_Sig_band = np.sqrt(np.mean(Sig_band**2));
        Sig_env_band = lfilter(b_env,a_env,np.maximum(Sig_band,0));
        
        # Prefilter, modulate carrier
        Mod_carrier = filtfilt(b_band_hp, a_band_hp, noisecarrier);
        Mod_carrier = filtfilt(b_band_lp, a_band_lp, Mod_carrier)*Sig_env_band;
        
        # Post filter
        Mod_carrier_filt = lfilter(b_band_hp, a_band_hp, Mod_carrier);
        Mod_carrier_filt = lfilter(b_band_lp, a_band_lp, Mod_carrier_filt);
        summed_carriers += Mod_carrier/np.sqrt(np.mean(Mod_carrier**2))*rms_Sig_band;
        
    return summed_carriers * ( np.sqrt(np.mean(signal**2)) / np.sqrt(np.mean(summed_carriers**2)) );
    