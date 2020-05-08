# -*- coding: utf-8 -*-

# Copyright (c) 2010-2019 Christopher Brown
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
# contributions are welcome. Go to http://github.com/cbrown1/psylab/ 
# for more information and to contribute. Or send an e-mail to: 
# cbrown1@pitt.edu.
#

"""
plot_tools - A set of helper functions for formatting matplotlib figures
"""

from itertools import groupby
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as patches
from matplotlib.path import Path
import matplotlib.colors as colors
import matplotlib.mathtext as mathtext
import matplotlib.artist as artist
import matplotlib.image as image


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

# Use these markers in mpl plots with the marker kwarg: ...lw=2, marker=markers.x,...
# You can use the rotate_marker function below to rotate them: m = rotate_marker(markers.plus, 45)

class markers:
    loudspeaker = [(-0.5,    0.866),
                   (-0.5,    0.5  ),
                   (-1.,     0.   ),
                   ( 1.,     0.   ),
                   ( 0.5,    0.5  ),
                   ( 0.5,    0.866),
                   (-0.5,    0.866)]

    plus = [(-0.333,  1.),
            ( 0.333,  1.),
            ( 0.333,  0.333),
            ( 1.,     0.333),
            ( 1.,    -0.333),
            ( 0.333, -0.333),
            ( 0.333, -1.),
            (-0.333, -1.),
            (-0.333, -0.333),
            (-1.,    -0.333),
            (-1.,     0.333),
            (-0.333,  0.333),
            (-0.333,  1.)]

    # This is just marker_plus rotated 45 degrees
    x = [(-0.943,  0.472),
         (-0.472,  0.943),
         ( 0.   ,  0.471),
         ( 0.472,  0.943),
         ( 0.943,  0.472),
         ( 0.471, -0.   ),
         ( 0.943, -0.472),
         ( 0.472, -0.943),
         (-0.   , -0.471),
         (-0.472, -0.943),
         (-0.943, -0.472),
         (-0.471,  0.   ),
         (-0.943,  0.472)]

    arrow = [( 0.,   1.),
             ( 1.,   0.),
             ( 0.4,  0.),
             ( 0.4, -1),
             (-0.4, -1),
             (-0.4,  0),
             (-1.,   0.),
             ( 0.,   1.)]

    star = [( 0.,     1.   ),
            ( 0.294,  0.405),
            ( 0.951,  0.309),
            ( 0.476, -0.155),
            ( 0.588, -0.809),
            ( 0.,    -0.5  ),
            (-0.588, -0.809),
            (-0.476, -0.155),
            (-0.951,  0.309),
            (-0.294,  0.405),
            ( 0.,     1.   )]


# A roughly estimated points to pixels conversion function
def pt2px(x):
    return np.round((4.*x)/3.)


def show_all_markers(x,y, ms=None, dpi=None):
    """Given arrays x and y, returns them with x values adjusted so those with
        common y values do not overlap.

        Example
        -------
        CA = [0,4,0,3,0,5]
        CB = [0,0,4,4,2,2,2,2,3,0,5]

        x,y = show_all_markers(CA, CB, ms=12)

        ret = plt.plot(x, y, 'o', ms=12)
        plt.xlim((0,3))
    """

    xout = []
    yout = []
    if ms:
        ms = float(ms)
    else:
        ms = float(plt.rcParams['lines.markersize'])
    if dpi:
        dpi = float(dpi)
    else:
        dpi = float(plt.rcParams['figure.dpi'])
    for indx, klass in enumerate([x, y]):
        klass = groupby(sorted(klass))
        for item, objt in klass:
            objt = list(objt)
            points = len(objt)
            pos = 1 + indx + (1 - points) / 50.
            for item in objt:
                xout.append(pos)
                yout.append(item)
                pos += (ms/dpi)/2
    return xout,yout


def update_plotline(line, x, y):
    line.set_data(x, y)
    line.get_axes().get_figure().canvas.draw()


class slider_array():
    """Provide a set of sliders to manipulate the levels of a set of variables

        Given a dict with variable names as keys and lists of levels as vals,
        this class provides a matplotlib figure with a slider for each
        variable specified, each having a number of ticks equal to the number
        of levels for that variable.

        You also specify a callback function, which recevies an updated dict
        of vars and current levels whenever a slider is moved.

        One usecase for this is for interacting with factorial data. Suppose
        you have multiple levels of multiple factorialized variables, and it
        would be useful to see how your data change as the levels do. You can
        specify a callback in which you would update a figure with new data
        based on the current combination of variable levels, and then as you
        slide the sliders, the figure will be updated.

        Parameters
        ----------
        data: dict
            dict with variable names as keys and lists of levels as vals.
        callback: function
            The name of a function to call when a slider is moved. should
            accept a dict that will contain variable names as keys and the
            current variable levels as vals.

        Example
        -------
        # Assume raw_data is a pandas object with variables 'color',
        # 'position', 'quality', and 'Resp'
        >>> keyvals = {'color': ['red','blue','green'],
                       'position': ['left','right','center','up','down'],
                       'quality': ['good','bad']}
        >>> data = raw_data.copy()  # Make an intial plot
        >>> for key,val in keyvals.items():
                data = data[ data[key] == val[0] ]
        >>> p, = plt.plot(data['Resp'])
        >>> update(current): # function will run everytime a slider is updated
                data = raw_data.copy()
                # Filter data to include only current levels
                for key,val in current.items:
                    data = data[ data[ key ] == val ]
                p.set_ydata(data['Resp'])
                p.axes.figure.canvas.draw_idle()
        >>> d = slider_array(keyvals, update)
    """

    def __init__(self, vars_dict, callback):
        self.vars_dict = vars_dict
        self.keys = []
        self.vals = []
        for key, val in vars_dict.items():
            self.keys.append(key)
            self.vals.append(val)
        self.callback = callback
        tb = mpl.rcParams['toolbar']
        mpl.rcParams['toolbar'] = 'None'
        self.fig, self.axs = plt.subplots(len(self.keys), 1, sharex=True, figsize=(3, .5*len(self.vals)))
        self.fig.canvas.set_window_title("Data x")
        mpl.rcParams['toolbar'] = tb
        self.fig.subplots_adjust(left=0.25, right=0.75, hspace = 0.1)

        self.sliders = []
        for i in range(len(self.keys)):
            key = self.keys[i]
            n = len(self.vals[i])
            sl = Slider(self.axs[i], key, 0., 100., valfmt="None")
            sl.on_changed(self.update)
            sl.valtext.set_text(self.vals[i][0])
            self.sliders.append(sl)

    def update(self, val):
        current_vals = {}
        for i in range(len(self.keys)):
            key = self.keys[i]
            v = ( (self.sliders[i].val / 100.) * (len(self.vals[i])-1) )
            v = np.maximum(v,0)
            v = np.minimum(int(round(v)), len(self.vals[i])- (1/ len(self.vals[i])))
            val = self.vals[i][v]
            current_vals[key] = val
            self.sliders[i].valtext.set_text(val)
        self.callback(current_vals)


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
    ap.set_facecolor('none')
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

