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
from scipy import stats

def bonferroni(p,k):
    # Ref: http://books.google.com/books?id=3jpvrEhozGgC&pg=PA70
    return p*k

def sidak(p,k):
    # Ref: http://books.google.com/books?id=3jpvrEhozGgC&pg=PA70
    return 1.0 - (1.0 - p)**k

def paired_diff_test(data, comparisons, correction=None,
                     factors=None,
                     levels=None,
                     within=False):
    """Computes a table of pairwise comparisons.

    Parameters:
    -----------
    data : numpy.ndarray
        Representation of the experimental data (see, eg.,  anova_between).

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

    if within:
        ttest = stats.ttest_rel(sample_a, sample_b)
    else:
        ttest = stats.ttest_ind(sample_a, sample_b)

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

        t,p = ttest(sample_a, sample_b)
        if correction = None:
            adjp = p
        else:
            adjp = correction(p,k)
        result.append((comp_str, t, adjp))
    return result
