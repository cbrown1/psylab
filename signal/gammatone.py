# -*- coding: utf-8 -*-

import numpy as np

def gammatone_make(fs,numChannels,loFreq,hiFreq,method='moore'):
    '''
    Computes the filter coefficients for a bank of Gammatone filters.

    Gammatone filters were defined by Patterson and Holdworth for
    simulating the cochlea. The results are returned as arrays of filter
    coefficients. Each row of the filter arrays (forward and feedback)
    can be passed to the scipy "lfilter" function.

    This is a straight-up port of the GammaTone Tool Kit v2.0 by Nick Clark:
    http://www.mathworks.de/matlabcentral/fileexchange/15313-gammatone-tool-kit-v2-0
    '''

    loFreq = max(loFreq, 75);

    if method in ['lyon','stanley']:
        EarQ = 8;       # Lyon + Stanley Parameters (1988)
        minBW = 125;
        order = 2;
    elif method in ['greenwood']:
        EarQ = 7.23824; # Greenwood Parameters (1990) as (nearly) in DSAM
        minBW = 22.8509;
        order = 1;
    elif method in ['moore','glasberg']:
        EarQ = 9.26449; # Glasberg and Moore Parameters (1990)
        minBW = 24.7;
        order = 1;
    elif method in ['wierddsam']:
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

    part1 = (-2.*np.exp(4.*i*cf*np.pi*T)*T + 2.*np.exp(-(B*T) + 2.*i*cf*np.pi*T)*T*(np.cos(2.*cf*np.pi*T) - sqrt(3. - 2.^(3./2.)) *np.sin(2.*cf*np.pi*T)))
    part2 = (-2.*np.exp(4.*i*cf*np.pi*T)*T + 2.*np.exp(-(B*T) + 2.*i*cf*np.pi*T)*T*(np.cos(2.*cf*np.pi*T) + sqrt(3. - 2.^(3./2.)) *np.sin(2.*cf*np.pi*T)))
    part3 = (-2.*np.exp(4.*i*cf*np.pi*T)*T + 2.*np.exp(-(B*T) + 2.*i*cf*np.pi*T)*T*(np.cos(2.*cf*np.pi*T) - sqrt(3. + 2.^(3./2.)) *np.sin(2.*cf*np.pi*T)))
    part4 = (-2.*np.exp(4.*i*cf*np.pi*T)*T + 2.*np.exp(-(B*T) + 2.*i*cf*np.pi*T)*T*(np.cos(2.*cf*np.pi*T) + sqrt(3. + 2.^(3./2.)) *np.sin(2.*cf*np.pi*T)))
    part5 = (-2. / np.exp(2.*B*T) - 2.*np.exp(4.*i*cf*np.pi*T) +2.*(1. + np.exp(4.*i*cf*np.pi*T))/np.exp(B*T))^4.
    gain = np.abs(part1 * part2 * part3 * part4 / part5);

'''
Remaining Matlab code:
gain = abs((-2*exp(4*i*cf*pi*T)*T + 2*exp(-(B*T) + 2*i*cf*pi*T).*T.*(cos(2*cf*pi*T) - sqrt(3 - 2^(3/2))*sin(2*cf*pi*T))) .*(-2*exp(4*i*cf*pi*T)*T +2*exp(-(B*T) + 2*i*cf*pi*T).*T.*(cos(2*cf*pi*T) + sqrt(3 - 2^(3/2)) *sin(2*cf*pi*T))).*(-2*exp(4*i*cf*pi*T)*T +2*exp(-(B*T) + 2*i*cf*pi*T).*T.*(cos(2*cf*pi*T) -sqrt(3 + 2^(3/2))*sin(2*cf*pi*T))) .*(-2*exp(4*i*cf*pi*T)*T+2*exp(-(B*T) + 2*i*cf*pi*T).*T.*(cos(2*cf*pi*T) + sqrt(3 + 2^(3/2))*sin(2*cf*pi*T))) ./(-2 ./ exp(2*B*T) - 2*exp(4*i*cf*pi*T) +2*(1 + exp(4*i*cf*pi*T))./exp(B*T)).^4);
feedback=zeros(length(cf),9);
forward=zeros(length(cf),5);
forward(:,1) = T^4 ./ gain;
forward(:,2) = -4*T^4*cos(2*cf*pi*T)./exp(B*T)./gain;
forward(:,3) = 6*T^4*cos(4*cf*pi*T)./exp(2*B*T)./gain;
forward(:,4) = -4*T^4*cos(6*cf*pi*T)./exp(3*B*T)./gain;
forward(:,5) = T^4*cos(8*cf*pi*T)./exp(4*B*T)./gain;
feedback(:,1) = ones(length(cf),1);
feedback(:,2) = -8*cos(2*cf*pi*T)./exp(B*T);
feedback(:,3) = 4*(4 + 3*cos(4*cf*pi*T))./exp(2*B*T);
feedback(:,4) = -8*(6*cos(2*cf*pi*T) + cos(6*cf*pi*T))./exp(3*B*T);
feedback(:,5) = 2*(18 + 16*cos(4*cf*pi*T) + cos(8*cf*pi*T))./exp(4*B*T);
feedback(:,6) = -8*(6*cos(2*cf*pi*T) + cos(6*cf*pi*T))./exp(5*B*T);
feedback(:,7) = 4*(4 + 3*cos(4*cf*pi*T))./exp(6*B*T);
feedback(:,8) = -8*cos(2*cf*pi*T)./exp(7*B*T);
feedback(:,9) = exp(-8*B*T);
'''