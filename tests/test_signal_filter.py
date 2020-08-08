# -*- coding: utf-8 -*-

import numpy as np
import numpy.testing as np_testing
import psylab


def test_win_attack_1():
    ref = [0.5, 1.,  1.,  1.,  1. ]
    ret = psylab.signal.win_attack(5, 2)
    np_testing.assert_allclose(ref, ret, rtol=1e-5)


def test_win_attack_2():
    ref = [0.1, 0.2, 0.3, 0.4, 0.5]
    ret = psylab.signal.win_attack(5, 10)
    np_testing.assert_allclose(ref, ret, rtol=1e-5)


def test_sliding_window_1():
    arr = np.arange(20)

    ref = np.array([[ 0,  1,  2,  3],
                    [ 4,  5,  6,  7],
                    [ 8,  9, 10, 11],
                    [12, 13, 14, 15],
                    [16, 17, 18, 19]])
    ret = psylab.signal.sliding_window(arr, 4)
    np_testing.assert_allclose(ref.shape, ret.shape)


def test_sliding_window_2():
    arr = np.arange(20)

    ref = np.array([[ 0,  1,  2,  3],
                    [ 2,  3,  4,  5],
                    [ 4,  5,  6,  7],
                    [ 6,  7,  8,  9],
                    [ 8,  9, 10, 11],
                    [10, 11, 12, 13],
                    [12, 13, 14, 15],
                    [14, 15, 16, 17],
                    [16, 17, 18, 19]])
    ret = psylab.signal.sliding_window(arr, 4, ss=2)

    np_testing.assert_allclose(ref.shape, ret.shape)

