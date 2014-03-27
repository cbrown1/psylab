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

"""
spl: Pedagogical functions involving sound level conversion. 

Sound power (sound intensity) is the cause and sound pressure is the effect.
"""

import numpy as np

def spl2sp(spl):
    """Converts a Sound Pressure Level (dB) value to Sound Pressure (Pa)
    
    """
    ref = .00002 # Standard reference of 20 uPa
    sp = ref * np.power(10.,spl/20.)
    return sp

def sp2spl(sp):
    """Converts a Sound Pressure (Pa) value to Sound Pressure Level (dB)
    
    """
    ref = .00002 # Standard reference of 20 uPa
    spl = 20*np.log10(sp/ref)
    return spl
    
def spl2si(spl):
    """Converts a Sound Pressure Level (dB) value to Sound Intensity (W/m2)
    
    """
    ref = .000000000001 # Standard reference of 10**−12 W/m2
    si = ref * np.power(10.,spl/10.)
    return si
    
def si2spl(si):
    """Converts a Sound Intensity (W/m2) value to Sound Pressure Level (dB)
    
    """
    ref = .000000000001 # Standard reference of 10**−12 W/m2
    spl = 10*np.log10(si/ref)
    return spl