def draw_electrode_array(electrodes, array_pos, e_height, e_width=None, direction='e', ax=None, color='k', lw=1.5):
    """draws a simple graphical representation of a cochlear implant electrode array

        Parameters
        ----------
        electrodes: array-like
            A list of electrode positions, in axes coordinates.
        array_pos: scalar
            An axes coordinate of the array. If electrodes will be positioned along the x axis, this
            value will specify where on the y axis to place the array, and vice versa.
        e_height: scalar
            Size of the electrodes, and consequently, the array, along the axes that is perpendicular
            to the axes along which the electrodes are positioned. That is, if electrode position is
            along the x axis, this will specify their height, and if it is along y, this would actually
            be width.
        e_width: scalar
            Size of the electrodes along the axes along which the electrodes are positioned.
            Default == e_height.
        direction: str
            Specifies the direction of the array. One of either 'n' (array points up), 'e' (left to
            right), 's' (down), or 'w' (right to left). Default == 'e'.
        ax: matplotlib axes handle
            The axes to draw the array onto. Default == plt.gca()
        color: matplotlib color
            The color to use. Default == 'k' (black)

    """

    if not e_width:
        e_width = e_height
    if not ax:
        ax = plt.gca()

    # Compute distance between electrodes
    e_space = np.abs((electrodes[1] - electrodes[0]))

    # Used to draw tip (apical end) of array via a bezier curve
    codes = [Path.MOVETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             ]

    if direction == 'w':
        # Compute array positions
        array_start = electrodes[0] - (e_space/8.)
        array_end = electrodes[-1] + e_space
        cap_end = array_start-(e_space/2.)
        # Draw array sides and square (apical) end
        ax.hlines([array_pos, array_pos+e_height], array_start, array_end, color=color, lw=lw)
        ax.vlines(array_end, array_pos, array_pos+e_height, color=color)
        # Draw electrodes
        for place in electrodes:
            ax.add_patch(
                patches.Rectangle(
                    (place-(e_width/2.), array_pos), # (x,y)
                    e_width,                         # width
                    e_height,                        # height
                    facecolor=color,
                    lw=lw,
                )
            )
        # Compute tip (basal) end of array, as bezier points
        verts = [
            (array_start, array_pos),          # P0
            (cap_end, array_pos),              # P1
            (cap_end, array_pos+e_height),     # P2
            (array_start, array_pos+e_height), # P3
            ]

    elif direction == 'e':
        array_start = electrodes[0] - e_space
        array_end = electrodes[-1] + (e_space/8.)
        cap_end = array_end+(e_space/2.)
        ax.hlines([array_pos, array_pos+e_height], array_start, array_end, color=color, lw=lw)
        ax.vlines(array_start, array_pos, array_pos+e_height, color=color)
        for place in electrodes:
            ax.add_patch(
                patches.Rectangle(
                    (place-(e_width/2.), array_pos), # (x,y)
                    e_width,                         # width
                    e_height,                        # height
                    facecolor=color,
                    lw=lw,
                )
            )
        verts = [

            (array_end, array_pos),          # P0 Bezier
            (cap_end, array_pos),            # P1 Bezier
            (cap_end, array_pos+e_height),   # P2 Bezier
            (array_end, array_pos+e_height), # P3 Bezier
            ]

    elif direction == 'n':
        array_start = electrodes[0] - e_space
        array_end = electrodes[-1] + (e_space/8.)
        cap_end = array_end+(e_space/2.)
        ax.vlines([array_pos, array_pos+e_height], array_start, array_end, color=color, lw=lw)
        ax.hlines(array_start, array_pos, array_pos+e_height, color=color)
        for place in electrodes:
            ax.add_patch(
                patches.Rectangle(
                    (array_pos, place-(e_height/2.)), # (x,y)
                    e_height,                         # width
                    e_width,                          # height
                    facecolor=color,
                    lw=lw,
                )
            )
        verts = [
            (array_pos, array_end),          # P0
            (array_pos, cap_end),            # P1
            (array_pos+e_height, cap_end),   # P2
            (array_pos+e_height, array_end), # P3
            ]

    else:
        array_start = electrodes[0] - (e_space/8.)
        array_end = electrodes[-1] + e_space
        cap_end = array_start-(e_space/2.)
        ax.vlines([array_pos, array_pos+e_height], array_start, array_end, color=color, lw=lw)
        ax.hlines(array_end, array_pos, array_pos+e_height, color=color)
        for place in electrodes:
            ax.add_patch(
                patches.Rectangle(
                    (array_pos, place-(e_height/2.)), # (x,y)
                    e_height,                         # width
                    e_width,                          # height
                    facecolor=color,
                    lw=lw,
                )
            )
        verts = [
            (array_pos, array_start),          # P0
            (array_pos, cap_end),              # P1
            (array_pos+e_height, cap_end),     # P2
            (array_pos+e_height, array_start), # P3
            ]

    # Draw array tip
    path = Path(verts, codes)
    patch = patches.PathPatch(path, ec=color, fc='none', lw=lw)
    ax.add_patch(patch)

