# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join("..","src"))
import pal

if __name__ == "__main__":
    d = pal.dataview.from_csv("data/three.csv", dv="dv")
    v = d.view({'a':[],'b':[]})
    #d = Dataset("data/threebad.csv", dv="dv", subject=None)

    print v.treatments
    print v.mean
    #antb = fact_anova(d.rawdata, d.ivs)
    #antb = fact_anova(d.rawdata)
    # pretty print
    #for x in antb:
    #    a,b,c,d,e,f = x
    #    print "%s\t%.3f\t%d\t%.3f\t%.3f\t%.3f" % (a,b,c,d,e,f)
