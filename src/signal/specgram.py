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

from matplotlib import colors, pyplot as pp

def specgram(signal, fs):
    '''Plots a nice spectrogram
  
       Parameters
       ----------
       signal : array
          The input signal.
       fs : scalar
          The sampling frequency
    '''

    cdict = {'red': ((0.0, 0.0, 0.0), (0.5, 0.2, 0.2), (0.78, 0.6, 0.6), (1.0, 1.0, 1.0)), 
    'green': ((0.0, 0.0, 0.0), (0.93, 0.0, 0.0), (1.0, 0.9, 0.9)), 
    'blue': ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0))}
    my_cmap = colors.LinearSegmentedColormap('my_colormap',cdict,256)
    s1 = pp.specgram(signal,Fs=fs,NFFT=1024,noverlap=1000,cmap=my_cmap,scale_by_freq=False)
