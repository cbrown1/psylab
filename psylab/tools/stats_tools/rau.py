# -*- coding: utf-8 -*-

# Copyright (c) 2010 Christopher Brown
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

import numpy as np

def rau( p ):
    '''Normalizes percent correct data by converting to rationalized arcsine units

        The arcsine transform normalizes percent-correct data. The
        "Rationalized" nature of the transform simply means that the
        resulting values are roughly similar to PC data for a large
        range of the distribution (between about .15 and .85). This
        transform is appropriate if you have data falling outside of
        this range (data falling within this range won't be appreciably
        affected). Rau values are between -.23 (PC=0) and 1.23 (PC=1).

        Parameters
        ----------
        p : scalar or array
            Should be percent correct values, between 0 and 1

        Returns
        -------
        r : scalar or array
            Converted rau values

        Notes
        -----
        Reference: Studebaker, G.A. (1985). "A "rationalized" arcsine
        transform," J. Speech Hear. Res. 28, 455-462.
    '''

    return ((92.94648673*np.arcsin(np.sqrt(p)))-23)/100.;
