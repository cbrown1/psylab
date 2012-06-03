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

from matplotlib import pyplot as pp

from magspec import magspec

def specplot(signal, fs, plotspec='b-',log=False, fighandle=None):
    '''Plots magnitude spectra
        
        Plots a magnitude spectrum of the waveform. You can overlay 
        several spectra on top of one another, and specify different
        plot properties.
        
       Parameters
       ----------
       signal : array
          The input signal.
       fs : scalar
          The sampling frequency
       plotspec : string
          A matlab (matplotlib) style string specifying the plot 
          properties (eg., 'b-')
       log : bool
          Specfies wheter the x-axis is log or linear
       fighandle : Int
          A matplotlib figure handle to plot to

    '''
    if fighandle is None:
      fighandle = 4639 # An int unlikely to have been used
    
    if pp.fignum_exists(fighandle):  # MPL > 0.98.6svn
      pp.figure(fighandle).get_axes()[0].set_autoscale_on(False)

    h = pp.figure(num=fighandle)
    h.canvas.set_window_title('Spectrum Plot')
    x,y = magspec(signal,fs);
    if log:
      pp.semilogx(x,y,plotspec,figure=fighandle);
    else:
      pp.plot(x,y,plotspec,figure=fighandle);
    pp.xlabel('Frequency (Hz)')
    pp.ylabel('Magnitude (dB)')
    pp.show()
