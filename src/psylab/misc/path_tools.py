# -*- coding: utf-8 -*-

# Copyright (c) 2010-2012 Christopher Brown
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
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# Comments and/or additions are welcome. Send e-mail to: cbrown1@pitt.edu.
#

"""
path_tools

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