def draw_filterbank(cutoffs, y, height, slope_width, gap=0, ax=None, **kwargs):
    """Draws a simple graphical representation of a bank of contiguous bandpass filters

        Parameters
        ----------
        cutoffs: array like
            The cutoff frequencies to use, in x axis units
        y: scalar
            The position of the filterbank, in y axis units
        height: scalar
            The height of the filterbank, in y axis units
        slope_width: scalar
            The width of the filter slopes, in x axis units
        gap: scalar
            The width of the gap between contiguous filters (3-dB down points), in x axis units
        ax: matplotlib axes handle
            The axes to plot to. Default == plt.gca()
        kwargs: matplotlib kwargs
            Plotting parameters to use. Eg., lw=2, c='r', etc

        Returns
        -------
        handles: list
            A list of matplotlib lines2D object handles, one per bandpass filter.
            EG., handles[2].set_color("blue"); handles[2].set_linewidth(2)

        Notes
        -----
        The plot function is used to draw each filter, so if you don't specify a color in
        the kwargs, the current color map will be cycled through.

    """

    if not ax:
        ax = plt.gca()
    handles = []
    gap1 = gap / 2.
    gap2 = -gap / 2.
    for i in np.arange(len(cutoffs)-1):
        y1 = (np.float32(y), np.float32(y+height), np.float32(y+height), np.float32(y))
        x1 = (cutoffs[i] - slope_width + gap1, cutoffs[i] + gap1, cutoffs[i+1] + gap2, cutoffs[i+1] + slope_width + gap2)
        h, = ax.plot(x1, y1, **kwargs)
        handles.append(h)

    return handles

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

def rotate_marker(marker, angle):
    """Rotates the specified custom mpl marker to the specified angle.

        This might be useful in (and is intended for) drawing a schematic of
        a loudspeaker array as is often used in free-field listening
        environments, in which the angle of rotation of each loudspeaker
        changes with its location

        Parameters
        ----------
        marker : list of x,y tuples
            Each tuple is an x,y point. This list can be passed to
            matplotlib's plot function using the 'marker' keyword
        angle : float
            The angle of rotation of the marker. 0 would yeild a
            downward-facing marker, -90 a rightward facing marker, and 90 a
            leftward-facing marker

        Returns
        -------
        marker : list of x,y tuples
            Each tuple is an x,y point. This list can be passed as is to
            matplotlib's plot function, using the 'marker' keyword

        Example
        -------
        marker_loudspeaker = [(-0.5, .866), (-0.5, .5), (-1, 0), (1, 0), (.5, .5), (.5, .866), (-0.5, .866)]
        fig = plt.figure(figsize=(8,8)) # the fig should be symmetrical to look right
        rect = .1,.1,.8,.8 # Axes should be symmetric in fig as well
        ax = fig.add_axes(rect)

        radius = 6

        for loc in np.arange(-90, 90, 15):
            x = np.cos(np.deg2rad(loc+90)) * radius # +90 puts zero at the top
            y = np.sin(np.deg2rad(loc+90)) * radius
            marker = rotate_marker(marker_loudspeaker, loc)
            plt.plot(x, y, mew=1, markersize=20, mfc='none', mec='k', marker=marker)

        plt.ylim(-10, 10)
        plt.xlim(-10, 10)
        psylab.tools.plot_tools.add_head(w=.1, h=.1, dutchPart=True)

        plt.show()
    """

    angle = np.deg2rad(angle)

    marker_rotated = []

    for p in marker:

        x = p[0]*np.cos(angle) - p[1]*np.sin(angle)
        y = p[0]*np.sin(angle) + p[1]*np.cos(angle)

        marker_rotated.append((x,y))

    return marker_rotated


def plot_discrete_signal(x,y):

    pos = np.where(y>0)[0]
    neg = np.where(y<0)[0]
    zp = np.zeros(pos.shape[0])
    zn = np.zeros(neg.shape[0])

    plt.axhline(color='k')
    plt.plot(x,y,'ko')
    plt.vlines(pos,zp,y[pos])
    plt.vlines(neg,zn,y[neg])


def jitter_vals(data, jitter):
    """Returns an array of vals that are jittered so similar datapoints don't overlap completely
    """

    j = np.random.rand(len(data))*jitter
    j = j - (jitter/2.)
    j = j - j.mean()

    return xdata + j


class Widget(object):
    """
    Abstract base class for GUI neutral widgets
    """
    drawon = True
    eventson = True


