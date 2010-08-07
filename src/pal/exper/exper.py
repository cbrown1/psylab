# -*- coding: utf-8 -*-

# Copyright (c) 2008-2010 Christopher Brown; All Rights Reserved.
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

"""Experiment - A Python script to run psychophysical experiments

    The goal of Experiment is to handle the routines that are common across
    experiments (like the psychophysical procedure, keeping track of
    responses, writing to data files, etc), to allow the experimenter to
    worry about the things that are unique to each experiment (like the
    design, stimulus generation, etc.).

    See settings.py for more information.
"""

import os
from random import shuffle
import sys
import getopt
import numpy as np
import utils

def configure(settingsFile = None, frontend = None):

    var = utils.var()
    stim = utils.stim()
    exp = utils.exp()
    run = utils.run()
    user = utils.user()
    exp.utils = utils
    exp.utils.get_frontend(exp, frontend)

    # Settings File
    if settingsFile == None:
        settingsFile = exp.term.get_file(None, "Open Exper Settings File", "", "Python or Plain Text Files (*.py *.txt);;All files (*.*)");
        if settingsFile == '':
            print "Exper cancelled at user request"
            return;
    exp.settingsPath,exp.settingsFile = os.path.split(settingsFile)
    exp.settingsBase = os.path.splitext(exp.settingsFile)[0]
    exp.settingsFilePath = os.path.join(exp.settingsPath,exp.settingsFile)
    sys.path.append(exp.settingsPath)
    settings = __import__(exp.settingsBase)

    settings.setup(exp,run,stim,var,user)

    exp.gui.show_config( exp, run, stim, var, user )


def list_conditions(settingsFile = None, frontend = None):

    var = utils.var()
    stim = utils.stim()
    exp = utils.exp()
    run = utils.run()
    user = utils.user()
    exp.utils = utils

    # Settings File
    if settingsFile == None:
        settingsFile = exp.term.get_file(None, "Open Exper Settings File", "", "Python or Plain Text Files (*.py *.txt);;All files (*.*)");
        if settingsFile == '':
            print "Exper cancelled at user request"
            return;
    exp.settingsPath,exp.settingsFile = os.path.split(settingsFile)
    exp.settingsBase = os.path.splitext(exp.settingsFile)[0]
    exp.settingsFilePath = os.path.join(exp.settingsPath,exp.settingsFile)
    sys.path.append(exp.settingsPath)
    settings = __import__(exp.settingsBase)

    settings.setup(exp,run,stim,var,user)

    exp.utils.process_variables(var);
    print exp.utils.get_variable_strtable(var)


