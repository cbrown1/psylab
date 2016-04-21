# -*- coding: utf-8 -*-

# Copyright (c) 2010-2014 Christopher Brown
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

import os, sys, fnmatch
import numpy as np
import socket
import datetime
import codecs
import types
import collections
from time import sleep
from inspect import getmembers
from functools import reduce
from .frontends import term

#TODO: Modularize/standardize input methods. 
# That is, implement modular, reuseable input methods that can be 
# attached to gui forms with support for callbacks (instead of polling):
# Single-key keyboard input [numeric only or ascii]
# Multi-key keyboard input [numeric only or ascii]
# Mouse click input
# Joystick input
# etc
# The idea is you could have a single callback in your experiment script which 
# gets called everytime a registered imput method is used (keypress, etc). 
# Experimenter could then check for method and value in the callback function:
# def response(ev):
#     if ev.method = 'keypress' and ev.val = '2':
#        # Got valid response


# TODO: Implement experiment templates, which are typical combinations of 
# experimental classes (forms, input methods, datafile formats, psychophysical 
# procedures, etc). The templates would work like methods, with relevant 
# functions implemented as needed (pre_exp, etc) and inserted and run between 
# method and experiment script functions. They would drastically simplify the 
# experiment script, ideally down to a few settings in setup, and stimgen. 

# TODO: Prepend all exp.vars that are 'known' to gustav (ie., called by name in 
# utils) with an underscore,to differentiate them from exp.vars that are 
# optional (eg., exp.validKeys). Alternative is to put optional vars into 
# exp.exp, but this seems lame.

class exp:
    """Experimental settings
    """
    name = ''
    host = socket.gethostname()
    subjID = ''
    experimentPath = ''
    experimentFile = ''
    experimentFilePath = ''
    frontend = None
    debug = False
    method = 'constant'
    prompt = ''
    logString_pre_exp = None   #Write this string to the console and/or logfile at start of exp
    logString_pre_block = None #Write this string to the console and/or logfile before every block
    logString_pre_trial = None #Write this string to the console and/or logfile before every trial
    logString_post_trial = None#Write this string to the console and/or logfile after every trial
    logString_post_block = None#Write this string to the console and/or logfile after every block
    logString_post_exp = None  #Write this string to the console and/or logfile at end of exp
    logString_header = "# A log file for Gustav\n\n" #Write this string to the logfile if it is new
    logFile = 'gustav_logfile_$date.log'
    logFile_unexpanded = ""
    logConsole = True
    dataString_pre_exp = ''    #Write this string to datafile at exp begin
    dataString_pre_block = ''  #Write this string to datafile before every block
    dataString_pre_trial = ''  #Write this string to datafile before every trial
    dataString_post_trial = '' #Write this string to datafile after every trial
    dataString_post_block = '' #Write this string to datafile after every block
    dataString_post_exp = ''   #Write this string to datafile at exp end
    dataString_header = '#A data file for Gustav\n\n'#Write this string to datafile if the file is new
    dataFile ='$name.csv'
    dataFile_unexpanded =''
    recordData = True
    comments = ''
    disable_functions = []          # Experimenter can add function names as strings to disable them
    quitKeys = ['/', 'q']
    eventTypes = [ 'pre_exp', 'pre_block', 'pre_trial', 'post_trial', 'post_block', 'post_exp' ]
    frontendTypes = ['qt', 'tk', 'term']
    from .frontends import term

    def prompt_response(self,exp):
        while True:
            ret = exp.frontend.get_input(None, "Gustav!","Enter Response: ")
            # Check for quit
            if ret in exp.quitKeys:
                # User wants to exit. Break out of block, gustav loops
                exp.run.block_on = False
                exp.run.gustav_is_go = False
                break
            else:
                # Its good. Record response
                exp.run.response = ret
                # Exit while-True loop
                break
            
    def prompt_condition(self,exp):
        while True:
            ret = exp.frontend.get_input(None, "Gustav!","Enter Condition # (1-{:})".format(exp.var.nlevels_total))
            if ret in exp.quitKeys:
                exp.run.block_on = False
                exp.run.gustav_is_go = False
                break
            elif ret.isdigit():
                iret = int(ret) - 1
                if iret in range(exp.var.nlevels_total):
                    exp.run.condition = iret
                    break

    def present_trial(self,exp):
        pass

    def pre_exp(exp):
        pass

    def pre_block(exp):
        pass

    def pre_trial(exp):
        pass

    def post_trial(exp):
        pass

    def post_block(exp):
        pass

    def post_exp(exp):
        pass

    pre_exp_ = [pre_exp]
    pre_block_ = [pre_block]
    pre_trial_ = [pre_trial]
    post_trial_ = [post_trial]
    post_block_ = [post_block]
    post_exp_ = [post_exp]


    class var:
        """Experiment variable settings
        """
        factorial = collections.OrderedDict()
        covariable = collections.OrderedDict()
        current = collections.OrderedDict()
        ignore = []
        default = []
        varlist = []
        levelsbycond = {}
        nlevels_fact = 0
        nlevels_list = 0
        nlevels_total = 0
        order = 'natural'
        order_ = 0
        prompt = []
        dynamic = {}

    
    class run:
        """Settings associated with the details of running the experiment
        """
        time = ''
        date = ''
        trials_block = 0     # Current trial count within a block
        trials_exp = 0      # Current total trial count
        block = 0      # Current block (treatment) count
        blocks = 0     # Current total block count
        condition = 0  # Current condition
        block_on = True
        trial_on = True
        gustav_is_go = True
        response = ''
    
    
    class user:
        """Convenience container for user settings
        """
        pass

    class stim:
        """Convenience container for stimulus stuff
        """
        pass


