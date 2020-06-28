# -*- coding: utf-8 -*-

import numpy as np
import numpy.testing as np_testing
import psylab


def test_compensate_1():
    fs = 44100
    tone = psylab.signal.tone(200, fs, 1000)
    ref = psylab.signal.tone(200, fs, 1000, amp=0.7079)
    out = psylab.signal.compensate(tone,fs,np.array([[200,-3]]))
    np.testing.assert_allclose(ref, out, atol=1e-3)

