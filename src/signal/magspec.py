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
from lts import lts

def magspec(wave,fs,fftsize=8192):
    '''Computes the magnitude spectrum of a signal
    
        Performs an fft on the input, and passes back an array of frequency 
        values, and an array of magnitude values, suitable for plotting. The 
        magnitude spectrum is in dB (20*log10).
    '''
    #amp=np.abs(np.fft.fft(wave,fftsize));
    #fsize = np.round(len(amp)/2.)-1;
    #outamp= amp[0:np.round(len(amp)/2)-1];
    
    outamp = 20*np.log10(lts(wave, fftsize))
    #outamp=20*log10(outamp/max(outamp));
    f = np.linspace(1, fs/2, (fftsize/2)+1)
    return f,outamp
