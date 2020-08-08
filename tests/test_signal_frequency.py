# -*- coding: utf-8 -*-

import numpy as np
import numpy.testing as np_testing
import psylab


def test_logspace():
    ref = np.array([125., 250., 500.])
    ret = psylab.signal.logspace(125, 500, 3)
    np_testing.assert_allclose(ref, ret, rtol=1e-5)


def test_oct2f_1():
    ref = (500.0, 2000.0)
    ret = psylab.signal.oct2f(1000,1)
    assert ref == ret


def test_oct2f_2():
    ref = (796.0, 1257.0)
    ret = psylab.signal.oct2f(1000,.33)
    assert ref == ret


def test_f2oct_1():
    ref = 0.3299864
    ret = psylab.signal.f2oct(1000,1257)
    assert ref == ret


def test_f2oct_2():
    ref = 2.0
    ret = psylab.signal.f2oct(1000,4000)
    assert ref == ret


def test_f2erbs_1():
    ref = 0.3299864
    ret = psylab.signal.f2erbs(1000)
    assert ref == ret


def test_f2erbs_2():
    ref = 2.0
    ret = psylab.signal.f2erbs(4000)
    assert ref == ret

