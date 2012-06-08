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
from time import sleep
from inspect import getmembers
from .frontends import term

class exp:
    '''Experimental settings
    '''
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
    logString_pre_exp = None   #Write this string to the console and/or logfileat start of exp
    logString_pre_block = None #Write this string to the console and/or logfilebefore every block
    logString_pre_trial = None #Write this string to the console and/or logfile before every trial
    logString_post_trial = None#Write this string to the console and/or logfileafter every trial
    logString_post_block = None#Write this string to the console and/or logfileafter every block
    logString_post_exp = None  #Write this string to the console and/or logfileat end of exp
    logString_header = "# A log file for Gustav\n\n" #Write this string to the logfile if it is new
    logFile = 'gustav_logfile_$date.log'
    logFile_unexpanded = ""
    logConsole = True
    dataString_pre_exp = ''   #Write this string to datafile at exp begin
    dataString_pre_block = '' #Write this string to datafile before every block
    dataString_pre_trial = '' #Write this string to datafile before every trial
    dataString_post_trial = '' #Write this string to datafile after every trial
    dataString_post_block = '' #Write this string to datafile after every block
    dataString_post_exp = ''   #Write this string to datafile at exp end
    dataString_header = '#A data file for Gustav\n\n'#Write this string to datafile if the file is new
    dataFile ='$name.csv'
    dataFile_unexpanded =''
    recordData = True
    stimtext_fmt = 'file,kw,text'  # Default format for stimulus text files
    comments = ''
    disable_functions = []          # Experimenter can add function names as strings to disable them
    methodTypes = ['constant', 'staircase'] # TODO: remove methodTypes
    stimLoadTypes = ['auto', 'manual']
    stimTypes = ['files', 'manual']
    varTypes = ['stim', 'manual', 'dynamic']
    eventTypes = [ 'pre_exp', 'pre_block', 'pre_trial', 'post_trial', 'post_block', 'post_exp' ]
    frontendTypes = ['qt', 'tk', 'term']
    from frontends import term

    def prompt_response(self,exp,run,var,stim,user):
        while True:
            ret = exp.frontend.get_input(None, "Gustav!","Enter Response: ")
            # Check for quit
            if ret in ['/', 'q']:
                # User wants to exit. Break out of block, gustav loops
                run.block_on = False
                run.gustav_is_go = False
                break
            else:
                # Its good. Record response
                run.response = ret
                # Exit while-True loop
                break
            
    def prompt_condition(self,exp,run,var,stim,user):
        while True:
            ret = exp.term.get_input(None, "Gustav!","Enter Condition # (1-"+str(var.nlevels_total)+"): ")
            if ret in ['/', 'q']:
                run.block_on = False
                run.gustav_is_go = False
                break
            elif ret.isdigit():
                iret = int(ret) - 1
                if iret in range(var.nlevels_total):
                    run.condition = iret
                    break

    def present_trial(self,exp,run,var,stim,user):
        pass

    def pre_exp(exp,run,var,stim,user):
        pass

    def pre_block(exp,run,var,stim,user):
        pass

    def pre_trial(exp,run,var,stim,user):
        pass

    def post_trial(exp,run,var,stim,user):
        pass

    def post_block(exp,run,var,stim,user):
        pass

    def post_exp(exp,run,var,stim,user):
        pass

    pre_exp_ = [pre_exp]
    pre_block_ = [pre_block]
    pre_trial_ = [pre_trial]
    post_trial_ = [post_trial]
    post_block_ = [post_block]
    post_exp_ = [post_exp]


class var:
    '''Experiment variable settings
    '''
    factvars = []
    listvars = []
    ignore = []
    default = []
    current = []
    varlist = []
    levelsbycond = {}
    nlevels_fact = 0
    nlevels_list = 0
    nlevels_total = 0
    order = 'natural'
    order_ = 0
    debug = False
    dynamic = {}


class stim:
    '''Stimulus (files on disk) settings
    '''
    sets = {}
    current = {}
    stimvars = []
    debug = False
    stimarray = 0


class run:
    '''Settings associated with the details of running the experiment
    '''
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
    '''Any user settings
    '''
    pass


