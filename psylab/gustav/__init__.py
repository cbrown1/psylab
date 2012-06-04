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
# along with Psylab.  If not, see <http://www.gnu.org/licenses/>.
#
# Bug reports, bug fixes, suggestions, enhancements, or other 
# contributions are welcome. Go to http://code.google.com/p/psylab/ 
# for more information and to contribute. Or send an e-mail to: 
# cbrown1@pitt.edu.
#

"""Gustav - A Python module to run psychophysical experiments

    The goal of Gustav is to handle the routines that are common across
    experiments (like the psychophysical procedure, keeping track of stimulus
    and condition orders, recording response data, etc), to allow the 
    experimenter to worry about the things that are unique to each experiment
    (like the experimental design, stimulus generation, etc.).
 
    See one of the settings.py files for more information.
	
	The main functions in Gustav are:
	
	    run - runs an experiment
	    
	    configure [not currently working] - intended to be a gui to help 
	    with experimental design
	    
	    list_conditions - simply lists all of the conditions in an 
	    experiment, along with all of the corresponding condition levels
	
"""

__version__ = '0.1'
__author__ = 'Christopher Brown <c-b@asu.edu>'

from gustav import run, configure, list_conditions
import frontends, methods
