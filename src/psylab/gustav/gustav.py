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
        settingsFile = exp.term.get_file(None, "Open Gustav Settings File", "", "Python or Plain Text Files (*.py *.txt);;All files (*.*)");
        if settingsFile == '':
            print "Gustav cancelled at user request"
            return;
    exp.settingsPath,exp.settingsFile = os.path.split(settingsFile)
    exp.settingsBase = os.path.splitext(exp.settingsFile)[0]
    exp.settingsFilePath = os.path.join(exp.settingsPath,exp.settingsFile)
    sys.path.append(exp.settingsPath)
    settings = __import__(exp.settingsBase)

    settings.setup(exp,run,var,stim,user)

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
        settingsFile = exp.term.get_file(None, "Open Gustav Settings File", "", "Python or Plain Text Files (*.py *.txt);;All files (*.*)");
        if settingsFile == '':
            print "Gustav cancelled at user request"
            return;
    exp.settingsPath,exp.settingsFile = os.path.split(settingsFile)
    exp.settingsBase = os.path.splitext(exp.settingsFile)[0]
    exp.settingsFilePath = os.path.join(exp.settingsPath,exp.settingsFile)
    sys.path.append(exp.settingsPath)
    settings = __import__(exp.settingsBase)

    settings.setup(exp,run,var,stim,user)

    exp.utils.process_variables(var);
    print exp.utils.get_variable_strtable(var)

# TODO: recordData should be a s
def run(settingsFile = None, subjectID = None, frontend = None, recordData = True):

    var = utils.var()
    stim = utils.stim()
    exp = utils.exp()
    run = utils.run()
    user = utils.user()
    exp.utils = utils

    sys.path.append( os.path.dirname( os.path.realpath( __file__ ) ) )

    #if settingsFile == None:
    #    settingsFile = exp.term.get_file(None, "Open "+exp.exp_name+" Settings File", "", "Python or Plain Text Files (*.py *.txt);;All files (*.*)");
    #    if settingsFile == '':
    #        print ""+exp.exp_name+" cancelled at user request"
    #        return;
    settingsFile = 'settings_adaptive.py'
    subjectID = 4

    if subjectID == None:
        exp.subjID = exp.term.get_input(parent=None, title = "Gustav!", prompt = 'Enter a Subject ID:')
        if exp.subjID == '':
            print "No Subject ID entered, Gustav cancelled at user request"
            return;
    else:
        exp.subjID = str(subjectID)

    exp.settingsPath,exp.settingsFile = os.path.split(settingsFile)
    exp.settingsBase = os.path.splitext(exp.settingsFile)[0]
    exp.settingsFilePath = os.path.join(exp.settingsPath,exp.settingsFile)
    sys.path.append(exp.settingsPath)
    exp.settings = __import__(exp.settingsBase)

    var.factvars[:] = []
    var.listvars[:] = []

    exp.settings.setup(exp,run,var,stim,user)

    exp.method_str = exp.method
    try:
        methodi = __import__('methods',globals(), locals(), exp.method_str)
    except ImportError:
        raise Exception, "Unknown experimental method: " + exp.method_str
    exp.method = getattr(methodi, exp.method_str)

    exp.utils.initialize_experiment(exp,run,var,stim,user)

    exp.recordData = recordData
    if exp.recordData:
        if not hasattr(exp, 'save_data_trial') and not hasattr(exp, 'save_data_block') and not hasattr(exp, 'save_data_exp'):
            if (exp.dataString_trial == None or exp.dataString_trial == ''):
                if (exp.dataString_block == None or exp.dataString_block == ''):
                    if (exp.dataString_exp == None or exp.dataString_exp == ''):
                        raise Exception, "Can't record data, because no available method has been specified.\nYou must specify at least one of the following:\nStrings exp.dataString_trial, exp.dataString_block, exp.dataString_exp\nFunctions: save_data_trial, save_data_block, save_data_exp"

    if var.order == 'menu':
        exp.utils.menu_condition(exp,run,var,stim,user)
    else:
        if not exp.recordData:
            print "WARNING: No data will be recorded!"
    if run.gustav_is_go == False:
        print "Gustav cancelled at user request"
        return;
    ret = exp.gui.get_yesno(None, title = "Gustav!", prompt = "Ready to begin testing?")
    if not ret:
        print "Gustav cancelled at user request"
        return;

    for f in exp.pre_exp_:
        if f.func_name not in exp.disable_functions:
            f(exp,run,var,stim,user)
    exp.utils.update_time(run)
    exp.utils.log(exp,run,var,stim,user, 'pre_exp')
    run.gustav_is_go = True
    # TODO: handle datafile headers
    #exp.utils.record_data(exp,run,var,stim,user, header=True)
    for run.block in range(run.startblock-1,var.nblocks):
        if var.order == 'prompt':
            exp.prompt_condition(exp,run,var,stim,user)
        else:
            run.condition = var.orderarray[run.block]
        if run.gustav_is_go and ( var.order == 'prompt' or run.condition+1 not in var.ignore ):
            if run.block != run.startblock: run.btrial = 0;
            else: run.btrial = run.starttrial - 1;
            run.block_on = True
            exp.utils.get_current_variables(var, stim, run.condition)
            exp.utils.update_time(run)
            for f in exp.pre_block_:
                if f.func_name not in exp.disable_functions:
                    f(exp,run,var,stim,user)
            exp.utils.log(exp,run,var,stim,user, 'pre_block')

            while run.block_on:
                # TODO: trialsperblock is method (constant) specific, and does not belong here. run.trial should be computed in methods
                run.trial = (run.block*run.trialsperblock)+run.btrial
                run.trial_on = True

                for s in stim.stimvars:
                    if stim.sets[s]['type'] != 'manual':
                        exp.utils.get_current_stimulus(stim, s)
                while run.trial_on:
                    exp.pre_trial(exp,run,var,stim,user)
                    exp.utils.log(exp,run,var,stim,user, 'pre_trial')
                    exp.present_trial(exp,run,var,stim,user)
                    exp.prompt_response(exp,run,var,stim,user)

                    for f in exp.post_trial_:
                        if f.func_name not in exp.disable_functions:
                            f(exp,run,var,stim,user)
                    exp.utils.log(exp,run,var,stim,user, 'post_trial')
                    exp.utils.save_data(exp,run,var,stim,user, 'trial')

                    run.btrial += 1

            exp.utils.update_time(run)
            for f in exp.post_block_:
                if f.func_name not in exp.disable_functions:
                    f(exp,run,var,stim,user)
            exp.utils.log(exp,run,var,stim,user, 'post_block')
            exp.utils.save_data(exp,run,var,stim,user, 'block')
            if not run.gustav_is_go:
                break;
            # End while-block loop
        if not run.gustav_is_go:
            break;
    # End block loop
    exp.utils.update_time(run)
    for f in exp.post_exp_:
        if f.func_name not in exp.disable_functions:
            f(exp,run,var,stim,user)
    exp.utils.log(exp,run,var,stim,user, 'post_exp')
    exp.utils.save_data(exp,run,var,stim,user, 'exp')

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