def initialize_experiment( exp, run, var, stim, user):
    '''Do stuff necessary for the start of an experiment
    '''
    logpath = os.path.split(exp.logFile)
    if not os.path.isdir(logpath[0]):
        print("Creating logfile path: " + logpath[0])
        os.makedirs(logpath[0])
    # We expand date only and not full variable expansion because many variables haven't been set.
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    exp.logFile = exp.logFile.replace("$date", date)
    if not os.path.isfile(exp.logFile):
        exp.logString_header = exp.logString_header.replace("$date", date)
        write_data(exp.logString_header, exp.logFile)

    exp.utils.get_frontend(exp, exp.frontend)
    debug(exp, 'Got frontend: %s' % exp.frontend.name)
    # For each event type, look for a function in method, and in experiment.
    # If a function is found, add to list to be run during that event. 
    for event in exp.eventTypes:
        if hasattr(exp.method, event):
            thisstr = '%s_' % event
            thisfunclist = getattr(exp, thisstr)
            thisfunclist.append(getattr(exp.method, event))
            debug(exp, 'Found event in method: %s' % event)
        if hasattr(exp.experiment, event):
            thisstr = '%s_' % event
            thisfunclist = getattr(exp, thisstr)
            thisfunclist.append(getattr(exp.experiment, event))
            debug(exp, 'Found event in experiment: %s' % event)

    # A few 'special' events that should only occur (if at all) in the experiment file:
    if hasattr(exp.experiment, 'present_trial'):
        exp.present_trial = exp.experiment.present_trial
        debug(exp, 'Found event in experiment: present_trial')
    if hasattr(exp.experiment, 'prompt_response'):
        exp.prompt_response = exp.experiment.prompt_response
        debug(exp, 'Found event in experiment: prompt_response')
    if hasattr(exp.experiment, 'prompt_condition'):
        exp.prompt_condition = exp.experiment.prompt_condition
        debug(exp, 'Found event in experiment: prompt_condition')

    stim.get_next = exp.utils.stim_get_next
    stim.reset_order = exp.utils.stim_reset_order
    exp.utils.process_stimuli(exp, stim)
    # Make a list of the stimuli that are actually used
    for v in range(len(var.factvars)):
        if var.factvars[v]['type'] == 'stim':
            for level in var.factvars[v]['levels']:
                if level not in stim.stimvars:
                    stim.stimvars.append(level)

    exp.utils.process_variables(exp, var)
    run.nblocks = var.nblocks
    if exp.recordData:
        datapath = os.path.split(exp.dataFile)
        if not os.path.isdir(datapath[0]):
            os.makedirs(datapath[0])
            debug(exp, "Created datafile path: " + datapath[0])
        exp.dataFile_unexpanded = exp.dataFile
        exp.dataFile = get_expanded_vals_in_string(exp.dataFile, exp, run, var, stim, user)
        if not os.path.isfile(exp.dataFile):
            exp.dataString_header = get_expanded_vals_in_string(exp.dataString_header, exp, run, var, stim, user)
            write_data(exp.dataString_header, exp.dataFile)
            debug(exp, "Created datafile: " + exp.dataFile)


