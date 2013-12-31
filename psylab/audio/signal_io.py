# -*- coding: utf-8 -*-
"""
Helper functions for reading audio data in less typical ways

"""

import os
import glob
import numpy as np
import medussa as m

def read_multi_file (folder, file_base, file_ext):
    """Reads audio data split across mulitple files
        
        A typical use case is audio with more than 8 channels
        saved in flac format, which is limited to 8 channels per
        file. So these data would thus be saved to multiple files.
        
        Function assumes a file format similar to:
        
            track01_1.flac
            track01_2.flac
            track01_3.flac
        
        That is, assumes that the file counter is the last part 
        of the file base name, and that the first file contains 
        the first set of audio channels, etc.. In the example, 
        the function will read in all three of these files, and 
        you would pass 'track01' as the file_base parameter, and 
        '.flac' as the file_ext parameter. 
    
    
    """
    files = glob.glob(os.path.join(folder,file_base+'*'+file_ext))
    files.sort()
    y = np.array(())
    for file_path in files:
        this_data,fs = m.read_file(file_path)
        if y.ndim==1:
            y = this_data
        else:
            y = np.concatenate((y,this_data),axis=1)
    return y
    