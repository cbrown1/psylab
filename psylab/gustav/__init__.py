# -*- coding: utf-8 -*-

# Copyright (c) 2010-2014 Christopher Brown
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

"""Gustav: An event-based framework for psychophysical experiments

    Gustav tries to handle all of the aspects of experimentation that are 
    common across experiments (organizing and enumerating experimental 
    variables, the psychophysical procedure, interacting with subjects, 
    logging, saving data, etc.), and leaves to the experimenter the aspects 
    that are unique to each experiment (stimulus generation and delivery, etc). 
    
    An experiment is represented by a Gustav experiment file, which is simply 
    a python script that has various functions and properties specified. For 
    example, the setup function is where many aspects of the experiment are 
    set, such as the name of the experiment, where and how to save data, what 
    the experimental variables and their levels are, and so on. The best way 
    to understand how one works is to have a look at one. See one of the 
    gustav_settings.py files for more information.

"""

from .gustav import run, info, main
from . import frontends, methods
