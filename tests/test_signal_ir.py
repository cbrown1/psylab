# -*- coding: utf-8 -*-

import os
import numpy as np
import numpy.testing as np_testing
import psylab

                         
def test_next_power_of_two():
    ref = 64
    ret = psylab.signal.ir.next_power_of_two(55)
    assert ref == ret


def test_compute_recording_delay():
    # 1-d array
    ref = 1154
    hardware_delay = 1000
    playback_distance = 1.2
    ret = psylab.signal.ir.compute_recording_delay(hardware_delay, playback_distance)
    assert ref == ret


def test_gen_sweep():
    ref_sweep = np.array([ 0.        ,  0.00762101,  0.01632964,  0.02628022,  0.03764839,
        0.05063376,  0.06546269,  0.08239115,  0.10170746,  0.12373465,
        0.14883199,  0.17739506,  0.2098532 ,  0.24666269,  0.28829343,
        0.33520518,  0.38780832,  0.44640145,  0.51107503,  0.5815666 ,
        0.65704837,  0.73582397,  0.81490975,  0.88948254,  0.95220024,
        0.99246339,  0.99581482,  0.94391499,  0.81592687,  0.59268835,
        0.26554667, -0.14850611, -0.58635122, -0.92161331, -0.97479271,
       -0.59169791,  0.18022831,  0.89653539,  0.82270419, -0.24669458,
       -0.9977268 ,  0.08384251,  0.94698102, -0.73742651,  0.05658252])

    ref_invsweep = np.array([ 5.65825216e-02, -6.45286685e-01,  7.25118839e-01,  5.61779801e-02,
       -5.84988683e-01, -1.26569597e-01,  3.69357951e-01,  3.52212803e-01,
        6.19576100e-02, -1.77994116e-01, -2.56597159e-01, -2.12286444e-01,
       -1.18185804e-01, -2.61930306e-02,  4.09841808e-02,  8.00452830e-02,
        9.64260876e-02,  9.76135598e-02,  9.01134902e-02,  7.85886229e-02,
        6.59792574e-02,  5.39324962e-02,  4.32371010e-02,  3.41629165e-02,
        2.66939173e-02,  2.06751363e-02,  1.58989170e-02,  1.21518509e-02,
        9.23778647e-03,  6.98707607e-03,  5.25839805e-03,  3.93691587e-03,
        2.93090817e-03,  2.16801414e-03,  1.59166190e-03,  1.15792337e-03,
        8.32866272e-04,  5.90387270e-04,  4.10472622e-04,  2.77820612e-04,
        1.80760976e-04,  1.10413271e-04,  6.00347789e-05,  2.45172958e-05,
        0.00000000e+00])

    ret_sweep, ret_invsweep = psylab.signal.ir.gen_sweep(dur=.001)
    np_testing.assert_allclose(ref_sweep, ret_sweep, rtol=1e-5)
    np_testing.assert_allclose(ref_invsweep, ret_invsweep, rtol=1e-5)


def test_get_level_difference():
    ar1 = np.array((1,2,3,4,5))
    ar2 = ar1 * 2
    ref = 6.020599913279624
    ret = psylab.signal.ir.get_level_difference(ar1,ar2)
    assert ref == ret


def test_apply_level_difference():
    ar1 = np.array((1,2,3,4,5))
    ar2 = ar1 * 2
    db = 6.020599913279624
    ref1,ref2 = psylab.signal.ir.apply_level_difference(ar1, ar2, db)
    np.testing.assert_allclose(ar1, ref1, rtol=1e-5)
    np.testing.assert_allclose(ar1, ref2, rtol=1e-5)

def test_get_ir():
    ref = np.array([[-4.82561940e-02, -5.78861860e-02, -6.79692758e-02,
        -7.84663954e-02, -8.93534691e-02, -1.00567516e-01,
        -1.11950246e-01, -1.23183673e-01, -1.33712386e-01,
        -1.42649929e-01, -1.48674009e-01, -1.49930572e-01,
        -1.43996353e-01, -1.28000862e-01, -9.90868362e-02,
        -5.54801880e-02,  1.51995782e-03,  6.45248900e-02,
         1.16763343e-01,  1.31363992e-01,  7.95352683e-02,
        -4.39484188e-02, -1.79257534e-01, -1.85633610e-01,
         4.28620576e-02,  2.81687931e-01, -4.29449726e-02,
        -5.96004175e-01,  9.40580210e-01,  3.66154498e+00,
         8.23056775e-01, -4.56370135e-01, -2.87749250e-02,
         1.65159693e-01,  2.19908897e-02, -8.33413155e-02,
        -7.04230963e-02, -1.51082760e-02,  2.39257391e-02,
         3.45792768e-02,  2.68955264e-02,  1.30057307e-02,
         2.68085284e-04, -8.56275111e-03, -1.33821322e-02,
        -1.51271184e-02, -1.48911679e-02, -1.35675497e-02,
        -1.17728127e-02, -9.88440880e-03]]).T

    sig,inv = psylab.signal.ir.gen_sweep(dur=.001)
    rec = np.concatenate((sig,np.zeros(550)))
    ir = psylab.signal.ir.get_ir(rec,inv, ir_length=50)
    np.testing.assert_allclose(ref, ir, rtol=1e-5)