class AxesWidget(Widget):
    """Widget that is connected to a single :class:`~matplotlib.axes.Axes`.

    Attributes:

    *ax* : :class:`~matplotlib.axes.Axes`
        The parent axes for the widget
    *canvas* : :class:`~matplotlib.backend_bases.FigureCanvasBase` subclass
        The parent figure canvas for the widget.
    *active* : bool
        If False, the widget does not respond to events.
    """
    def __init__(self, ax):
        self.ax = ax
        self.canvas = ax.figure.canvas
        self.cids = []
        self.active = True

    def connect_event(self, event, callback):
        """Connect callback with an event.

        This should be used in lieu of `figure.canvas.mpl_connect` since this
        function stores call back ids for later clean up.
        """
        cid = self.canvas.mpl_connect(event, callback)
        self.cids.append(cid)

    def disconnect_events(self):
        """Disconnect all events created by this widget."""
        for c in self.cids:
            self.canvas.mpl_disconnect(c)

    def ignore(self, event):
        """Return True if event should be ignored.

        This method (or a version of it) should be called at the beginning
        of any event callback.
        """
        return not self.active


class Slider(AxesWidget):
    """
    A slider representing a floating point range

    The following attributes are defined
      *ax*        : the slider :class:`matplotlib.axes.Axes` instance

      *val*       : the current slider value

      *vline*     : a :class:`matplotlib.lines.Line2D` instance
                     representing the initial value of the slider

      *poly*      : A :class:`matplotlib.patches.Polygon` instance
                     which is the slider knob

      *valfmt*    : the format string for formatting the slider text

      *label*     : a :class:`matplotlib.text.Text` instance
                     for the slider label

      *closedmin* : whether the slider is closed on the minimum

      *closedmax* : whether the slider is closed on the maximum

      *slidermin* : another slider - if not *None*, this slider must be
                     greater than *slidermin*

      *slidermax* : another slider - if not *None*, this slider must be
                     less than *slidermax*

      *dragging*  : allow for mouse dragging on slider

    Call :meth:`on_changed` to connect to the slider event
    """
    def __init__(self, ax, label, valmin, valmax, valinit=0.5, valfmt='%1.2f',
                 closedmin=True, closedmax=True, slidermin=None, slidermax=None,
                 dragging=True, **kwargs):
        """
        Create a slider from *valmin* to *valmax* in axes *ax*

        *valinit*
            The slider initial position

        *label*
            The slider label

        *valfmt*
            Used to format the slider value

        *closedmin* and *closedmax*
            Indicate whether the slider interval is closed

        *slidermin* and *slidermax*
            Used to constrain the value of this slider to the values
            of other sliders.

        additional kwargs are passed on to ``self.poly`` which is the
        :class:`matplotlib.patches.Rectangle` which draws the slider
        knob.  See the :class:`matplotlib.patches.Rectangle` documentation
        valid property names (e.g., *facecolor*, *edgecolor*, *alpha*, ...)
        """
        AxesWidget.__init__(self, ax)

        self.valmin = valmin
        self.valmax = valmax
        self.val = valinit
        self.valinit = valinit
        self.poly = ax.axvspan(valmin,valinit,0,1, **kwargs)

        self.vline = ax.axvline(valinit,0,1, color='r', lw=1)


        self.valfmt=valfmt
        ax.set_yticks([])
        ax.set_xlim((valmin, valmax))
        ax.set_xticks([])
        ax.set_navigate(False)

        self.connect_event('button_press_event', self._update)
        self.connect_event('button_release_event', self._update)
        if dragging:
            self.connect_event('motion_notify_event', self._update)
        self.label = ax.text(-0.02, 0.5, label, transform=ax.transAxes,
                             verticalalignment='center',
                             horizontalalignment='right')

        if self.valfmt == "None":
            self.valtext = ax.text(1.02, 0.5, " ",
                                   transform=ax.transAxes,
                                   verticalalignment='center',
                                   horizontalalignment='left')
        else:
            self.valtext = ax.text(1.02, 0.5, valfmt%valinit,
                                   transform=ax.transAxes,
                                   verticalalignment='center',
                                   horizontalalignment='left')

        self.cnt = 0
        self.observers = {}

        self.closedmin = closedmin
        self.closedmax = closedmax
        self.slidermin = slidermin
        self.slidermax = slidermax
        self.drag_active  = False

    def _update(self, event):
        'update the slider position'
        if self.ignore(event):
            return

        if event.button != 1:
            return

        if event.name == 'button_press_event' and event.inaxes == self.ax:
            self.drag_active = True
            event.canvas.grab_mouse(self.ax)

        if not self.drag_active:
            return

        elif ((event.name == 'button_release_event')
             or (event.name == 'button_press_event' and event.inaxes != self.ax)):
            self.drag_active = False
            event.canvas.release_mouse(self.ax)
            return

        val = event.xdata
        if val <= self.valmin:
            if not self.closedmin:
                return
            val = self.valmin
        elif val >= self.valmax:
            if not self.closedmax:
                return
            val = self.valmax

        if self.slidermin is not None and val <= self.slidermin.val:
            if not self.closedmin:
                return
            val = self.slidermin.val

        if self.slidermax is not None and val >= self.slidermax.val:
            if not self.closedmax:
                return
            val = self.slidermax.val

        self.set_val(val)

    def set_val(self, val):
        xy = self.poly.xy
        xy[2] = val, 1
        xy[3] = val, 0
        self.poly.xy = xy
        if self.valfmt is not "None":
            self.valtext.set_text(self.valfmt%val)
        if self.drawon: self.ax.figure.canvas.draw()
        self.val = val
        if not self.eventson: return
        for cid, func in self.observers.items():
            func(val)

    def on_changed(self, func):
        """
        When the slider value is changed, call *func* with the new
        slider position

        A connection id is returned which can be used to disconnect
        """
        cid = self.cnt
        self.observers[cid] = func
        self.cnt += 1
        return cid

    def disconnect(self, cid):
        'remove the observer with connection id *cid*'
        try: del self.observers[cid]
        except KeyError: pass

    def reset(self):
        "reset the slider to the initial value if needed"
        if (self.val != self.valinit):
            self.set_val(self.valinit)


