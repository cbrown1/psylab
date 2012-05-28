# -*- coding: utf-8 -*-

# Copyright (c) 2008-2011 Christopher Brown; All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the distribution
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Comments and/or additions are welcome (send e-mail to: c-b@asu.edu).
#

import os, sys, fnmatch
import numpy as np
import socket
import datetime
import codecs
import types
from time import sleep
from inspect import getmembers
from waveio import wavread

class exp:
    '''Experimental settings
    '''
    name = ''
    host = socket.gethostname()
    subjID = ''
    settingsPath = ''
    settingsFile = ''
    settingsFilePath = ''
    frontend = None
    debug = False
    method = 'constant'
    prompt = ''
    responseMethod = 'key' # 'key' or 'text'. If key, be sure to set'validresponses'
    validKeys = '1, 2'  # list of valid responses
    logString_pre_trial = "" #Write this string to the console and/or logfile before every trial
    logString_post_trial = ""#Write this string to the console and/or logfileafter every trial
    logString_pre_block = "" #Write this string to the console and/or logfilebefore every block
    logString_post_block = ""#Write this string to the console and/or logfileafter every block
    logString_pre_exp = ""   #Write this string to the console and/or logfileat start of exp
    logString_post_exp = ""  #Write this string to the console and/or logfileat end of exp
    logString_header = "#A log file for Gustav\n\n" #Write this string to the logfile if it is new (variables expand to names, not values)
    logFile = 'gustav_logfile_$date.log'
    logFile_unexpanded = ""
    logConsole = True
    dataString_trial = '' #Write this string to datafile after every trial
    dataString_block = '' #Write this string to datafile after every block
    dataString_exp = ''   #Write this string to datafile at exp end
    dataString_header = '#A data file for Gustav\n\n'#Write this string to datafile if the file is new  (variables expand to names, not values)
    dataFile ='$name.csv'
    dataFile_unexpanded =''
    recordData = True
    stimtext_fmt = 'file,kw,text'  # Default format for stimulus text files
    comments = ''
    cacheTrials = False             # Unimplemented
    quitKeys = ['q', '/']
    responseTypes = ['key', 'text'] # 'key' or 'text'. If key, be sure to set'validresponses'
    disable_functions = []          # Experimenter can add function names as strings to disable them
    methodTypes = ['constant', 'staircase'] # TODO: remove methodTypes
    stimLoadTypes = ['auto', 'manual']
    stimTypes = ['soundfiles', 'manual']
    varTypes = ['stim', 'manual', 'dynamic']
    frontendTypes = ['qt', 'tk']
    from frontends import term

    def prompt_response(self,exp,run,var,stim,user):
        while True:
            ret = exp.gui.get_input(None, "Gustav!","Enter Response: ")
            # Check for valid response
            if ret in exp.validKeys_:
                # Its good. Record response
                run.response = ret
                # Exit while-True loop
                break
            elif ret in exp.quitKeys:
                # User wants to exit. Break out of block, gustav loops
                run.block_on = False
                run.gustav_is_go = False
                break

    def prompt_condition(self,exp,run,var,stim,user):
        while True:
            ret = exp.term.get_input(None, "Gustav!","Enter Condition # (1-"+str(var.nlevels_total)+"): ")
            if ret in exp.quitKeys:
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

    def post_trial(exp,run,var,stim,user):
        pass

    def post_block(exp,run,var,stim,user):
        pass

    def post_exp(exp,run,var,stim,user):
        pass

    def save_data_trial_(self,exp,run,var,stim,user):
        if exp.dataString_trial is not None and exp.dataString_trial != '':
            exp.utils.write_data(exp.utils.get_expanded_vals_in_string(exp.dataString_trial, exp, run, var, stim, user), exp.dataFile)

    def save_data_block_(self,exp,run,var,stim,user):
        if exp.dataString_block is not None and exp.dataString_block != '':
            exp.utils.write_data(exp.utils.get_expanded_vals_in_string(exp.dataString_block, exp, run, var, stim, user), exp.dataFile)

    def save_data_exp_(self,exp,run,var,stim,user):
        if exp.dataString_exp is not None and exp.dataString_exp != '':
            exp.utils.write_data(exp.utils.get_expanded_vals_in_string(exp.dataString_exp, exp, run, var, stim, user), exp.dataFile)

    pre_exp_ = [pre_exp]
    pre_block_ = [pre_block]
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
    exp.utils.get_frontend(exp, exp.frontend)
    # For the following functions, run exp version first, then method (if present), then settings:
    # pre_exp, pre_block, post_trial, post_block, post_exp
    if hasattr(exp.method, 'pre_exp'):
        exp.pre_exp_.append(exp.method.pre_exp)
    if hasattr(exp.method, 'pre_block'):
        exp.pre_block_.append(exp.method.pre_block)
    if hasattr(exp.method, 'post_trial'):
        exp.post_trial_.append(exp.method.post_trial)
    if hasattr(exp.method, 'post_block'):
        exp.post_block_.append(exp.method.post_block)
    if hasattr(exp.method, 'post_exp'):
        exp.post_exp_.append(exp.method.post_exp)

    if hasattr(exp.settings, 'pre_exp'):
        exp.pre_exp_.append(exp.settings.pre_exp)
    if hasattr(exp.settings, 'pre_block'):
        exp.pre_block_.append(exp.settings.pre_block)
    if hasattr(exp.settings, 'post_trial'):
        exp.post_trial_.append(exp.settings.post_trial)
    if hasattr(exp.settings, 'post_block'):
        exp.post_block_.append(exp.settings.post_block)
    if hasattr(exp.settings, 'post_exp'):
        exp.post_exp_.append(exp.settings.post_exp)

    # For save_data functions, look for any present in settings first, then look in method.
    # But only run one each.
    elif hasattr(exp.method, 'save_data_trial'):
        exp.save_data_trial = exp.method.save_data_trial
    elif hasattr(exp.method, 'save_data_block'):
        exp.save_data_block = exp.method.save_data_block
    elif hasattr(exp.method, 'save_data_exp'):
        exp.save_data_exp = exp.method.save_data_exp

    if hasattr(exp.settings, 'save_data_trial'):
        exp.save_data_trial = exp.settings.save_data_trial
    if hasattr(exp.settings, 'save_data_block'):
        exp.save_data_block = exp.settings.save_data_block
    if hasattr(exp.settings, 'save_data_exp'):
        exp.save_data_exp = exp.settings.save_data_exp

    # A few that should be settings-specific:
    if hasattr(exp.settings, 'present_trial'):
        exp.present_trial = exp.settings.present_trial
    if hasattr(exp.settings, 'prompt_response'):
        exp.prompt_response = exp.settings.prompt_response
    if hasattr(exp.settings, 'prompt_condition'):
        exp.prompt_condition = exp.settings.prompt_condition

    # And one that needs to be in settings
    if hasattr(exp.settings, 'pre_trial'):
        exp.pre_trial = exp.settings.pre_trial
    else:
        raise Exception, "Function `pre_trial` must be specified in exp.settings file"

    exp.utils.process_stimuli(stim)
    exp.utils.process_variables(var)
    run.nblocks = var.nblocks
    stim.debug = exp.debug
    var.debug = exp.debug
    if exp.recordData:
        datapath = os.path.split(exp.dataFile)
        if not os.path.isdir(datapath[0]):
            print "Creating datafile path: " + datapath[0]
            os.makedirs(datapath[0])
        exp.dataFile_unexpanded = exp.dataFile
        exp.dataFile = get_expanded_vals_in_string(exp.dataFile, exp, run, var, stim, user)
        if not os.path.isfile(exp.dataFile):
            exp.dataString_header = get_expanded_vals_in_string(exp.dataString_header, exp, run, var, stim, user)
            write_data(exp.dataString_header, exp.dataFile)
    logpath = os.path.split(exp.logFile)
    if not os.path.isdir(logpath[0]):
        print "Creating logfile path: " + logpath[0]
        os.makedirs(logpath[0])
    exp.logFile_unexpanded = exp.logFile
    exp.logFile = get_expanded_vals_in_string(exp.logFile, exp, run, var, stim, user)
    if not os.path.isfile(exp.logFile):
        exp.logString_header = get_expanded_vals_in_string(exp.logString_header, exp, run, var, stim, user)
        write_data(exp.logString_header, exp.logFile)
    exp.validKeys_ = exp.validKeys.split(',')
    # Make a list of the stimuli that are actually used
    for v in range(len(var.factvars)):
        if var.factvars[v]['type'] == 'stim':
            for level in var.factvars[v]['levels']:
                if level not in stim.stimvars:
                    stim.stimvars.append(level)


