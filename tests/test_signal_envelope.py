# -*- coding: utf-8 -*-

import numpy as np
import numpy.testing as np_testing
import psylab


def test_apply_ild_1():
    arr_in_1 = np.linspace(1,10,10)
    arr_in = np.vstack((arr_in_1, arr_in_1)).T
    ref = np.array([[ 1.        ,  0.70794889],
                    [ 2.        ,  1.41589778],
                    [ 3.        ,  2.12384667],
                    [ 4.        ,  2.83179556],
                    [ 5.        ,  3.53974446],
                    [ 6.        ,  4.24769335],
                    [ 7.        ,  4.95564224],
                    [ 8.        ,  5.66359113],
                    [ 9.        ,  6.37154002],
                    [10.        ,  7.07948891]])

    arr_out = psylab.signal.apply_ild(arr_in, -3) # us
    np.testing.assert_allclose(ref, arr_out)

def test_apply_ild_2():
    arr_in_1 = np.linspace(1,10,10)
    arr_in = np.vstack((arr_in_1, arr_in_1)).T
    ref = np.array([[ 0.84139699,  1.18849962],
                    [ 1.68279398,  2.37699924],
                    [ 2.52419096,  3.56549886],
                    [ 3.36558795,  4.75399848],
                    [ 4.20698494,  5.9424981 ],
                    [ 5.04838193,  7.13099772],
                    [ 5.88977891,  8.31949734],
                    [ 6.7311759 ,  9.50799696],
                    [ 7.57257289, 10.69649658],
                    [ 8.41396988, 11.8849962 ]])

    arr_out = psylab.signal.apply_ild(arr_in, 3, .5) # us
    np.testing.assert_allclose(ref, arr_out)

def test_gso_1():
    arr_in_1 = np.random.randn(10)
    arr_in_2 = np.random.randn(10)
    arr_in = np.vstack((arr_in_1.copy(), arr_in_2.copy())).T
    out = psylab.signal.gso(arr_in, 1.)
    np.testing.assert_allclose(out[:,0], out[:,1])

