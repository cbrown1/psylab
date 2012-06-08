# -*- coding: utf-8 -*-

# Copyright (c) 2010, 2012 Christopher Brown
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

'''
stats - A random collection of stats functions.

Functions include:

anova_between - Performs a between-subjects anova for any number of factors
anova_table - Generates a nicely formatted anova summary table
anova_within - Performs a within-subjects anova for any number of factors
cumr2 - Comuputes cumulative R**2 values
pairwise_comparisons - Computes a table of pairwise comparisons
rau - Normalizes percent correct data, converting to rationalized arcsine units
'''

from .cumr2 import cumr2
from .rau import rau
from .anova import anova_between, anova_within, anova_table
from .pairwise import pairwise_comparisons
