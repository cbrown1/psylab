# -*- coding: utf-8 -*-

# Copyright (c) 2010 Christopher Brown; All Rights Reserved.
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

"""
formatplot - A set of helper functions for formatting matplotlib figures
"""

#from matplotlib import pyplot as pp

def set_foregroundcolor(ax, color):
    '''For the specified axes, sets the color of the frame, major ticks,
        tick labels, axis labels, title and legend
    '''
    for tl in ax.get_xticklines() + ax.get_yticklines():
        tl.set_color(color)
    for spine in ax.spines:
        ax.spines[spine].set_edgecolor(color)
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_color(color)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_color(color)
    ax.axes.xaxis.label.set_color(color)
    ax.axes.yaxis.label.set_color(color)
    ax.axes.title.set_color(color)
    lh = ax.get_legend()
    if lh != None:
        lh.legendPatch.set_edgecolor(color)
        labels = lh.get_texts()
        for lab in labels:
            lab.set_color(color)

def set_backgroundcolor(ax, color):
    '''Sets the background color of the current axes (and legend).
        Use 'None' (with quotes) for transparent. To get transparent
        background on saved figures, use:
        pp.savefig("fig1.svg", transparent=True)
    '''
    ax.patch.set_facecolor(color)
    lh = ax.get_legend()
    if lh != None:
        lh.legendPatch.set_facecolor(color)

def set_framelinewidth(ax, width):
    '''For the specified axes, sets the linewidth of the frame and major ticks
    '''
    for tl in ax.get_xticklines() + ax.get_yticklines():
        tl.set_markeredgewidth(width)
    for spine in ax.spines:
        ax.spines[spine].set_linewidth(width)

def set_ticklabelfontsize(ax, fontsize):
    '''Sets the, uh, ticklabelfontsize.
    '''
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)

def set_legendtitlefontsize(ax, fontsize):
    lh = ax.get_legend()
    if lh != None:
        lh.get_title().set_fontsize(fontsize)
