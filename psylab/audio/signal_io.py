# -*- coding: utf-8 -*-

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

def read_audio_file(file_path):
    data,fs = m.read_file(file_path)
    return data,fs

class get_consecutive_files:
    """A simple class for retrieving filesnames in a folder, one at a time

        Usage:
        >>> f = get_consecutive_files(path_to_files)
        >>> f.get_next()
        'AW001.WAV'
        >>> f.get_next()
        'AW002.WAV'
    """
    def reset(self):
        self.index = 0
        if self.random:
            np.random.shuffle(self.file_list)

    def __init__(self, path, file_ext='.wav;.WAV',random=False):
        self.path = path
        self.file_ext = file_ext.split(';')
        self.random = random
        self.file_list = []
        self.index = 0
        files = os.listdir( self.path )

        for f in files:
            fileName, ext = os.path.splitext(f)
            if not os.path.isdir(f) and ext in self.file_ext:
                self.file_list.append(f)
        if self.random:
            np.random.shuffle(self.file_list)
        else:
            self.file_list.sort()
        self.n = len(self.file_list)

    def get_next(self):
        item = self.file_list[self.index]
        self.index += 1
        if self.index == self.n:
            self.reset()
        return item