def table(col_widths, row_heights, cols=None, rows=None, labels=None, hmerge=[], vmerge=[], omit=[], color='k'):

    """Generates tables in mpl with basic control over cell height and width

        Cells can be merged horizontally and/or vertically, and the borders
        for particular cells can be omitted from drawing.

        Also provides facility to add labels to individual cells, with the
        ability to format and align each label, and specify cell padding.
        No check is performed on whether the text fits in the cell.

        The target usecase of this function is to generate simple tables that
        can be saved to pdf or another format to be included , eg., in lab
        worksheets, for use as data-entry tables by students in a lab class.
        This is the kind of task that is typically performed with spreadsheets,
        but this function provides a fully scriptable solution.

        Parameters
        ----------
        col_widths: scalar or array
            The width(s) of the columns. If an array is used, its length will
            specify the number of columns (and cols is ignored), and each list
            item is the length of each correspoding column. If a scalar is
            used, all columns will have the same width, and the number of
            columns must be specified using cols.
        row_heights: scalar or array
            The height(s) of the rows. If an array is used, its length will
            specify the number of rows (and rows is ignored), and each list
            item is the height of each corresponding row. If a scalar is used,
            all rows will have the same height, and the number of rows must be
            specified using rows.
        cols : Scalar
            The number of columns, only used if column_widths is a scalar
        rows : Scalar
            The number of rows, only used if row_heights is a scalar
        labels : dict
            A dict to specify cell labels. Each key is a string representation
            of a 2-element tuple, where the first element is the row number and
            the second element is the column number (top to bottom) of the cell
            in which to apply the label. Each value is either a string (the
            label text) or a list. If a list is specified, the first element is
            the string label, the second is an mpl fontdict (eg.,
            {'weight': 'bold', 'ha': 'left'}), and the third is optionally a
            float indicating the amount of padding, which is used when an
            alignment is not center. By default, labels will be centered both
            vertically and horizontally within a cell.
        hmerge : list
            A list of indices. For each item listed, merge it with the cell to
            the left. Eg., if an item is '0,1', then 0,1 and 1,1 will be
            merged. Must be < the number of columns
        vmerge : list
            A list of indices. For each item listed, merge it with the cell
            below. Eg., if an item is '0,1', then 0,1 and 0,2 will be
            merged. Must be < the number of rows
        omit : list
            A list of indices to cells that should not be drawn. Note that if
            a cell is specified that is surrounded on all four sides with
            other cells, this will have no visible effect since the borders of
            those cells will still be visible

        Returns
        -------
        ax: mpl axes handle
            A handle to the newly created matplotlib axes that holds the table

        Example
        -------
        # Four columns
        col_widths = [1, 2, .5, 1, 1]
        # Five rows
        row_heights = [.5, .5, .33,.25,.25]
        # Add some labels
        labels = {'1,0': 'Label 1', '3,1': ['Another', {'weight': 'bold'}] }
        # Merge cells 1,1 and 2,1
        hmerge = ['1,1']
        ax = table(col_widths, row_heights, labels=labels, hmerge=hmerge)

    """

    x = [0]
    y = [0]
    w = 0
    h = 0
    if isinstance(col_widths, (int, float)):
        c = cols
        cw = col_widths
        col_widths = []
        for i in np.arange(c):
            col_widths.append(cw)
    else:
        c = len(col_widths)
    for i in np.arange(c):
        w += col_widths[i]
        x.append(w)

    if isinstance(row_heights, (int, float)):
        r = rows
        rh = row_heights
        row_heights = []
        for i in np.arange(r):
            row_heights.append(rh)
    else:
        r = len(row_heights)
    for i in np.arange(r):
        h += row_heights[i]
        y.append(h)

    page_width = w
    page_height = h

    # Create mpl figure, remove all default items (ticks, spines, etc)
    f = plt.figure(figsize=(page_width, page_height))
    ap = f.add_axes([0, 0, 1, 1])
    ap.set_facecolor('none')
    ap.set_xticks([])
    ap.set_yticks([])
    for spine in ap.spines:
        ap.spines[spine].set_visible(False)
    ap.set_xlim([0, page_width])   # Page coordinates are
    ap.set_ylim([0, page_height])  # now in units of inches
    ap.invert_yaxis()

    # Draw each cell as a rect
    # xx and yy are the x and y coords of the current rect
    yy = 0
    y_ind = 0
    hmerged = []
    vmerged = []
    # For all subsequent comments, assume:
    # Current cell in loop is 0,0, & that
    # hmerge = ['0,0', '1,0'] (cells to horizontally merge: 0,0 1,0 2,0),
    # and vmerge = ['0,0'] (cells to vertically merge: 0,0 0,1)
    for yh in row_heights:
        #print ("Y{:}: {:}".format(y_ind, yy))
        xx = 0
        x_ind = 0
        for xw in col_widths:
            #print ("  X{:}: {:}".format(x_ind, xx))
            ind = ",".join((str(x_ind), str(y_ind)))
            if ind not in hmerged and ind not in vmerged:
                #print ("    not a previous merge {}".format(ind))
                # Temp lists
                this_hmerged = []
                this_vmerged = []
                # Ind lists
                got_hmerged = []
                got_vmerged = []
                xwm = xw
                # For each cell, find each subsequent cell to merge
                for x_ind_m in np.arange(x_ind, len(col_widths)-1):
                    ind_m = ",".join((str(x_ind_m), str(y_ind)))
                    #print ("      checking: {}".format(ind_m))
                    # 0,0 is in list, which means 1,0 should be merged, and added to merged list (same for 2,0)
                    if ind_m in hmerge and ind_m not in hmerged:
                        #print ("      vmerge: {}".format(ind_m))
                        xwm += col_widths[x_ind_m+1] # add width of 1,0
                        ind_m_next = ",".join((str(x_ind_m+1), str(y_ind))) # Generate ind for 1,0 (and then 2,0)
                        #print ("      adding ind to hmerge: {}".format(ind_m_next))
                        # Add 1,0 and 2,0 to a temp hmerged
                        this_hmerged.append(ind_m_next)
                        # Add 1 and 2 to hmerge ind list, so that 1,1 and 2,1 will eventually be added
                        #print ("      adding x_ind to got_hmerge: {:}".format(x_ind_m+1))
                        got_hmerged.append(x_ind_m+1)
                    else:
                        break

                yhm = yh
                # Same for columns
                for y_ind_m in np.arange(y_ind, len(row_heights)-1):
                    ind_m = ",".join((str(x_ind), str(y_ind_m)))
                    if ind_m in vmerge and ind_m not in vmerged:
                        yhm += row_heights[y_ind_m+1]
                        ind_m_next = ",".join((str(x_ind), str(y_ind_m+1)))
                        this_vmerged.append(ind_m_next)
                        got_vmerged.append(y_ind_m+1)
                    else:
                        break

                for this in this_hmerged:
                    # Add merged cells for current row
                    #print ("    adding temp hmerge to hmerge: {}".format(this))
                    hmerged.append(this)
                    for vm in got_vmerged:
                        for hm in got_hmerged:
                            # Create indices for all merged cells not in current row and not in current column ie., 1,1 2,1
                            this_i = ",".join((str(hm), str(vm)))
                            #print ("    building ind for non-current row/cell to add to hmerge: {}".format(this_i))
                            # Add those to hmerged
                            hmerged.append(this_i)

                for this in this_vmerged:
                    # Add merged cells for current column
                    vmerged.append(this)
                    for vm in got_vmerged:
                        for hm in got_hmerged:
                            # Create indices for all merged cells not in current row and not current column ie., 1,1 2,1
                            this_i = ",".join((str(hm), str(vm)))
                            # Add those to vmerged
                            vmerged.append(this_i)

                if ind not in omit:

                    ap.add_patch(
                        mpl.patches.Rectangle(
                            (xx, yy),
                            xwm,
                            yhm,
                            fill=False,      # remove background
                            ec=color,
                        )
                    )
            else:
                #print ("    a previous merge: {}".format(ind))
                pass

            xx += xw
            x_ind += 1
        yy += yh
        y_ind += 1

