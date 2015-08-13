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
# contributions are welcome. Go to http://psylab.googlecode.com/ 
# for more information and to contribute. Or send an e-mail to: 
# cbrown1@pitt.edu.
#

import os
import sys
import sqlite3
from matplotlib import pyplot as pp
import matplotlib.patches as mpp
import matplotlib.markers as mpm
from matplotlib.lines import Line2D
import numpy as np

# The report must have the property 'name'
name = "Show_Audio"

def draw_page():

    # Derive this from the column names
    x = [125, 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000]
    
    xpos = np.arange(1,len(x)+1)

    fh = pp.figure(figsize=(8.5, 11))

    # Set up a `page` axis, to place text etc.
    ap = fh.add_axes([0, 0, 1, 1])

    af = fh.add_axes([.2, .3, .5*11/8.5, .5*8.5/11])
    af.axhspan(-5,20, fc='0.7', ec='None', alpha=0.5)

    af.set_ylim([-5, 115])
    af.yaxis.set_ticks(range(0, 120, 10))
    af.yaxis.set_ticklabels(range(0, 120, 10))
    af.invert_yaxis()
    af.xaxis.set_ticks(xpos)
    af.xaxis.set_ticklabels(x)
    af.set_xlim([.5, len(xpos)+.5])
    af.grid(True)
    af.set_ylabel('Threshold (Hearing Level)')
    af.set_xlabel('Frequency (Hz)')

    ap.set_xticks([])
    ap.set_yticks([])
    for spine in ap.spines:
	    ap.spines[spine].set_visible(False)
    ap.set_xlim([0, 8.5]) # Page coordinates are
    ap.set_ylim([0, 11])  # now in units of inches
    ap.invert_yaxis()

    ap.text(4.25, 1, "Psychoacoustics Lab",horizontalalignment='center', fontsize="x-large")
    ap.text(4.25, 1.25, "5057 Forbes Tower, Pittsburgh PA 15260",horizontalalignment='center', fontsize="medium")
    ap.text(4.25, 1.5, "The University of Pittsburgh",horizontalalignment='center', fontsize="medium")
    ap.text(4.25, 1.85, "Hearing Screening",horizontalalignment='center', fontsize="large")

    ap.text(6.4, 2.25, "Tester:",horizontalalignment='right')
    ap.text(6.4, 2.55, "Date of Audiogram:",horizontalalignment='right')
    ap.text(2, 2.25, "Patient Name:", horizontalalignment='right')
    ap.text(2, 2.55, "Date of Birth:", horizontalalignment='right')
    ap.text(2, 2.85, "Gender:", horizontalalignment='right')
    ap.hlines([2.25, 2.55, 2.85], 2.1, 4.5)
    ap.hlines([2.25, 2.55], 6.5, 7.5)

    ap.add_line(Line2D([1, 7.5],[3, 3],color='k',lw=2))

    ap.text(5, 8.6, "Notes: For research purposes")
    ap.text(5, 8.95, "only - not a clinical assessment")
    ap.hlines(np.arange(8.6,10,.35), 5, 7.5)

    # Legend:
    lx = 1.4
    ly = 8.5

    lbox = mpp.Rectangle((lx-.4, ly), 3.7, 1.48, facecolor="None", edgecolor="k", lw=1)
    ap.add_patch(lbox)

    ap.text(lx+2.4, ly+.4, "Right",horizontalalignment='center')
    ap.text(lx+3., ly+.4, "Left", horizontalalignment='center')

    ap.text(lx+2, ly+.8, "Air conduction - Unmasked",horizontalalignment='right')
    ap.text(lx+2, ly+1.2, "No response",horizontalalignment='right')

    ap.plot(lx+2.37,ly+.73, marker='o', ms=10, ls='None', mfc='None', mec='r', mew=3)
    ap.plot(lx+2.97,ly+.73, marker='x', ms=10, ls='None', mfc='None', mec='b', mew=3)

    ap.plot(lx+2.42,ly+1.13, marker=mpm.CARETRIGHT, ms=10, ls='None', mfc='None', mec='r', mew=3)
    ap.plot(lx+2.92,ly+1.13, marker=mpm.CARETLEFT, ms=10, ls='None', mfc='None', mec='b', mew=3)

    return fh,ap,af


