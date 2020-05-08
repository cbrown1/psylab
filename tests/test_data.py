# -*- coding: utf-8 -*-

import numpy as np
import psylab

def test_derangement():
    a = np.arange(5)
    b = psylab.data.random_derangement(5)
    assert not np.any(np.equal(a, b))