def process_variables(exp, var):
    '''Processes conditions
        Factorialize all 'factvars' conditions, and add all 'listvars' conditions
        For each variable, make a list of levels for each condition
    '''

    # Begin get number of levels
    factvars = []
    listvars = []
    if len(var.factvars) > 0:
        var.nlevels_fact = 1
        for v in range(len(var.factvars)):
            var.levelsbycond[var.factvars[v]['name']] = []
            var.varlist.append(var.factvars[v]['name'])
            var.factvars[v]['n'] = len(var.factvars[v]['levels'])
            var.nlevels_fact *= var.factvars[v]['n']
            debug(exp, "Found factorial variable: %s [%i levels]" % (var.factvars[v]['name'], len(var.factvars[v]['levels'])))

        factvars = var.varlist
    nlist = 0
    for v in range(len(var.listvars)):
        if var.listvars[v]['name'] not in var.levelsbycond.keys():
            var.levelsbycond[var.listvars[v]['name']] = []
        listvars.append(var.listvars[v]['name'])
        var.listvars[v]['n'] = len(var.listvars[v]['levels'])
        if nlist == 0 or nlist == 1:
            nlist = var.listvars[v]['n']
        else:
            if nlist != var.listvars[v]['n'] and var.listvars[v]['n'] != 1:
                raise Exception("All 'listvars' variables must either have the same number of levels, or one level")
        debug(exp, "Found list variable: %s [%i levels]" % (var.listvars[v]['name'], len(var.listvars[v]['levels'])))
    if len(factvars) == 0:
        for v in range(len(var.listvars)):
            var.varlist.append(var.listvars[v]['name'])
    var.nlevels_list = nlist
    var.nlevels_total = var.nlevels_fact + var.nlevels_list
    debug(exp, "Counted total conditions: %i [%i fact, %i list]" % (var.nlevels_total, var.nlevels_fact, var.nlevels_list))
    # End get number of levels

    # Begin process conditions
    if var.nlevels_fact > 0:
        i = 0
        done = 1
        todo = var.nlevels_fact
        varmatrix = np.zeros((todo,len(var.factvars)),dtype=int)

        # create varmatrix, which will have 1 column for each variable in factvars,
        # and nlevels_fact rows containing indices to the levels of each variable
        for v in range(len(var.factvars)):
            varmatrix[:,i] = np.tile(np.arange(var.factvars[v]['n']).repeat(todo/var.factvars[v]['n']),done)
            done *= var.factvars[v]['n']
            todo /= var.factvars[v]['n']
            i += 1
        # For each variable, generate a list, of nlevels_fact long, of level names
        for v in range(len(var.factvars)):
            for i in range(len(varmatrix)):
                var.levelsbycond[var.factvars[v]['name']].append(var.factvars[v]['levels'][varmatrix[i,v]])

    # Append 'listvars' levels to each list
    if var.nlevels_list > 0:
        for i,v in enumerate(var.varlist):
            gotvar = False
            if not v in listvars:
                # Variable is in factvars but not mentioned in listvars.
                if len(var.factvars[i]['levels']) == 1:
                    # There is only 1 level specified in factvars. Use that for all 'listvars' conditions for that var.
                    for condition in range(var.nlevels_list):
                        var.levelsbycond[v].append(var.factvars[i]['levels'][0])
                    gotvar = True
            elif len(var.listvars[i]['levels']) == 1:
                # There is only one level specified. Use that for all conditions for that var.
                for condition in range(var.nlevels_list):
                    var.levelsbycond[v].append(var.listvars[i]['levels'][0])
                gotvar = True
            elif len(var.listvars[i]['levels']) == var.nlevels_list:
                # More than one level specified. Use them all.
                for condition in range(var.nlevels_list):
                    var.levelsbycond[v].append(var.listvars[i]['levels'][condition])
                gotvar = True
            if not gotvar:
                raise Exception("Unable to process the following variable: " + v)

    # Process order
    if var.order == 'random':
        var.orderarray = np.random.permutation(var.nlevels_total)
        var.nblocks = var.nlevels_total
    elif var.order == 'natural':
        var.orderarray = np.arange(var.nlevels_total)
        var.nblocks = var.nlevels_total
    elif var.order == 'prompt':
        var.orderarray = 0
        var.nblocks = 999
    elif var.order == 'menu':
        var.orderarray = []
        var.nblocks = 0
    else:
        var.orderarray = str_to_range(var.order)
        var.nblocks = var.nlevels_total
    debug(exp, "Presentation order: " + var.order)
# End process_variables


