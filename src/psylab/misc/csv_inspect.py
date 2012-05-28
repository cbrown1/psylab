# -*- coding: utf-8 -*-

# Copyright (c) 2010 Christopher Brown
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
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# Comments and/or additions are welcome. Send e-mail to: cbrown1@pitt.edu.
#

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
