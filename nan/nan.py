import numpy as np

def mean(arr):
    n = 0
    s = 0
    all_nan = True
    for x in arr:
        if not np.isnan(x):
            all_nan = False
            n += 1
            s += x
    if all_nan:
        m = np.nan
    elif n == 0:
        m = 0
    else:
        m = s/n
    return m

def product(arr):
    return np.product(tuple(x for x in arr if not np.isnan(x)))
