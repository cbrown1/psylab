#!/usr/bin/env python

import csv
import numpy as np

def csv_inspect(csv_path, vars=None):
    if vars == None: # We just want a list of the experiment's variables
        f = csv.reader(open(csv_path))
        labels = f.next()
        return labels
    elif type(vars) == type("") or (type(vars) == type([]) and len(vars) == 1): # One var specified for level info
        if type(vars) == type([]):
            vars = vars[0]
        r = csv.reader(open(csv_path))
        n = ",".join(r.next())
        arr = np.rec.fromrecords([tuple(x) for x in r], names=n)
        levels = list(set(arr[vars]))
        return levels
    else: # We have a list of vars specified
        r = csv.reader(open(csv_path))
        n = ",".join(r.next())
        arr = np.rec.fromrecords([tuple(x) for x in r], names=n)

        def level(var):
            return list(set(arr[var]))

        d = {}
        for v in vars:
            d[v] = level(v)

        return d

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        sys.stdout.write("Specify args\n")
    elif len(sys.argv) == 2:
        print (str(inspect(sys.argv[1])))
    elif len(sys.argv) == 3:
        print (str(inspect(sys.argv[1], sys.argv[2])))
    else:
        print (str(inspect(sys.argv[1], vars=sys.argv[2:])))
