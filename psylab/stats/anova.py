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
from itertools import combinations, product

def nanproduct(arr):
    return np.product(tuple(x for x in arr if not np.isnan(x)))

def anova_table(anova_data):
    """Generates a nicely formatted anova summary table

    Parameters:
    -----------
    anova_data : record array
        The output of an anova function

    Returns:
    --------
    table : string
        A formatted summary table, with space-delimited columns
    """
    sourcetab = 8
    mintab = 10
    sfmts = "%"+str(mintab)+"s"
    sfmt = "%"+str(mintab)+".4g"
    for x in anova_data:
        if len(x[anova_data.dtype.names[0]]) > sourcetab:
            sourcetab = len(x[anova_data.dtype.names[0]])
    sourcetab += 1
    ret = anova_data.dtype.names[0] + " " * (sourcetab - len(anova_data.dtype.names[0]))
    for x in anova_data.dtype.names[1:]:
        ret += sfmts % x
    ret += "\n"
    for x in anova_data:
        ret += x[anova_data.dtype.names[0]] + " " * (sourcetab - len(x[anova_data.dtype.names[0]]))
        for y in range(1,6):
            if not np.isnan( x[anova_data.dtype.names[y]]):
                ret += sfmt % x[anova_data.dtype.names[y]]
        if x['p'] < .001:
            ret += "  ***"
        elif x['p'] < .01:
            ret += "  **"
        elif x['p'] < .05:
            ret += "  *"
        ret += "\n"
    return ret

def anova_between(data, factors=None):
    """Performs a between-subjects analysis of variance for any number of factors.

    Parameters:
    -----------
    data : ndarray
        Representation of the experimental data as a multi-dimensional array,
        in which each dimension represents a factor, the length of each
        dimension is the number of levels of that factor, and the last
        dimension is the dependent variable (the length of this dimension is
        the number of scores in each treatment).

        For example, suppose an experiment has 3 factors, A, B, and C.
        Suppose also that factors A and B have 2 levels, and C has 3:
        A := A1, A2
        B := B1, B2
        C := C1, C2, C3
        Finally, suppose that there are 5 scores per AxBxC treatment.

        Then it is the case that data.shape == (2,2,3,5).

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

    n["total"] = data.size

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
            squares += np.nansum(data[i])**2 / data[i].size

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

def anova_within(data, subject_index=0, factors=None):
    """Performs a within-subjects analysis of variance for any number of factors.

       All factors must be within (no split-plot designs, etc.).

    Parameters:
    -----------
    data : ndarray
        Representation of the experimental data as a multi-dimensional array,
        in which each dimension represents a factor (one of which is the
        'subject' factor), the length of each dimension is the number of
        levels of that factor, and the last dimension is the dependent
        variable (the length of this dimension is the number of scores in
        each treatment).

        For example, suppose an experiment has 3 factors, S(ubjects), A, and B.
        Suppose also that factor A has 2 levels, B has 3, and there are 5
        subjects:
        S := S1, S2, S3, S4, S5
        A := A1, A2
        B := B1, B2, B3

        Then it is the case that data.shape == (5,2,3,5).

    factors : list or tuple
        String of human-readable factor names.

    subect_index : int
        The index of the axis of `data` which is the subject variable [default=0].

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

    n["total"] = data.size

    if factors is None: #If factors aren't specified
        num_factors = len(data.shape) - 1
        if num_factors <= 18: # If the factor dimensions can be mapped to
                                 # letters of the alphabet...
            factors = []
            j = 0
            for i in xrange(num_factors):
                if i == subject_index:
                    factors.append("S")
                else:
                    factors.append(chr(65+j))
                    j += 1
        else: # just give them indexed dummy names
            factors = []
            j = 0
            for i in xrange(num_factors):
                if i == subject_index:
                    factors.append("S")
                else:
                    factors.append("A%d" % (j))
                    j += 1
            factors = tuple("F%s" % (i) for i in xrange(num_factors))

    subject = (factors[subject_index],)

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

    error_term_from_source = {}

    for s in sources:
        # Compute the sum of squares
        squares = 0
        for i in ss_indices(s):
            squares += np.nansum(data[i])**2 / data[i].size

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

        if subject[0] in s:
            error_term_from_source[s] = None
        else:
            error_term_from_source[s] = subject + s

    ss["total"] = np.nansum(data**2) - cm
    df["total"] = 0

    for s in sources:
        etfs = error_term_from_source[s]
        if etfs is None:
            f[s] = np.nan
            p[s] = np.nan
        else:
            ms[etfs] = ss[etfs] / df[etfs]
            f[s] = ms[s] / ms[etfs]
            p[s] = 1 - stats.f.cdf(f[s], df[s], df[etfs])
        df["total"] += df[s]


    anova_table = []
    for s in [x for x in sources if subject[0] not in x]:
        anova_table.append(("*".join(s),ss[s],df[s],ms[s],f[s],p[s]))
    for s in [x for x in sources if subject[0] in x]:
        anova_table.append(("*".join(s),ss[s],df[s],ms[s],f[s],p[s]))

    anova_table.append(("total",
                        ss["total"],
                        df["total"],
                        np.nan, np.nan, np.nan))

    dt_names = ",".join(("source","ss","df","ms","f","p"))
    anova_table = np.rec.fromrecords(anova_table, names=dt_names)

    return anova_table
