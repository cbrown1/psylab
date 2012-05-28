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
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# Comments and/or additions are welcome. Send e-mail to: cbrown1@pitt.edu.
#

import numpy as np
import random

# Encodings of primitive polynomials for use as tap values,
# decremented to account for mapping onto zero-indexed arrays.
taps = {2 : [1, 0],
        3 : [2, 0],
        4 : [3, 0],
        5 : [4, 1],
        6 : [5, 0],
        7 : [6, 0],
        8 : [7, 5, 4, 0],
        9 : [8, 3],
        10 : [9, 2],
        11 : [10, 1],
        12 : [11, 6, 3, 2],
        13 : [12, 3, 2, 0],
        14 : [13, 11, 10, 0],
        15 : [14, 0],
        16 : [15, 4, 2, 1],
        17 : [16, 2],
        18 : [17, 2],
        19 : [18, 5, 4, 0],
        20 : [19, 2],
        21 : [20, 1],
        22 : [21, 0],
        23 : [22, 4],
        24 : [23, 3, 2, 0],
        25 : [24, 2],
        26 : [25, 7, 6, 0],
        27 : [26, 7, 6, 0],
        28 : [27, 2],
        29 : [28, 1],
        30 : [29, 15, 14, 0],
        31 : [30, 2],
        32 : [31, 27, 26, 0]
       }

# Encodings of the above polynomials as binary digits in a hexadecimal representation.
# For a given k in "taps", the argument to np.uint32 is determined by sum([2**i for i in taps[k]])
bintaps = {2 : np.uint32(3),
           3 : np.uint32(5),
           4 : np.uint32(9),
           5 : np.uint32(18),
           6 : np.uint32(33),
           7 : np.uint32(65),
           8 : np.uint32(177),
           9 : np.uint32(264),
           10 : np.uint32(516),
           11 : np.uint32(1026),
           12 : np.uint32(2124),
           13 : np.uint32(4109),
           14 : np.uint32(11265),
           15 : np.uint32(16385),
           16 : np.uint32(32790),
           17 : np.uint32(65540),
           18 : np.uint32(131076),
           19 : np.uint32(262193),
           20 : np.uint32(524292),
           21 : np.uint32(1048578),
           22 : np.uint32(2097153),
           23 : np.uint32(4194320),
           24 : np.uint32(8388621),
           25 : np.uint32(16777220),
           26 : np.uint32(33554625),
           27 : np.uint32(67109057),
           28 : np.uint32(134217732),
           29 : np.uint32(268435458),
           30 : np.uint32(536920065),
           31 : np.uint32(1073741828),
           32 : np.uint32(2348810241)
          }

def generate_lfsr(n, use_rand_seed):
    toggle_mask = bintaps[n]
    if use_rand_seed:
        lfsr = np.uint32(random.randint(1, (2**n - 1)))
    else:
        lfsr = np.uint32(1)

    while 1:
        lsb = lfsr & np.uint32(1)
        yield lsb
        lfsr = (lfsr >> np.uint32(1)) ^ (np.uint32(0) - (lfsr & np.uint32(1)) & toggle_mask)

def mls(n, rand_seed=False):
    '''Generates maximum-length sequences

        Implements a Galois-configuration linear feedback shift register
        to generate maximum-length sequences, which are pseudorandom noises
        useful for acoustic measurements.

        Parameters
        ----------
        n : scalar
            The number of starting bits.
        rand_seed : bool
            True to begin with a sequence of all ones (repeatable).
            False to begin with a random sequence.

        Returns
        -------
        y : array
            The maximum-length sequence, which is 2^(n-1) in length.

        Notes
        -----
        Further information at:
        http://www.newwaveinstruments.com/resources/articles/m_sequence_linear_feedback_shift_register_lfsr.htm
        http://www.cfn.upenn.edu/aguirre/wiki/public:m_sequences
        Primitive binary polynomials obtained from:
          Stahnke, W. (1973). "Primitive binary polynomials," Mathematics of Computation, 27:977-980.
'''

    try:
        assert type(n) == type(1) # Ensure 'n' is an int
        assert 2 <= n <= 32
    except:
        print "n must be an integer in the interval [2, 32]."

    seqlen = 2**n - 1;

    # Initialize the linear feedback shift register, val = 1 for all indices.
    lfsr = generate_lfsr(n, rand_seed)

    #mls = np.ones(n, dtype=np.int32)
    def zero_to_neg_one(x):
        if x == 0:
            return -1
        else:
            return 1
    zero_to_neg_one = lambda x: x
    return np.array([zero_to_neg_one(lfsr.next()) for i in xrange(seqlen)], np.int32)