def initialize_experiment( exp ):
    """Do stuff necessary for the start of an experiment
    """
    logpath = os.path.split(exp.logFile)
    if not os.path.isdir(logpath[0]):
        print("Created logfile path: {}".format(logpath[0]))
        os.makedirs(logpath[0])
    else:
        debug(exp, "Found logfile path: {}".format(logpath[0]))
    # For logfile name, we expand date and exp name only and dont do full  
    # variable expansion because many variables haven't been set yet.
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    exp.logFile = exp.logFile.replace("$date", date)
    exp.logFile = exp.logFile.replace("$name", exp.name)
    exp.logFile = exp.logFile.replace("$host", exp.host)
    if not os.path.isfile(exp.logFile):
        exp.logString_header = exp.logString_header.replace("$date", date)
        write_data(exp.logString_header, exp.logFile)
        debug(exp, "Created log file: {}".format(exp.logFile))
    else:
        debug(exp, "Found log file: {}".format(exp.logFile))

    exp.utils.get_frontend(exp, exp.frontend)
    debug(exp, "Got frontend: {}".format(exp.frontend.name))
    # For each event type, look for a function in method, and in experiment.
    # If a function is found, add to list to be run during that event. 
    for event in exp.eventTypes:
        if hasattr(exp.method, event):
            thisstr = "{}_".format(event)
            thisfunclist = getattr(exp, thisstr)
            thisfunclist.append(getattr(exp.method, event))
            debug(exp, "Found event in method: {}".format(event))
        if hasattr(exp.experiment, event):
            thisstr = "{}_".format(event)
            thisfunclist = getattr(exp, thisstr)
            thisfunclist.append(getattr(exp.experiment, event))
            debug(exp, "Found event in experiment: {}".format(event))

    # A few 'special' events that should only occur (if at all) in the experiment file:
    if hasattr(exp.experiment, "present_trial"):
        exp.present_trial = exp.experiment.present_trial
        debug(exp, "Found event in experiment: present_trial")
    if hasattr(exp.experiment, "prompt_response"):
        exp.prompt_response = exp.experiment.prompt_response
        debug(exp, "Found event in experiment: prompt_response")
    if hasattr(exp.experiment, "prompt_condition"):
        exp.prompt_condition = exp.experiment.prompt_condition
        debug(exp, "Found event in experiment: prompt_condition")

    exp.utils.process_variables(exp)
    exp.run.nblocks = exp.var.nblocks
    if exp.recordData:
        debug(exp, "Data will be recorded")
        datapath = os.path.split(exp.dataFile)
        if not os.path.isdir(datapath[0]):
            os.makedirs(datapath[0])
            debug(exp, "Created datafile path: {}".format(datapath[0]))
        else:
            debug(exp, "Found datafile path: {}".format(datapath[0]))
        exp.dataFile_unexpanded = exp.dataFile
        exp.dataFile = get_expanded_vals_in_string(exp.dataFile, exp)
        if not os.path.isfile(exp.dataFile):
            exp.dataString_header = get_expanded_vals_in_string(exp.dataString_header, exp)
            write_data(exp.dataString_header, exp.dataFile)
            debug(exp, "Created datafile: {}".format(exp.dataFile))
        else:
            debug(exp, "Found datafile: {}".format(exp.dataFile))
    else:
        debug(exp, "Data will not be recorded")