def process_variables(var):
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
                raise Exception, "All 'listvars' variables must either have the same number of levels, or one level"
    if len(factvars) == 0:
        for v in range(len(var.listvars)):
            var.varlist.append(var.listvars[v]['name'])
    var.nlevels_list = nlist
    var.nlevels_total = var.nlevels_fact + var.nlevels_list
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
                raise Exception, "Unable to process the following variable: " + v

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
# End process_variables


def process_stimuli(stim):
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
                raise Exception, "No path set for Stimulus Set: " + str(stimset) + "\nIf you want to process manually, set 'type' to 'manual'"
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
                reset_stim_order(stim, stimset)
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
    for i in range(1,var.nlevels_total+1):
        conditions.append(str(i))
    while True:
        disp = strtable
        for s in sel:
            disp += " " + s
        disp += " ]\n\nMenu"
        if not exp.recordData:
            disp += "  [NO DATA WILL BE RECORDED]"
        disp += ":\nCondition # - Add condition\n"
        disp += "%11s - Add all conditions\n" % 'a'
        disp += "%11s - run exp using selected conditions in random order\n" % 'r'
        disp += "%11s - run exp using selected conditions in selected order\n" % 's'
        disp += "%11s - clear condition list\n" % 'c'
        disp += "%11s - quit\n" % ", ".join(exp.quitKeys)
        clearscreen()
        ret = exp.term.get_input(parent=None, title = "Gustav!", prompt = disp)
        if ret in conditions:
            sel.append(ret)
        elif ret in ['a']:
            for cond in conditions:
                sel.append(cond)
        elif ret in exp.quitKeys:
            run.gustav_is_go = False
            break;
        elif ret in ['c']:
            sel = []
        elif ret in ['r']:
            sel = np.random.permutation(sel).tolist()
            for s in sel:
                var.orderarray.append(int(s)-1)
            run.nblocks = len(var.orderarray)
            run.gustav_is_go = True
            break;
        elif ret in ['s']:
            for s in sel:
                var.orderarray.append(int(s)-1)
            run.nblocks = len(var.orderarray)
            run.gustav_is_go = True
            break;


