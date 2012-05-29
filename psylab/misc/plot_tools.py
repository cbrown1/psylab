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

"""
plot_tools - A set of helper functions for formatting matplotlib figures
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

def ax_to_page(ax, page_width=8.5, page_height=11.):

    axp = ax.get_position()
    ax_width = axp.width * ax.figure.bbox_inches.width
    ax_height = axp.height * ax.figure.bbox_inches.height
    vertical_shift = 2.
    
    for n in range(1,101):
        if n not in pp.get_fignums():
            break
    
    fh = pp.figure(num=n,figsize=(page_width, page_height))
    ah = fh.add_axes(ax)
    
    ah.set_position([(page_width/2.-ax_width/2)/page_width, 
                       vertical_shift/page_height+(page_height/2-ax_height/2)/page_height, 
                       ax_width/page_width, 
                       ax_height/page_height])
    ah.plot((1,2,3))

    return fh

def set_foregroundcolor(ax, color=None):
    '''For the specified axes, sets the color of the frame, major ticks,
        tick labels, axis labels, title and legend. 
        
        Defaults to current axes.
    '''
    
    if color is None:
        color = ax
        ax = pp.gca()
    
    for spine in ax.spines:
        ax.spines[spine].set_edgecolor(color)
        
    ax.tick_params(colors=color)
    
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
    if width is None:
        width = ax
        ax = pp.gca()
    
    ax.tick_params(width=width)
    for spine in ax.spines:
        ax.spines[spine].set_linewidth(width)

def set_fontsize(ax, fontsize=None):
    '''Sets the fontsize for the most common figure text
        (title, tick labels, axis labels, and legend text)
        
        Defaults to current axes.
    '''
    if fontsize is None:
        fontsize = ax
        ax = pp.gca()
    
    ax.tick_params(labelsize=fontsize)
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
    if fontsize is None:
        fontsize = ax
        ax = pp.gca()
    
    ax.tick_params(labelsize=fontsize)

def set_legendtitlefontsize(ax, fontsize=None):
    if fontsize is None:
        fontsize = ax
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

