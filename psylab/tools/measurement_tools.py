# -*- coding: utf-8 -*-
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