def get_current_stimulus(stim, stimset):
    '''Load the next stimulus for each stimulus set
    '''
    stim.current[stimset]['ind'] += 1  # Index of index
    stim.current[stimset]['ind2'] = stim.sets[stimset]['order_'][stim.current[stimset]['ind']]
    stim.current[stimset]['file'] = os.path.join(stim.sets[stimset]['path'],stim.sets[stimset]['tokens'][stim.current[stimset]['ind2']]['name'])
    stim.current[stimset]['filebase'] = os.path.splitext(stim.sets[stimset]['tokens'][stim.current[stimset]['ind2']]['name'])[0]
    stim.current[stimset]['txt'] = stim.sets[stimset]['tokens'][stim.current[stimset]['ind2']]['text']
    stim.current[stimset]['kw'] = stim.sets[stimset]['tokens'][stim.current[stimset]['ind2']]['kw']
    if stim.sets[stimset]['load'] == 'auto':
        if stim.sets[stimset]['type'] == 'soundfiles':  # Check for manual done in gustav
            if stim.debug:
                stim.current[stimset]['data'] = [0]
            else:
                stim.current[stimset]['data'],fs = wavread(stim.current[stimset]['filelist'][0])
        else:
            raise Exception, "Unknown stimulus type: " + stim.sets[stimset]['type'] + " for stimulus set: " + stimset

    if stim.current[stimset]['ind'] == stim.sets[stimset]['n']-1:
        if stim.sets[stimset]['repeat']:
            reset_stim_order(stim,stimset)
        else:
            raise Exception, "Ran out of stimulus files for stimset: " + stimset


