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

'''Provides views of your data
    
    Dataview allows you to easily extract subsets of a dataset to use for 
    plotting, analysis, etc.. The main class is DataSet, which loads your data
    into an ndarray. DataSetView allows you to pass a dictionary of variable 
    names as keys, and lists of levels as values, to view only those data. 
'''

import numpy as np
import csv
from itertools import product
from scipy.stats import nanmean
import pal.stats

class Dataset:
    """Representation of experimental data with one dependent variable.

    Attributes
    ----------
    data : ndarray
        Each axis represents a variable, and each coordinate along that
        axis represents a level in that variable.

    labels : tuple of tuple
        Label for each axis and coordinate on that axis.
        Of the form: ((axis_name_1, (coord_name_1, ..., coord_name_i)),
                      ...,
                      (axis_name_n, (coord_name_1, ..., coord_name_j)))

    dv : str
        Name of the dependent variable.
    """
    data = None
    dv = None
    ivs = None
    labels = None
    design = None
    index_from_var = None
    index_from_level = None
    comments = ""

    def view(self, var_dict=None, looks=None):
        return DatasetView(self, var_dict, looks)

    def anova_between(self):
        return pal.stats.anova.anova_between(self.data, self.ivs)
    
    def anova_within(self, looks=None):
        if looks == None:
            return pal.stats.anova.anova_within(self.data,
                                                factors=self.ivs)
        else:
            return pal.stats.anova.anova_within(self.data,
                                                looks_index=self.index_from_var[looks],
                                                factors=self.ivs)

    def index_names(self):
        return [(x,self.index_from_var[x]) for x in self.ivs] + [(self.dv, len(self.data.shape)-1)]

    def indices_from_vars(self, d):
        collapsedIndex = [[Ellipsis] for x in self.data.shape]
        for group in d:
            i = self.index_from_var[group]
            collapsedIndex[i] = sorted(self.index_from_level[(group,level)] for level in d[group])

        takeThisProduct = []
        maxlen = max(len(x) for x in collapsedIndex)
        for i in collapsedIndex:
            if i == Ellipsis:
                takeThisProduct.append([Ellipsis])
            else:
                takeThisProduct.append(i)
        indices = product(*takeThisProduct)
        return indices

    def indices_from_comparison(self, comparisons):
        indices = [(tuple(self.indices_from_vars(x)),
                    tuple(self.indices_from_vars(y))) for x,y in comparisons]
        return indices

#     def write_to_csv(self, csv_name):
#         def index_to_line(index):
#             pass # translate an index tuple to a line of variable names
#         writer = csv.writer(open(csv_name, "w"), delimiter=" ")
#         for index in product(*map(xrange, self.data.shape)):
#             writer.writerow(index_to_line(index))


