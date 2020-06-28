# -*- coding: utf-8 -*-

# Copyright (c) 2014-2018 Christopher Brown
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
# contributions are welcome. Go to https://github.com/cbrown1/psylab/
# for more information and to contribute. Or send an e-mail to:
# cbrown1@pitt.edu.
#

"""
level: Pedagogical functions involving sound level conversion.

Sound power (sound intensity) is the cause and sound pressure is the effect.
"""

import numpy as np

hl_conversion = {
            125: 45.0,
            250: 27.0,
            500: 13.5,
            750: 9.0,
            1000: 7.5,
            1500: 7.5,
            2000: 9.0,
            3000: 11.5,
            4000: 12.0,
            6000: 16.0,
            8000: 15.5,
            }

def spl2hl(spl, f):
    """ Converts Sound Pressure Level (SPL) to Hearing Level (HL)

    """
    if f in hl_conversion.keys():
        return spl + hl_conversion[f]
    else:
        raise "Invalid frequency; must be an audiometric octave or half-octave frequency. Specifically, one of:\n{:}".format(hl_conversion.keys())


def hl2spl(hl, f):
    """ Converts Hearing Level (HL) to Sound Pressure Level (SPL)

    """
    if f in hl_conversion.keys():
        return hl - hl_conversion[f]
    else:
        raise "Invalid frequency; must be an audiometric octave or half-octave frequency. Specifically, one of:\n{:}".format(hl_conversion.keys())


def spl2n0(spl, fc, bw):
    """ Converts Sound Pressure Level (SPL) to Spectrum Level (N0)

    """
    lo = np.round(fc*(2.**np.float32(-bw/2.)));
    hi = np.round(fc*(2.**np.float32(bw/2.)));
    n0 = spl - (10 * np.log10(hi - lo))
    return n0


def spl2sp(spl):
    """Converts a Sound Pressure Level (SPL) value to Sound Pressure (Pa)

    """
    ref = .00002 # Standard reference of 20 uPa
    sp = ref * np.power(10.,spl/20.)
    return sp


def sp2spl(sp):
    """Converts a Sound Pressure (Pa) value to Sound Pressure Level (SPL)

    """
    ref = .00002 # Standard reference of 20 uPa
    spl = 20*np.log10(sp/ref)
    return spl


def spl2si(spl):
    """Converts a Sound Pressure Level (dB SPL) value to Sound Intensity (W/m2)

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
