# -*- coding: utf-8 -*-

# Copyright (c) 2013 Christopher Brown
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

"""listPlayer - Standalone script to play blocks of soundfiles in folders

Useful if you preprocess all your stimuli, and have a folder for each 
condition in your experiment. Run this script from the root (where all the 
condition folders are) with no options and you can choose a condition 
(folder) at a time, and 10 tokens will be run, followed by another menu. 
If you choose another condition, the next 10 tokens will be run in that 
condition, and so on. 

The type of experimental design that this is useful for is when you want to
randomize the presentation order of your conditions, but present the 
particular stimuli (eg., speech) in the same order across subjects. You would 
preprocess the same set of stimuli in all conditions, and save the output to 
separate folders. In this case, listPlay can be used to easily present the 
conditions in a particular order (ie., you could select each condition at 
random), and it will automatically step through the stimuli in the correct
order across all conditions.

Parameters
----------
  folder [-f] : Rel or abs path to condition subfolders. default = '.'
    skip [-s] : The number of tokens to skip. default = 0
       n [-n] : The number of tokens to run per condition. default = 10
filemask [-m] : Semicolon-delimited case-insensitive filemask list.
                 default = .wav

Examples:
listPlayer.py
listPlayer.py --folder=/path/to/conditionFolders
listPlayer.py --folder=/path/to/conditionFolders --skip=100 --n=20
listPlayer.py --folder=/path/to/conditionFolders --filemask=.wav;.flac

Dependencies
------------
medussa [http://medussa.googlecode.com]
"""

import os
import sys
import getopt
import medussa


def getFileList(directory, fileExtList=[]):
    """Returns a list of files of particular extensions in a folder
    """
    fileList = [os.path.normcase(f) for f in os.listdir(directory)]
    if len(fileExtList)>0:
        fileList = [os.path.join(directory, f) for f in fileList if os.path.splitext(f)[1].lower() in fileExtList]
    fileList.sort()
    return fileList

    
def getSubList(folder):
    """Returns a list of subfolders in a folder
    """
    flist= [name for name in os.listdir(folder)
            if os.path.isdir(os.path.join(folder, name))]
    flist.sort()
    return flist

    
def chooseFolder(folder):
    """Shows a menu of subfolders, allows user to choose one
    """
    flist = getSubList(folder)
    for i,f in enumerate(flist):
        print("%i) %s" % (i, f))
    print("q) quit")
    ret = raw_input("Select: ")
    if ret in ['q']:
        return None
    elif ret.isdigit():
        iret = int(ret)
        if iret < len(flist):
            return flist[iret]


def playSoundFiles(folder, skip, n, filemask, done):
    """Plays a block of soundfiles in a folder, given 'skip' and 'n'
        where 'skip' is the number of soundfiles to skip, and 'n' is the 
        number of soundfiles to play. User hits enter to move to the next 
        soundfile, hits 'r' to repeat the current soundfile, or 'q' to quit.
    """
    d=medussa.open_default_device()
    files = getFileList(folder,filemask)
    base = os.path.basename(folder)
    print("%s: %i files remaining" % (base, len(files)-skip))
    keepGoing = True
    i = 0
    #while keepGoing:
    for filename in files[skip:skip+n]:
        repeat = True
        i = i + 1
        (fpath, fname) = os.path.split(filename)
        if not os.path.isdir (filename):
            s = d.open_file(filename)
            while repeat:
                s.play()
                r = raw_input(" %i) %s, \'r\'epeat, \'q\'uit: " % (done+i, fname))
                if r.strip() in ['q']:
                    repeat = False
                    keepGoing = False
                elif r.strip() in ['r']:
                    repeat = True
                else:
                    repeat = False
        if not keepGoing: break            
    return keepGoing


def run(folder, skip=0, n=10, filemask=['.wav']):
    """The main listPlayer function. Use this to run an experiment. 
        
        Parameters
        ----------
        folder: string
        skip: scalar
            The number of tokens to skip. default = 0
        n : scalar
            The number of tokens to run per condition. default = 10
        filemask : list of strings
            A case-insensitive filemask list. default = ['.wav']
    
        Notes
        -----
        listPlayer.run() #Run from the current folder with default vaues
        #Specify a folder, a number of tokens to skip, and a token number to start with:
        listPlayer.run(folder, skip, n) 
    """
    done = 0
    keepGoing = True
    afolder = os.path.abspath(folder)
    while keepGoing:
        sub = chooseFolder(afolder)
        if sub is None:
            keepGoing = False
        else:
            keepGoing = playSoundFiles(os.path.join(afolder,sub), skip, n, filemask, done)
            skip = skip + n
            done = done + n


if __name__ == '__main__':
    folder = '.'
    skip = 0
    n = 10
    filemask = ['.wav']
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:s:n:m:", ["help", "folder=", "skip=", "n=", "filemask="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for var, val in opts:
        if var in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        elif var in ["--folder", "-f"]:
            folder = val
        elif var in ["--skip", "-s"]:
            skip = int(val)
        elif var in ["--n", "-n"]:
            n = int(val)
        elif var in ["--filemask", "-m"]:
            n = var.split(';')
    run(folder, skip, n)
