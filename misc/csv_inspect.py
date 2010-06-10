# -*- coding: utf-8 -*-

# Copyright (c) 2010 Christopher Brown and Joseph Ranweiler; 
# All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
#    * Redistributions of source code must retain the above copyright 
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright 
#      notice, this list of conditions and the following disclaimer in 
#      the documentation and/or other materials provided with the distribution
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
#
# Comments and/or additions are welcome (send e-mail to: c-b@asu.edu).
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
