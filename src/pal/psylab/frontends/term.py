# -*- coding: utf-8 -*-

import Tkinter
import tkFileDialog, tkSimpleDialog, tkMessageBox

name = 'term'

def show_config(exp,run,stim,var,user):
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

def get_input(parent=None, title = 'User Input', prompt = 'Enter a value:'):
    """Opens a simple prompt for user input, returns a string
    """
    try:
        ret = raw_input(prompt)
    except EOFError:
        ret = ''
    return ret

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

