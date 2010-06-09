import sys
sys.path.append("..")

if __name__ == "__main__":
    from anova import fact_anova
    from dataset import Dataset
    d = Dataset("data/three.csv", dv="dv", subject=None)
    #d = Dataset("data/threebad.csv", dv="dv", subject=None)

    #antb = fact_anova(d.rawdata, d.ivs)
    antb = fact_anova(d.rawdata)
    # pretty print
    for x in antb:
        a,b,c,d,e,f = x
        print "%s\t%.3f\t%d\t%.3f\t%.3f\t%.3f" % (a,b,c,d,e,f)
