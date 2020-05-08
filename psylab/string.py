# -*- coding: utf-8 -*-

# Copyright (c) 2010-2020 Christopher Brown
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
# contributions are welcome. Go to http://github.com/cbrown1/psylab/ 
# for more information and to contribute. Or send an e-mail to: 
# cbrown1@pitt.edu.
#

#from functools import reduce
import numpy as np

def str_to_list(s, unique=True):
    """Translate a print-range style string to a list of integers

      The input should be a string of comma-delimited values, each of
      which can be either a number, or a colon-delimited range. If the
      first token in the list is the string "random" or "r", then the
      output list will be randomized before it is returned ("r,1:10").

      >>> str_to_list('1:5, 20, 22')
      [1, 2, 3, 4, 5, 20, 22]
    """
    s = s.strip()
    randomize = False
    tokens = [] # List of tuples of length 1 or 2
    for x in s.split(","):
        if x.count(":"):
            tokens.append(x.strip().split(":"))
        elif x.count("-"):
            tokens.append(x.strip().split("-"))
        else:
            if len(x) > 0: # Item could be empty
                tokens.append( (x.strip()) )

    # if s.count(":"):
    #     tokens = [x.strip().split(":") for x in s.split(",")]
    # else:
    #     tokens = [x.strip().split("-") for x in s.split(",")]

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
                return [int(x[0])]
        elif len(x) == 2:
            a,b = x
            return range(int(a), int(b)+1)
        else:
            raise ValueError

    result = list()
    for tok in tokens:
        result += parse(tok)

    if randomize:
        np.random.shuffle(result)
    
    if unique:
      return list(set(result))
    else:
      return result


def list_to_str(data):
    """Translate a list of integers to a print-range style string

      The input should be a list or array of integers, and the output
      will be a string of comma-delimited values, each of
      which will be either a number, or a colon-delimited range.

      >>> list_to_str([1,2,3,4,12,14,15,16])
      '1:4,12,14:16'
    """
    data = np.array(data)
    runs = np.split(data, np.where(np.diff(data) != 1)[0]+1)
    str = []
    for run in runs:
        if run.size == 1:
            str.append("{:}".format(run[0]))
        else:
            str.append("{:}:{:}".format(run[0], run[-1]))
    return ",".join(str)


class reverse_template():

    def __init__(self):
        pass

    def find_nth(self, haystack, needle, n=0, overlap=False):
        """ Find the nth occurence of a substring in a string

            Parameters
            ----------
            haystack : str
                The string to extract info from 
            needle : str
                The substring to find
            n : int
                Which occurence of needle to find. 0 is the first
            overlap : bool
                Whether to search using overlap
            
            Returns
            -------
            ret : int
                The position of the nth occurence of the needle in haystack

        """
        l = 1 if overlap else len(needle)
        i = -l
        for c in range(n + 1):
            i = haystack.find(needle, i + l)
            if i < 0:
                break
        return i

    def get_negative_text(self, haystack, needles):

        """Returns a list of the strings from haystack that occur between each string in needle list

            ie., if haystack is 'one///two|||three~~~'
            and needles was ['one', 'two', 'three']
            this function would return ['///', '|||', '~~~']

            This is intended for extracting text from formatted strings, since
            running this function twice can be used for reverse templating by
            passing the output from the first pass as the variables in a second pass


                vars = ['var1', 'var2', 'var3']
                template = "var1 - some unwanted text - var2 || more uninteresting text @@@ var3"
                text = "here is important text - some unwanted text - here is text bit 2 || more uninteresting text @@@ and the third interesting bit"
                ivs = get_negative_text(template, vars)
                # ivs == [ - some unwanted text - ', '2 || more uninteresting text @@@ ']
                interesting_only = get_negative_text(text, ivs)
                # interesting_only == ['here is important text', 'here is text bit 2', 'and the third interesting bit']
        """

        # Get locations of each needle in the haystack
        var_locs = []
        var_strs = []
        occurences = {}
        for needle in needles:
            occurences[needle] = []
            found = True
            n=0
            while found:
                this_i = self.find_nth(haystack, needle, n)
#                print("FOUND: {:}: {}".format(this_i, needle))
                var_locs.append(this_i)
                var_strs.append(needle)
                n += 1
                if this_i == -1:
                    found = False

#        print("var_locs:")
#        print(var_locs)
#        print("var_strs:")
#        print(var_strs)
        # Sort vars as they appear in haystack
        vl_temp=[] 
        for i in range(len(var_locs)): 
            vl_temp.append((var_locs[i],i)) 
        vl_temp.sort() 
        var_index = [] 
        for x in vl_temp:
            var_index.append(x[1])
#        print("VARIABLES: {}".format(needles))
#        print("VAR_INDEX: {}".format(var_index))
#        print("TEMPLATE: {}".format(haystack))
        
        # Generate sorted list of vars and locs
        var_locs_local = []
        var_strs_local = []
        for i in var_index:
            if var_locs[i] > -1:
                var_locs_local.append(var_locs[i])
                var_strs_local.append(var_strs[i])
#                print("SORTED loc: {:}; str: {}".format(var_locs[i], var_strs[i]))

#        print("SORTED LOCS: {}".format(var_locs_local))
#        print("SORTED STRS: {}".format(var_strs_local))
        # Good to here

        # Pull subtext from string between each var
        intertext = [] # list of segments of text between vars
        intertext_start = 0
        intertext_stop = var_locs_local[0]
        if intertext_stop > intertext_start:
#            print("Got init intertext: {}".format(haystack[intertext_start:intertext_stop]))
            intertext.append(haystack[intertext_start:intertext_stop])
        for var_i in range(len(var_locs_local)-1):
            if len(var_strs_local[var_i]) > 0:
                intertext_start = var_locs_local[var_i] + len(var_strs_local[var_i])
                intertext_stop = var_locs_local[var_i + 1]
                if intertext_stop > intertext_start:
#                    print("Got intertext: {}".format(haystack[intertext_start:intertext_stop]))
                    intertext.append(haystack[intertext_start:intertext_stop])
        if var_locs_local[-1] + len(var_strs_local[-1]) < len(haystack):
#            print("Got end intertext: {}".format(haystack[var_locs_local[-1] + len(var_strs_local[-1]):]))
            intertext.append(haystack[var_locs_local[-1] + len(var_strs_local[-1]):])

        return(intertext, var_strs_local)


    def process(self, text, template, variables):
        """Extracts bits of text from a string based on a template

            text is the haystack to search in
            template describes which bits of text to extract from, and how they are 
            situated in haystack variables is a list of the variable names to use in 
            template

            the reason for the variables var is that it allows any arbitrary
            variable format to be used

            Parameters
            ----------
            text : str
                The string to extract info from 
            template : str
                The template to use, indicating the layout in the text string
            variables : list of str
                A list of the variables used in template
            
            Returns
            -------
            ret : list of 2-element tuples
                Element one of each tuple is a variable name, element 2 is the corresponding text

        """ 

        delims,vars_used = self.get_negative_text(template, variables)
        vals,v_ = self.get_negative_text(text, delims)
        return list(zip(vars_used, vals)) # List of tuples in case of duplicate keys

