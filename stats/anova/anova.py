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
from itertools import combinations, product
from pal.nan import product as nanproduct

def anova_between(data, factors=None):
    """Performs analysis of variance for any number of factors.
    
    Parameters:
    -----------
    data : ndarray
        Representation of the experimental data as a multi-dimensional array.

        This can be thought of as a generalization of the textbook table used
        to present the data in two-factor anovas.

        For an experiment with N factors, with R the maximum number of
        repetitions, then the first N dimensions should determine a treatment--
        a combination of factor levels--and the last dimension should be large
        enough to contain as many repetitions as were recorded, thus of size R.

        Suppose an experiment had factors A, B, and C, each with two levels.
        A := A1, A2
        B := B1, B2
        C := C1, C2
        Suppose that, for each treatment, 4 measurements were taken, so R = 4.
        
        Then it is the case that data.shape == (2,2,2,4).

        In other words, the last dimension must be the "repeated y" dimension.

    factors : list or tuple
        String of human-readable factor names.

    Returns:
    --------
    anova_table : dict
        An anova table
    """

    n = {}
    ss = {}
    df = {}
    ms = {}
    f = {}
    p = {}

    n["total"] = len(data.flatten())

    if factors is None: #If factors aren't specified
        num_factors = len(data.shape) - 1
        if num_factors <= 26: # If the factor dimensions can be mapped to
                                 # letters of the alphabet...
            factors = [x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:num_factors]]
        else: # just give them indexed dummy names
            factors = tuple("F%s" % (i) for i in xrange(len(data.shape)-1))

    assert "error" not in factors
    assert "total" not in factors

    def ss_indices(s):
        product_to_take = []
        # Considering each dimension...
        for i in xrange(len(data.shape)-1):
            if factors[i] in s: #...if this is a specified factor,
                                # then we care about each level...
                product_to_take.append(range(data.shape[i]))
            else: #We don't care about the levels, so,
                product_to_take.append([Ellipsis])
        product_to_take.append([Ellipsis])
        return product(*product_to_take)

    # Find all treatment combinations
    sources = []
    for i in xrange(1, 1+len(factors)):
        sources.extend(tuple(combinations(factors, i)))

    # Compute the interaction terms for each source
    srcs_to_inter = {}
    for s in sources:
        inter = []
        for x in sources:
            if set(x) < set(s):
                inter.append(x)
        srcs_to_inter[s] = inter

    for i in xrange(len(factors)):
        df[factors[i]] = data.shape[i] - 1

    cm = np.nansum(data.flatten())**2 / n["total"]

    for s in sources:
        # Compute the sum of squares
        squares = 0
        for i in ss_indices(s):
            squares += np.nansum(data[i].flatten())**2 / len(data[i].flatten())

        # Uncorrected SS that includes interaction effects
        unc = squares - cm

        # Compute correction term from interactions
        if len(s) > 1:
            correction = np.nansum(tuple(ss[x] for x in srcs_to_inter[s]))
        else:
            correction = 0

        ss[s] = unc - correction

        if s not in df:
            df[s] = nanproduct(tuple(df[z] for z in s))

        ms[s] = ss[s] / df[s]


    ss["total"] = np.nansum(data.flatten()**2) - cm
    ss["error"] = ss["total"] - np.nansum(tuple(ss[s] for s in sources))
    df["error"] = n["total"] - nanproduct(data.shape[:-1])
    df["total"] = df["error"]
    ms["error"] = ss["error"] / df["error"]

    for s in sources:
        f[s] = ms[s] / ms["error"]
        p[s] = 1 - stats.f.cdf(f[s], df[s], df["error"])
        df["total"] += df[s]

    anova_table = []
    for s in sources:
        anova_table.append(("*".join(s),ss[s],df[s],ms[s],f[s],p[s]))
    anova_table.append(("error",
                        ss["error"],
                        df["error"],
                        ms["error"],
                        np.nan, np.nan))
    anova_table.append(("total", 
                        ss["total"],
                        df["total"],
                        np.nan, np.nan, np.nan))

    dt_names = ",".join(("source","ss","df","ms","f","p"))
    anova_table = np.rec.fromrecords(anova_table, names=dt_names)

    return anova_table