#    ap.hlines(y, 0, page_width)
#    ap.vlines(x, 0, page_height)

    if labels:
        for i,label in labels.items():
            if isinstance(label, list):
                l = label[0]
                fd = label[1]
                if len(label) == 3:
                    pad = label[2]
                else:
                    pad = .1
            else:
                l = label
                fd = {'weight': 'normal'}
                pad = .1

            cell_x,cell_y = i.split(',')
            cell_x = int(cell_x)
            cell_y = int(cell_y)

            if 'ha' not in fd:
                fd['ha'] = 'center'
            if fd['ha'] == 'left':
                lx = x[cell_x] + pad
            elif fd['ha'] == 'right':
                lx = x[cell_x+1] - pad
            else:
                lx = x[cell_x] + ((x[cell_x+1]-x[cell_x])/2.)

            if 'va' not in fd:
                fd['va'] = 'center'
            if fd['va'] == 'top':
                ly = y[cell_y] + pad
            elif fd['va'] == 'bottom':
                ly = y[cell_y+1] - pad
            else:
                ly = y[cell_y] + ((y[cell_y+1]-y[cell_y])/2.)

            ap.text(lx, ly, l, fd)

    return ap


def hinton(matrix, max_weight=None, ax=None, color_n='black', color_p='white', color_bg='gray'):

    """Draw Hinton diagram for visualizing a weight matrix.

        Matrix should be a 2d array of weights

    """
    if ax is None:
        ax = plt.gca()

    if not max_weight:
        max_weight = 2 ** np.ceil(np.log(np.abs(matrix).max()) / np.log(2))

    ax.patch.set_facecolor(color_bg)

    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())

    for (x, y), w in np.ndenumerate(matrix):
        color = color_p if w > 0 else color_n
        size = np.sqrt(np.abs(w) / max_weight) * 12
        plt.plot(x,y,'s', mfc = color, mec = color, ms = size)
    return ax


def subplots_ax_labels_where(rows, cols, ax='x'):

    """subplots_ax_labels_where computes the subplot indexes that should received x or y axis lables for a good looking grid

       For example if you are plotting a 3 row x 4 column grid of subplots, it is most often
       desirable to have y axis labels on the left-most subplots (1, 5, and 9),
       and x axis labels on the bottom 4 subplots (9, 10, 11, and 12). This function returns
       an array of indexes for x or y labels accordingly, given a number of rows, and columns.

    """
    total = rows * cols

    if ax == 'y':
        ret = np.arange(1, total, cols)
    else:
        ret = np.arange(total-cols+1, total+1)

    return ret


