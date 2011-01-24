# -*- coding: utf-8 -*-

# Copyright (c) 2008-2010 Christopher Brown; All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
#    * Redistributions of source code must retain the above copyright 
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright 
#      notice, this list of conditions and the following disclaimer in 
#      the documentation and/or other materials provided with the distribution
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
#
# Comments and/or additions are welcome (send e-mail to: c-b@asu.edu).
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