def reset_stim_order(stim, stimset):
    '''Resets the order of stimuli
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


def log(exp,run,var,stim,user, event):
    '''Writes info to the console, to a log file, or both
    '''
    if hasattr(exp, 'logString_'+event) and getattr(exp, 'logString_'+event) is not None:
        message = exp.utils.get_expanded_vals_in_string(getattr(exp, 'logString_'+event), exp, run, var, stim, user)
        if exp.logConsole:
            print(message),
        if exp.logFile is not None and exp.logFile is not '':
            write_data(message, exp.logFile)


def write_data(data, filename):
    '''Data IO.
    '''
    if os.path.isfile(filename):
        f = codecs.open(filename, encoding='utf-8', mode='a')
    else:
        f = codecs.open(filename, encoding='utf-8', mode='w')
        f.write(u"# -*- coding: utf-8 -*-\n\n")

    f.write(data)
    f.close()


def save_data(exp,run,var,stim,user, which):
    if exp.recordData:
        if which == 'trial' and 'save_data_trial' not in exp.disable_functions:
            if hasattr(exp, 'save_data_trial'):
                exp.save_data_trial(exp,run,var,stim,user)
            else:
                exp.save_data_trial_(exp,run,var,stim,user)
        elif which == 'block' and 'save_data_block' not in exp.disable_functions:
            if hasattr(exp, 'save_data_block'):
                exp.save_data_block(exp,run,var,stim,user)
            else:
                exp.save_data_block_(exp,run,var,stim,user)
        elif which == 'exp' and 'save_data_exp' not in exp.disable_functions:
            if hasattr(exp, 'save_data_exp'):
                exp.save_data_exp(exp,run,var,stim,user)
            else:
                exp.save_data_exp_(exp,run,var,stim,user)


def get_frontend(exp, frontend):
    '''Tries to load the specified frontend
    '''
    if frontend not in exp.frontendTypes:
        print 'Unknown frontend. Using tk'
        frontend = 'tk'

    try:
        gui = __import__('frontends',globals(), locals(), frontend)
    except ImportError:
        raise Exception, "Could not import frontend "+frontend
    exp.gui = getattr(gui, frontend)

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
        $user[varname]   : Any user variables
        $resp            : The current response
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


# Now that header is its own variable, this function is not needed
def get_expanded_vars_in_string(instr, exp, run, var, stim, user):
    """Replaces all variable references with the name of the specified variable

        Or, generates a header line in a datafile
    """

    outstr = instr.replace("$name", "ExpName")
    outstr = instr.replace("$note", "Note")
    outstr = instr.replace("$comment", "Comments")
    outstr = outstr.replace("$host", "Host")
    outstr = outstr.replace("$subj", "SubjID")
    outstr = outstr.replace("$trials", "Trial")
    outstr = outstr.replace("$block", "Block")
    outstr = outstr.replace("$conditions", "Conditions")
    outstr = outstr.replace("$condition", "Condition")
    outstr = outstr.replace("$time", "Time")
    outstr = outstr.replace("$date", "Date")
    outstr = outstr.replace("$response", "Response")

    for s in stim.stimvars:
        outstr = outstr.replace("$stim_kw["+stim.sets[s]['name']+"]", "KW")
        outstr = outstr.replace("$stim_file["+stim.sets[s]['name']+"]", 'File')
        outstr = outstr.replace("$stim_text["+stim.sets[s]['name']+"]", 'Text')
        outstr = outstr.replace("$stim_ind["+stim.sets[s]['name']+"]", 'Ind')

    varlist = []
    for key in var.varlist:
        outstr = outstr.replace("$var["+key+"]", key)
        varlist.append(key)

    got_cv = True
    while got_cv:
        expr, delim = get_arg(outstr,"$currentvars")
        if expr != "":
            if delim == "":
                delim = ","
            outstr = outstr.replace(expr, delim.join(varlist))
        else:
            got_cv = False

    items = getmembers(user)
    for key, val in items:
        if key[:2] != "__":
            outstr = outstr.replace("$user["+str(key)+"]", str(key))

    if hasattr(var,'dynamic'):
        for key, val in var.dynamic.items():
            outstr = outstr.replace("$dynamic["+str(key)+"]", str(key))

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
    def get_input(parent=None, title = 'User Input', prompt = 'Enter a value:'):
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

