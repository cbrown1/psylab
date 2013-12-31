# -*- coding: utf-8 -*-

# Copyright (c) 2013 Christopher Brown
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
audio - Audio-specific functions that depend on the medussa package

Modules include:

signal_io - Helper functions for reading audio data in less typical ways
listPlayer - Standalone script to play blocks of soundfiles in folders

Notes
-----
To access TDT modules via the serial port, set both jumpers on
the back of the OI1 to the RIGHT (can be accessed from the front
of the XBUS rack). Jumpers to the left for AP2 control.

Tested on windows and linux.

Depends on medussa (http://medussa.googlecode.com)
'''

import signal_io
import listPlayer

