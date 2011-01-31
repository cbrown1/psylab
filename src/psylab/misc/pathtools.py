# -*- coding: utf-8 -*-
"""
pathproc

Some convenience functions for extracting bits of info from filenames.
The only usefulness of this module is to have all of these common tasks 
in one place.
"""

from os import path

def get_fileext(filename):
    return path.splitext(path.basename(filename))[1]

def get_filebase(filename):
    return path.splitext(path.basename(filename))[0]

def get_filename(filename):
    return path.basename(filename)

def get_path(filename):
    return path.dirname(filename)