def process_stimuli(exp, stim):
    '''Account for all stimuli present, and attach any associated text
    '''
    for stimset in stim.sets:
        if 'type' not in stim.sets[stimset]:
            stim.sets[stimset]['type'] = 'manual'
        if stim.sets[stimset]['type'] != 'manual':
            # Set defaults for stim vars
            if 'type' not in stim.sets[stimset]:
                stim.sets[stimset]['type'] = 'manual'
            if 'order' not in stim.sets[stimset]:
                stim.sets[stimset]['order'] = 1
            if 'repeat' not in stim.sets[stimset]:
                stim.sets[stimset]['repeat'] = False

            stim.current[stimset] = {'file': '', 'filebase': '', 'txt': '', 'kw': '', 'ind': -1, 'data': None}
            if 'path' not in stim.sets[stimset] or (stim.sets[stimset]['path'] == None and stim.sets[stimset]['path'] == "") :
                raise Exception("No path set for Stimulus Set: " + str(stimset) + "\nIf you want to process manually, set 'type' to 'manual'")
            elif stim.sets[stimset]['path']=='None':
                pass
            else:
                stim.sets[stimset]['name'] = stimset
                stim.sets[stimset]['tokens'] = []
                if 'text' in stim.sets[stimset] and stim.sets[stimset]['text'] != '':
                    dlm_toks = ','
                    if stim.sets[stimset]['txtfmt'] != '':
                        if stim.sets[stimset]['txtfmt'].find(',') != -1:
                            fmt_toks = stim.sets[stimset]['txtfmt'].split(',')
                        else:
                            fmt_toks = stim.sets[stimset]['txtfmt'].split(' ')
                            dlm_toks = ' '
                    else:
                        fmt_toks = exp.stimtext_fmt.split(',')
                    thislisth = open(stim.sets[stimset]['text'], 'r')
                    thislist = thislisth.readlines()
                    thislisth.close()
                    thisset = {}
                    for line in thislist:
                        if line != "":
                            thistext = line.split(dlm_toks,len(fmt_toks)-1)
                            thisset[thistext[0]] = {}
                            for tkn in fmt_toks:
                                thisset[thistext[0]][tkn] = thistext[fmt_toks.index(tkn)].strip()
                filelist = sorted(os.listdir(stim.sets[stimset]['path']))
                masks = [x.strip() for x in stim.sets[stimset]['mask'].split(";")]
                for filename in filelist:
                    Goodfile = True
                    if 'mask' in stim.sets[stimset] and len(masks) > 0:
                        if not any(fnmatch.fnmatch(filename, fm) for fm in masks):
                            Goodfile = False
                    if Goodfile:
                        thisn = {}
                        thisn['name'] = filename
                        if 'text' in stim.sets[stimset] and stim.sets[stimset]['text'] != '':
                            thisn['kw'] = thisset[os.path.splitext(filename)[0]]['kw']
                            thisn['text'] = thisset[os.path.splitext(filename)[0]]['text']
                        else:
                            thisn['kw'] = ''
                            thisn['text'] = ''
                        stim.sets[stimset]['tokens'].append(thisn)
                stim.reset_order(stim, stimset)
                stim.sets[stimset]['n'] = len(stim.sets[stimset]['order_'])
# End process_stimuli


def get_current_variables(var, condition):
    '''Get current levels of each variable for a given condition
    '''
    var.current = {}
    for v in var.varlist:
        var.current[v] = var.levelsbycond[v][condition]

def get_variable_strtable(var):
    '''Creates a table specifying the levels of each variable for each condition
    '''
    vlength = {}
    out = "Condition"
    for v in var.varlist:
        vlength[v] = np.maximum(len(max(var.levelsbycond[v], key=len)), len(v)) + 2
        fmt = "%"+str(vlength[v])+"s"
        out += fmt % v
    out += "\n"
    for i in range(var.nlevels_total):
        out += "%9d" % (i+1)
        for v in var.varlist:
            fmt = "%"+str(vlength[v])+"s"
            out += fmt % var.levelsbycond[v][i]
        out += "\n"
    return out

def menu_condition(exp,run,var,stim,user):
    '''Prompts the experiment to choose the conditions to run
    '''
    strtable = exp.utils.get_variable_strtable(var) + "\nSelected Conditions: ["
    sel = []
    conditions = []
    message = ''
    for i in range(1,var.nlevels_total+1):
        conditions.append(str(i))
    while True:
        disp = strtable
        for s in sel:
            disp += " " + s
        disp += " ]\n\n%sMenu" % message
        if not exp.recordData:
            disp += "  [NO DATA WILL BE RECORDED]"
        disp += ":\nCondition # - Add condition\n"
        disp += "%11s - Add all conditions\n" % 'a'
        disp += "%11s - run exp using selected conditions in random order\n" % 'r'
        disp += "%11s - run exp using selected conditions in selected order\n" % 's'
        disp += "%11s - clear condition list\n" % 'c'
        disp += "%11s - quit\n" % (exp.quitKey)
        term.clearscreen()
        message = ''
        ret = exp.term.get_input(parent=None, title = "Gustav!", prompt = disp)
        if ret in conditions:
            sel.append(ret)
        elif ret in ['a']:
            for cond in conditions:
                sel.append(cond)
        elif ret == exp.quitKey:
            run.gustav_is_go = False
            break;
        elif ret in ['c']:
            sel = []
        elif ret in ['r']:
            if len(sel) > 0:
                sel = np.random.permutation(sel).tolist()
                for s in sel:
                    var.orderarray.append(int(s)-1)
                run.nblocks = len(var.orderarray)
                run.gustav_is_go = True
                break;
            else:
                message = "You must select at least 1 condition to run!\n\n"
        elif ret in ['s']:
            if len(sel) > 0:
                for s in sel:
                    var.orderarray.append(int(s)-1)
                run.nblocks = len(var.orderarray)
                run.gustav_is_go = True
                break;
            else:
                message = "You must select at least 1 condition to run!\n\n"

