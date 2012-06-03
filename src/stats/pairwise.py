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

import numpy as np
from scipy import stats

def bonferroni(p,k):
    # Ref: http://books.google.com/books?id=3jpvrEhozGgC&pg=PA70
    return p*k

def sidak(p,k):
    # Ref: http://books.google.com/books?id=3jpvrEhozGgC&pg=PA70
    return 1.0 - (1.0 - p)**k

def pairwise_comparisons(data, comparisons, correction=None,
                     factors=None,
                     levels=None,
                     within=False):
    """Computes a table of pairwise comparisons.

    Parameters:
    -----------
    data : numpy.ndarray
        Representation of the experimental data (see, eg., anova_between).

    comparisons : list or tuple
        A list of pairs of the form `(ii,jj)`, where `ii` and `jj` are lists
        of advanced indices used to pull samples out of `data`.

    correction : function
        The correction function to control the family-wise error rate.
        Possible values include: None [default], bonferroni, sidak.

    factors : list or tuple
        String of human-readable factor names.

    Returns:
    --------
    result : list

    """


    if factors is None: #If factors aren't specified
        num_factors = len(data.shape) - 1
        if num_factors <= 26: # If the factor dimensions can be mapped to
                                 # letters of the alphabet...
            factors = [x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:num_factors]]
        else: # just give them indexed dummy names
            factors = tuple("F%s" % (i) for i in xrange(len(data.shape)-1))

    def samplename(indices):
        index = tuple(tuple(sorted(set(y))) for y in zip(*indices))

        name = []
        # This is broken if level names are actually passed
        for i in xrange(len(index)-1):
            case = index[i]
            if case[0] == Ellipsis:
                pass
            elif len(case) == 1:
                name.append("%s[%d]" % (factors[i], index[i][0]))
            else:
                if index[i] == tuple(xrange(index[i][0],index[i][-1]+1)):
                    name.append("%s[%d:%d]" %
                                (factors[i], index[i][0],index[i][-1]+1))
                else:
                    name.append("%s[%s]" %
                                (factors[i],
                                 (",".join(map(str, index[i])))))
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