def plot_data(ax, data, side):
    global pp, mpp, Line2D, np
    da = np.asarray(data)
    
    # Derive this from the column names
    x = [125, 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000]
    
    xpos = np.arange(1,len(x)+1)
    
    # Mask no responses
    dm_r = np.ma.masked_where(da<-10,da)
    xm_r = np.ma.masked_where(da<-10,xpos)
    
    # Mask responses
    dm_n = np.ma.masked_where(da>=-10,da)

    if side == 'left':
        c = 'b'
        nr_x = -.1
        mp_nr_y = [0, 2.]
        m='x'
        mnr = mpm.CARETLEFT
    else:
        c = 'r'
        nr_x = .1
        mp_nr_y = [0., 2.]
        mnr = mpm.CARETRIGHT
        m='o'
    
    ax.plot(xm_r, dm_r, marker=m, ms=10, ls='None', mfc='None', mec=c, mew=3)
    for i in range(len(dm_n)):
        if not dm_n.mask[i]:
            this_data = np.abs(dm_n.data[i])
            this_ind = xpos[i]
            ax.plot(this_ind+nr_x,this_data, marker=mnr, ms=10, ls='None', mfc='None', mec=c, mew=3)

def is_number(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError) as e:
        return False

def proc_subject(db, SubjN):
    """
    the report must have a function named 'proc_subject' for the report 
    to show up on the edit subject page ie, to run it on individual subjects.
    In this case, the full path to the db and the subject number will be 
    passed to the function.
    """
    fh,ap,af = draw_page()

    #af.text(8,50,'V',horizontalalignment='center',verticalalignment='center', rotation=45,color='r',fontweight='bold', fontsize=14)
    #af.plot(8,50,marker='v',color='r')
    x = [125, 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000]
    xpos = np.arange(1,len(x)+1)

    if db and os.path.exists(db):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("""SELECT FName,LName,DOB,Gender,User_Audio_Date,User_Audio_Tester FROM Subjects WHERE SubjN == \'%s\'""" % SubjN)
        subject = list(c.fetchone())
        for i in range(len(subject)):
            if subject[i] is None:
                subject[i] = ''
        if subject is not None:

            ap.text(6.5, 2.25, "%s" % subject[5],horizontalalignment='left')
            ap.text(6.5, 2.55, "%s" % subject[4],horizontalalignment='left')
            ap.text(2.1, 2.25, "%s %s" % (subject[0],subject[1]), horizontalalignment='left')
            ap.text(2.1, 2.55, "%s" % subject[2], horizontalalignment='left')
            ap.text(2.1, 2.85, "%s" % subject[3], horizontalalignment='left')

            c.execute("""SELECT User_L125,User_L250,User_L500,User_L750,User_L1k,
                         User_L15,User_L2k,User_L3k,User_L4k,User_L6k,User_L8k FROM Subjects WHERE SubjN == \'%s\'""" % (SubjN))
            uservar_this = c.fetchone()
            left = []
            for var in uservar_this:
                if var and is_number(var):
                    left.append(float(var))
                else:
                    left.append(np.nan)
            plot_data(af,left,'left')

            c.execute("""SELECT User_R125,User_R250,User_R500,User_R750,User_R1k,
                         User_R15,User_R2k,User_R3k,User_R4k,User_R6k,User_R8k FROM Subjects WHERE SubjN == \'%s\'""" % (SubjN))
            uservar_this = c.fetchone()
            right = []
            for var in uservar_this:
                if var and is_number(var):
                    right.append(float(var))
                else:
                    right.append(np.nan)
            plot_data(af,right,'right')

        fh.show()

if __name__ == "__main__":
    db = None
    SubjN = None
    if len(sys.argv) > 1:
        db = sys.argv[1].strip("\"").strip("\'")
    if len(sys.argv) > 2:
        SubjN = sys.argv[2]
    proc_subject(db, SubjN)

