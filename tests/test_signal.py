# -*- coding: utf-8 -*-

import os
import numpy as np
import numpy.testing as np_testing
import psylab

                         
def test_atten_1():
    # Single scalar
    ref = 0.7079488911418277
    ret = psylab.signal.atten(1,3)
    assert ref == ret

def test_atten_2():
    # 1-d array
    ref = np.array([0.        , 0.07866099, 0.15732198, 0.23598296, 0.31464395,
                    0.39330494, 0.47196593, 0.55062692, 0.6292879 , 0.70794889])
    a = np.linspace(0,1,10)
    ret = psylab.signal.atten(a,3)
    np_testing.assert_allclose(ref, ret)


def test_atten_3():
    # 2-d array
    ref = np.array([[0.        , 1.00238326],
                    [0.05568796, 1.44788694],
                    [0.11137592, 1.89339061],
                    [0.16706388, 2.33889428],
                    [0.22275184, 2.78439796],
                    [0.2784398 , 3.22990163],
                    [0.33412775, 3.6754053 ],
                    [0.38981571, 4.12090898],
                    [0.44550367, 4.56641265],
                    [0.50119163, 5.01191632]])

    a = np.linspace(0,1,10)
    b = np.linspace(2,10,10)
    c = np.vstack((a,b)).T
    ret = psylab.signal.atten(c,6)
    np_testing.assert_allclose(ref, ret)


def test_apply_itd():
    ref = np.array([[  0.,   1.],
                    [  0.,   2.],
                    [  1.,   3.],
                    [  2.,   4.],
                    [  3.,   5.],
                    [  4.,   6.],
                    [  5.,   7.],
                    [  6.,   8.],
                    [  7.,   9.],
                    [  8.,  10.],
                    [  9.,   0.],
                    [ 10.,   0.]])

    arr = np.linspace(1,10,10)
    arr_in = np.vstack((arr, arr)).T
    arr_out = psylab.signal.apply_itd(arr_in, 10, 200000) # us
    np.testing.assert_allclose(ref, arr_out)


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


def test_compensate_1():
    fs = 44100
    tone = psylab.signal.tone(200, fs, 1000)
    ref = psylab.signal.tone(200, fs, 1000, amp=0.7079)
    out = psylab.signal.compensate(tone,fs,np.array([[200,-3]]))
    np.testing.assert_allclose(ref, out, atol=1e-3)