def process_variables(exp):
    """Processes conditions
        Factorialize all 'factorial' conditions, and add all 'covariable' conditions
        For each variable, make a list of levels for each condition
    """

    # Begin get number of levels
    factorial = []
    covariable = []
    nfact = {}
    ncov = {}
    if len(exp.var.factorial) > 0:
        exp.var.nlevels_fact = 1
        for v in exp.var.factorial:
            exp.var.levelsbycond[v] = []
            exp.var.varlist.append(v)
            nfact[v] = len(exp.var.factorial[v])
            exp.var.nlevels_fact *= nfact[v]
            debug(exp, "Found factorial variable: {} [{:} levels]".format(v, len(exp.var.factorial[v])))

        factorial = exp.var.varlist
    nlist = 0
    for v in exp.var.covariable:
        if v not in exp.var.levelsbycond.keys():
            exp.var.levelsbycond[v] = []
        covariable.append(v)
        ncov[v] = len(exp.var.covariable[v])
        if nlist == 0 or nlist == 1:
            nlist = ncov[v]
        else:
            if nlist != ncov[v] and ncov[v] != 1:
                raise Exception("All 'covariable' variables must either have the same number of levels, or one level")
        debug(exp, "Found list variable: {} [{:} levels]".format(v, len(exp.var.covariable[v])))
    if len(factorial) == 0:
        for v in exp.var.covariable:
            exp.var.varlist.append(v)
    exp.var.nlevels_list = nlist
    exp.var.nlevels_total = exp.var.nlevels_fact + exp.var.nlevels_list
    debug(exp, "Counted total conditions: {:} [{:} fact, {:} list]".format(exp.var.nlevels_total, exp.var.nlevels_fact, exp.var.nlevels_list))
    # End get number of levels

    # Begin process conditions
    if exp.var.nlevels_fact > 0:
        i = 0
        done = 1
        todo = exp.var.nlevels_fact
        varmatrix = np.zeros((todo,len(exp.var.factorial)),dtype=int)

        # create varmatrix, which will have 1 column for each variable in factorial,
        # and nlevels_fact rows containing indices to the levels of each variable
        for v in exp.var.factorial:
            varmatrix[:,i] = np.tile(np.arange(nfact[v]).repeat(todo/nfact[v]),done)
            done *= nfact[v]
            todo /= nfact[v]
            i += 1
        # For each variable, generate a list, of nlevels_fact long, of level names
        j = 0
        for v in exp.var.factorial:
            for i in range(len(varmatrix)):
                exp.var.levelsbycond[v].append(exp.var.factorial[v][varmatrix[i,j]])
            j += 1

    # Append 'covariable' levels to each list
    if exp.var.nlevels_list > 0:
        for v in exp.var.varlist:
            gotvar = False
            if not v in covariable:
                # Variable is in factorial but not mentioned in covariable.
                if len(exp.var.factorial[v]) == 1:
                    # There is only 1 level specified in factorial. Use that for all 'covariable' conditions for that var.
                    for condition in range(exp.var.nlevels_list):
                        exp.var.levelsbycond[v].append(exp.var.factorial[v][0])
                    gotvar = True
            elif len(exp.var.covariable[v]) == 1:
                # There is only one level specified. Use that for all conditions for that var.
                for condition in range(exp.var.nlevels_list):
                    exp.var.levelsbycond[v].append(exp.var.covariable[v][0])
                gotvar = True
            elif len(exp.var.covariable[v]) == exp.var.nlevels_list:
                # More than one level specified. Use them all.
                for condition in range(exp.var.nlevels_list):
                    exp.var.levelsbycond[v].append(exp.var.covariable[v][condition])
                gotvar = True
            if not gotvar:
                raise Exception("Unable to process the following variable: {}".format(v))

    # Process order
    if exp.var.order == "random":
        exp.var.orderarray = np.random.permutation(exp.var.nlevels_total)
        exp.var.nblocks = exp.var.nlevels_total
    elif exp.var.order == "natural":
        exp.var.orderarray = np.arange(exp.var.nlevels_total)
        exp.var.nblocks = exp.var.nlevels_total
    elif exp.var.order == "prompt":
        exp.var.orderarray = []
        exp.var.nblocks = 999
    elif exp.var.order == "menu":
        exp.var.orderarray = []
        exp.var.nblocks = 0
    else:
        exp.var.orderarray = str_to_range(exp.var.order)
        exp.var.nblocks = len(exp.var.orderarray)
    debug(exp, "Got presentation order input string: {}".format(exp.var.order))
    debug(exp, "Generated presentation order: {}".format(", ".join(str(i) for i in exp.var.orderarray)))
