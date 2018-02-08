# -*- coding: utf-8 -*-

# Copyright (c) Matt Gouppel
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

import numpy as np

def apply_itd( signal, fs, itd ):
    '''Applies an interaural time difference to a signal

        Convenience function to apply an itd to a signal. Accepts both 1d and 
        2d (shape[1] == 2) input arrays, although the output is always 2d.

        Positive itd values will result in right-leading output signal (delay 
        to left channel) and negative itds will result in left-leading signals.

        Parameters
        ----------
        signal : array
            The input signal. The shape can be (n,) or (n,2) [ie, mono or 
            stereo].
        fs : scalar
            The sampling frequency.
        itd : scalar
            The itd to apply, in µs.

        Returns
        -------
        out : 2d array
            The input signal, with the specified itd applied.
            
        Examples
        --------
        >>> a = np.ones(5)
        >>> apply_itd(a,5,400000)
        array([[ 0.,  1.],
               [ 0.,  1.],
               [ 1.,  1.],
               [ 1.,  1.],
               [ 1.,  1.],
               [ 1.,  0.],
               [ 1.,  0.]])
        >>> apply_itd(a,5,-200000)
        array([[ 1.,  0.],
               [ 1.,  1.],
               [ 1.,  1.],
               [ 1.,  1.],
               [ 1.,  1.],
               [ 0.,  1.]])
        >>> 
    '''
    # Compute delay in samples
    itd_samp = np.int32(np.round((np.float32(np.abs(itd))/1000000.)*np.float32(fs)))
    delay = np.zeros(itd_samp)

    # Ensure 2d
    if len(signal.shape) == 1:
        sig = np.vstack((signal, signal)).T
    else:
        sig = signal

    # Generate output array of correct shape
    out = np.zeros((signal.shape[0]+itd_samp,2))
    
    # Apply itd
    if itd > 0 :
        out[:,0] = np.hstack((delay, sig[:,0]))
        out[:,1] = np.hstack((sig[:,1], delay))
    else:
        out[:,0] = np.hstack((sig[:,0], delay))
        out[:,1] = np.hstack((delay, sig[:,1]))

    return out
    

def apply_ild(signal, ild):
    '''Applies an interaural level difference to a signal

        Convenience function to apply an ild to a signal. Accepts both 1d and 
        2d (shape[1] == 2) input arrays, although the output is always 2d.

        The ild is applied by always attenuating one or the other channel
        (ie, positive gain is never applied).

        Positive ild values will result in right-leading output signal 
        (attenuation to left channel) and negative ilds will result in 
        left-leading signals.

        Parameters
        ----------
        signal : array
            The input signal. The shape can be (n,) or (n,2) [ie, mono or 
            stereo].
        ild : scalar
            The ild to apply, in dB.

        Returns
        -------
        out : 2d array
            The input signal, with the specified ild applied.
            
        Examples
        --------
        >>> a = np.ones(5)
        >>> apply_ild(a,6)
        array([[ 0.50119163,  1.        ],
               [ 0.50119163,  1.        ],
               [ 0.50119163,  1.        ],
               [ 0.50119163,  1.        ],
               [ 0.50119163,  1.        ]])
        >>> apply_ild(a,-12)
        array([[ 1.        ,  0.25119305],
               [ 1.        ,  0.25119305],
               [ 1.        ,  0.25119305],
               [ 1.        ,  0.25119305],
               [ 1.        ,  0.25119305]])
        >>> 
    '''

    # Ensure 2d
    if len(signal.shape) == 1:
        out = np.vstack((signal, signal)).T
    else:
        out = signal
    
    # Apply ild
    if ild > 0 :
        out[:,0] = out[:,0] * np.exp(np.float32(-np.abs(ild))/8.6860)
    else:
        out[:,1] = out[:,1] * np.exp(np.float32(-np.abs(ild))/8.6860)

    return out
    

def gso(signal, rho):
    """Varies the inter-aural correlation of a stereo signal
        by performing Gram-Schmidt orthogonalization

        This does not work with diotic input signals. That is, 
        this function correlates signals that are uncorrelated,
        not the opposite.
        
        Parameters
        ----------
        signal : array
            The input signal. shape[1] == 2.
        rho : scalar
            The target cross-correlation. Should be 0 <= 1.
       
        Returns
        -------
        y : array
            The correlated signal.

        Notes
        -----
        Adapted from matlab code provided by Matt Goupell
    """
    
    xL = signal[:,0]
    xR = signal[:,1]

    y = np.zeros_like(signal)

    Lrms = np.sqrt(np.mean(xL**2.))
    Rrms = np.sqrt(np.mean(xR**2.))
    num = np.mean(xL*xR)
    dem = Lrms * Rrms
    rhoLR = num / dem
    factor1 = Lrms/(Rrms*np.sqrt(1.-rhoLR**2.))
    factor2 = rhoLR/np.sqrt(1.-rhoLR**2.)
    xRstar = factor1*xR-factor2*xL
    
    alpha = np.sqrt(1-rho**2.)
    y[:,0] = xL;
    y[:,1] = rho * xL + alpha * xRstar

    return y
    
