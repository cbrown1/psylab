# -*- coding: utf-8 -*-

# Copyright (c) 2010-2019 Christopher Brown
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
# contributions are welcome. Go to http://github.com/cbrown1/psylab/ 
# for more information and to contribute. Or send an e-mail to: 
# cbrown1@pitt.edu.
#

"""
Functions to do simple arithmetic in feet and inches. 

Each arg should be a tuple as in (feet, inches). The return is another tuple.
"""

def imperial_add(*args):
    """Adds numbers expressed in feet and inches

        Parameters
        ----------
        args: tuple of tuples
            A number of tuples, each in the form (feet, inches)

        Returns
        -------
        ret : tuple
            The sum of the input tuples, in (feet, inches) 
    """
    total = 0
    for arg in args:
        total += ((arg[0]*12)+arg[1])
    feet = total / 12
    inches = total % 12
    return (feet, inches)

def imperial_subtract(l1, l2):
    """Subtracts one number from another in feet and inches

        Parameters
        ----------
        l1: tuple
            A length in the form (feet, inches)
        l2: tuple
            A length in the form (feet, inches)

        Returns
        -------
        ret : tuple
            Length 1 minus length 2, in (feet, inches) 
    """
    total = ((l1[0]*12)+l1[1]) - ((l2[0]*12)+l2[1])
    feet = total / 12
    inches = total % 12
    return (feet, inches)

def imperial_multiply(l1, l2):
    """Multiplies one number with another in feet and inches

        Parameters
        ----------
        l1: tuple
            A length in the form (feet, inches)
        l2: tuple
            A length in the form (feet, inches)

        Returns
        -------
        ret : tuple
            Length 1 times length 2, in (feet, inches) 
    """
    total = ((l1[0]*12)+l1[1]) * ((l2[0]*12)+l2[1])
    feet = int(total / 12)
    inches = int(total % 12)
    return (feet, inches)

def imperial_divide(l1, l2):
    """Divides a number into a number of feet and inches

        Parameters
        ----------
        l1: tuple
            A length in the form (feet, inches)
        l2: tuple
            A length in the form (feet, inches)

        Returns
        -------
        ret : scalar
            Return is a scalar representing Length 1 divided by length 2 
            (units cancel). 
    """
    total = float((l1[0]*12)+l1[1]) / float((l2[0]*12)+l2[1])
    return total