def from_csv(csv_path, dv):
    ds = Dataset()

    file_data = csv.reader(open(csv_path))
    comments = ""

    # Get the first line of the .csv that isn't blank or commented, 
    # which is assumed to be a row of labels for each column.
    for row in file_data:
        if len(row)==0:
            comments += '\n'
        elif row[0].lstrip().find('#') != -1:
            comments += ','.join(row).lstrip(' #') + "\n"
        else:
            labels = tuple(x.strip().strip("'").strip('"') for x in row)
            break
    # (Now the file_data cursor should be pointed at the first substantive row
    # of the csv file, so if we iterate now, we'll just be getting data rows)

    dv_index = labels.index(dv)
    ivs = tuple(x for x in labels if x != dv)

    # Prepare a row for `np.rec.fromrecs`
    def format_row(row):
        row = [x.strip().strip("'").strip('"') for x in row if x is not dv]
        row[dv_index] = np.float64(row[dv_index])
        return tuple(row)

    # A temporary recarray for computing other values
    temp_array = np.rec.fromrecords(map(format_row, file_data), names=labels)

    # Compute index mappings
    index_from_var = {}
    index_from_level = {}
    shape = [0 for x in labels[:-1]]

    i = 0
    for v in ivs:
        index_from_var[v] = i
        j = 0
        unique = set(temp_array[v])
        for l in unique:
            index_from_level[(v,l)] = j
            j += 1
        shape[i] = len(unique)
        i += 1

    axis_from_var = dict([x[::-1] for x in index_from_var.iteritems()])

    treatments = {}
    for r in temp_array:
        key = tuple(r[v] for v in ivs)
        if key in treatments:
            treatments[key].append(r[dv])
        else:
            treatments[key] = [r[dv]]
    
    # Find the shape of the ndarray
    max_looks = max(map(len, treatments.values()))
    shape.append(max_looks)

    array = np.ones(shape) * np.nan

    proto_index = [0] * len(ivs)
    def treatment_to_index(t):
        index = proto_index
        i = 0
        for v in ivs:
            index[i] = index_from_level[(v,t[i])]
            i += 1
        return tuple(index)
            
    for t,vals in treatments.iteritems():
        index = treatment_to_index(t)
        i = 0
        for v in vals:
            array[index+(i,)] = v
            i += 1

    items = index_from_level.items()
    design_list = []

    for var in labels:
        t = var, tuple(l for i,l in sorted((i,l) for (v,l),i in items if v == var))
        if t[0] == dv:
            t = (t[0], None)
        design_list.append(t)

    ds = Dataset()
    ds.data = array
    ds.labels = tuple(design_list)
    ds.design = dict(design_list)
    ds.dv = dv
    ds.ivs = ivs
    ds.index_from_var = index_from_var
    ds.index_from_level = index_from_level
    ds.comments = comments

    return ds


class DatasetView:
    def __init__(self, ds, var_dict=None, looks=None):
        # Stats
        self.dataset = ds
        self.data = None
        self.treatments = None
        self.var_dict = var_dict

        self.mean = None
        self.sd = None
        self.se = None
        self.n = None

        if var_dict is None:
            self.treatments = np.array([str(x) for x in 
                                        product(*[ds.design[x] for x in ds.ivs])])
            var_dict = vs.design
        else:
            indexPrototype = [[Ellipsis] for x in ds.data.shape]
            for k in var_dict:
                indexPrototype[ds.index_from_var[k]] = var_dict[k]
            self.treatments = np.array([str(x) for x in
                                        product(*indexPrototype)])

        if looks != None:
            looks_index = ds.index_from_var[looks]
            if looks_index == 0: # No need to swap
                sh = ds.data.shape[:-1] + (1,)
                self.data = nanmean(ds.data, -1).reshape(sh)
            else:
                self.data = ds.data.swapaxes(0, looks_index)
                sh = self.data.shape[:-1] + (1,)
                self.data = nanmean(self.data, -1).reshape(sh)
                self.data = self.data.swapaxes(0, looks_index)
        else:
            sh = ds.data.shape[:-1] + (1,)
            self.data = nanmean(ds.data, -1).reshape(sh)

        self.n = np.ones(shape=self.treatments.shape)
        self.mean = np.ones(shape=self.treatments.shape)
        self.sd = np.ones(shape=self.treatments.shape)
        self.se = np.ones(shape=self.treatments.shape)

        def index_from_tuple(t):
            index = [Ellipsis] * len(self.data.shape)

            for i in xrange(len(ds.ivs)):
                var = ds.ivs[i]
                j = ds.index_from_var[var]
                if t[i] == Ellipsis:
                    index[j] = Ellipsis
                else:
                    index[j] = ds.index_from_level[(var,t[i])]
            return tuple(index)

        for i in xrange(len(self.treatments)):
            t = eval(self.treatments[i])
            j = index_from_tuple(t)
            jdata = np.array([x for x in self.data[j].flatten() if not np.isnan(x)])
            
            if looks is None:
                kdata = np.array([x for x in ds.data[j].flatten() if not np.isnan(x)])
                n = kdata.size
                sd = kdata.std()
            else:
                n = jdata.size
                sd = jdata.std()
            mean = jdata.mean()
            se = sd / np.sqrt(n)
            
            self.n[i] = n
            self.mean[i] = mean
            self.sd[i] = sd
            self.se[i] = se