def stim_get_next(stim, stimset):
    '''Load the next stimulus for a stimulus set
    '''
    stim.current[stimset]['ind'] += 1  # Index of index
    stim.current[stimset]['ind2'] = stim.sets[stimset]['order_'][stim.current[stimset]['ind']]
    stim.current[stimset]['file'] = os.path.join(stim.sets[stimset]['path'],stim.sets[stimset]['tokens'][stim.current[stimset]['ind2']]['name'])
    stim.current[stimset]['filebase'] = os.path.splitext(stim.sets[stimset]['tokens'][stim.current[stimset]['ind2']]['name'])[0]
    stim.current[stimset]['txt'] = stim.sets[stimset]['tokens'][stim.current[stimset]['ind2']]['text']
    stim.current[stimset]['kw'] = stim.sets[stimset]['tokens'][stim.current[stimset]['ind2']]['kw']

    if stim.current[stimset]['ind'] == stim.sets[stimset]['n']-1:
        if stim.sets[stimset]['repeat']:
            stim.reset_order(stim,stimset)
        else:
            raise Exception("Ran out of stimulus files for stimset: " + stimset)


def stim_reset_order(stim, stimset):
    '''Resets the order of a stimulus set
    '''
    stim.current[stimset]['ind'] = -1
    if stim.sets[stimset]['order'] == 'random':
        stim.sets[stimset]['order_'] = np.random.permutation(len(stim.sets[stimset]['tokens']))
    elif stim.sets[stimset]['order'] == 'natural':
        stim.sets[stimset]['order_'] = np.arange(len(stim.sets[stimset]['tokens']))
    else:
        stim.sets[stimset]['order_'] = str_to_range(stim.sets[stimset]['order'])


def update_time(run):
    '''Updates the date and time
    '''
    run.time = datetime.datetime.now().strftime('%H:%M:%S')
    run.date = datetime.datetime.now().strftime('%Y-%m-%d')


def write_data(data, filename):
    '''Data IO.
    '''
    if os.path.isfile(filename):
        f = codecs.open(filename, encoding='utf-8', mode='a')
    else:
        f = codecs.open(filename, encoding='utf-8', mode='w')
        f.write("# -*- coding: utf-8 -*-\n\n")

    f.write(data)
    f.close()


def save_data(exp,run,var,stim,user, message):
    if exp.recordData:
        if message is not None and message != '':
            message_exp = exp.utils.get_expanded_vals_in_string(message, exp, run, var, stim, user)
            exp.utils.write_data(message_exp, exp.dataFile)


def log(exp,run,var,stim,user, message):
    '''Writes info to the console, to a log file, or both
    '''
    if message is not None and message != '':
        message_exp = exp.utils.get_expanded_vals_in_string(message, exp, run, var, stim, user)
        if exp.logConsole:
            print(message_exp),
        if exp.logFile is not None and exp.logFile is not '':
            write_data(message_exp, exp.logFile)

        
def debug(exp, message):
    '''Writes debug info to the console, to a log file, or both
    '''
    if exp.debug:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        dmessage = "DEBUG %s,%s: %s" % (date, time, message)
        if exp.logConsole:
            print(dmessage)
        if exp.logFile is not None and exp.logFile is not '':
            write_data(dmessage, exp.logFile)

        
def do_event(exp,run,var,stim,user, event):
    exp.utils.update_time(run)
    if hasattr(exp, "%s_" % event):
        funcs = getattr(exp, "%s_" % event)
        for f in funcs:
            if f.func_name not in exp.disable_functions:
                f(exp,run,var,stim,user)
    if hasattr(exp, 'logString_%s' % event):
        exp.utils.log(exp,run,var,stim,user, getattr(exp, 'logString_%s' % event))
    if hasattr(exp, 'dataString_%s' % event):
        exp.utils.save_data(exp,run,var,stim,user, getattr(exp, 'dataString_%s' % event))
            
        
