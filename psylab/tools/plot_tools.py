# -*- coding: utf-8 -*-

# Copyright (c) 2010-2014 Christopher Brown
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

from matplotlib import pyplot as plt
import numpy as np

colors_asu = {}
colors_asu['maroon'] = list(np.array((153,0,51))/255.)
colors_asu['gold'] = list(np.array((255,179,16))/255.)
colors_asu['grey'] = list(np.array((79,85,87))/255.)
colors_asu['green'] = list(np.array((86, 142, 20))/255.)
colors_asu['blue'] = list(np.array((0, 142, 214))/255.)
colors_asu['orange'] = list(np.array((244, 124, 0))/255.)
colors_asu['warmgrey'] = list(np.array((175, 165, 147))/255.)

colors_pitt = {}
colors_pitt['blue'] = list(np.array((0,31,91))/255.)
colors_pitt['gold'] = list(np.array((182,162,105))/255.)
colors_pitt['black'] = list(np.array((13,34,63))/255.)

font_pitt = ["Janson","http://fontzone.net/font-details/janson-ssi"]

def ax_on_page(page_image=None, page_width=8.5, page_height=11., ax_image=None, ax_width=6., ax_height=4.5, ax_x=None, ax_y=None, dpi=None):
    """Returns a matplotlib axes that resides on a page,
        such as to create a slide for a presenation, or a figure page for a 
        manuscript. The page itself is also an axes with units in inches, so 
        it is easy to place text (eg, Titles, Fig captions, etc) and other 
        items on it. 
        
        Parameters
        ----------
        page_image: str
            The path to an image to be used as the background. If supplied,
            page_width and page_height are ignored
        page_width: scalar
            The width of the page, in inches. [default = 8.5]
        page_height: scalar
            The height of the page, in inches. [default = 11]
        ax_image: str
            The path to an image to be shown on the axes. If supplied,
            ax_width and ax_height are used as maximum constraints (aspect 
            ratio will be maintained), and all axes ticks marks and spines 
            will be turned off
        ax_width: scalar
            The width of the axes, in inches. [default = 6]
        ax_height: scalar
            The height of the axes, in inches. [default = 4.5]
        ax_x: scalar
            The x location of the lower-left corner of the axes, in inches. 
            [default = centered]
        ax_y: scalar
            The y location of the lower-left corner of the axes, in inches. 
            [default = centered]
        dpi: scalar
            The resolution, in dots-per-inch, to use. Because the coordinates 
            used are inches, you might want to set this value. The default is 
            matplotlib's savefig default (plt.rcParams[savefig.dpi]) because 
            then if you save the figure, any images will be scaled correctly. 
            

        Returns
        -------
        f : scalar
            The figure handle.
        ap : scalar
            The axes handle to the page.
        ax : scalar
            The axes handle to the plot.

        Notes
        -----
        When using an axis image, there is at least one possibly unexpected 
        outcome. Because the aspect ratio is maintained, if the image is less 
        than the axes along an axis, there will be space on either side of the 
        image. For example, an image that is wide and short will likely have 
        blank space above and below. As a result, in this example if you set 
        ax_y, the image will appear to be above that position because of the 
        blank space below it. 
        
        Another potential confusion stems from the fact that when saving a fig,
        the default resolution may be different than the display resolution. 
        So, when saving figures, be sure to use the same dpi as the figure:
        
        plt.savefig('example.png',dpi = f.get_dpi())
        
        If you use images and would like to save to a vector format (svg, pdf), 
        try using a dpi of 72 for both ax_on_page and savefig, which is the 
        only resolution that produces good-looking vector-based figures on my 
        machine.

        Example:
        
        # Generate axes with default page size
        f,ap,ax = ax_on_slide()
        # plot something
        h = ax.plot([1,2,3])
        # add some text to the page, towards the bottom, centered:
        ap.text(5.5,1,"A slide title!", horizontalalignment='center', fontsize='x-large')
    """
    
    page_width = float(page_width)
    page_height = float(page_height)
    ax_width = float(ax_width)
    ax_height = float(ax_height)
    
    if page_image is not None:
        if dpi is not None:
            dpi = float(dpi)
        else:
            # Default to savefig.dpi, so it looks good when saving
            dpi = float(plt.rcParams['savefig.dpi'])
            #dpi = float(plt.rcParams['figure.dpi'])
        z = plt.imread(page_image)
        page_width = z.shape[1] / dpi
        page_height = z.shape[0] / dpi
        f = plt.figure(figsize=(page_width, page_height), dpi=dpi)
        fi = f.figimage(z)
    else:
        f = plt.figure(figsize=(page_width, page_height))
    # Set up a `page` axis, to place text etc.
    ap = f.add_axes([0, 0, 1, 1])
    ap.set_axis_bgcolor('none')
    ap.set_xticks([])
    ap.set_yticks([])
    for spine in ap.spines:
        ap.spines[spine].set_visible(False)
    ap.set_xlim([0, page_width])   # Page coordinates are
    ap.set_ylim([0, page_height])  # now in units of inches
    ap.invert_yaxis()

    # Compute x, y, w, h of axes
    ax_w = ax_width / page_width # Coordinates are 0-1
    ax_h = ax_height / page_height

    if ax_x is None:
        ax_x = (page_width - ax_width) / 2 # Default = center
    ax_x /= page_width
    if ax_y is None:
        ax_y = (page_height - ax_height) / 2
    ax_y /= page_height

    ax = f.add_axes([ax_x, ax_y, ax_w, ax_h])

    if ax_image:
        z = plt.imread(ax_image)
        ax.imshow(z)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines:
            ax.spines[spine].set_visible(False)
        
    return f,ap,ax


