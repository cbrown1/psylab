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
# along with Psylab.  If not, see <http://www.gnu.org/licenses/>.
#
# Bug reports, bug fixes, suggestions, enhancements, or other 
# contributions are welcome. Go to http://code.google.com/p/psylab/ 
# for more information and to contribute. Or send an e-mail to: 
# cbrown1@pitt.edu.
#

from collections import OrderedDict, Hashable
import numpy as np
from scipy import stats


def bonferroni(p,k):
    # Ref: http://books.google.com/books?id=3jpvrEhozGgC&pg=PA70
    return p*k


def sidak(p,k):
    # Ref: http://books.google.com/books?id=3jpvrEhozGgC&pg=PA70
    return 1.0 - (1.0 - p)**k


def pairwise_table(pairwise_data, decimals=4):
    """Generates a nicely formatted anova summary table

    Parameters:
    -----------
    pairwise_data : record array
        The output of the pairwise_comparisons function

    sig : int
        The number of decimals to display

    Returns:
    --------
    table : string
        A formatted summary table, with space-delimited columns
    """

    lengths = [10,10,10]

    fmt = "{{:.{:}f}}".format(decimals)
    for pair in pairwise_data:
        if len(pair[0]) > lengths[0]:
            lengths[0] = len(pair[0])
        if len(fmt.format(pair[1])) > lengths[1]:
            lengths[1] = len(fmt.format(pair[1]))
        if len(fmt.format(pair[2])) > lengths[2]:
            lengths[2] = len(fmt.format(pair[2]))

    fmt = []
    fmt.append("{{:>{:}}}".format(lengths[0]))
    fmt.append("{{:>{:}}}".format(lengths[1]))
    fmt.append("{{:>{:}}}".format(lengths[2]))

    fmt_line = "{}: {}; {}\n".format(fmt[0], fmt[1], fmt[2])

    output = fmt_line.format("Comparison", "Mean Diff", "p")

    fmt = []
    fmt.append("{{:>{:}}}".format(lengths[0]))
    fmt.append("{{:>{:}.{:}f}}".format(lengths[1], decimals))
    fmt.append("{{:>{:}.{:}f}}".format(lengths[2], decimals))

    fmt_line = "{}: {}; {}{}\n".format(fmt[0], fmt[1], fmt[2], "{}")

    for comparison, mean_diff, p in pairwise_data:
        if p < .001:
            sig = "  ***"
        elif p < .01:
            sig = "  **"
        elif p < .05:
            sig += "  *"
        else:
            sig = " "
        output += fmt_line.format(comparison, mean_diff, p, sig)

    return output


def pairwise_comparisons(data, 
                         comparisons,
                         var_dict=None,
                         correction=None,
                         within=False):
    """Computes pairwise comparisons

    Parameters:
    -----------
    data : numpy.ndarray
        Representation of the experimental data (see, eg., anova_between).

    comparisons : list or tuple
        A list of pairs of the form `(ii,jj)`, where `ii` and `jj` are lists
        of advanced indices used to pull samples out of `data`. You can 
        generate this list using dataview.indices_from_comparison

    var_dict : dict
        A dict with var names as keys, and lists of var levels as vals.
        (ie., dataview.var_dict)

    correction : function
        The correction function to control the family-wise error rate.
        Possible values include: None [default], bonferroni, sidak.

    within : bool
        True if the comparisons are within subjects, otherwise False

    Returns:
    --------
    result : list

    """


    if var_dict is None: 
        num_factors = len(data.shape) - 1
        if num_factors <= 26: # If the factor dimensions can be mapped to
                                 # letters of the alphabet...
            factors = [x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:num_factors]]
        else: # just give them indexed dummy names
            factors = tuple("F{}".format(i) for i in range(len(data.shape)-1))

        var_dict = OrderedDict()
        for ii in range(len(factors)):
            this_levels = []
            for levels in range(data.shape[ii]):
                    this_levels.append("{}{:}".format(factors[ii],levels))
            var_dict[factors[ii]] = this_levels


    def orig_samplename(indices):
        index = tuple(tuple(sorted(set(y))) for y in zip(*indices) if not isinstance(y[0], slice) )

        name = []
        # This is broken if level names are actually passed
        for i in range(len(index)-1):
            case = index[i]
            if  len(case) == 1:
                name.append("{}[{:}]".format(factors[i], index[i][0]))
            else:
                if index[i] == tuple(range(index[i][0],index[i][-1]+1)):
                    name.append("{}[{:}:{:}]".format(factors[i], index[i][0],index[i][-1]+1))
                else:
                    name.append("{}[{}]".format(factors[i],
                                 (",".join(map(str, index[i])))))
        return ",".join(name)

    def samplename(indices):
        index = tuple(tuple(sorted(set(y))) for y in zip(*indices) if not isinstance(y[0], slice) )

        name = []
        for i in range(len(index)):
            cases = index[i]
            var = list(var_dict.keys())[i]
            levels = []
            for case in cases:
                levels.append(var_dict[var][case])
            name.append("{}[{:}]".format(var, ",".join(levels)))
        return ",".join(name)

    k = len(comparisons)
    result = []
    for x in comparisons:
        ii,jj = x
        comp_str = " -- ".join(map(samplename, (ii,jj)))

        sample_a = []
        for i in ii:
            sample_a.extend(data[i].flatten())
        sample_a = np.array(sample_a)

        sample_b = []
        for j in jj:
            sample_b.extend(data[j].flatten())
        sample_b = np.array(sample_b)

        if within:
            t,p = stats.ttest_rel(sample_a, sample_b)
        else:
            t,p = stats.ttest_ind(sample_a, sample_b)


        #t,p = ttest(sample_a, sample_b)
        if correction == None:
            adjp = p
        else:
            adjp = correction(p,k)
        result.append((comp_str, t, adjp))
    return result
