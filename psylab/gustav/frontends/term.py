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
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# Comments and/or additions are welcome. Send e-mail to: cbrown1@pitt.edu.
#

import Tkinter
import tkFileDialog, tkSimpleDialog, tkMessageBox
import os

name = 'term'

def show_config(exp,run,var,stim,user):
    print "Sorry, there is no terminal version of the Experiment Configuration Dialog."

def get_file(parent=None, title = 'Open File', default_dir = "", file_types = ("All files (*.*)")):
    """Opens a file dialog, returns file path as a string

        To specify filetypes, use the (qt) format:
        "Python or Plain Text Files (*.py *.txt);;All files (*.*)"
    """
    ftl = file_types.split(";;")
    fts = []
    for ft in ftl:
        d,t = ft.split("(")
        fts.append(tuple([d," ".join(t.strip(" )").split())]))
    toplevel=Tkinter.Tk()
    toplevel.withdraw()
    fname = tkFileDialog.askopenfilename( title = title, initialdir = default_dir, filetypes = fts, multiple = False)
    toplevel.deiconify()
    toplevel.destroy()
    if isinstance(fname, tuple):
        # you suck tk
        return ''
    else:
        return fname

def get_folder(parent=None, title = 'Open Folder', default_dir = ""):
    """Opens a folder dialog, returns the path as a string
    """
    toplevel=Tkinter.Tk()
    toplevel.withdraw()
    fname = tkFileDialog.askdirectory( title = title, initialdir = default_dir )
    toplevel.deiconify()
    toplevel.destroy()
    if isinstance(fname, tuple):
        return ''
    else:
        return fname

def get_item(parent=None, title = 'User Input', prompt = 'Choose One:', items = [], current = 0, editable = False):
    """Opens a simple prompt to choose an item from a list, returns a string
    """
    for ind, item in enumerate(items):
        print " ",ind+1,". ", item
    ret = raw_input(prompt)
    if ret != '':
        ind = int(ret)-1
        if ind < len(items):
            return items[ind]
        else:
            return ""
    else:
        return ""


def get_yesno(parent=None, title = 'User Input', prompt = 'Yes or No:'):
    """Opens a simple yes/no message box, returns a bool
    """
    ret = raw_input(prompt+" (Y/N) ")

    return ret

def show_message(parent=None, title = 'Title', message = 'Message', msgtype = 'Information'):
    """Opens a simple message box

      msgtype = 'Information', 'Warning', or 'Critical'
    """
    if msgtype == 'Information':
        print message
    else:
        print msgtype + ": "+ message


def get_input(parent=None, title = 'User Input', prompt = 'Enter a value:'):
    """Opens a simple prompt for user input, returns a string
    """
    try:
        ret = raw_input(prompt)
    except EOFError:
        ret = ''
    return ret


# System-specific functions
if os.name in ["posix", "mac"]:
    import termios
    TERMIOS = termios
    def get_char(parent=None, title = 'User Input', prompt = 'Enter a value:'):
        '''Returns a single character from standard input
        '''
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def clearscreen():
        """Clear the console.
        """
        os.system('tput clear')
        #os.system('clear')

elif os.name in ("nt", "dos", "ce"):
    from msvcrt import getch
    def get_char(parent=None, title = 'User Input', prompt = 'Enter a value:'):
        '''Returns a single character from standard input
        '''
        ch = getch()
        return ch

    def clearscreen():
        """Clear the console.
        """
        os.system('CLS')

elif os.name == "mac":
    def get_char(parent=None, title = 'User Input', prompt = 'Enter a value:'):
        '''Returns a single character from standard input
        '''
        # Nope. Try the posix function, since osx seems to have termios

    def clearscreen():
        """Clear the console.
        """
        os.system('tput clear')
