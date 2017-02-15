# -*- coding: utf-8 -*-

# Copyright (c) 2010-2012 Christopher Brown
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
# along with Psylab.  If not, see <http://www.gnu.org/licenses/>.
#
# Bug reports, bug fixes, suggestions, enhancements, or other 
# contributions are welcome. Go to http://code.google.com/p/psylab/ 
# for more information and to contribute. Or send an e-mail to: 
# cbrown1@pitt.edu.
#

'''Provides views of your data

    Dataview allows you to easily extract subsets of a dataset to use for
    plotting, analysis, etc.. The main class is DataSet, which loads your data
    into an ndarray. DataSetView allows you to pass a dictionary of variable
    names as keys, and lists of levels as values, to view only those data.


'''

import numpy as np
import csv
import codecs
from itertools import product
from numpy import nanmean, nanstd
import psylab.stats

class Dataset:
    """Representation of a set of data with one dependent variable.

    Attributes
    ----------
    data : ndarray
        Each axis represents a variable, and each coordinate along that
        axis represents a level of that variable. So, the data object
        is a fully factorialized representation. nan's are used when
        treatments contain no data.

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

    def anova_between(self):
        return psylab.stats.anova.anova_between(self.data, self.ivs)

    def anova_within(self, looks=None):
        if looks == None:
            return psylab.stats.anova.anova_within(self.data,
                                                factors=self.ivs)
        else:
            return psylab.stats.anova.anova_within(self.data,
                                                looks_index=self.index_from_var[looks],
                                                factors=self.ivs)

    def index_names(self):
        return [(x,self.index_from_var[x]) for x in self.ivs] + [(self.dv, len(self.data.shape)-1)]

    def indices_from_vars(self, d):
        """Takes a dict in which keys are [str] var names and vals are lists of [str] levels
        """
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

    def from_var_dict(self, var_dict):
        """Creates a new Dataset from a parent Dataset and a dictionary of var
        to level mappings. We assume the `dv` is the same.

        Parameters
        ----------
        var_dict : dict

        Returns
        -------
        ds : Dataset
        """

        # Initialize the Dataset we will flesh out and return
        ds = Dataset()

        labels = []  # Initialize what will be the `labels` attribute for `ds`
        for var,lvs in self.labels:
            if var == self.dv:
                labels.append((var,None))
            elif var in var_dict:
                if var_dict[var] == []: # var -> [] is shorthand for "all levels"
                    var_dict[var] = lvs  # fix up var_dict for later assignment
                    labels.append((var,lvs))
                else:
                    labels.append((var,tuple(var_dict[var])))
        labels = tuple(labels)

        index_from_var = {}
        index_from_level = {}

        # Compute new indexing dicts for `ds`
        i = 0
        for v,lvls in labels[:-1]: # last axis is `dv`, so we ignore it here
            index_from_var[v] = i
            j = 0
            for l in lvls:
                index_from_level[(v,l)] = j
                j += 1
            i += 1
        index_from_var[self.dv] = i  # `i` was incremented before the loop
                                     # terminated, so it should point to
                                     # the last axis, as desired.

        ivs = tuple(v for v,l in labels[:-1] if v in var_dict)

        # How many data points will be extracted based on vars
        size = 0
        # We can't just do `self.data.size` because in most cases we'll just
        # want a proper subset of the values in `self.data`.
        for i in self.indices_from_vars(var_dict):
            size += self.data[i].size

        # How large our dv should be to fit each value.
        # This is determined by (size of our new array)/(product of all desired non-dv axes)
        dv_size = size / np.product([len(l) for v,l in labels if v in var_dict and v != self.dv])

        shape = tuple(len(lvs) for var,lvs in labels[:-1] if var in var_dict) + (dv_size,)
        data = np.ones(shape)

        ds.data = data
        ds.labels = labels
        ds.ivs = ivs
        ds.index_from_level = index_from_level
        ds.index_from_var = index_from_var
        ds.design = dict(labels)
        ds.dv = self.dv

        for t in product(*[l for v,l in labels[:-1]]):
            z = zip(ivs,t)

            i = [Ellipsis] * len(ds.data.shape)
            j = [Ellipsis] * len(self.data.shape)
            for v,l in z:
                i[ds.index_from_var[v]] = ds.index_from_level[(v,l)]
                j[self.index_from_var[v]] = self.index_from_level[(v,l)]
            ds.data[i] = self.data[j].flatten()

        return ds

    def view(self, var_dict=None, looks=None):
        if var_dict == None:
            var_dict1 = None
        else:
            var_dict1 = var_dict.copy()
            if (looks != None) and (looks  not in var_dict1):
                var_dict1[looks] = []
        v1 = DatasetView(self, var_dict1, looks)
        d = v1.as_dataset().from_var_dict(var_dict)
        v2 = DatasetView(d, var_dict)
        
        return v2


def from_csv(csv_path, dv, ivs=None):
    '''Create a Datset object from a csv file

        The dv variable is expected to be numeric, the levels of all other
        variables are treated as strings. in cases where there are many
        levels of many variables but you aren't interested in all of them,
        you can pass a list of variables that you are interested in, and
        only those will be used.

        Header lines (lines at the beginning of the file that begin with '#')
        are skipped (the text is stored in 'comments').
    '''

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
    if ivs == None:
        ivs = tuple(x for x in labels if x != dv)

    # Prepare a row for `np.rec.fromrecs`
    def format_row(row):
        row = [x.strip().strip("'").strip('"') for x in row if x is not dv]
        row[dv_index] = np.float32(row[dv_index])
        return tuple(row)

    # A temporary recarray for computing other values
    temp_array = np.rec.fromrecords(map(format_row, file_data), names=labels)

    # Compute index mappings
    index_from_var = {}
    index_from_level = {}
    shape = [0 for x in [y for y in labels[:-1] if y in ivs]]

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
    ds.labels = tuple((v,l) for v,l in design_list if v in ivs or v == dv)
    ds.design = dict(design_list)
    ds.dv = dv
    ds.ivs = ivs
    ds.index_from_var = index_from_var
    ds.index_from_level = index_from_level
    ds.comments = comments

    return ds

def from_arrays(labels=None, *args):
    """Create a Datset object from a number of 1-dimensional arrays

        The first argument is a tuple of strings that represent the
        names of each variable. The last string should be the name of the
        dependent variable.

        >>> import numpy as np
        >>> import psylab
        >>> a = np.array("a1 a1 a2 a2".split(" "))
        >>> b = np.array("b1 b2 b1 b2".split(" "))
        >>> dv = np.array([1,2,3,4])
        >>> d = psylab.dataview.from_arrays(("A", "B", "dv"), a, b, dv)
        >>> d.labels
        (('A', ('a1', 'a2')), ('B', ('b1', 'b2')), ('dv', None))
        >>> d.data
        array([[[ 1.],
                [ 2.]],
        <BLANKLINE>
               [[ 3.],
                [ 4.]]])
    """
    assert len(args) > 2
    assert np.all([type(x) == type(np.ones(1)) for x in args])

    if labels == None:
        num_vars = len(args) - 1
        if num_vars <= 26: # If the factor dimensions can be mapped to
                              # letters of the alphabet...
            labels = [x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:num_factors]]
        else: # just give them indexed dummy names
            labels = tuple("F%s" % (i) for i in xrange(num_vars))
        dv = "dv"
        labels.append(dv)
    else:
        dv = labels[-1]

    ds = Dataset()

    comments = ""

    ivs = labels[:-1]

    # A temporary recarray for computing other values
    temp_array = np.rec.fromrecords(zip(*args), names=tuple(labels))

    # Compute index mappings
    index_from_var = {}
    index_from_level = {}
    shape = [0 for x in [y for y in labels[:-1] if y in ivs]]

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
    ds.labels = tuple((v,l) for v,l in design_list if v in ivs or v == dv)
    ds.design = dict(design_list)
    ds.dv = dv
    ds.ivs = ivs
    ds.index_from_var = index_from_var
    ds.index_from_level = index_from_level
    ds.comments = comments

    return ds

class DatasetView:
    '''Allows you to view only the specified variables and levels.

        The var_dict should have variable names as keys, and lists of
        levels as vals. You can also specify a 'looks' variable, which is
        useful in the 'multiple looks' situaion (for example, when the same
        subject generates more than one data point in a treatment, the
        variable that codes for subject would be the looks variable).
    '''

    def __init__(self, ds, var_dict=None, looks=None):
        # Stats
        self.dataset = None
        self.data = None
        self.treatments = None
        self.vars = []
        self.var_dict = var_dict
        self.looks = looks
        self.dv = None

        self.mean = None
        self.sd = None
        self.se = None
        self.n = None

        # Since `[]` values of `var_dict` are shorthand for "all levels",
        # expand them using the level information in `ds`
        for v in var_dict:
            if var_dict[v] == []:
                var_dict[v] = ds.design[v]

        dv = ds.dv
        
        labels = []
        for (v,l) in ds.labels:
            if v in var_dict:
                self.vars.append(v)
                labels.append((v,tuple(var_dict[v])))
            elif v == looks:
                labels.append((v,ds.design[v]))
            elif v == ds.dv:
                labels.append((v,None))
        labels = tuple(labels)

        treatments = {}
        for t in product(*[zip((v,)*len(l), [[x] for x in l])
                           for (v,l) in labels[:-1]]):
            dt = dict(t)
            t = tuple(l[0] for (v,l) in t) # Unbox levels coordinate,
                                           # make suitable for hashing
            indices = ds.indices_from_vars(dt)
            idata = np.array([x for x in np.array([ds.data[i]
                                                   for i in indices]).flatten()
                              if np.isfinite(x)])
            treatments[t] = idata


        dv_size = max(map(len, treatments.values()))

        shape = tuple(len(l) for (v,l) in labels[:-1]) + (dv_size,)

        data = np.ones(shape) * np.nan


        # Populate indexing dictionaries.
        # Will be recomputed after axis switches.
        index_from_var = {}
        index_from_level = {}
        i = 0
        for (v,l) in labels:
            if v == dv:
                index_from_var[v] = i
            else:
                index_from_var[v] = i
                j = 0
                for lvl in l:
                    index_from_level[(v,lvl)] = j
                    j += 1
            i += 1
            

        # Update values of `data`
        for t,d in treatments.iteritems():
            i = tuple(index_from_level[(x,y)] for (x,y) in
                      zip(tuple(tuple(v for (v,l) in labels[:-1])), t))
            j = 0
            for x in d:
                data[i + (j,)] = x
                j += 1


        # Take mean wrt to `looks` variable
        if looks != None:
            if looks in var_dict:
                # ...then we don't need to recompute indexing
                data = nanmean(data, index_from_var[dv]).reshape(shape[:-1] + (1,))
            else:
                j = index_from_var[looks] # index we are deleting
                index_from_var.pop(looks)

                for v,i in index_from_var.iteritems():
                    if j <= index_from_var[v]:
                        index_from_var[v] -= 1

                data = nanmean(data, -1).reshape(shape[:-1] + (1,))
                dv_size = len(ds.design[looks])
                shape = tuple(len(l) for (v,l) in labels if v in var_dict) + (dv_size,)
                data = data.swapaxes(-2, j).reshape(shape)
                labels = tuple((v,l) for (v,l) in labels if v != looks)

        self.dataset = Dataset()
        self.dataset.data = data
        self.dataset.dv = dv
        self.dataset.factors = tuple(v for (v,l) in labels[:-1])
        self.dataset.ivs = tuple(x for x in self.dataset.factors if x != self.dataset.dv)
        self.dataset.labels = labels
        self.dataset.design = dict(labels)
        self.dataset.index_from_var = index_from_var
        self.dataset.index_from_level = index_from_level

        self.data = data
        self.treatments = np.array([str(x) for x in
                                   product(*[l for (v,l) in
                                                  labels[:-1]])])
        self.n = np.ones(self.treatments.shape)
        self.mean = np.ones(self.treatments.shape)
        self.sd = np.ones(self.treatments.shape)
        self.se = np.ones(self.treatments.shape)

        self.var_dict = var_dict
        self.looks = looks

        for i in xrange(self.treatments.size):
            t = self.treatments[i]
            # print "DEBUG:", self.dataset.ivs
            # print "DEBUG:", eval(t)
            # print "DEBUG:", zip(self.dataset.ivs, eval(t))
            index = tuple(self.dataset.index_from_level[(v,l)] for
                          (v,l) in zip(self.dataset.ivs, eval(t)))
                          
            index = index + (Ellipsis,)
            loop_data = self.data[index]
            

            self.n[i] = len(tuple(x for x in loop_data if np.isfinite(x)))
            self.mean[i] = nanmean(loop_data)
            if loop_data.size == 1:
                # for n == 1, std should be 0
                self.sd[i] = 0.0
            else:
                self.sd[i] = nanstd(loop_data)
            self.se[i] = self.sd[i] / np.sqrt(self.n[i])

        self.stats = np.rec.fromrecords(zip(tuple("|".join(eval(t)) for
                                                  t in self.treatments),
                                            self.n,
                                            self.mean,
                                            self.sd,
                                            self.se),
                                        names="treatment,n,mean,sd,se")

    def as_dataset(self):
        return self.dataset.from_var_dict(self.var_dict)

    def levels(self, var):
        '''Returns an array of codes for a given variable name

            This is a convenience function to return an array of
            labels that is the same length as the properties 'mean,'
            'n,' etc. This is useful, eg., when plotting, to easily
            generate axis labels.
        '''
        return np.array([eval(t)[self.dataset.index_from_var[var]] for t in self.treatments])
    
    def to_csv(self, filename, data="mean", decimal_places=2, write_nan=False, append=False):
        """Writes data to the specified filename in csv format.

            data can be one of "mean" [default], "sd", "se", or "n".
            Careful! default is append=False, which overwrites output file!
            if append==True, no header data will be written.
        """

        if data=="mean":
            data = self.mean
        elif data=="sd":
            data = self.sd
        elif data=="se":
            data = self.se
        elif data=="n":
            data = self.n
            
        if append:
            mode = 'a'
        else:
            mode = 'w'

        fmt = u"%" + u"1.%if\n" % decimal_places

        f = codecs.open(filename, encoding='utf-8', mode=mode)
        if not append:
            # Header:
            f.write( unicode( ",".join((",".join(self.vars),self.dataset.dv)) ) + u"\n" )
        # Data:
        for i in range(len(self.mean)):
            if write_nan or not np.isnan(self.mean[i]):
                f.write( unicode( ",".join((",".join(eval(self.treatments[i])), fmt % data[i])) ) )
        f.close()

