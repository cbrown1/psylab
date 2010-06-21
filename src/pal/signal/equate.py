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

import os
import numpy as np

from waveio import wavread, wavwrite
from rms import rms

def equate(indir, reloutdir="norm", ext='wav'):
    '''Equates wavefiles in rms
        
        Batch process all wavefiles in a directory (or a 
        list of directories). The lowest rms value is found
        and all files are scaled to that. Only tested with 
        1-channel soundfiles.
      
        Parameters
        ----------
        indir : string, or list of strings
            Directories to process. 
        reloutdir : string
            The subdirectory name to save processing files to.
            This should be relative. It will be appended to indir
        ext : string
            File extension masks, comma separated
        
        Returns
        -------
        ret : tuple
            ret[0] is the lowest rms value, ret[1] is the last 
            filename where that value occurred.
    '''

    if isinstance( indir, str ):
        indir = [ indir ];
    elif not isinstance( indir, list ):
        print "Indir must be either a string or a list of strings";
        return
    else:
        for item in indir:
            if not isinstance( item, str ):
                print "Indir must be either a string or a list of strings";
                return

    if ext is not None:
        exts = ext.split( "," )
        for n in range( 0, len(exts) ):
            exts[n] = exts[n].lower()
            if exts[n][0] != ".":
                exts[n] = "." + exts[n]
    target = 1.;
    targetfile = '';
    goodpaths = []; # When writing, use only 'good' paths 
    
    # Analysis
    for filepath in indir:
        if not os.path.exists( filepath ):
            print "Invalid path, skipping: " + filepath;
            break;
        else:
            goodpaths.append(filepath);
        files = os.listdir(filepath)
        for fname in files:
            filename, fileext = os.path.splitext( fname )
            if ext is None or fileext.lower() in exts:
                filefull = os.path.join(filepath,fname);
                data,fs = wavread(filefull);
                thisrms = rms(data);
                if thisrms < target:
                    target = thisrms;
                    targetfile = fname

    # Processing
    for filepath in goodpaths:
        files = os.listdir(filepath)
        if not os.path.exists(os.path.join( filepath, reloutdir )):
            os.makedirs(os.path.join( filepath, reloutdir ))
        for fname in files:
            filename, fileext = os.path.splitext( fname )
            if ext is None or fileext.lower() in exts:
                filefull = os.path.join( filepath, fname );
                outfull = os.path.join( filepath, reloutdir, fname );
                data,fs = wavread(filefull);
                data = data * (target / rms(data));
                wavwrite( data, fs, outfull );

    return target,targetfile;
    