def get_nearest_factors(n):
    """Give a number, returns its factor pair nearest each other
        EG., for the number 6, it would return (2,3), 20: (4,5)

        Intended usecase is to aid with layout of a multi-axes grid,
        in which the returned tuple would be used to specify the
        number of rows and columns of the figure. EG, I've 12 panels
        to plot, so the desired layout would be 3x4.

        Function won't work with n <=0

    """
    testNum = int(np.sqrt(n))
    while n % testNum != 0:
        testNum -= 1
    return (testNum, int(n / float(testNum)))


def sigmoid_normalized(x, center, width):
   '''Returns array of a horizontal mirrored normalized sigmoid function
        output between 0 and 1

        Parameters
        ----------
        center: scalar
            The center of the sigmoid function
        width: scalar
            The width of the sigmoid function
        x : Array
            The x axis data for the sigmoid

        Example
        -------
        >>> center = .5
        >>> width = 8
        >>> x = np.linspace(0,1,5)
        >>> sigmoid_normalized(x, center, width)
        array([ 0.        ,  0.10499359,  0.5       ,  0.89500641,  1.        ])

   '''
   s= 1/(1+np.exp(width*(x-center)))
   return np.flip(1*(s-np.min(s))/(np.max(s)-np.min(s)),0) # normalize function to 0-1


# Text Wrapping
# Defines wrapText which will attach an event to a given mpl.text object,
# wrapping it within the parent axes object.  Also defines a the convenience
# function textBox() which effectively converts an axes to a text box.
def wrapText(text, margin=4):
    """ Attaches an on-draw event to a given mpl.text object which will
        automatically wrap its string wthin the parent axes object.

        The margin argument controls the gap between the text and axes frame
        in points.

        Copied from : https://stackoverflow.com/questions/4018860/text-box-with-line-wrapping-in-matplotlib

        Example
        -------

        ax = plot.plt.figure(figsize=(6, 6)).add_subplot(111)
        an = ax.annotate(t, fontsize=12, xy=(0.5, 1), ha='center', va='top', xytext=(0, -6),
                 xycoords='axes fraction', textcoords='offset points')
        wrapText(an)
    """
    ax = text.get_axes()
    margin = margin / 72 * ax.figure.get_dpi()

    def _wrap(event):
        """Wraps text within its parent axes."""
        def _width(s):
            """Gets the length of a string in pixels."""
            text.set_text(s)
            return text.get_window_extent().width

        # Find available space
        clip = ax.get_window_extent()
        x0, y0 = text.get_transform().transform(text.get_position())
        if text.get_horizontalalignment() == 'left':
            width = clip.x1 - x0 - margin
        elif text.get_horizontalalignment() == 'right':
            width = x0 - clip.x0 - margin
        else:
            width = (min(clip.x1 - x0, x0 - clip.x0) - margin) * 2

        # Wrap the text string
        words = [''] + _splitText(text.get_text())[::-1]
        wrapped = []

        line = words.pop()
        while words:
            line = line if line else words.pop()
            lastLine = line

            while _width(line) <= width:
                if words:
                    lastLine = line
                    line += words.pop()
                    # Add in any whitespace since it will not affect redraw width
                    while words and (words[-1].strip() == ''):
                        line += words.pop()
                else:
                    lastLine = line
                    break

            wrapped.append(lastLine)
            line = line[len(lastLine):]
            if not words and line:
                wrapped.append(line)

        text.set_text('\n'.join(wrapped))

        # Draw wrapped string after disabling events to prevent recursion
        handles = ax.figure.canvas.callbacks.callbacks[event.name]
        ax.figure.canvas.callbacks.callbacks[event.name] = {}
        ax.figure.canvas.draw()
        ax.figure.canvas.callbacks.callbacks[event.name] = handles

    ax.figure.canvas.mpl_connect('draw_event', _wrap)

def _splitText(text):
    """ Splits a string into its underlying chucks for wordwrapping.  This
        mostly relies on the textwrap library but has some additional logic to
        avoid splitting latex/mathtext segments.
    """
    import textwrap
    import re
    math_re = re.compile(r'(?<!\\)\$')
    textWrapper = textwrap.TextWrapper()

    if len(math_re.findall(text)) <= 1:
        return textWrapper._split(text)
    else:
        chunks = []
        for n, segment in enumerate(math_re.split(text)):
            if segment and (n % 2):
                # Mathtext
                chunks.append('${}$'.format(segment))
            else:
                chunks += textWrapper._split(segment)
        return chunks

def textBox(text, axes, ha='left', fontsize=12, margin=None, frame=True, **kwargs):
    """ Converts an axes to a text box by removing its ticks and creating a
        wrapped annotation.
    """
    if margin is None:
        margin = 6 if frame else 0
    axes.set_xticks([])
    axes.set_yticks([])
    axes.set_frame_on(frame)

    an = axes.annotate(text, fontsize=fontsize, xy=({'left':0, 'right':1, 'center':0.5}[ha], 1), ha=ha, va='top',
                       xytext=(margin, -margin), xycoords='axes fraction', textcoords='offset points', **kwargs)
    wrapText(an, margin=margin)
    return an

# Menu on a figure:
#    fig = plt.figure()
#    fig.subplots_adjust(left=0.3)
#    props = ItemProperties(labelcolor='black', bgcolor='yellow',
#                           fontsize=15, alpha=0.2)
#    hoverprops = ItemProperties(labelcolor='white', bgcolor='blue',
#                                fontsize=15, alpha=0.2)
#
#    menuitems = []
#    for label in ('open', 'close', 'save', 'save as', 'quit'):
#        def on_select(item):
#            print('you selected %s' % item.labelstr)
#        item = MenuItem(fig, label, props=props, hoverprops=hoverprops,
#                        on_select=on_select)
#        menuitems.append(item)