def get_frontend(exp, frontend):
    '''Tries to load the specified frontend
    '''
    frontend_s = frontend
    if frontend_s not in exp.frontendTypes:
        print("Unknown frontend. Using tk")
        frontend = 'tk'

    try:
        frontend = __import__('frontends',globals(), locals(), frontend)
    except ImportError:
        raise Exception("Could not import frontend "+frontend)
    exp.frontend = getattr(frontend, frontend_s)

def obj_to_str(obj, name, indent=''):
    """Returns formatted, python-callable string representations of objects
        including classes, dicts, lists, and other built-in var types
    """
    if isinstance(obj, dict):
        outstr = "%s%s = {\n" % (indent, name)
        for key, val in obj.items():
            if key[:2] != "__":
                outstr += "%s    '%s' : %r,\n" % (indent, key,val)
        outstr += "%s}\n" % indent
    elif isinstance(obj, list):
        outstr = "%s%s = [\n" % (indent, name)
        for val in obj:
            outstr += "%s    %r,\n" % (indent, val)
        outstr += "%s]\n" % indent
    elif isinstance(obj,(types.ClassType,types.InstanceType)):
        outstr = "%sclass %s():\n" % (indent, name)
        items = getmembers(obj)
        for key, val in items:
            if key[:2] != "__":
                outstr += "%s    %s = %r\n" % (indent, key,val)
        outstr += "%s\n" % indent
    else:
        outstr = "%s%s = %r\n" % (indent, name, obj)

    return outstr

def get_expanded_vals_in_string(instr, exp, run, var, stim, user):
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
        $stim_kw[name]   : The current kw value for the specified stimulus set
        $stim_file[name] : The current filename for the specified stimulus set
        $stim_text[name] : The current text for the specified stimulus set
        $stim_ind[name]  : The current file ind for the specified stimulus set
        $var[varname]    : varname is the name of one of your variables
        $currentvars[';']: A delimited list of the current levels of all vars
                            The delimiter can be specified (use empty brackets
                            to specify default: ',')
        $currentvarsvals : Same as currentvars, but you will get 'var = val'
                            instead of just 'val'
        @currentvars     : Same as currentvars, but you will get var names 
                            instead of values (eg., for datafile header). 
        $user[varname]   : The value of a user variables
    """

    outstr = instr.replace("$name", exp.name)
    outstr = outstr.replace("$note", exp.note)
    outstr = outstr.replace("$comment", exp.comments)
    outstr = outstr.replace("$host", exp.host)
    outstr = outstr.replace("$subj", exp.subjID)
    outstr = outstr.replace("$trial_block", str(run.trials_block+1))
    outstr = outstr.replace("$trial", str(run.trials_exp+1))
    outstr = outstr.replace("$blocks", str(run.nblocks))
    outstr = outstr.replace("$block", str(run.block+1))
    outstr = outstr.replace("$conditions", str(var.nlevels_total))
    outstr = outstr.replace("$condition", str(run.condition+1))
    outstr = outstr.replace("$time", run.time)
    outstr = outstr.replace("$date", run.date)
    outstr = outstr.replace("$response", run.response)

    for s in stim.stimvars:
        outstr = outstr.replace("$stim_kw["+stim.sets[s]['name']+"]", stim.current[s]['kw'])
        outstr = outstr.replace("$stim_file["+stim.sets[s]['name']+"]", stim.current[s]['filebase'])
        outstr = outstr.replace("$stim_text["+stim.sets[s]['name']+"]", stim.current[s]['txt'])
        outstr = outstr.replace("$stim_ind["+stim.sets[s]['name']+"]", str(stim.current[s]['ind']))

    # This func gets called from initialize (for datafilename), and var.current is not set at that point
    if len(var.current)>0:
        currentvars = []
        currentvarsvals = []
        for key in var.current:
            currentvars.append(var.current[key])
            currentvarsvals.append(key + " = " + var.current[key])
            outstr = outstr.replace("$var["+key+"]", var.current[key])

        got_cv = True # TODO: Look into generators
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
    for key in var.varlist:
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

    items = getmembers(user)
    for key, val in items:
        if key[:2] != "__":
            outstr = outstr.replace("$user["+str(key)+"]", str(val))
            outstr = outstr.replace("@user["+str(key)+"]", str(key))

    if hasattr(var,'dynamic'):
        for key, val in var.dynamic.items():
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
        from random import shuffle
        shuffle(result)
        return result
    else:
        return sorted(result)


