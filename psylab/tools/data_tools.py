# -*- coding: utf-8 -*-

# Copyright (c) 2014 Christopher Brown
#
# This file is part of Psylab.
#
# Psylab is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Psylab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Psylab.  If not, see <http://www.gnu.org/licenses/>.
#
# Bug reports, bug fixes, suggestions, enhancements, or other 
# contributions are welcome. Go to http://code.google.com/p/psylab/ 
# for more information and to contribute. Or send an e-mail to: 
# cbrown1@pitt.edu.
#
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import numpy as np

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

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def random_derangement(n):
    """Generates a random permutation of size n with no fixed points.
    
        Returns a numpy array of ints in which no value is equal to its index.
        
        Parameters
        ----------
        n : int
            The length of the array
            
        Returns
        -------
        a : array
            The array
        
        Notes
        -----
        This was adapted from an answer to a stackoverflow question, and 
        apparently implements the "early refusal" algorithm. 
    
    """
    while True:
        v = np.arange(n)
        for j in np.arange(n - 1, -1, -1):
            p = np.random.randint(0, j+1)
            if v[p] == j:
                break
            else:
                v[j], v[p] = v[p], v[j]
        else:
            if v[0] != 0:
                return v
