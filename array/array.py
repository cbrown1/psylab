#import numpy as np
from itertools import product

def indices(arr):
    return product(*tuple(xrange(y) for y in arr.shape))

def to_columns(arr):
    dvs = list(arr[i] for i in indices(arr))
    return np.array(zip(*tuple(indices(arr))) + [dvs])

def from_columns(arr):
    sh = tuple(1+int(max(x)) for x in arr[:-1])
    dv = arr[-1]
    ans = np.ones(shape=sh)

    j = 0
    for i in product(*tuple(xrange(y) for y in sh)):
        ans[i] = dv[j]
        j += 1

    return ans
