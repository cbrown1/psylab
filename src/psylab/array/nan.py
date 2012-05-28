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
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# Comments and/or additions are welcome. Send e-mail to: cbrown1@pitt.edu.
#


import numpy as np

def nanmean(arr):
    n = 0
    s = 0
    all_nan = True
    for x in arr:
        if not np.isnan(x):
            all_nan = False
            n += 1
            s += x
    if all_nan:
        m = np.nan
    elif n == 0:
        m = 0
    else:
        m = s/n
    return m

def nanproduct(arr):
    return np.product(tuple(x for x in arr if not np.isnan(x)))