# End process_variables


def get_current_variables(exp):
    """Get current levels of each variable for a given condition
    """
    condition = exp.run.condition
    #exp.var.current = {}
    exp.var.current = collections.OrderedDict()
    for v in exp.var.varlist:
        if v in exp.var.prompt:
            ret = exp.frontend.get_input(prompt = "Enter a value for variable: {}\nor hit enter for current level ({}): ".format(v, exp.var.levelsbycond[v][condition]))
            if ret == "":
                exp.var.current[v] = exp.var.levelsbycond[v][condition]
            else:
                exp.var.current[v] = ret
        else:
            exp.var.current[v] = exp.var.levelsbycond[v][condition]
        debug(exp, "Getting level: {}; for variable: {}".format(exp.var.current[v],v))

def get_variable_strtable(exp):
    """Creates a table specifying the levels of each variable for each condition
    """
    vlength = {}
    out = "Condition"
    for v in exp.var.varlist:
        vlength[v] = np.maximum(len(max(exp.var.levelsbycond[v], key=len)), len(v)) + 2
        out += "{{: >{:}}}".format(vlength[v]).format(v)
    out += "\n"
    for i in range(exp.var.nlevels_total):
        out += "{: >9d}".format(i+1)
        for v in exp.var.varlist:
            out += "{{: >{:}}}".format(vlength[v]).format(exp.var.levelsbycond[v][i])
        out += "\n"
    return out

def menu_condition(exp):
    """Prompts the experiment to choose the conditions to run
    """
    debug(exp, "Deriving presentation order via menu")
    strtable = exp.utils.get_variable_strtable(exp)
    sel = []
    conditions = []
    message = ""
    for i in range(1,exp.var.nlevels_total+1):
        conditions.append(str(i))
    while True:
        disp = strtable + "\nExperiment: {}\nSelected Conditions: [".format(exp.name)
        for s in sel:
            disp += " " + s
        disp += " ]\n\n{}Menu".format(message)
        if not exp.recordData:
            disp += "  [NO DATA WILL BE RECORDED]"
        disp += ":\nCondition # - Add condition\n"
        disp += "{: >11} - Add all conditions\n".format('a')
        disp += "{: >11} - Run exp using selected conditions in random order\n".format('r')
        disp += "{: >11} - Run exp using selected conditions in selected order\n".format('s')
        disp += "{: >11} - Clear condition list\n".format('c')
        disp += "{: >11} - Quit\n".format(",".join(exp.quitKeys))
        # Poor man's clearscreen: Prepend blank lines (assume console is 25 lines long)
        if disp.count("\n") < 25:
            disp = "\n" * (25-disp.count('\n')) + disp 
        message = ""
        ret = exp.term.get_input(parent=None, title = "Gustav!", prompt = disp)
        if ret in conditions:
            sel.append(ret)
        elif ret in ["a"]:
            for cond in conditions:
                sel.append(cond)
        elif ret in exp.quitKeys:
            exp.run.gustav_is_go = False
            break;
        elif ret in ["c"]:
            sel = []
        elif ret in ["r", "s"]:
            if len(sel) > 0:
                if ret == "r":
                    sel = np.random.permutation(sel).tolist()
                for s in sel:
                    exp.var.orderarray.append(int(s)-1)
                exp.run.nblocks = len(exp.var.orderarray)
                exp.run.gustav_is_go = True
                break;
            else:
                message = "You must select at least 1 condition to run!\n\n"
        elif ret.isdigit():
            message = "Condition numbers for this experiment are 1 <= {:}\n\n".format(exp.var.nlevels_total)
        elif ret != "":
            message = "Unrecognized input: {}\n\n".format(ret)
            

