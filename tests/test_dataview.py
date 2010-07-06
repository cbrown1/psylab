# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join("..","src"))
import pal
import numpy as np

if __name__ == "__main__":

    print "Dataset demo [get all data]:"

    d = pal.dataview.from_csv("data/small_2x3.csv", dv="score")

    print "Independent variables:",
    print d.ivs
    print "Design (the last dim is the number of scores in each treatment):"
    print d.data.shape
    print "A dict with variable names as keys, and tuples of level names as vals:"
    print d.design
    print "data:"
    print d.data


    print ""
    print "Dataset demo [get only 1 variable]:"

    # Now, specify a list of IV's to use (in this case, only 1: 'size')
    d = pal.dataview.from_csv("data/small_2x3.csv", "score", ['size'])

    print "Independent variables:",
    print d.ivs
    print "data:"
    print d.data


    print ""
    print "DatasetView demo [get specified variable levels]:"

    # Read all data
    d = pal.dataview.from_csv("data/three.csv", dv="dv")
    # Create a view of the data where a = a1, and b = b1 | b2
    # This will give us a mean property with 2 values,
    # one for all scores in a1b1, one for scores in a1b2
    v = d.view({'a':['a1'],'b':['b1','b2']})
    # The corresponding data pulled manually from the data file
    a1b1 = np.array((4.1, 4.3, 4.5, 3.8, 4.3, 4.8, 4.5, 5.0, 4.6, 5.0))
    a1b2 = np.array((4.6, 4.9, 4.2, 4.5, 4.8, 5.6, 5.8, 5.4, 6.1, 5.4))

    print "Precomputed means: ",
    print [np.mean(a1b1), np.mean(a1b2)]
    print "DatasetView means: ",
    print v.mean


    print ""
    print "DatasetView demo [Using 'looks' variable]:"

    # Read all data
    d = pal.dataview.from_csv("data/1f_within.csv", dv="dv")
    print "Variables in dataset: ",
    print d.ivs
    # First, don't specify a looks variable
    # Use empty list to get all levels of 'a'
    v1 = d.view({'a':[]})
    # Same thing, with looks
    v2 = d.view({'a':[]},looks='s')

    print "Treatment means are the same:"
    print v1.mean
    print v2.mean
    print "But n's are different, because 3 scores per subject, per treatment:"
    print v1.n
    print v2.n
    print "And so are se's:"
    print v1.se
    print v2.se


