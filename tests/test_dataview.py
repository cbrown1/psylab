# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join("..","src"))
import pal
import numpy as np

if __name__ == "__main__":

    ## View demo:

    # Read all data
    d = pal.dataview.from_csv("data/three.csv", dv="dv")
    # Create a view of the data where a = a1, and b = b1 | b2
    # This will give us a mean property with 2 values,
    # one for a1b1, one for a1b2
    v = d.view({'a':['a1'],'b':['b1','b2']})
    # The corresponding data pulled manually from the data file
    a1b1 = np.array((4.1, 4.3, 4.5, 3.8, 4.3, 4.8, 4.5, 5.0, 4.6, 5.0))
    a1b2 = np.array((4.6, 4.9, 4.2, 4.5, 4.8, 5.6, 5.8, 5.4, 6.1, 5.4))

    print np.mean(a1b1), np.mean(a1b2)
    print v.mean
