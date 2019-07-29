# -*- coding: utf-8 -*-

import numpy as np
import numpy.testing as np_testing
import psylab


def test_str_to_list():
    ref = [1,2,3,4,8,10,11,12,50]
    ret = psylab.tools.list_tools.str_to_list('1-4,8,10-12,50')
    assert all([a == b for a, b in zip(ref, ret)])


def test_list_to_str():
    ref = '0:3,7,9:11,49'
    ret = psylab.tools.list_tools.list_to_str([0, 1, 2, 3, 7, 9, 10, 11, 49])
    assert ref == ret

