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

'''
PsyLab - Psychophysics Lab

A loose collection of modules useful for various aspects of running
psychophysical experiments, although several might be more generally
useful.

In addition to the modules that are imported automatically, others include:

subject_manager: Manage subjects with a useful user interface [dep: pyqt]
io.tdt2: Access Tucker Davis System II hardware via serial port dep: pyserial]
io.audio: Perform tasks related to file i/o [dep: medussa]
io.listPlayer - Standalone script to play blocks of soundfiles in folders [dep: medussa]
io.hid - Access human interface devices like joysticks [dep: linux]
'''

__version__ = '0.4.7.6'

#from dataview import dataview
from . import tools
from . import signal
from . import stats
from . import gustav