def update_time(run):
    """Updates the date and time
    """
    exp.run.time = datetime.datetime.now().strftime('%H:%M:%S')
    exp.run.date = datetime.datetime.now().strftime('%Y-%m-%d')


def write_data(data, filename):
    """Data IO.
    """
    if os.path.isfile(filename):
        f = codecs.open(filename, encoding='utf-8', mode='a')
    else:
        f = codecs.open(filename, encoding='utf-8', mode='w')
        f.write("# -*- coding: utf-8 -*-\n\n")

    f.write(data)
    f.close()


def save_data(exp, message):
    if exp.recordData:
        if message is not None and message != '':
            message_exp = exp.utils.get_expanded_vals_in_string(message, exp)
            exp.utils.write_data(message_exp, exp.dataFile)


def log(exp, message):
    """Writes info to the console, to a log file, or both
    """
    if message is not None and message != '':
        message_exp = exp.utils.get_expanded_vals_in_string(message, exp)
        if exp.logConsole:
            print(message_exp),
        if exp.logFile is not None and exp.logFile is not '':
            write_data(message_exp, exp.logFile)

    
def debug(exp, message):
    """Writes debug info to the console, to a log file, or both
    """
    if exp.debug:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        dmessage = "DEBUG {},{}: {}".format(date, time, message)
        if exp.logConsole:
            print(dmessage)
        if exp.logFile is not None and exp.logFile is not '':
            if dmessage[-1:] != "\n":
                dmessage += "\n"
            write_data(dmessage, exp.logFile)

        
def do_event(exp, event):
    debug(exp, "Begin Event: {}".format(event))
    exp.utils.update_time(exp.run)
    if hasattr(exp, "{}_".format(event)):
        funcs = getattr(exp, "{}_".format(event))
        for f in funcs:
            if f.__name__ not in exp.disable_functions:
                f(exp)
    if hasattr(exp, "logString_{}".format(event)):
        exp.utils.log(exp, getattr(exp, "logString_{}".format(event)))
    if hasattr(exp, "dataString_{}".format(event)):
        exp.utils.save_data(exp, getattr(exp, "dataString_{}".format(event)))
    debug(exp, "End Event: {}".format(event))
        
        
def get_frontend(exp, frontend):
    """Tries to load the specified frontend
    """
    frontend_s = frontend
    if frontend_s not in exp.frontendTypes:
        exp.utils.log(exp, "Unknown frontend. Using tk")
        frontend = "tk"
    try:
        frontend = __import__("frontends",globals(), locals(), frontend)
    except ImportError:
        raise Exception("Could not import frontend: {}".format(frontend))
    exp.frontend = getattr(frontend, frontend_s)
    debug(exp, "Got frontend: {}".format(exp.frontend.name))

def obj_to_str(obj, name, indent=""):
    """Returns formatted, python-callable string representations of objects
        including classes, dicts, lists, and other built-in var types
    """
    if isinstance(obj, dict):
        outstr = "{}{} = {{\n".format(indent, name)
        for key, val in obj.items():
            if key[:2] != "__":
                outstr += "{}    '{}' : {},\n".format(indent, key, repr(val))
        outstr += "{}}}\n".format(indent)
    elif isinstance(obj, list):
        outstr = "{}{} = [\n".format(indent, name)
        for val in obj:
            outstr += "{}    {},\n".format(indent, repr(val))
        outstr += "{}]\n".format(indent)
    elif isinstance(obj,(types.ClassType,types.InstanceType)):
        outstr = "{}class {}():\n".format(indent, name)
        items = getmembers(obj)
        for key, val in items:
            if key[:2] != "__":
                outstr += "{}    {} = {}\n".format(indent, key, repr(val))
        outstr += "{}\n".format(indent)
    else:
        outstr = "{}{} = {}\n".format(indent, name, repr(obj))
    return outstr