def set_foregroundcolor(ax, color=None):
    '''For the specified axes, sets the color of the frame, major ticks,
        tick labels, axis labels, title and legend. 
        
        Defaults to current axes.
    '''
    
    if color is None:
        color = ax
        ax = plt.gca()
    
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
        plt.savefig("fig1.svg", transparent=True)
        
        Defaults to current axes.
    '''
    if color is None:
        color = ax
        ax = plt.gca()
    
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
        ax = plt.gca()
    
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
        ax = plt.gca()
    
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
        ax = plt.gca()
    
    ax.tick_params(labelsize=fontsize)

def set_legendtitlefontsize(ax, fontsize=None):
    if fontsize is None:
        fontsize = ax
        ax = plt.gca()
    
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
        f = plt.gcf()

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
    h_head=plt.plot(.5+np.cos(ar)*.4,.5+np.sin(ar)*.4,lw=lw,color=c, axes=hax)
    # Nose
    h_nose=plt.plot(.5+np.cos(ar)/30,.5+.4+np.sin(np.ma.masked_greater(ar,np.pi))/20,color=c,lw=lw, axes=hax)
    # Right ear
    h_rear=plt.plot(.5+.4+.021+np.cos(np.ma.masked_inside(ar,np.pi-.5, np.pi+.5))/40,.5+np.sin(np.ma.masked_inside(ar,np.pi-.5, np.pi+.5))/12,color=c,lw=lw, axes=hax)
    # Left ear
    h_lear=plt.plot(.5-.4-.021+np.cos(np.ma.masked_outside(ar, .5, np.pi*2-.5))/40,.5+np.sin(np.ma.masked_outside(ar, .5, np.pi*2-.5))/12,color=c,lw=lw, axes=hax)

    if dutchPart:
        # The short side
        hax.add_line(plt.Line2D([.35, .3], [.7, .75],linewidth=lw,color=c))
        hax.add_line(plt.Line2D([.35, .25], [.6, .65],linewidth=lw,color=c))
        hax.add_line(plt.Line2D([.35, .2], [.5, .55],linewidth=lw,color=c))
        hax.add_line(plt.Line2D([.35, .2], [.4, .42],linewidth=lw,color=c))
        hax.add_line(plt.Line2D([.35, .25],[.3, .3],linewidth=lw,color=c))
        hax.add_line(plt.Line2D([.35, .3], [.2, .2],linewidth=lw,color=c))

        # The Comb-over
        hax.add_line(plt.Line2D([.4, .45],[.7, .8],linewidth=lw,color=c))
        hax.add_line(plt.Line2D([.4, .6],[.6, .8],linewidth=lw,color=c))
        hax.add_line(plt.Line2D([.4, .7],[.5, .7],linewidth=lw,color=c))
        hax.add_line(plt.Line2D([.4, .8],[.4, .55],linewidth=lw,color=c))
        hax.add_line(plt.Line2D([.4, .8],[.3, .4],linewidth=lw,color=c))
        hax.add_line(plt.Line2D([.4, .7],[.2, .25],linewidth=lw,color=c))


def plot_discrete_signal(x,y):
    
    pos = np.where(y>0)[0]
    neg = np.where(y<0)[0]
    zp = np.zeros(pos.shape[0])
    zn = np.zeros(neg.shape[0])
    
    plt.axhline(color='k')
    plt.plot(x,y,'ko')
    plt.vlines(pos,zp,y[pos])
    plt.vlines(neg,zn,y[neg])