class ItemProperties(object):
    def __init__(self, fontsize=14, labelcolor='black', bgcolor='yellow',
                 alpha=1.0):
        self.fontsize = fontsize
        self.labelcolor = labelcolor
        self.bgcolor = bgcolor
        self.alpha = alpha

        self.labelcolor_rgb = colors.to_rgba(labelcolor)[:3]
        self.bgcolor_rgb = colors.to_rgba(bgcolor)[:3]


class MenuItem(artist.Artist):
    parser = mathtext.MathTextParser("Bitmap")
    padx = 5
    pady = 5

    def __init__(self, fig, labelstr, props=None, hoverprops=None,
                 on_select=None):
        artist.Artist.__init__(self)

        self.set_figure(fig)
        self.labelstr = labelstr

        if props is None:
            props = ItemProperties()

        if hoverprops is None:
            hoverprops = ItemProperties()

        self.props = props
        self.hoverprops = hoverprops

        self.on_select = on_select

        x, self.depth = self.parser.to_mask(
            labelstr, fontsize=props.fontsize, dpi=fig.dpi)

        if props.fontsize != hoverprops.fontsize:
            raise NotImplementedError(
                'support for different font sizes not implemented')

        self.labelwidth = x.shape[1]
        self.labelheight = x.shape[0]

        self.labelArray = np.zeros((x.shape[0], x.shape[1], 4))
        self.labelArray[:, :, -1] = x/255.

        self.label = image.FigureImage(fig, origin='upper')
        self.label.set_array(self.labelArray)

        # we'll update these later
        self.rect = patches.Rectangle((0, 0), 1, 1)

        self.set_hover_props(False)

        fig.canvas.mpl_connect('button_release_event', self.check_select)

    def check_select(self, event):
        over, junk = self.rect.contains(event)
        if not over:
            return

        if self.on_select is not None:
            self.on_select(self)

    def set_extent(self, x, y, w, h):
        print(x, y, w, h)
        self.rect.set_x(x)
        self.rect.set_y(y)
        self.rect.set_width(w)
        self.rect.set_height(h)

        self.label.ox = x + self.padx
        self.label.oy = y - self.depth + self.pady/2.

        self.rect._update_patch_transform()
        self.hover = False

    def draw(self, renderer):
        self.rect.draw(renderer)
        self.label.draw(renderer)

    def set_hover_props(self, b):
        if b:
            props = self.hoverprops
        else:
            props = self.props

        r, g, b = props.labelcolor_rgb
        self.labelArray[:, :, 0] = r
        self.labelArray[:, :, 1] = g
        self.labelArray[:, :, 2] = b
        self.label.set_array(self.labelArray)
        self.rect.set(facecolor=props.bgcolor, alpha=props.alpha)

    def set_hover(self, event):
        'check the hover status of event and return true if status is changed'
        b, junk = self.rect.contains(event)

        changed = (b != self.hover)

        if changed:
            self.set_hover_props(b)

        self.hover = b
        return changed


class Menu(object):
    def __init__(self, fig, menuitems):
        self.figure = fig
        fig.suppressComposite = True

        self.menuitems = menuitems
        self.numitems = len(menuitems)

        maxw = max([item.labelwidth for item in menuitems])
        maxh = max([item.labelheight for item in menuitems])

        totalh = self.numitems*maxh + (self.numitems + 1)*2*MenuItem.pady

        x0 = 100
        y0 = 400

        width = maxw + 2*MenuItem.padx
        height = maxh + MenuItem.pady

        for item in menuitems:
            left = x0
            bottom = y0 - maxh - MenuItem.pady

            item.set_extent(left, bottom, width, height)

            fig.artists.append(item)
            y0 -= maxh + MenuItem.pady

        fig.canvas.mpl_connect('motion_notify_event', self.on_move)

    def on_move(self, event):
        draw = False
        for item in self.menuitems:
            draw = item.set_hover(event)
            if draw:
                self.figure.canvas.draw()
                break


def range_brace(x_min, x_max, mid=0.5, 
                beta1=100.0, beta2=100.0, height=1, 
                initial_divisions=11, resolution_factor=1.5):
    # determine x0 values adaptively using second derivitive
    # could be replaced with less snazzy:
    #   x0 = np.arange(0, 0.5, .001)
    x0 = np.array(())
    tmpx = np.linspace(0, 0.5, initial_divisions)
    tmp = beta1**2 * (np.exp(beta1*tmpx)) * (1-np.exp(beta1*tmpx)) / np.power((1+np.exp(beta1*tmpx)),3)
    tmp += beta2**2 * (np.exp(beta2*(tmpx-0.5))) * (1-np.exp(beta2*(tmpx-0.5))) / np.power((1+np.exp(beta2*(tmpx-0.5))),3)
    for i in np.arange(0, len(tmpx)-1):
        t = np.int32(np.ceil(resolution_factor*max(np.abs(tmp[i:i+2]))/np.float32(initial_divisions)))
        x0 = np.append(x0, np.linspace(tmpx[i],tmpx[i+1],t))
    x0 = np.sort(np.unique(x0)) # sort and remove dups
    # half brace using sum of two logistic functions
    y0 = mid*2*((1/(1.+np.exp(-1*beta1*x0)))-0.5)
    y0 += (1-mid)*2*(1/(1.+np.exp(-1*beta2*(x0-0.5))))
    # concat and scale x
    x = np.concatenate((x0, 1-x0[::-1])) * np.float32((x_max-x_min)) + x_min
    y = np.concatenate((y0, y0[::-1])) * np.float32(height)
    return (x,y)
