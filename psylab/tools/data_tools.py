# -*- coding: utf-8 -*-
"""
Created on Sat Sep  6 16:57:37 2014

@author: code-breaker
"""

from StringIO import StringIO

def read_csv(filename, comment="#"): 
    """Gracefully handle comments and blank lines when reading csv files.
    
        Pandas is great, but doesn't do a good job with headers. This function 
        skips blank and comment lines in a csv properly, and passes back a 
        file-like object ready to be passed to pandas.read_csv.
        
        Parameters
        ----------
        filename : string
            The path to the csv file.
        comment : string
            A comment character to look for. Lines that start with this 
            character will be skipped. 

        Returns
        -------
        StringIO object
            A file-like object, suitable to be passed to pandas.read_csv.
            
        Usage
        -----
        f = read_csv(filename)
        data = pandas.read_csv(f, **kwargs)
    """
    lines = ""
    for line in open(filename):
        line = line.strip()
        if not line.startswith(comment):
            if line != "":
                lines += line + "\n"
    return StringIO(lines)
