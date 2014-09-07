# -*- coding: utf-8 -*-
"""
Created on Sat Sep  6 16:57:37 2014

@author: code-breaker
"""

from StringIO import StringIO
import pandas as pd

def read_csv(filename, comment="#", **kwargs): 
    """Gracefully handle comments and blank lines when reading csv files wih pandas.
    
        Pandas doesn't do a good job with headers. So this function wraps
        pandas.read_csv and does it.
    """
    lines = ""
    for line in open(filename):
        line = line.strip()
        if not line.startswith(comment):
            if line != "":
                lines += line + "\n"
    return pd.read_csv(StringIO(lines), **kwargs)
