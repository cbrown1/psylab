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

import sys
import sqlite3
from matplotlib import pyplot as pp
import matplotlib.patches as mpp
from matplotlib.lines import Line2D
import numpy as np

# The report must have the property 'name'
name = "Audiogram"

def draw_page():

    fh = pp.figure(figsize=(8.5, 11))

    # Set up a `page` axis, to place text etc.
    ap = fh.add_axes([0, 0, 1, 1])
    ap.set_xticks([])
    ap.set_yticks([])
    for spine in ap.spines:
	    ap.spines[spine].set_visible(False)
    ap.set_xlim([0, 8.5]) # Page coordinates are
    ap.set_ylim([0, 11])  # now in units of inches
    ap.invert_yaxis()

    ap.add_line(Line2D([1, 7.5],[3, 3],color='k',lw=2))

    for i in np.arange(8.6,10,.35):
	    ap.add_line(Line2D([5,7.5],[i,i],color='k',lw=1))
	
    ap.text(5, 8.6, "Notes:")

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

    ap.add_patch(mpp.FancyArrowPatch((lx+2.37,ly+1.13), (lx+2.27,ly+1.23), arrowstyle='->', lw=3, ec='r', mutation_scale=20))
    ap.add_patch(mpp.FancyArrowPatch((lx+2.97,ly+1.13), (lx+3.07,ly+1.23), arrowstyle='->', lw=3, ec='b', mutation_scale=20))

    return fh,ap


def plot_data(ax, data, side):
    global pp, mpp, Line2D, np
    da = np.asarray(data)
    
    # Derive this from the column names
    x = [125, 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000]
    
    xpos = np.arange(1,len(x)+1)
    
    # Mask no responses
    dm_r = np.ma.masked_where(da<0,da)
    xm_r = np.ma.masked_where(da<0,xpos)
    
    # Mask responses
    dm_n = np.ma.masked_where(da>=0,da)

    if side == 'left':
        c = 'b'
        mp_nr_x = [0., .2]
        mp_nr_y = [0, 2.]
        m='x'
    else:
        c = 'r'
        mp_nr_x = [0., -.2]
        mp_nr_y = [0., 2.]
        m='o'
    
    ax.plot(xm_r, dm_r, marker=m, ms=10, ls='None', mfc='None', mec=c, mew=3)
    for i in range(len(dm_n)):
        if not dm_n.mask[i]:
            this_data = np.abs(dm_n.data[i])
            this_ind = xpos[i]
            ar = mpp.FancyArrowPatch((this_ind+mp_nr_x[0],this_data+mp_nr_y[0]), (this_ind+mp_nr_x[1],this_data+mp_nr_y[1]), arrowstyle='->', lw=3, ec=c, mutation_scale=20)
            ax.add_patch(ar)
            
    ax.set_ylim([-5, 115])
    ax.yaxis.set_ticks(range(0, 120, 10))
    ax.yaxis.set_ticklabels(range(0, 120, 10))
    ax.invert_yaxis()
    ax.set_xlim([0, 110])
    ax.xaxis.set_ticks(xpos)
    ax.xaxis.set_ticklabels(x)
    ax.set_xlim([.5, len(xpos)+.5])
    ax.grid(True)
    ax.set_ylabel('Threshold (Hearing Level)')
    ax.set_xlabel('Frequency (Hz)')

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def proc_subject(db, SubjN):
    """
    the report must have a function named 'proc_subject' for the report 
    to show up on the edit subject page ie, to run it on individual subjects.
    In this case, the full path to the db and the subject number will be 
    passed to the function.
    """
    fh,ap = draw_page()

    af = fh.add_axes([.2, .3, .5*11/8.5, .5*8.5/11])
    af.axhspan(-5,20, fc='0.7', ec='None', alpha=0.5)

    #af.text(8,50,'V',horizontalalignment='center',verticalalignment='center', rotation=45,color='r',fontweight='bold', fontsize=14)
    #af.plot(8,50,marker='v',color='r')
    print (db)
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("""SELECT FName,LName,DOB,Gender,User_Audio_Date,User_Audio_Tester FROM Subjects WHERE SubjN == \'%s\'""" % SubjN)
    subject = c.fetchone()
    if subject is not None:

        ap.text(4.25, 1, "Psychoacoustics Lab",horizontalalignment='center', fontsize="x-large")
        ap.text(7.5, 1.5, "Tester: %s" % subject[5],horizontalalignment='right')
        ap.text(7.5, 1.7, "Date of Audiogram: %s" % subject[4],horizontalalignment='right')

        ap.text(1, 1.5, "Patient Name: %s %s" % (subject[0],subject[1]))
        ap.text(1, 1.7, "Date of Birth: %s" % subject[2])
        ap.text(1, 1.9, "Gender: %s" % subject[3])

        c.execute("""SELECT User_L125,User_L250,User_L500,User_L750,User_L1k,
                     User_L15,User_L2k,User_L3k,User_L4k,User_L6k,User_L8k FROM Subjects WHERE SubjN == \'%s\'""" % (SubjN))
        uservar_this = c.fetchone()
        left = []
        for var in uservar_this:
            if is_number(var):
                left.append(float(var))
            else:
                left.append(np.nan)
        plot_data(af,left,'left')

        c.execute("""SELECT User_R125,User_R250,User_R500,User_R750,User_R1k,
                     User_R15,User_R2k,User_R3k,User_R4k,User_R6k,User_R8k FROM Subjects WHERE SubjN == \'%s\'""" % (SubjN))
        uservar_this = c.fetchone()
        right = []
        for var in uservar_this:
            if is_number(var):
                right.append(float(var))
            else:
                right.append(np.nan)
        plot_data(af,right,'right')

        fh.show()

if __name__ == "__main__":
    db = sys.argv[1].strip("\"").strip("\'")
    SubjN = sys.argv[2]
    proc_subject(db, SubjN)

