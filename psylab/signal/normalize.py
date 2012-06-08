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
# along with Psylab.  If not, see <http://www.gnu.org/licenses/>.
#
# Bug reports, bug fixes, suggestions, enhancements, or other 
# contributions are welcome. Go to http://code.google.com/p/psylab/ 
# for more information and to contribute. Or send an e-mail to: 
# cbrown1@pitt.edu.
#

import os
import numpy as np

from scipy.io.wavfile import read as wavread, write as wavwrite

def normalize(indir, reloutdir="norm", ext='wav'):
    '''Normalizes wavefiles, so that the overall peak is 1
      
        Batch process all wavefiles in a directory (or a 
        list of directories). A single peak value is found
        and all files are normalized using that. Only tested 
        with 1-channel soundfiles.
        
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
            ret[0] is the peak value, ret[1] is the last filename 
            where the peak occurred.
        
        Notes
        -----
        See also: equate
    '''

    if isinstance( indir, str ):
        indir = [ indir ]
    elif not isinstance( indir, list ):
        print("Indir must be either a string or a list of strings")
        return
    else:
        for item in indir:
            if not isinstance( item, str ):
                print("Indir must be either a string or a list of strings")
                return

    if ext is not None:
        exts = ext.split( "," )
        for n in range( 0, len(exts) ):
            exts[n] = exts[n].lower()
            if exts[n][0] != ".":
                exts[n] = "." + exts[n]
    peak = 0.
    peakfile = ''
    goodpaths = [] # When writing, use only 'good' paths 
    
    # Analysis
    for filepath in indir:
        if not os.path.exists( filepath ):
            print("Invalid path, skipping: " + filepath)
            break
        else:
            goodpaths.append(filepath)
        files = os.listdir(filepath)
        for fname in files:
            filename, fileext = os.path.splitext( fname )
            if ext is None or fileext.lower() in exts:
                filefull = os.path.join(filepath,fname)
                data,fs = wavread(filefull)
                thispeak = np.max(np.abs(data))
                if thispeak > peak:
                    peak = thispeak
                    peakfile = filefull

    # Processing
    for filepath in goodpaths:
        files = os.listdir(filepath)
        if not os.path.exists(os.path.join( filepath, reloutdir )):
            os.makedirs(os.path.join( filepath, reloutdir ))
        for fname in files:
            filename, fileext = os.path.splitext( fname )
            if ext is None or fileext.lower() in exts:
                filefull = os.path.join( filepath, fname )
                outfull = os.path.join( filepath, reloutdir, fname )
                data,fs = wavread(filefull)
                data = data / peak
                wavwrite( data, fs, outfull )

    return peak,peakfile
    
