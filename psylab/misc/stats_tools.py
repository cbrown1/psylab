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
stats_tools - A set of helper functions for working with statsmodels and pandas
"""

def print_pairwise_table ( tuk, sigpairsonly=False ):
    """Prints a reasonably formatted summary table, given the output of sm.stats.multicomp.pairwise_tukeyhsd
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


