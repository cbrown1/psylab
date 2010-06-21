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
