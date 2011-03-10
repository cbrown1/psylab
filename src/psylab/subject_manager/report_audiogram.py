# -*- coding: utf-8 -*-

from matplotlib import pyplot as pp
import matplotlib.patches as mpp
from matplotlib.lines import Line2D
import numpy as np

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

ap.text(4.25, 1, "Psychoacoustics Lab",horizontalalignment='center')
ap.text(7.5, 1.5, "Today's Date: %s" % '2011-03-08',horizontalalignment='right')

ap.text(1, 1.5, "Patient Name: %s" % 'Joseph Smith')
ap.text(1, 1.7, "Date of Birth: %s" % '1970-12-31')
ap.text(1, 1.9, "Gender: %s" % 'Male')

ap.add_line(Line2D([1, 7.5],[3, 3],color='k',lw=2))

for i in np.arange(8.6,10.4,.4):
    ap.add_line(Line2D([5,7.5],[i,i],color='k',lw=1))
    

# Legend:
lx = 1.4
ly = 8.5

lbox = mpp.Rectangle((lx-.4, ly), 3.7, 1.48, facecolor="None", edgecolor="k", lw=1)
ap.add_patch(lbox)

ap.text(lx+2.4, ly+.4, "Right",horizontalalignment='center')
ap.text(lx+3., ly+.4, "Left", horizontalalignment='center')

ap.text(lx+2, ly+.8, "Air conduction - Unmasked",horizontalalignment='right')
ap.text(lx+2, ly+1.2, "No response",horizontalalignment='right')

ap.plot(lx+2.37,ly+.73, marker='o', ms=10, ls='None', mfc='None', mec='b', mew=3)
ap.plot(lx+2.97,ly+.73, marker='x', ms=10, ls='None', mfc='None', mec='r', mew=3)

ap.add_patch(mpp.FancyArrowPatch((lx+2.37,ly+1.13), (lx+2.27,ly+1.23), arrowstyle='->', lw=3, ec='b', mutation_scale=20))
ap.add_patch(mpp.FancyArrowPatch((lx+2.97,ly+1.13), (lx+3.07,ly+1.23), arrowstyle='->', lw=3, ec='r', mutation_scale=20))


def plot_data(ax, data, side):
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
        c = 'r'
        mp_nr_x = [0., .2]
        mp_nr_y = [0, 2.]
        m='x'
    else:
        c = 'b'
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

            
    ax.set_ylim([0, 110])
    ax.yaxis.set_ticks(range(0, 110, 10))
    ax.yaxis.set_ticklabels(range(0, 110, 10))
    ax.invert_yaxis()
    ax.set_xlim([0, 110])
    ax.xaxis.set_ticks(xpos)
    ax.xaxis.set_ticklabels(x)
    ax.set_xlim([.5, len(xpos)+.5])
    ax.grid(True)
    ax.set_ylabel('Threshold (Hearing Level)')
    ax.set_xlabel('Frequency (Hz)')

af = fh.add_axes([.2, .3, .5*11/8.5, .5*8.5/11])
af.axhspan(0,20, fc='0.7', ec='None', alpha=0.5)

#af.text(8,50,'V',horizontalalignment='center',verticalalignment='center', rotation=45,color='r',fontweight='bold', fontsize=14)
#af.plot(8,50,marker='v',color='r')

plot_data(af,[20, 25, 20, 30, 35, 65, 75, 90, 100,105,-50],'left')
plot_data(af,[40, 55, 60, 80, 90, 95, 105, 105, -70,-70,-60],'right')

fh.show()
