# -*- coding: utf-8 -*-

import numpy as np
import numpy.testing as np_testing
import psylab


def test_spl2hl():
    ref = 23.5
    ret = psylab.signal.spl2hl(10,500)
    assert ref == ret

def test_hl2spl():
    ref = 17
    ret = psylab.signal.spl2hl(28,750)
    assert ref == ret

