# -*- coding: utf-8 -*-
"""
Created on Fri Feb 04 13:32:29 2011

@author: cabrown4
"""
from inspect import getmembers
import gc, sys

class user():
    dur = 500
    fs = 44100
    isi = 250
    postbuff = 150
    prebuff = 150

u = user()
d1 = {'yes': [1,2,3],'no': [5,6,7]}

def obj_to_str(obj, name, indent=''):
    """Returns a python-callable string representation of either a class or a dict
    """

    if isinstance(obj, dict):
        outstr = "%s%s = {\n" % (indent, name)
        for key, val in obj.items():
            if key[:2] != "__":
                outstr += "%s    '%s' : %r,\n" % (indent, key,val)
        outstr += "%s}" % indent
    else:                
        outstr = "%s%s():\n" % (indent, name)
        items = getmembers(obj)
        for key, val in items:
            if key[:2] != "__":
                outstr += "%s    %s = %r\n" % (indent, key,val)
        outstr += "%s" % indent
    return outstr
