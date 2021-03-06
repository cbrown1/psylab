# -*- coding: utf-8 -*-

# Copyright (c) 2010-2018 Christopher Brown
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

'''
PsyLab - Psychophysics Lab

A loose collection of modules useful for various aspects of running
psychophysical experiments, although several might be more generally
useful.

'''
from . import version
__version__ = version.__version__

from . import config
from . import data
from . import folder
from . import string
from . import measurement
from . import stimulus_manager
from . import path
from . import plot
from . import signal
from . import stats
from . import time
