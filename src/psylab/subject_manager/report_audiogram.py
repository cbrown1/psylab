# -*- coding: utf-8 -*-

from matplotlib import pyplot as pp

fh = pp.figure(figsize=(8.5, 11))

# page axis, to place text etc.
ap = fh.add_axes([0, 0, 1, 1])
ap.set_xticks([])
ap.set_yticks([])
for spine in ap.spines:
    ap.spines[spine].set_visible(False)
ap.set_xlim([0, 8.5]) # Page coordinates are
ap.set_ylim([0, 11])  # now in units of inches
ap.invert_yaxis()
ap.text(4.25, 1, "Psychoacoustics Lab",horizontalalignment='center')
ap.text(1, 1.5, "Patient Name: %s" % 'Joseph Smith')
ap.text(4.35, 1.5, "Date: %s" % '2011-03-08')
ap.text(1, 1.7, "Date of Birth: %s" % '1970-12-31')
ap.text(4.35, 1.7, "Sex: %s" % 'Male')

af = fh.add_axes([.2, .3, .5*11/8.5, .5*8.5/11])
af.axhspan(0,20, facecolor='0.5', alpha=0.5)
x = [125, 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000]
xpos = [1,2,3,4,5,6,7,8,9,10,11]
af.plot(xpos, [20, 25, 20, 30, 35, 65, 75, 90, 100, 105, 105],
        marker='o', ms=10, ls='None', mfc='None', mec='b', mew=3)

af.set_ylim([0, 110])
af.yaxis.set_ticks(range(0, 110, 10))
af.yaxis.set_ticklabels(range(0, 110, 10))
af.invert_yaxis()
af.xaxis.set_ticks(xpos)
af.xaxis.set_ticklabels(x)
af.set_xlim([.5, len(xpos)+.5])
af.grid(True)
af.set_ylabel('Threshold (Hearing Level)')
af.set_xlabel('Frequency (Hz)')

fh.show()