def get_expanded_vals_in_string(instr, exp):
    """Replaces all variable references with the specified variable's current value

        Here is a list of available variable references:

        Var ref:         : Will be replaced with:
        $name            : The name of the experiment
        $host            : The name of the machine that the exp is being run on
        $subj            : The subject id
        $resp            : The current response
        $trial           : The current trial number
        $trial_block     : The current trial number within the current block
        $block           : The current block number
        $condition       : The current condition number
        $conditions      : The total number of conditions
        $time            : The time the session started
        $date            : The date the session started
        $var[varname]    : varname is the name of one of your variables
        $currentvars[';']: A delimited list of the current levels of all vars
                            The delimiter can be specified (use empty brackets
                            to specify default: ',')
        $currentvarsvals : Same as currentvars, but you will get 'var = val'
                            instead of just 'val'
        @currentvars     : Same as currentvars, but you will get var names 
                            instead of values (eg., for datafile header). 
        $user[varname]   : The value of a user variable
        $stim[varname]   : The value of a stim variable
    """

    outstr = instr.replace("$name", exp.name)
    outstr = outstr.replace("$note", exp.note)
    outstr = outstr.replace("$comments", "\n# ".join(exp.comments.split('\n')) )
    outstr = outstr.replace("$host", exp.host)
    outstr = outstr.replace("$subj", exp.subjID)
    outstr = outstr.replace("$trial_block", str(exp.run.trials_block+1))
    outstr = outstr.replace("$trial", str(exp.run.trials_exp+1))
    outstr = outstr.replace("$blocks", str(exp.run.nblocks))
    outstr = outstr.replace("$block", str(exp.run.block+1))
    outstr = outstr.replace("$conditions", str(exp.var.nlevels_total))
    outstr = outstr.replace("$condition", str(exp.run.condition+1))
    outstr = outstr.replace("$time", exp.run.time)
    outstr = outstr.replace("$date", exp.run.date)
    outstr = outstr.replace("$response", exp.run.response)

    # This func gets called from setup (for datafilename), and exp.var.current is not set at that point
    if len(exp.var.current)>0:
        currentvars = []
        currentvarsvals = []
        for key, val in exp.var.current.iteritems():
            currentvars.append(val)
            currentvarsvals.append("{} = {}".format(key, val))
            outstr = outstr.replace("$var[{}]".format(key), val)

        got_cv = True
        while got_cv:
            expr, delim = get_arg(outstr,"$currentvarsvals")
            if expr != "":
                if delim == "":
                    delim = ","
                outstr = outstr.replace(expr, delim.join(currentvarsvals))
            else:
                got_cv = False

        got_cv = True
        while got_cv:
            expr, delim = get_arg(outstr,"$currentvars")
            if expr != "":
                if delim == "":
                    delim = ","
                outstr = outstr.replace(expr, delim.join(currentvars))
            else:
                got_cv = False

    varlist = []
    for key in exp.var.varlist:
        varlist.append(key)

    got_cv = True
    while got_cv:
        expr, delim = get_arg(outstr,"@currentvars")
        if expr != "":
            if delim == "":
                delim = ","
            outstr = outstr.replace(expr, delim.join(varlist))
        else:
            got_cv = False

    items = getmembers(exp.user)
    for key, val in items:
        if key[:2] != "__":
            outstr = outstr.replace("$user["+str(key)+"]", str(val))
            outstr = outstr.replace("@user["+str(key)+"]", str(key))

    items = getmembers(exp.stim)
    for key, val in items:
        if key[:2] != "__":
            outstr = outstr.replace("$stim["+str(key)+"]", str(val))
            outstr = outstr.replace("@stim["+str(key)+"]", str(key))

    if hasattr(exp.var,'dynamic'):
        for key, val in exp.var.dynamic.items():
            outstr = outstr.replace("$dynamic["+str(key)+"]", str(val))
            outstr = outstr.replace("@dynamic["+str(key)+"]", str(key))

    return outstr


def get_arg(instr, var):
    """Returns the bracketed argument that immediately follows the first
        occurance of the 'var' string, along with the entire expression
        for easy replace

        example:
        >>> instr = "some text $var['user'] more text"
        >>> get_arg(instr,'$var')
        ("$var['user']", 'user')
    """
    s = len(var) + 1 # Plus 1 for [ char
    i = instr.find(var+"[")
    if i != -1:
        o = instr.find("]",i+s)
        if o != -1:
            arg = instr[i+s:o].strip("\"\'")
            exp = instr[i:o+1]
            return exp, arg
        else:
            return "",""
    else:
        return "",""


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
    if s.count(":"):
        tokens = [x.strip().split(":") for x in s.split(",")]
    else:
        tokens = [x.strip().split("-") for x in s.split(",")]

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

