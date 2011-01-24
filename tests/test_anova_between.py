# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join("..","src"))
import numpy as np
import psylab

if __name__ == "__main__":

    # F values taken from
    # http://davidmlane.com/hyperstat/factorial_ANOVA.html
    known_f = [273.038, 535.154, 246.416, 141.543, 55.290, 60.314, 7.891, np.nan, np.nan]

    d = psylab.dataview.from_csv("data/hyperstat_3f_between.csv", dv="dv")
    an = psylab.stats.anova_between(d.data)

    print known_f
    print an.f
    #print psylab.stats.anova_table(an)
