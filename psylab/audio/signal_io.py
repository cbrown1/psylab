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

        This class also allows you to load bits of text associated with each
        filename as needed. The intended use case is if you are loading stimuli 
        in one at a time for an experiment, you might want to show info 
        about each stimulus, such as keywords etc. 

        Parameters
        ----------
        path : string
            The full path where the files are.
        file_ext : string
             A string of semicolon-separated extensions [default = '.wav;.WAV'].
        file_range : string
            A print-range style string, indicating the files to include. 
            Example: '1:5, 7, 10' [default = all].
        random : boolean
            Whether to randomize the file order.
        repeat : boolean
            Whether to start again if the list is exhausted.
        text_file : string
            the full path to a text file that specifies text for each token.
            There should be one line per token, and the format can be
            specified (see below). 
        text_format : string
            Indicates the format of the lines in text_file. Should be something 
            like "file,kw,text" where `file` is the only mandatory item, and 
            indicates the position of the filename (file extensions are optional). So
            eg., if a line in your text file is: "AW001,Palin,I came here for an argument." 
            and you set text_format to "file,actor,text", then if you call 
            get_text('AW001', 'text'), it would return 'I came here for an argument.'
            Hint: The get_text function accepts a default item of 'text', so in the 
            example get_text('AW001') would yield the same result.

        Functions
        ---------
        get_next()
            Returns the next filename in the list.
        get_filename(ind)
            Returns the filename in the list specified by the index ind.
        get_text(filename, [item])
            Returns text for the specified filename. [Default item = 'text']

        Usage
        -----
        >>> f = get_consecutive_files(path_to_files)
        >>> f.get_next()
        'AW001.WAV'
        >>> f.get_next()
        'AW002.WAV'
        >>> f.get_text('AW001')
        'The BIRCH CANOE SLID on the SMOOTH PLANKS.'
        >>>
    """
    def reset(self):
        if self.repeat:
            self.index = 0
            if self.random:
                np.random.shuffle(self.file_list)
        else:
            raise Exception('File list is exhausted!')

    def __init__(self, path, file_ext='.wav;.WAV', file_range=None, random=False, repeat=False, text_file=None, text_format='file kw text'):
        self.path = path
        self.file_ext = file_ext.split(';')
        self.random = random
        self.repeat = repeat
        self.file_list = []
        self.index = 0
        self.text_format = text_format
        self.text_file = text_file
        self.file_range = file_range

        files = os.listdir( self.path )
        files.sort()
        n = len(files)
        if file_range:
            self.range = self.str_to_range(file_range)
        else:
            self.range = range(n)

        i = 0
        for f in files:
            if i in self.range:
                fileName, ext = os.path.splitext(f)
                if not os.path.isdir(f) and ext in self.file_ext:
                    self.file_list.append(f)
            i += 1
        if self.random:
            np.random.shuffle(self.file_list)
        else:
            self.file_list.sort()
        self.n = len(self.file_list)

        # Text
        if self.text_file:
            dlm_toks = ','
            if self.text_format.find(dlm_toks) != -1:
                fmt_toks = self.text_format.split(dlm_toks)
            else:
                fmt_toks = self.text_format.split(' ')
                dlm_toks = ' '
            thislisth = open(self.text_file, 'r')
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
        if self.index == self.n:
            self.reset()
        item = self.file_list[self.index]
        self.index += 1
        return item

    def get_filename(self, ind):
        """ Gets the filename specified by ind
        """
        self.index = ind
        if self.index == self.n:
            self.reset()
        item = self.file_list[self.index]
        self.index += 1
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


    def str_to_range(self, s):
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

