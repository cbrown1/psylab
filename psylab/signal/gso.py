# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 14:50:41 2013

@author: code-breaker
"""

import numpy as np

def gso(sig, rho):
    """Varies the inter-aural correlation of a stereo signal
        by performing Graham-Schmidt Orthogonalization
        
        Parameters
        ----------
        sig : array
            The input signal.
        rho : scalar
            The target cross-correlation. Should be 0 <= 1.
        
        Returns
        -------
        y : array
            The noise.

        Notes
        -----
        Adapted from matlab code provided by Matt Goupell
    """
    
    xL = sig[:,0]
    xR = sig[:,1]

    y = np.zeros(shape(sig))

    Lrms = np.sqrt(np.mean(xL**2))
    Rrms = np.sqrt(np.mean(xR**2))
    num = np.mean(xL*xR)
    dem = Lrms * Rrms
    rhoLR = num / dem
    
    factor1 = Lrms/(Rrms*np.sqrt(1-rhoLR**2))
    factor2 = rhoLR/np.sqrt(1-rhoLR**2)
    xRstar = factor1*xR-factor2*xL
    
    alpha = np.sqrt(1-rho**2.)
    y[:,0] = xL;
    y[:,1] = rho * xL + alpha * xRstar

    return y