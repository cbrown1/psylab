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

import numpy as np
import csv
from itertools import product
from pal import nanmean
import pal.stats

class Dataset:
    def __init__(self, csv_path, dv, subject):
        self.design = {}
        self.group_indices = {}
        self.level_indices = {}
        self.ivs = None
        self.dv = dv
        self.subject = subject
        self.rawdata = None
        self.data = None

        # Get the first line of the .csv containing experimental data, which is
        # assumed to be a row of labels for each column.
        file_data = csv.reader(open(csv_path))
        csv_labels = file_data.next()

        tmparr = np.rec.fromrecords([tuple(x) for x in file_data],
                                    names=csv_labels)

        self.ivs = [x for x in csv_labels if x != dv]

        # Characterize the semantic structure of the experiment
        for v in self.ivs:
            self.design[v] = []
            for entry in tmparr[v]:
                if entry not in self.design[v]:
                    self.design[v].append(entry)

        # Compute mappings from:
        #     Treatment groups to indices (`group_indices`)
        #     Levels within groups to indices (`level_indices`)
        i = 0
        for g in self.ivs:
            self.group_indices[g] = i
            i += 1

            j = 0
            for l in self.design[g]:
                self.level_indices[(g,l)] = j
                j += 1

        treatments = tuple(product(*tuple(self.design[x] for x in self.ivs)))

        # Read data from .csv and partition up to repeated measures
        partitions = {}
        for t in tmparr:
            tk = tuple([t[n] for n in self.ivs])
            if tk not in partitions:
                partitions[tk] = [np.float64(t[dv])]
            else:
                partitions[tk] = partitions[tk] + [np.float64(t[dv])]

        newshape = [len(set(tmparr[n])) for n in tmparr.dtype.names if n != dv]
        newshape.append(max([len(x) for x in partitions.values()]))
        newshape = tuple(newshape)

        self.rawdata = np.zeros(shape=newshape) * np.nan

        for k in partitions:
            gk = tuple(zip(self.ivs, k))

            index = tuple([self.level_indices[k0] for k0 in gk])
            index = [Ellipsis for dimension in self.rawdata.shape]
            for k0 in gk:
                index[self.group_indices[k0[0]]] = self.level_indices[k0]
            index = tuple(index)

            for i in xrange(len(partitions[k])):
                self.rawdata[index][i] = partitions[k][i]

        tmp = np.ones(shape=self.rawdata.shape)
        
        # Generate the keys that will let us extract the last dimensions.
        # i.e., for an array of shape: 
        #     (a_1, ... a_(k-1), a_k),
        # we should get all possible tuples of the shape:
        #     (b_1, ..., b_(k-1), Ellipsis)
        # Where b_1 is in range(a_1),
        #       b_2 is in range(a_2),
        #         ...
        #       b_(k-1) is in range(a_(k-1))
        keys = [x for x in apply(product,
                                 map(range,
                                     self.rawdata.shape[:-1]) + [[Ellipsis]])]

        newshape = self.rawdata.shape[:-1] + (1,)
        self.data = np.ones(shape=newshape)
        for k in keys:
            k2 = k[:-1] + (0,)
            self.data[k2] = nanmean(self.rawdata[k])

    def view(self, var_dict):
        t = [Ellipsis for i in self.data.shape]
        for var in var_dict:
            i = self.group_indices[var]
            k = tuple([self.level_indices[(var,x)] for x in var_dict[var]])
            t[i] = k
        t = tuple(t)

        # Account for fact that the advanced index:
        #   ((0,1),(0,1,2),(0,1))
        # is not equivalent to the advanced index:
        #   (Ellipsis,Ellipsis,Ellipsis)
        def fixtuple(t):
            fixed = []
            for i in xrange(len(t)):
                if t[i] is Ellipsis:
                    fixed.append(Ellipsis)
                elif len(t[i]) == self.data.shape[i]:
                    fixed.append(Ellipsis)
                else:
                    fixed.append(t[i])
            return tuple(fixed)

        return self.data[fixtuple(t)]

    def anova_between(self):
        return pal.stats.anova.anova_between(self.rawdata, self.ivs)
    
    def anova_within(self):
        if self.subject == None:
            return pal.stats.anova.anova_within(self.rawdata,
                                                factors=self.ivs)            
        else:
            return pal.stats.anova.anova_within(self.rawdata,
                                                subject_index=self.group_indices[self.subject],
                                                factors=self.ivs)

    def index_names(self):
        return [(x,self.group_indices[x]) for x in self.ivs] + [(self.dv, len(self.rawdata.shape)-1)]

    def pairwise(self, comparisons):
        def indices_from_dict(d):
            collapsedIndex = [[Ellipsis] for x in self.rawdata.shape]
            for group in d:
                i = self.group_indices[group]
                collapsedIndex[i] = sorted(self.level_indices[(group,level)] for level in d[group])

            takeThisProduct = []
            maxlen = max(len(x) for x in collapsedIndex)
            for i in collapsedIndex:
                if i == Ellipsis:
                    takeThisProduct.append([Ellipsis])
                else:
                    takeThisProduct.append(i)
            indices = product(*takeThisProduct)
            return indices

        indices = [(tuple(indices_from_dict(x)), tuple(indices_from_dict(y))) for x,y in comparisons]
        return pal.stats.paired_diff_test(self.rawdata, indices, factors=self.ivs)

class DatasetView:
    def __init__(self, dat, vars=None):
        # Stats
        self.data = None
        self.treatments = None

        self.mean = None
        self.sd = None
        self.se = None
        self.n = None

        # Extract data we care about, as indicated by vars
        # This breaks indexing in a way that is a huge pain
        if vars is None:
            self.data = dat.data
            self.treatments = np.array([str(x) for x in 
                                        product(*[dat.design[x] for x in dat.ivs])])
            vars = dat.design
        else:
            self.data = dat.view(vars)
            self.treatments = np.array([str(x) for x in
                                        product(*vars.values())])

        self.n = np.ones(shape=self.treatments.shape)
        self.mean = np.ones(shape=self.treatments.shape)
        self.sd = np.ones(shape=self.treatments.shape)
        self.se = np.ones(shape=self.treatments.shape)

        def index_from_tuple(t):
            index = [Ellipsis] * len(self.data.shape)

            for i in xrange(len(dat.ivs)):
                group = dat.ivs[i]
                j = dat.group_indices[group]
                index[j] = dat.level_indices[(group,t[i])]
            return tuple(index)

        for i in xrange(len(self.treatments)):
            t = eval(self.treatments[i])
            j = index_from_tuple(t)
            jdata = np.array([x for x in dat.data[j].flatten() if not np.isnan(x)])
            print "jdata",jdata

            n = len(jdata)
            mean = jdata.mean()
            sd = jdata.std()
            se = sd / np.sqrt(n)
            
            self.n[i] = n
            self.mean[i] = mean
            self.sd[i] = sd
            self.se[i] = se
