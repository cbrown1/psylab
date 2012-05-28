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

def irn(dur, fs, delay, gain, its, type=1):
    '''Generates iterated rippled noise
    
        Generates iterated rippled noise, or noise with a rippled spectrum, by 
        implementing a delay-attenuate-add method. 
        
        Parameters
        ----------
        dur : scalar
            Duration of the noise, in s.
        fs : scalar
            The sample frequency.
        delay : scalar
            The delay, in ms. The F0 of the pitch will be 1/delay.
        gain : scalar
            The attenuation. The strength of the pitch is set by the gain.
        its : scalar
            The number of iterations.
        type : scalar
            1 = IRNO; 2 = IRNS.
        
        Returns
        -------
        y : array
            The noise.
    '''
    dd = dur/1000.;
    wbn = np.random.randn(fs);
    rip = wbn;
    
    if type == 1:
        for it in range(its):
            rip[:fs-delay] = rip[delay:fs];
            rip = ( rip * gain ) + wbn;
        
    elif type == 2:
        for it in range(its):
            rip1 = rip;
            rip[:fs-delay] = rip[delay:fs];
            rip = rip + ( gain * rip1 );
    
    rip = rip / np.max(np.abs(rip))
    return rip[:np.round(dd * fs)];
