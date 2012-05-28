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
from scipy.signal import lfilter

def gammatone(fs, numChannels, loFreq, hiFreq, method = 'moore'):
    '''DON'T USE THIS FUNCTION! USE the Brian package instead!
    (http://briansimulator.org/)
    
    Computes the filter coefficients for a bank of Gammatone filters.

    Gammatone filters were defined by Patterson and Holdworth for
    simulating the cochlea. The results are returned as arrays of filter
    coefficients. Each row of the filter arrays (forward and feedback)
    can be passed to the scipy "lfilter" function.

    This is a straight-up port of the GammaTone Tool Kit v2.0 by Nick Clark:
    http://www.mathworks.de/matlabcentral/fileexchange/15313-gammatone-tool-kit-v2-0
    '''

    loFreq = max(loFreq, 75);

    if method in ('lyon','stanley'):
        EarQ = 8;       # Lyon + Stanley Parameters (1988)
        minBW = 125;
        order = 2;
    elif method in ('greenwood'):
        EarQ = 7.23824; # Greenwood Parameters (1990) as (nearly) in DSAM
        minBW = 22.8509;
        order = 1;
    elif method in ('moore','glasberg'):
        EarQ = 9.26449; # Glasberg and Moore Parameters (1990)
        minBW = 24.7;
        order = 1;
    elif method in ('wierddsam'):
        EarQ = 9.26; # Glasberg and Moore Parameters (1990)
        minBW = 15.719; #WORKS IF YOU SWCREW WITH THIS PARAMETER AS SO. . .
        order = 1;
    T=1./fs;

    ERBlo = ((loFreq/EarQ)**order + minBW**order) ** (1./order);
    ERBhi = ((hiFreq/EarQ)**order + minBW**order) ** (1./order);
    overlap = (ERBhi/ERBlo)**(1./(numChannels-1.));
    ERB = ERBlo * (overlap**np.arange(numChannels));
    cf = EarQ*(((ERB**order) - (minBW**order))**(1./order));

    B=1.019*2.*np.pi*ERB; # in rad here - note to self: some models require B in Hz (NC)

    part1 = (-2.*np.exp(4.*1j*cf*np.pi*T)*T + 2.*np.exp(-(B*T) + 2.*1j*cf*np.pi*T)*T*(np.cos(2.*cf*np.pi*T) - np.sqrt(3. - 2.**(3./2.)) *np.sin(2.*cf*np.pi*T)))
    part2 = (-2.*np.exp(4.*1j*cf*np.pi*T)*T + 2.*np.exp(-(B*T) + 2.*1j*cf*np.pi*T)*T*(np.cos(2.*cf*np.pi*T) + np.sqrt(3. - 2.**(3./2.)) *np.sin(2.*cf*np.pi*T)))
    part3 = (-2.*np.exp(4.*1j*cf*np.pi*T)*T + 2.*np.exp(-(B*T) + 2.*1j*cf*np.pi*T)*T*(np.cos(2.*cf*np.pi*T) - np.sqrt(3. + 2.**(3./2.)) *np.sin(2.*cf*np.pi*T)))
    part4 = (-2.*np.exp(4.*1j*cf*np.pi*T)*T + 2.*np.exp(-(B*T) + 2.*1j*cf*np.pi*T)*T*(np.cos(2.*cf*np.pi*T) + np.sqrt(3. + 2.**(3./2.)) *np.sin(2.*cf*np.pi*T)))
    part5 = (-2. / np.exp(2.*B*T) - 2.*np.exp(4.*1j*cf*np.pi*T) +2.*(1. + np.exp(4.*1j*cf*np.pi*T))/np.exp(B*T))**4.
    gain = np.abs(part1 * part2 * part3 * part4 / part5);

    feedback=np.zeros((len(cf),9));
    forward=np.zeros((len(cf),5));
    forward[:,0] = T**4. / gain;
    forward[:,1] = -4.*T**4.*np.cos(2.*cf*np.pi*T)/np.exp(B*T)/gain;
    forward[:,2] = 6.*T**4.*np.cos(4.*cf*np.pi*T)/np.exp(2.*B*T)/gain;
    forward[:,3] = -4.*T**4.*np.cos(6.*cf*np.pi*T)/np.exp(3.*B*T)/gain;
    forward[:,4] = T**4.*np.cos(8.*cf*np.pi*T)/np.exp(4.*B*T)/gain;
    feedback[:,0] = np.ones(len(cf));
    feedback[:,1] = -8.*np.cos(2.*cf*np.pi*T)/np.exp(B*T);
    feedback[:,2] = 4.*(4. + 3.*np.cos(4.*cf*np.pi*T))/np.exp(2.*B*T);
    feedback[:,3] = -8.*(6.*np.cos(2.*cf*np.pi*T) + np.cos(6.*cf*np.pi*T))/np.exp(3.*B*T);
    feedback[:,4] = 2.*(18. + 16.*np.cos(4.*cf*np.pi*T) + np.cos(8.*cf*np.pi*T))/np.exp(4.*B*T);
    feedback[:,5] = -8.*(6.*np.cos(2.*cf*np.pi*T) + np.cos(6.*cf*np.pi*T))/np.exp(5.*B*T);
    feedback[:,6] = 4*(4. + 3.*np.cos(4.*cf*np.pi*T))/np.exp(6.*B*T);
    feedback[:,7] = -8.*np.cos(2.*cf*np.pi*T)/np.exp(7.*B*T);
    feedback[:,8] = np.exp(-8.*B*T);

    return forward,feedback


def filterbank(b, a, x):
    '''Filters the input array with a bank of filters

    Use y.sum(1) to sum the bands
    '''
    y = np.ones((len(x),b.shape[1]))
    for this in range(b.shape[1]):
        y[:,this] = lfilter(b[:,this],a[:,this],x);
    return y