def run(settingsFile = None, subjectID = None, frontend = None, recordData = True):

    var = utils.var()
    stim = utils.stim()
    exp = utils.exp()
    run = utils.run()
    user = utils.user()
    exp.utils = utils

    sys.path.append( os.path.dirname( os.path.realpath( __file__ ) ) )

    if settingsFile == None:
        settingsFile = exp.term.get_file(None, "Open Exper Settings File", "", "Python or Plain Text Files (*.py *.txt);;All files (*.*)");
        if settingsFile == '':
            print "Exper cancelled at user request"
            return;

    if subjectID == None:
        exp.subjID = exp.term.get_input(parent=None, title = 'Exper!', prompt = 'Enter a Subject ID:')
        if exp.subjID == '':
            print "No Subject ID entered, Exper cancelled at user request"
            return;
    else:
        exp.subjID = str(subjectID)

    exp.settingsPath,exp.settingsFile = os.path.split(settingsFile)
    exp.settingsBase = os.path.splitext(exp.settingsFile)[0]
    exp.settingsFilePath = os.path.join(exp.settingsPath,exp.settingsFile)
    sys.path.append(exp.settingsPath)
    settings = __import__(exp.settingsBase)

    settings.setup(exp,run,stim,var,user)

    try:
        methodi = __import__('methods',globals(), locals(), exp.method)
    except ImportError:
        raise Exception, "Unknown experimental method: " + exp.method
    method = getattr(methodi, exp.method)
    print method

    exp.utils.get_frontend(exp, frontend)

    if hasattr(settings, 'prompt_response'):
        exp.prompt_response = settings.prompt_response;
    if hasattr(settings, 'prompt_condition'):
        exp.prompt_condition = settings.prompt_condition

    if hasattr(settings, 'pre_trial'):
        exp.pre_trial = settings.pre_trial
    else:
        raise Exception, "Function pre_trial must be specified in settings file"
    if hasattr(settings, 'post_trial'):
        exp.post_trial = settings.post_trial
    else:
        exp.post_trial = method.post_trial
    if hasattr(settings, 'pre_exp'):
        exp.pre_exp = settings.pre_exp
    else:
        exp.pre_exp = method.pre_exp
    if hasattr(settings, 'post_exp'):
        exp.post_exp = settings.post_exp
    else:
        exp.post_exp = method.post_exp

    exp.utils.process_initialize(exp,run,var,stim,user)
    exp.recordData = recordData
    if exp.recordData:
        if exp.dataString_Trial == '' or exp.dataString_Trial == None:
            raise Exception, "Can't record data, variable not set: exp.dataString_Trial"

    if var.order == 'menu':
        exp.utils.menu_condition(exp,run,var,stim,user)
    else:
        if not exp.recordData:
            print "WARNING: No data will be recorded!"
    if run.exper_is_go == False:
        print "Exper cancelled at user request"
        return;
    ret = exp.gui.get_yesno(None, title = 'Exper!', prompt = "Ready to begin testing?")
    if not ret:
        print "Exper cancelled at user request"
        return;

    exp.pre_exp(exp,run,var,stim,user)

    # Begin block loop
    exp.utils.update_time(run)
    logstr = "\nTesting started on %s at %s. Exp: %s. Subject: %s.\n" % (run.date, run.time, exp.name, exp.subjID)
    exp.utils.log(logstr, exp.logFile)
    run.exper_is_go = True
    exp.utils.record_data(exp,run,var,stim,user, header=True)
    for run.block in range(run.startblock-1,var.nblocks):
        if var.order == 'prompt':
            exp.prompt_condition(exp,run,stim,var,user)
        else:
            run.condition = var.orderarray[run.block]
        if run.exper_is_go and ( var.order == 'prompt' or run.condition+1 not in var.ignore ):
            if run.block != run.startblock: run.btrial = 0;
            else: run.btrial = run.starttrial - 1;
            run.block_on = True
            exp.utils.get_current_variables(var, stim, run.condition)
            exp.utils.update_time(run)
            if exp.consoleString_Block != '':
                thisString = exp.utils.get_expanded_vals_in_string(exp.consoleString_Block, exp, run, var, stim, user)
                exp.utils.log(thisString,exp.logFile)
            exp.utils.record_data(exp,run,var,stim,user, block=True)

            while run.block_on:
                run.trial = (run.block*run.trialsperblock)+run.btrial
                run.trial_on = True

                for s in stim.stimvars:
                    if stim.sets[s]['type'] != 'manual':
                        exp.utils.get_current_stimulus(stim, s)
                while run.trial_on:
                    exp.pre_trial(exp,run,stim,var,user)
                    exp.prompt_response(exp,run,stim,var,user)
                    exp.post_trial(exp,run,stim,var,user);

                if exp.consoleString_Trial != '':
                    thisString = exp.utils.get_expanded_vals_in_string(exp.consoleString_Trial, exp, run, var, stim, user)
                    exp.utils.log(thisString,exp.logFile)
                exp.utils.record_data(exp,run,var,stim,user)

                run.btrial += 1

            if not run.exper_is_go:
                break;
            # End while-block loop
        if not run.exper_is_go:
            break;
    # End block loop
    exp.utils.update_time(run)
    logstr = "Testing ended on %s at %s. Exp: %s. Subject: %s.\n" % (run.date, run.time, exp.name, exp.subjID)
    exp.utils.log(logstr, exp.logFile)

if __name__ == '__main__':
    settingsFile = None
    subjectID = None
    frontend = None
    recordData = True
    action = 'run'
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hcldf:s:i:", ["help", "config", "list", "dontrecord", "frontend=", "settingsFile=", "subjectID="])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    for var, val in opts:
        if var in ("-h", "--help"):
            print __doc__
            sys.exit(0)
        elif var in ["--settingsFile", "-s"]:
            settingsFile = val
        elif var in ["--subjectID", "-i"]:
            subjectID = val
        elif var in ["--frontend", "-f"]:
            frontend = val
        elif var in ["--config", "-c"]:
            action = 'config'
        elif var in ["--dontrecord", "-d"]:
            recordData = False
        elif var in ["--list", "-l"]:
            action = 'list'
    if action in ['config']:
        configure(settingsFile = settingsFile, frontend = frontend)
    elif action in ['list']:
        list_conditions(settingsFile = settingsFile, frontend = frontend)
    else:
        run(settingsFile = settingsFile, subjectID = subjectID, frontend = frontend, recordData = recordData)
