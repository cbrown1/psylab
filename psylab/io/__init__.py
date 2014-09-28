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

'''
io - input / output functions that have dependencies

Because of the dependencies, each module must be imported specifically

Modules include [dependencies in brackets]:

audio - Helper functions for reading audio data in less typical ways [medussa]
listPlayer - Standalone script to play blocks of soundfiles in folders [medussa]
hid - Access human interface devices like joysticks [linux]
tdt2 - Control Tucker Davis Technologies System 2 hardware from the serial port [pyserial]

Notes
-----
hid is linux only. Other modules tested on windows and linux.

'''
