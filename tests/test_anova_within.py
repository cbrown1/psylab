# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join("..","src"))
import numpy as np
import psylab

if __name__ == "__main__":

    # F values taken from
    # http://davidmlane.com/hyperstat/within-subjects.html
    known_f = [33.0, 24.82, 3.00, np.nan, np.nan, np.nan, np.nan, np.nan]

    d = psylab.dataview.from_csv("data/hyperstat_2f_within.csv", dv="dv")
    an = psylab.stats.anova_within(d.data)

    print known_f
    print an.f
    #print psylab.stats.anova_table(an)
