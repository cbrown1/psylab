# -*- coding: utf-8 -*-

# Copyright (c) 2013 Christopher Brown
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

"""
stats_tools - Stats-related functions for working with statsmodels and pandas
"""

import csv
import numpy as np

def print_pairwise_table ( tuk, sigpairsonly=False ):
    """Prints a reasonably formatted summary table from output of statsmodels.stats.multicomp.pairwise_tukeyhsd
    """
    tuksumm = tuk.summary()
    print (tuksumm.title)
    print ("%10s %10s %8s %8s %8s %8s" % tuple(tuksumm.data[0]))
    for rec in tuksumm.data[1:]:
        if sigpairsonly and rec[5]:
            group1 = str(tuk.groupsunique.item(rec[0]))
            group2 = str(tuk.groupsunique.item(rec[1]))
            vals = (group1, group2) + tuple(rec[2:])
            print ("%10s %10s %8.2g %8.2g %8.2g %8s" % vals)
    print ("%10s %10s %8s %8s %8s %8s" % tuple(tuksumm.data[0]))

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

def rms_error(data, groupby, data_col, rms_col_title='rms'):
    """
    rms_error takes a pandas dataframe, and computes rms error
    based on the levels in the column names specified in groupby

    For each group, a mean will be computed and subtracted from each score.
    Then, the rms (root-mean-square) of all the difference scores will be
    computed, which is the square-root of the mean of the squared differences.

    Parameters
    ----------
    data : pandas dataframe
        The dataframe
    groupby : list of str
        A list of column names to sort data on, in the same form that you
        would pass to pd.groupby
    data_col : str
        The name of the column on which to compute the rms values
    rms_col_title : str
        The name to assign to the newly created rms data column. Default = 'rms'

    Returns
    -------
    new_data : pandas dataframe
        Will contain rms error values along with the groupby variables

    Example
    -------
    >>> a = pd.DataFrame({'proc': [1,1,1, 2,2,2, 3,3,3], 'scores': [4,5,6, 2,5,7, 0,5,10]})
    >>> rms_error(a,['proc'],'scores')
       proc       rms
    0     1  0.816497
    1     2  2.449490
    2     3  4.082483
    >>> np.sqrt(np.mean(np.square((-1,0,1)))) # Mean-diff scores for [4,5,6]
    0.81649658092772603
    >>> np.sqrt(np.mean(np.square((-3,0,3)))) # Mean-diff scores for [2,5,8]
    2.4494897427831779
    >>> np.sqrt(np.mean(np.square((-5,0,5)))) # Mean-diff scores for [0,5,10]
    4.0824829046386304
    """

    data_diff_fun = lambda data: data - data.mean()
    new_data = data.copy()
    new_data['diff'] = data.groupby(groupby).transform(data_diff_fun)[data_col]
    new_data['diff_sq'] = new_data['diff']**2
    new_data = new_data.groupby(groupby).agg(np.mean).reset_index()
    new_data[rms_col_title] = np.sqrt(new_data['diff_sq'])

    return new_data[groupby].join(new_data[rms_col_title])

