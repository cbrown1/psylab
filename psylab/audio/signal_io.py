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

        When the class is created, the input arguments are:

        path : The full path with the files are
        file_ext : A string of semicolon-separated extensions [default = '.wav;.WAV']
        random : A boolean specifying whether to randomize the file list [default = False]
        index : The starting index, if you want to skip some of the files. Not very 
                useful if you are randomizing the list. [default = 0]
        textfile : Path to a text file with text associated with each token. 
                    Each line should have text for a single filename. One of the items
                    should be the filename itself.
        textformat : Indicates the format of each line. Should be something like 
                     "file,kw,text" where `file` indicates the position of the filename 
                     (file extensions are optional). 

        Usage:
        >>> f = get_consecutive_files(path_to_files)
        >>> f.get_next()
        'AW001.WAV'
        >>> f.get_next()
        'AW002.WAV'
        >>> f.get_text('AW001')
        'The BIRCH CANOE SLID on the SMOOTH PLANKS.'
        >>>

        TODO: Add support for print-style ranges (str_to_range function is below)
    """
    def reset(self):
        self.ind = self.index
        if self.random:
            np.random.shuffle(self.file_list)

    def __init__(self, path, file_ext='.wav;.WAV', file_range=None, random=False, index=0, textfile=None, textformat='file kw text'):
        self.path = path
        self.file_ext = file_ext.split(';')
        self.random = random
        self.file_list = []
        self.index = index
        self.ind = index
        self.textformat = textformat
        self.textfile = textfile

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

        # Text
        if self.textfile:
            dlm_toks = ','
            if self.textformat.find(dlm_toks) != -1:
                fmt_toks = self.textformat.split(dlm_toks)
            else:
                fmt_toks = self.textformat.split(' ')
                dlm_toks = ' '
            thislisth = open(textfile, 'r')
            thislist = thislisth.readlines()
            thislisth.close()
            self.text = {}
            if 'file' in fmt_toks:
                fileind = fmt_toks.index('file')
            for line in thislist:
                if line != "" and line.lstrip()[0] != "#":
                    thistext = line.split(dlm_toks,len(fmt_toks)-1)
                    self.text[thistext[0]] = {}
                    for tkn in fmt_toks:
                        self.text[thistext[0]][tkn] = thistext[fmt_toks.index(tkn)].strip()

    def get_next(self):
        """ Gets the next filename in the list
        """
        item = self.file_list[self.ind]
        self.ind += 1
        if self.ind == self.n:
            self.reset()
        return item

    def get_filename(self, ind):
        """ Gets the filename specified by ind
        """
        self.ind = ind
        if self.ind == self.n:
            self.reset()
        item = self.file_list[self.ind]
        self.ind += 1
        if self.ind == self.n:
            self.reset()
        return item

    def get_text(self, filename, item='text'):
        """Gets a specified text item associated with the specified filename
            Filename extension is optional. 
        """
        if filename in self.text.keys(): # Check filename as entered
            filekey = filename
        elif os.path.splitext(filename)[0] in self.text.keys():  # Check file basename
            filekey = os.path.splitext(filename)[0]
        if not filekey:
            for ext in self.file_ext:
                if filename+ext in self.text.keys(): # Check filename with extensions
                    filekey = filename+ext
                    break
        if filekey:
            return self.text[filekey][item]
        else:
            return None


    def str_to_range(s):
        """Translate a print-range style string to a list of integers

          The input should be a string of comma-delimited values, each of
          which can be either a number, or a colon-delimited range. If the
          first token in the list is the string "random" or "r", then the
          output list will be randomized before it is returned ("r,1:10").

          >>> str_to_range('1:5, 20, 22')
          [1, 2, 3, 4, 5, 20, 22]
        """
        s = s.strip()
        randomize = False
        tokens = [x.strip().split(":") for x in s.split(",")]

        if tokens[0][0] in ["random","r","rand"]:
            randomize = True
            tokens = tokens[1:]

        # Translate ranges and enumerations into a list of int indices.
        def parse(x):
            if len(x) == 1:
                if x == [""]:  # this occurs when there are trailing commas
                    return []
                else:
                    #return map(int, x)
                    return [int(x[0])-1]
            elif len(x) == 2:
                a,b = x
                return range(int(a)-1, int(b))
            else:
                raise ValueError

        result = reduce(list.__add__, [parse(x) for x in tokens])

        if randomize:
            np.random.shuffle(result)

        return result

