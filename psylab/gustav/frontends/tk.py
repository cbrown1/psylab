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

try:
    # Python2
    import Tkinter as tk
    import tkFileDialog as filedialog, tkSimpleDialog as simpledialog, tkMessageBox as messagebox
except ImportError:
    # Python3
    import tkinter as tk
    from tkinter import filedialog, simpledialog, messagebox

name = 'tk'

def show_config(exp,run,var,stim,user):
    print("Sorry, there is no tk version of the Experiment Configuration Dialog.")

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
    toplevel=tk.Tk()
    toplevel.withdraw()
    fname = filedialog.askopenfilename( title = title, initialdir = default_dir, filetypes = fts, multiple = False)
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
    toplevel=tk.Tk()
    toplevel.withdraw()
    fname = filedialog.askdirectory( title = title, initialdir = default_dir )
    toplevel.deiconify()
    toplevel.destroy()
    if isinstance(fname, tuple):
        return ''
    else:
        return fname

def get_input(parent=None, title = 'User Input', prompt = 'Enter a value:'):
    """Opens a simple prompt for user input, returns a string
    """
    toplevel=tk.Tk()
    toplevel.withdraw()
    fname = simpledialog.askstring( title = title, prompt = prompt)
    if fname is None:
        fname = ''
    toplevel.deiconify()
    toplevel.destroy()
    return fname

def get_item(parent=None, title = 'User Input', prompt = 'Choose One:', items = [], current = 0, editable = False):
    """Opens a simple prompt to choose an item from a list, returns a string
    """
    class Radiobar(tk.Frame):
        def __init__(self, parent=None, items=[], side=tk.LEFT, anchor=tk.W):
            tk.Frame.__init__(self, parent)
            self.var = tk.StringVar()
            for ind, item in enumerate(items):
                rad = tk.Radiobutton(self, text=item, value=item, variable=self.var, indicatoron=0)
                if current == ind:
                    rad.select()
                rad.pack(side=side, anchor=anchor, expand=tk.YES)
        def state(self):
            return self.var.get()

    class r:
        ret = ''
        root = None

    def getstate():
        r.ret = gui.state()
        r.root.destroy()

    def quit():
        r.root.destroy()

    r = r();
    r.root = tk.Tk()
    r.root.title(title)
    tk.Label(r.root, text=prompt).pack(side=tk.TOP, fill=tk.Y)
    gui = Radiobar(r.root, items, side=tk.LEFT, anchor=tk.NW)
    gui.pack(side=tk.TOP, fill=tk.Y)
    gui.config(relief=tk.RIDGE,  bd=2)
    tk.Button(r.root, text='OK', command=getstate).pack(side=tk.RIGHT)
    tk.Button(r.root, text='Cancel', command=quit).pack(side=tk.RIGHT)
    r.root.mainloop()
    return r.ret

def get_yesno(parent=None, title = 'User Input', prompt = 'Yes or No:'):
    """Opens a simple yes/no message box, returns a bool
    """
    toplevel=tk.Tk()
    toplevel.withdraw()
    ret = messagebox.askyesno(title, prompt)
    toplevel.deiconify()
    toplevel.destroy()
    return ret

def show_message(parent=None, title = 'Title', message = 'Message', msgtype = 'Information'):
    """Opens a simple message box

      msgtype = 'Information', 'Warning', or 'Critical'
    """
    toplevel=tk.Tk()
    toplevel.withdraw()
    if msgtype == 'Information':
        messagebox.showinfo(title, message)
    elif msgtype == 'Warning':
        messagebox.showwarning(title, message)
    elif msgtype == 'Critical':
        messagebox.showerror(title, message)
    toplevel.deiconify()
    toplevel.destroy()

