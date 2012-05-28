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
import numpy as np

def samp2ms(samples, fs):
    '''Converts samples to milliseconds
        
        Returns a number of ms for a given number of samples
        
        Parameters
        ----------
        samples: scalar
            A number of samples.
        fs: scalar
            The sampling frequency.
        
        Returns
        -------
        y : scalar
            A number of milliseconds.
    '''
    return (np.float32(samples)/np.float32(fs))*1000.
