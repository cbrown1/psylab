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
from sinegen import sinegen

def vocoder(vect, fs, channels, **kwargs): 
    '''Implements an envelope vocoder
        
        Vocodes the input vector using specified parameters. 
    
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
        vect : array
            The input signal
        fs : scalar
            The sampling frequency
        channels : scalar
            The number of vocoder channels
        
        Kwargs
        ------
        inlo : scalar
            Low-side (start) frequency of the analysis channels [ default = 100 ]
        inhi : scalar
            High-side (end) frequency of the analysis channels [ default = 500 ]
        outlo : scalar
            Low-side (start) frequency of the output channels [ default = inlo ]
        outhi : scalar
            High-side (end) frequency of the output channels [ default = inhi ]
        envfilter : scalar
            Low-pass cutoff frequency of the envelope extraction filter [ default = 400 ]
        noise : bool
            False for sinusoidal carriers [ default ]
            True for noise band carriers
         
        Returns
        -------
        y : array
            The vocoded signal
        
        Notes
        -----
        Depends on sinegen.py
'''

    inlo = kwargs.get('inlo', 100) ;
    inhi = kwargs.get('inhi', 500) ;
    outlo = kwargs.get('outlo', inlo) ;
    outhi = kwargs.get('outhi', inhi) ;
    envfilter = kwargs.get('envfilter', 400) ;
    noise = kwargs.get('noise', False) ;

    if noise:
        noisecarrier = np.random.randn(len(vect));
        noisecarrier = noisecarrier/max(np.abs(noisecarrier));
    vect = vect - np.mean(vect);
    nyq=np.float32(fs/2.);
    ininterval=np.log10(np.float32(inhi)/np.float32(inlo))/np.float32(channels);
    outinterval=np.log10(np.float32(outhi)/np.float32(outlo))/np.float32(channels);
    summed_carriers = np.zeros(len(vect));
    ord = 3;
    for i in range(channels):
        # Estimate filters
        finhi=np.float32(inlo)*10.**(ininterval*(i+1));
        finlo=np.float32(inlo)*10.**(ininterval*i);
        fouthi=np.float32(outlo)*10.**(outinterval*(i+1));
        foutlo=np.float32(outlo)*10.**(outinterval*i);
        fcarrier=.5*(fouthi+foutlo);
        [b_sub_hp,a_sub_hp]=filters.butter(3,(finlo/nyq),btype='high');
        [b_sub_lp,a_sub_lp]=filters.butter(3,(finhi/nyq));

        [b_env,a_env]=filters.butter(2,min((.5*(fouthi-foutlo)), envfilter)/nyq);
        [b_out_hp,a_out_hp]=filters.butter(3,(foutlo/nyq),btype='high');
        [b_out_lp,a_out_lp]=filters.butter(3,(fouthi/nyq));

        ## Filter input
        Sig_sub = lfilter(b_sub_hp, a_sub_hp, vect);
        Sig_sub = lfilter(b_sub_lp, a_sub_lp, Sig_sub);
        rms_Sig_sub = np.sqrt(np.mean(Sig_sub**2));
        Sig_env_sub = lfilter(b_env,a_env,np.maximum(Sig_sub,0));
        if noise:
            Mod_carrier = filtfilt(b_out_hp, a_out_hp, noisecarrier);
            Mod_carrier = filtfilt(b_out_lp, a_out_lp, Mod_carrier)*Sig_env_sub;
        else:
            Mod_carrier = sinegen(np.ones(len(vect))*fcarrier,fs)*Sig_env_sub;

        ## Filter output
        Mod_carrier_filt = lfilter(b_out_hp, a_out_hp, Mod_carrier);
        Mod_carrier_filt = lfilter(b_out_lp, a_out_lp, Mod_carrier_filt);
        summed_carriers += Mod_carrier/np.sqrt(np.mean(Mod_carrier**2))*rms_Sig_sub;
    return summed_carriers;

