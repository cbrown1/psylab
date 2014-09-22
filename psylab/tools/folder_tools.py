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
Helper classes for working with folders and files in less typical ways

"""

import os
import collections
import numpy as np


class cd:
    """Context manager for changing the current working directory
    
        Usage
        -----
        with cd("/new/path") 
            # We are now in the new path
            pass
        # We are now in the previous path
           
        Notes
        -----
        Copy/pasted on 2014-09-07 from:
        http://stackoverflow.com/questions/431684/how-do-i-cd-in-python
    """
    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
    

class concurrent_files:
    """A simple class for retrieving one filename each from several folders. 

        This class tries to make it easy to access files in folders 
        one-each-at-a-time, and to access bits of text associated with each
        filename as needed. The intended use case is if you are running an 
        experiment and need to load in one stimulus from each folder at a time 
        (for each trial), as with the Coordinate-Response Measure set, or the 
        'NewBugs', and you might also want to show some text info about each 
        stimulus, such as keywords etc. 

        Parameters
        ----------
        path_list : list of strings
            A list of the the paths where the files are.
        file_ext : string
            A string of semicolon-separated extensions to mask (eg. '.wav;.WAV'). 
            [Default = all files]
        random : boolean
            Whether to randomize the file order. [default = False]
        repeat : boolean
            Whether to start again if the list is exhausted. [default = False]
        replacement : boolean
            Whether to sample with replacement. If True, 'random' and 'repeat' 
            parameters are ignored (and assumed True). [default = False]
        use : dict
            The keys are basenames from path_list, the vals are lists of 
            filenames to specifically use. If this is specified, only filenames 
            on this list are used and all others are skipped. This overrides 
            skip.
        skip : dict
            The keys are basenames from path_list, the vals are lists of 
            filenames to ignore.
        text_file : string
            the full path to a text file that specifies text for each token.
            There should be one line per token, and the format can be
            specified (see below). Because one textfile is assumed, all 
            filenames must be unique.
        text_format : string
            Indicates the format of the lines in text_file. Should be something 
            like "file,kw,text" where `file` is the only mandatory item, and 
            indicates the position of the filename, which is used as the 
            identifier.

        Usage
        -----
        Assume a folder on your system is stim/ and contains the following subfolders:
            |  1_Names/
            |    01_Bill.wav
            |    02_John.wav
            |    03_Mary.wav
            |  2_Verbs/
            |    01_took.wav
            |    02_had.wav
            |    03_sold.wav
            |  3_Numbers/
            |    01_one.wav
            |    02_two.wav
            |    03_three.wav
            |  4_Objects/
            |    01_clips.wav
            |    02_socks.wav
            |    03_pens.wav
            |  ...

        >>> f = concurrent_files(['stim/1_Names', 
                                  'stim/2_Verb',
                                  'stim/3_Numbers',
                                  'stim/4_Objects'],
                                  use={'1_Names':'01_Bill.wav'} # Only use name Bill
                                  )
        >>> f.get_filenames(fmt='file')
        ['01_Bill.WAV', '01_took.wav', '01_one.wav', '01_clips.wav']
        >>>
    """
    def __init__(self, path_list, 
                 file_ext=None, 
                 skip=None, 
                 use=None,
                 random=False,
                 repeat=False,
                 replacement=False,
                 text_file=None,
                 text_format='file,text'):
        self.path_list = path_list
        if file_ext:
            self.file_ext = file_ext.split(';')
        else:
            self.file_ext = '*'
        self.random = random
        self.repeat = repeat
        self.replacement = replacement
        self.file_dict = collections.OrderedDict()
        self.text_format = text_format
        self.text_file = text_file
        if skip: self.skip = skip
        else: self.skip = {}
        if use: self.use = use
        else: self.use = {}
        for path in path_list:
            name = os.path.basename(path)
            if not name in self.skip.keys():
                self.skip[name] = []
            if not name in self.use.keys():
                self.use[name] = None
                
        for path in path_list:
            name = os.path.basename(path.rstrip(os.sep))
            files = {'files': []}
            for f in os.listdir(path):
                if os.path.isfile(os.path.join(path, f)):
                    if self.file_ext == "*" or os.path.splitext(f)[1].lower() in self.file_ext:
                        if self.use[name]: # If we are using `use`, then only add if filename is specified
                            if f in self.use[name] or os.path.splitext(f)[0] in self.use[name]:
                                files['files'].append(os.path.join(path,f))
                        elif not f in self.skip[name] and not os.path.splitext(f)[0] in self.skip[name]:
                            files['files'].append(os.path.join(path,f))
            self.file_dict[name] = files
            self.reset(name)

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
            else: fileind = 0
            for line in thislist:
                if line != "" and line.lstrip()[0] != "#":
                    thistext = line.split(dlm_toks,len(fmt_toks)-1)
                    self.text[thistext[fileind]] = {}
                    for tkn in fmt_toks:
                        self.text[thistext[fileind]][tkn] = thistext[fmt_toks.index(tkn)].strip()


    def reset(self, name):
        self.file_dict[name]['index'] = -1
        if self.random:
            np.random.shuffle(self.file_dict[name]['files'])
        else:
            self.file_dict[name]['files'].sort()
        

    def get_filenames(self, use=None, skip=None, fmt='full'):
        """ Gets a list of filenames.

            Parameters
            ----------
            use : dict
                A dictionary with keys as list names and vals as lists of 
                filenames. If specified, then only the files listed will be 
                drawn from. You can specify only the list names you want.
            skip : dict
                A dictionary with keys as list names and vals as lists of 
                filenames. If specified, then the files listed will be 
                ignored. You can specify only the list names you want.
            fmt : str
                'file' returns the filename only with no path
                'base' returns the filebase with no path or extension
                'full' returns the full file path (default)
                
            Returns
            -------
            list
                A list of filenames, one from each file list.
        """
        f = []
        for name, files in self.file_dict.iteritems():
            got_file = False
            reset = False

            if use and use.has_key(name):
                if isinstance(use[name], str):
                    this_use = [use[name]]
                else: this_use = use[name]
            else: this_use = files['files']

            if skip and skip.has_key(name):
                if isinstance(skip[name], str):
                    this_skip = [skip[name]]
                else: this_skip = skip[name]
            else: this_skip = []

            while not got_file:
                if self.replacement:
                    # The only time replacement makes sense is if random=True and repeat = True
                    # So don't worry about those parameters
                    files['index'] = np.random.randint(len(files['files']))
                else:
                    files['index'] += 1
                    if files['index'] == len(files['files']):
                        if self.repeat:
                            # Protect against possible infinit loop: no need to reset more than once
                            if reset:
                                raise Exception("'%s' file list contains no allowable files (ie., that are not in skip)!" % name)
                            else:
                                self.reset(name)
                                reset = True
                        else: 
                            raise Exception('%s file list is exhausted!' % name)
                
                filepath = files['files'][files['index']]
                filename = os.path.split(filepath)[1]
                basename = os.path.splitext(filename)[0]
                if filepath in this_use or filename in this_use or basename in this_use:
                    if not filename in this_skip and not basename in this_skip:
                        if fmt == 'full': f.append(filepath)
                        elif fmt == 'base': f.append(basename)
                        else: f.append(filename)
                        got_file = True
        return f

    def get_text(self, file_names=None, item='text', delim=" "):
        """Gets a specified items of text associated with each specified filename.
            If no filenames are specified, the file name of the current indexes are used. 
            The filename extension is optional. The default item is 'text'.

            Parameters
            ----------
            file_names : string
                The name of the file that you want text for. It should be the string used 
                in the text file that you assigned `file` to in your text_format string. 
                However, the function will make several attempts at matching the name, 
                including removing the file extension, etc. [default = current file name]  
            item : string
                The name of the text item you would like. It should be one of the items you
                specified in the text_format argument when you instantiated the class. 
                [default = `text`]
            delim : string
                The character string to separate each token with. [default = " "]
                
            Returns
            -------
            str
                A list of tokens.
        """
        file_keys = []
        if not file_names:
            file_names = []
            for name, files in self.file_dict.iteritems():
                file_names.append(files['files'][files['index']])
        for file_name in file_names:
            if file_name in self.text.keys():  # Try filename as is
                file_keys.append(file_name)
            elif os.path.basename(file_name) in self.text.keys():  # Try stripping path
                file_keys.append(os.path.basename(file_name))
            elif os.path.basename(os.path.splitext(file_name)[0]) in self.text.keys():  # Try stripping both path and extension
                file_keys.append(os.path.basename(os.path.splitext(file_name)[0]))
            elif os.path.join(name,os.path.basename(file_name)) in self.text.keys(): # Try name/filename.ext (1 textfile is used for multiple folders)
                file_keys.append(os.path.join(name,os.path.basename(file_name)))
            else:
                got_file = False
                for ext in self.file_ext:
                    if file_name+ext in self.text.keys(): # Try adding extension, drawn from file_ext
                        file_keys.append(file_name+ext)
                        got_file = True
                        break
                if not got_file:
                    file_keys.append("[[%s]]" % os.path.basename(file_name)) # None found. Use filename.
        if file_keys:
            file_texts =[]
            for key in file_keys:
                if key[:2] == "[[" and key[-2:] == "]]":
                    file_texts.append(key)
                else:
                    file_texts.append(self.text[key][item])
            return delim.join(file_texts)
        else:
            return None


class consecutive_files:
    """A simple class for retrieving filesnames in a folder, one at a time

        This class tries to make it easy to access files in a folder 
        one-at-a-time, and to access bits of text associated with each
        filename as needed. The intended use case is if you are running an 
        experiment and need to load a stimulus in for each trial, you might 
        also want to show some text info about each stimulus, such as 
        keywords etc. 

        Parameters
        ----------
        path : string
            The full path where the files are.
        name : string
            A name to distinuish this set from others. If None, the basename of 
            path will be used.
        file_ext : string
            A string of semicolon-separated extensions to mask (eg. '.wav;.WAV'). 
            [Default = all files]
        file_range : string
            A print-range style string, indicating the file indexes to include. 
            Example: '1:5, 7, 10' would yield [1,2,3,4,5,7,10]. [default = all]
        random : boolean
            Whether to randomize the file order. [default = False]
        repeat : boolean
            Whether to start again if the list is exhausted. [default = False]
        text_file : string
            the full path to a text file that specifies text for each token.
            There should be one line per token, and the format can be
            specified (see below). 
        text_format : string
            Indicates the format of the lines in text_file. Should be something 
            like "file,kw,text" where `file` is the only mandatory item, and 
            indicates the position of the filename which is used as the 
            identifier.

        Usage
        -----
        Assume a folder on your system is /path/to/FCircus and contains the following files:
            |  MP001.wav
            |  MP002.wav
            |  MP003.wav
            |  ...
        And there is a textfile at /path/to/FCircus.txt which looks like this:
            |  MP001,Palin,I came here for an argument.
            |  MP002,Cleese,No you didnt.
            |  MP003,Chapman,Stupid git.
            |  ...

        >>> f = consecutive_files('/path/to/FCircus', text_file='/path/to/FCircus.txt', text_format='file,actor,text')
        >>> f.get_filename() # First call, so you get the first file in the list.
        'MP001.WAV'
        >>> f.get_text() # If you don't specify anything, return the `text` string of the current item.
        'I came here for an argument.'
        >>> f.get_filename(10) # Give me the 10th file in the list
        'MP011.WAV'
        >>> a = f.get_filename(full_path=True) # Now the next one (11th in this case), but with the full path
        >>> a
        '/path/to/files/MP012.WAV'
        >>> f.get_text(a) # You can pass the full path and it will still try to get it right
        'Its being-hit-on-the-head lessons in here.'
        >>> f.get_text('MP003','actor') # Wait, who said `Stupid git`?
        'Chapman'
        >>>
    """
    def __init__(self, path, name='', 
                 file_ext=None, 
                 file_range=None, 
                 skip=[], 
                 use=[], 
                 random=False, 
                 repeat=False, 
                 text_file=None, 
                 text_format='file kw text'):
        self.path = path
        if name == '':
            self.name = os.path.basename(path.rstrip(os.sep))
        else:
            self.name = name
        if file_ext:
            self.file_ext = file_ext.split(';')
        else:
            self.file_ext = '*'
        self.random = random
        self.repeat = repeat
        self.file_list = []
        self.index = -1
        self.index_list = []
        self.text_format = text_format
        self.text_file = text_file
        self.file_range = file_range
        self.n = 0
        self.skip = skip
        self.use = use

        files = (f for f in os.listdir(self.path)
                 if os.path.isfile(os.path.join(self.path, f)))
        ffiles = []
        for f in files:
            fileName, ext = os.path.splitext(f)
            if self.file_ext == '*' or ext.lower() in self.file_ext:
                ffiles.append(f)
        ffiles.sort()

        if self.file_range:
            index_list = self.str_to_range(self.file_range)
            i = 0
            for f in ffiles:
                if i in index_list:
                    self.file_list.append(f)
                i += 1
        else:
            self.file_list = ffiles
        self.index_list = range(len(self.file_list))

        if self.random:
            np.random.shuffle(self.index_list)
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
            else: fileind = 0
            for line in thislist:
                if line != "" and line.lstrip()[0] != "#":
                    thistext = line.split(dlm_toks,len(fmt_toks)-1)
                    self.text[thistext[fileind]] = {}
                    for tkn in fmt_toks:
                        self.text[thistext[fileind]][tkn] = thistext[fmt_toks.index(tkn)].strip()

    def reset(self):
        if self.repeat:
            self.index = -1
            if self.random:
                np.random.shuffle(self.index_list)
        else:
            raise Exception('%s file list is exhausted!' % self.name)

    def get_filename(self, index=None, fmt='full'):
        """ Gets a filename.

            Parameters
            ----------
            index : int
                The index of the desired filename. If unspecified, then index
                is incremented and the next filename in the list is returned 
                (current index+1). If zero or positive, the filename of 
                the specified index is returned. If negative, the filename of the  
                current index is returned (index is unchanged). 
            fmt : str
                'file' returns the filename only with no path (default)
                'base' returns the filebase with no path or extension
                'full' returns the full file path (default)
        """
        if index != 0 and not index:
            self.index += 1
            if self.index == self.n:
                self.reset()
        else:
            if index > -1: # If non-negative, use that index. (Don't change if negative)
                self.index = index
        item = self.file_list[self.index_list[self.index]]
        if fmt == 'full':
            item = os.path.join(self.path,item)
        elif fmt == 'base':
            item = os.path.splitext(item)[0]
        return item

    def get_text(self, file_name=None, item='text'):
        """Gets a specified item of text associated with the specified filename.
            If no filename is specified, the file name of the current index is used. 
            The filename extension is optional. The default item is 'text'.

            Parameters
            ----------
            file_name : string
                The name of the file that you want text for. It should be the string used 
                in the text file that you assigned `file` to in your text_format string. 
                However, the function will make several attempts at matching the name, 
                including removing the file extension, etc. [default = current file name]  
            item : string
                The name of the text item you would like. It should be one of the items you
                specified in the text_format argument when you instantiated the class. 
                [default = `text`]
                
            Returns
            -------
            str
                A token.
        """
        if not file_name:
            file_name = self.file_list[self.index]
        if file_name in self.text.keys():  # Try filename as is
            file_key = file_name
        elif os.path.basename(file_name) in self.text.keys():  # Try stripping path
            file_key = os.path.basename(file_name)
        elif os.path.basename(os.path.splitext(file_name)[0]) in self.text.keys():  # Try stripping both path and extension
            file_key = os.path.basename(os.path.splitext(file_name)[0])
        else:
            for ext in self.file_ext:
                if file_name+ext in self.text.keys(): # Try adding extension, drawn from file_ext
                    file_key = file_name+ext
                    break
        if file_key:
            return self.text[file_key][item]
        else:
            return None

    def str_to_range(self, s):
        """Translate a print-range style string to a list of integers

          The input should be a string of comma-delimited values, each of
          which can be either a number, or a colon-delimited range. 

          >>> str_to_range('1:5, 20, 22')
          [1, 2, 3, 4, 5, 20, 22]
        """
        s = s.strip()
        if s.count(":"):
            tokens = [x.strip().split(":") for x in s.split(",")]
        else:
            tokens = [x.strip().split("-") for x in s.split(",")]

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

        return result


class synched_consecutive_files:
    """Class to create a synchronized group of consecutive_files lists. 
        
        This convenience class allows you to group consecutive_files lists 
        and synchronize their indexes. Thus, when the file index changes for 
        one list, the indexes of the other lists are changed as well. 

        An example usecase is when you are running an experiment and have  
        folders of pre-processed speech stimuli, with each folder  
        representing the same speech set processed in a different condition.  
        In this case, when you change conditions you want to continue with 
        the same index you were using, so as not to repeat the same speech
        tokens. 

        Parameters
        ----------
        *args : tuple
            consecutive_files objects.
        random : bool
            Whether to randomize the lists. Randomization is synchronized, 
            meaning all lists will have the same random order
        repeat : bool
            Whether to repeat the lists when they are exhausted. If random is 
            true, the lists will be re-randomized.

        Examples:
        ---------
        >>> quotes = synched_consecutive_files (
                consecutive_files(
                    path='/path/to/FCircus', 
                    text_file='/path/to/FCircus.txt', 
                    text_format='file,actor,text'
                    file_range='1:100',
                ),

                consecutive_files (
                    path='/path/to/HGrail', 
                    text_file='/path/to/HGrail.txt', 
                    text_format='file,actor,text'
                    file_range='201:300',
                ),
                random=False,
                repeat=False,
            )

        >>> quotes.get_filename('FCircus')
        'FC001.WAV'
        >>> quotes.get_filename('HGrail')
        'HG202.wav'
        >>> quotes.get_text('HGrail','HG202.wav')
        'Strange women lying in ponds distributing swords is no basis for a system of government.'

        Notes
        -----
        All consecutive_files lists must have the same n, anything else will 
        cause an exception since synching file lists with unequal n's doesn't 
        make sense. 
        
        synched_consecutive_files keeps its own index and index_list, and 
        makes calls to consecutive_files always using an index. Thus, the 
        index and index_list data in each consecutive_files instance is 
        unused.
        
        Randomization is also done in a synchronized way. That is, the same 
        random order will be used for each file_list. Set the 'repeat'
        property to True if you would like to recycle (and re-randomize) 
        list items. Remember: If you use the 'random' property of the 
        individual file_lists, the random orders will not be synchronized.

        listPlayer.py is designed to do something similar, along with a simple
        interface to allow you to select conditions (folders) as you go, and it 
        plays the soundfiles as well. Thus, if your stimuli are organized this
        way and you want to run an experiment with minimal effort, listPlayer
        is an easy way to do it. 
        
        TODO: [Newbug] Add skip and use list properties to consecutive files. 
        But how? Reduce file_list on initialize? Or filter during get_filename? 
        skip_list is probably not needed, since it is to allow sampling 
        without replacement, which is built-in currently. How to handle 
        possible unequal n's (eg., due to filtering)?
    """
    def __init__(self, *args, **kwargs):
        self.random = False
        self.repeat = False
        self.group = {}
        self.n = None
        self.index = -1
        for arg in args:
            self.group[arg.name] = arg
        for key, value in kwargs.items():
            if key == 'random':
                self.random = value
            elif key == 'repeat':
                self.repeat = value
            
        n = np.inf
        for name,g in self.group.iteritems():
            if g.n < n:
                if n is not np.inf:
                    raise Exception("synched_consecutive_files members have unequal n's.")
                n = g.n
        self.n = n
        self.index_list = range(self.n)
        if self.random:
            self.randomize()
            
        
    def randomize(self):
        """Use a single random order for all the groups.
            
            Notes
            -----
            This function is called during initialization if the 'random' 
            parameter is set. It simply randomizes the index_list. 
        """
        self.random = True
        np.random.shuffle(self.index_list)


    def get_filename(self, file_list, index=None, fmt='file'):
        """ Gets a filename from the specified `consecutive` list.
            if index is specified, returns that filename. If index is not specified,
            returns the next filename in the list.

            Parameters
            ----------
            file_list : string
                The name of the `consecutive` file list to draw from.
            index : int
                The index of the desired filename. If unspecified, then next filename 
                in the list is returned, and the index will be incremented.
            fmt : str
                'file' returns the filename only with no path (default)
                'base' returns the filebase with no path or extension
                'full' returns the full file path
        """

        if index != 0 and not index: # 0 == None
            if self.repeat and  self.index == self.n-1:
                self.index = 0
                if self.random:
                    self.randomize()
            else:
                self.index += 1
            index = self.index_list[self.index]

        ret = ''
        for name,g in self.group.iteritems():
            if file_list == g.name:
                ret = g.get_filename(index, fmt)
        return ret

    def get_filenames_list(self, index=None, fmt='file'):
        """ Gets a filename from the specified `consecutive` list.
            if index is specified, returns that filename. If index is not specified,
            returns the next filename in the list.

            Parameters
            ----------
            file_list : string
                The name of the `consecutive` file list to draw from.
            index : int
                The index of the desired filename. If unspecified, then next filename 
                in the list is returned, and the index will be incremented.
            fmt : str
                'file' returns the filename only with no path (default)
                'base' returns the filebase with no path or extension
                'full' returns the full file path
        """

        if index != 0 and not index: # 0 == None
            if self.repeat and  self.index == self.n-1:
                self.index = 0
                if self.random:
                    self.randomize()
            else:
                self.index += 1
            index = self.index_list[self.index]

        ret = []
        for name,g in self.group.iteritems():
            ret.append(g.get_filename(index, fmt))
        return ret

    def get_text(self, file_list, file_name=None, item='text'):
        return self.group[file_list].get_text(file_name, item)

    def get_list_names(self):
        return self.group.keys()
