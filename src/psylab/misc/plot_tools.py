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

from matplotlib import pyplot as pp
import numpy as np

asu_colors = {}
asu_colors['maroon'] = list(np.array((153,0,51))/255.)
asu_colors['gold'] = list(np.array((255,179,16))/255.)
asu_colors['grey'] = list(np.array((79,85,87))/255.)
asu_colors['green'] = list(np.array((86, 142, 20))/255.)
asu_colors['blue'] = list(np.array((0, 142, 214))/255.)
asu_colors['orange'] = list(np.array((244, 124, 0))/255.)
asu_colors['warmgrey'] = list(np.array((175, 165, 147))/255.)


def set_foregroundcolor(ax, color=None):
    '''For the specified axes, sets the color of the frame, major ticks,
        tick labels, axis labels, title and legend. 
        
        Defaults to current axes.
    '''
    
    if color is None:
        color = ax
        ax = pp.gca()
    
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
        lh.get_title().set_color(color)
        lh.legendPatch.set_edgecolor(color)
        labels = lh.get_texts()
        for lab in labels:
            lab.set_color(color)

def set_backgroundcolor(ax, color=None):
    '''Sets the background color of the current axes (and legend).
        Use 'None' (with quotes) for transparent. To get transparent
        background on saved figures, use:
        pp.savefig("fig1.svg", transparent=True)
        
        Defaults to current axes.
    '''
    if color is None:
        color = ax
        ax = pp.gca()
    
    ax.patch.set_facecolor(color)
    lh = ax.get_legend()
    if lh != None:
        lh.legendPatch.set_facecolor(color)

def set_framelinewidth(ax, width=None):
    '''For the specified axes, sets the linewidth of the frame and major ticks.
         
        Defaults to current axes.
    '''
    if color is None:
        color = ax
        ax = pp.gca()
    
    for tl in ax.get_xticklines() + ax.get_yticklines():
        tl.set_markeredgewidth(width)
    for spine in ax.spines:
        ax.spines[spine].set_linewidth(width)

def set_fontsize(ax, fontsize=None):
    '''Sets the fontsize for the most common figure text
        (title, tick labels, axis labels, and legend text)
        
        Defaults to current axes.
    '''
    if color is None:
        color = ax
        ax = pp.gca()
    
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
    ax.axes.title.set_fontsize(fontsize)
    ax.axes.xaxis.label.set_fontsize(fontsize)
    ax.axes.yaxis.label.set_fontsize(fontsize)
    lh = ax.get_legend()
    if lh != None:
        lh.get_title().set_fontsize(fontsize)
        labels = lh.get_texts()
        for lab in labels:
            lab.set_fontsize(fontsize)

def set_ticklabelfontsize(ax, fontsize=None):
    '''Sets the, uh, ticklabelfontsize.
    
        Defaults to current axes.
    '''
    if color is None:
        color = ax
        ax = pp.gca()
    
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)

def set_legendtitlefontsize(ax, fontsize=None):
    if color is None:
        color = ax
        ax = pp.gca()
    
    lh = ax.get_legend()
    if lh != None:
        lh.get_title().set_fontsize(fontsize)

def add_head( f=None, x=.5, y=.5, w=.5, h=.5, c='k', lw=1, dutchPart=False ):
    """Draws a head, viewed from above, on the specified figure.
    
        Notes
        -----
       Coordinates and dimensions are in figure units ( 0 <= 1 ).
       
       The aspect ratio is always 1, meaning the head will always be a circle, 
       and the size will always be the smaller of w and h.
       
       The Dutch part is optional.
       
       Defaults to current figure.
    """

    if f is None:
        f = pp.gcf()

    hax = f.add_axes([x-(w/2.), y-(h/2.),  w, h])
    hax.set_aspect('equal')
    hax.set_xlim([0,1.1])
    hax.set_ylim([0,1])
    hax.set_xticks([],[])
    hax.set_yticks([],[])
    hax.patch.set_facecolor('None')
    hax.set_frame_on(False)

    ar = np.arange(np.pi/1000,np.pi/1000+np.pi*2,np.pi/1000)

    # Head
    h_head=pp.plot(.5+np.cos(ar)*.4,.5+np.sin(ar)*.4,lw=lw,color=c, axes=hax)
    # Nose
    h_nose=pp.plot(.5+np.cos(ar)/30,.5+.4+np.sin(np.ma.masked_greater(ar,np.pi))/20,color=c,lw=lw, axes=hax)
    # Right ear
    h_rear=pp.plot(.5+.4+.021+np.cos(np.ma.masked_inside(ar,np.pi-.5, np.pi+.5))/40,.5+np.sin(np.ma.masked_inside(ar,np.pi-.5, np.pi+.5))/12,color=c,lw=lw, axes=hax)
    # Left ear
    h_lear=pp.plot(.5-.4-.021+np.cos(np.ma.masked_outside(ar, .5, np.pi*2-.5))/40,.5+np.sin(np.ma.masked_outside(ar, .5, np.pi*2-.5))/12,color=c,lw=lw, axes=hax)

    if dutchPart:
        # The short side
        hax.add_line(pp.Line2D([.35, .3], [.7, .75],linewidth=lw,color=c))
        hax.add_line(pp.Line2D([.35, .25], [.6, .65],linewidth=lw,color=c))
        hax.add_line(pp.Line2D([.35, .2], [.5, .55],linewidth=lw,color=c))
        hax.add_line(pp.Line2D([.35, .2], [.4, .42],linewidth=lw,color=c))
        hax.add_line(pp.Line2D([.35, .25],[.3, .3],linewidth=lw,color=c))
        hax.add_line(pp.Line2D([.35, .3], [.2, .2],linewidth=lw,color=c))

        # The Comb-over
        hax.add_line(pp.Line2D([.4, .45],[.7, .8],linewidth=lw,color=c))
        hax.add_line(pp.Line2D([.4, .6],[.6, .8],linewidth=lw,color=c))
        hax.add_line(pp.Line2D([.4, .7],[.5, .7],linewidth=lw,color=c))
        hax.add_line(pp.Line2D([.4, .8],[.4, .55],linewidth=lw,color=c))
        hax.add_line(pp.Line2D([.4, .8],[.3, .4],linewidth=lw,color=c))
        hax.add_line(pp.Line2D([.4, .7],[.2, .25],linewidth=lw,color=c))

