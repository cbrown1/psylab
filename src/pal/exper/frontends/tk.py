# -*- coding: utf-8 -*-

import Tkinter
import tkFileDialog, tkSimpleDialog, tkMessageBox

name = 'tk'

def show_config(exp,run,stim,var,user):
    print "Sorry, there is no tk version of the Experiment Configuration Dialog."

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
    toplevel=Tkinter.Tk()
    toplevel.withdraw()
    fname = tkSimpleDialog.askstring( title = title, prompt = prompt)
    if fname is None:
        fname = ''
    toplevel.deiconify()
    toplevel.destroy()
    return fname

def get_item(parent=None, title = 'User Input', prompt = 'Choose One:', items = [], current = 0, editable = False):
    """Opens a simple prompt to choose an item from a list, returns a string
    """
    class Radiobar(Tkinter.Frame):
        def __init__(self, parent=None, items=[], side=Tkinter.LEFT, anchor=Tkinter.W):
            Tkinter.Frame.__init__(self, parent)
            self.var = Tkinter.StringVar()
            for ind, item in enumerate(items):
                rad = Tkinter.Radiobutton(self, text=item, value=item, variable=self.var, indicatoron=0)
                if current == ind:
                    rad.select()
                rad.pack(side=side, anchor=anchor, expand=Tkinter.YES)
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
    r.root = Tkinter.Tk()
    r.root.title(title)
    Tkinter.Label(r.root, text=prompt).pack(side=Tkinter.TOP, fill=Tkinter.Y)
    gui = Radiobar(r.root, items, side=Tkinter.LEFT, anchor=Tkinter.NW)
    gui.pack(side=Tkinter.TOP, fill=Tkinter.Y)
    gui.config(relief=Tkinter.RIDGE,  bd=2)
    Tkinter.Button(r.root, text='OK', command=getstate).pack(side=Tkinter.RIGHT)
    Tkinter.Button(r.root, text='Cancel', command=quit).pack(side=Tkinter.RIGHT)
    r.root.mainloop()
    return r.ret

def get_yesno(parent=None, title = 'User Input', prompt = 'Yes or No:'):
    """Opens a simple yes/no message box, returns a bool
    """
    toplevel=Tkinter.Tk()
    toplevel.withdraw()
    ret = tkMessageBox.askyesno(title, prompt)
    toplevel.deiconify()
    toplevel.destroy()
    return ret

def show_message(parent=None, title = 'Title', message = 'Message', msgtype = 'Information'):
    """Opens a simple message box

      msgtype = 'Information', 'Warning', or 'Critical'
    """
    toplevel=Tkinter.Tk()
    toplevel.withdraw()
    if msgtype == 'Information':
        tkMessageBox.showinfo(title, message)
    elif msgtype == 'Warning':
        tkMessageBox.showwarning(title, message)
    elif msgtype == 'Critical':
        tkMessageBox.showerror(title, message)
    toplevel.deiconify()
    toplevel.destroy()

