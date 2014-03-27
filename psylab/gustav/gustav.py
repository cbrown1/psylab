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

import os
from random import shuffle
import sys
import getopt
import numpy as np
from . import utils

def configure(experimentFile = None, frontend = None):

    var = utils.var()
    stim = utils.stim()
    exp = utils.exp()
    run = utils.run()
    user = utils.user()
    exp.utils = utils
    exp.utils.get_frontend(exp, frontend)

    # Experiment File
    if experimentFile == None:
        experimentFile = exp.term.get_file(None, "Open Gustav Experiment File", "", "Python or Plain Text Files (*.py *.txt);;All files (*.*)")
        if experimentFile == '':
            print("Gustav cancelled at user request")
            return
    exp.experimentPath,exp.experimentFile = os.path.split(experimentFile)
    exp.experimentBase = os.path.splitext(exp.experimentFile)[0]
    exp.experimentFilePath = os.path.join(exp.experimentPath,exp.experimentFile)
    sys.path.append(exp.experimentPath)
    experiment = __import__(exp.experimentBase)

    experiment.setup( exp, run, var, stim, user)

    exp.frontend.show_config( exp, run, var, stim, user )


def info(experimentFile = None, frontend = None):

    exp = utils.exp()
    run = utils.run()
    var = utils.var()
    stim = utils.stim()
    user = utils.user()
    exp.utils = utils

    # Experiment File
    if experimentFile == None:
        experimentFile = exp.term.get_file(None, "Open Gustav Experiment File", "", "Python or Plain Text Files (*.py *.txt);;All files (*.*)")
        if experimentFile == '':
            print("Gustav cancelled at user request")
            return
    exp.experimentPath,exp.experimentFile = os.path.split(experimentFile)
    exp.experimentBase = os.path.splitext(exp.experimentFile)[0]
    exp.experimentFilePath = os.path.join(exp.experimentPath,exp.experimentFile)
    sys.path.append(exp.experimentPath)
    experiment = __import__(exp.experimentBase)

    experiment.setup( exp, run, var, stim, user)

    exp.utils.process_variables(var)
    print(exp.utils.get_variable_strtable(var))

def run(experimentFile = None, subjectID = None, frontend = None, recordData = None):

    exp = utils.exp()
    run = utils.run()
    var = utils.var()
    stim = utils.stim()
    user = utils.user()
    exp.utils = utils

    sys.path.append( os.path.dirname( os.path.realpath( __file__ ) ) )

    if experimentFile == None:
        experimentFile = exp.term.get_file(None, "Open Gustav Experiment File", "", "Python or Plain Text Files (*.py *.txt);;All files (*.*)")
        if experimentFile == '':
            print("Gustav cancelled at user request")
            return

    if subjectID == None:
        exp.subjID = exp.term.get_input(parent=None, title = "Gustav!", prompt = 'Enter a Subject ID:')
        q = exp.quitKeys
        q.append('')
        if exp.subjID in q:
            print("Gustav cancelled at user request")
            return
    else:
        exp.subjID = str(subjectID)

    exp.experimentPath,exp.experimentFile = os.path.split(experimentFile)
    exp.experimentBase = os.path.splitext(exp.experimentFile)[0]
    exp.experimentFilePath = os.path.join(exp.experimentPath,exp.experimentFile)
    sys.path.append(exp.experimentPath)
    exp.experiment = __import__(exp.experimentBase)

    #var.factvars[:] = []
    #var.listvars[:] = []

    exp.experiment.setup( exp, run, var, stim, user )

    exp.method_str = exp.method
    try:
        methodi = __import__('methods',globals(), locals(), exp.method_str)
    except ImportError:
        raise Exception("Unknown experimental method: " + exp.method_str)
    exp.method = getattr(methodi, exp.method_str)

    exp.utils.initialize_experiment(exp,run,var,stim,user)
    if recordData is not None:
        exp.recordData = recordData

    if exp.recordData:
        got_dataString = False
        for datatype in exp.eventTypes:
            if hasattr(exp, 'dataString_%s' % datatype):
                got_dataString = True
                break
        if not got_dataString:
            ret = exp.frontend.get_yesno(None, title = "Gustav!", 
                    prompt = "exp.recordData == True, but no dataStrings were found so no data will be record data.\nAre you sure you want to continue?")
            if not ret:
                print("Gustav cancelled at user request")
                return
    else:
        print("WARNING: No data will be recorded!")
    if var.order == 'menu':
        exp.utils.menu_condition(exp,run,var,stim,user)

    if run.gustav_is_go == False:
        print("Gustav cancelled at user request")
        return
    ret = exp.frontend.get_yesno(None, title = "Gustav!", prompt = "Ready to begin testing?")
    if not ret:
        print("Gustav cancelled at user request")
        return

    exp.utils.update_time(run)
    if not os.path.isfile(exp.dataFile):
        exp.utils.save_data(exp,run,var,stim,user, 'header')
    exp.utils.do_event(exp,run,var,stim,user, 'pre_exp')
    run.trials_exp = 0
    run.gustav_is_go = True
    while run.gustav_is_go:
        if var.order == 'prompt':
            exp.prompt_condition(exp,run,var,stim,user)
        else:
            run.condition = var.orderarray[run.block]
        if var.order == 'prompt' or run.condition+1 not in var.ignore:
            run.trials_block = 0
            exp.utils.do_event(exp,run,var,stim,user, 'pre_block')
            exp.utils.get_current_variables(exp, var, run.condition)
            print(run.trials_block)
            print(run.trials_exp)
            run.block_on = True
            while run.block_on:
                exp.utils.get_current_stimuli(exp, stim)
                run.trial_on = True
                while run.trial_on:
                    exp.utils.do_event(exp,run,var,stim,user, 'pre_trial')
                    exp.present_trial(exp,run,var,stim,user)
                    exp.prompt_response(exp,run,var,stim,user)
                    exp.utils.do_event(exp,run,var,stim,user, 'post_trial')
                    run.trials_block += 1
                    run.trials_exp += 1

            exp.utils.do_event(exp,run,var,stim,user, 'post_block')
            run.block += 1
            if var.order != 'prompt' and run.block == run.nblocks:
                run.gustav_is_go = False

    # End gustav_is_go loop
    exp.utils.do_event(exp,run,var,stim,user, 'post_exp')

def main(argv):
    experimentFile = None
    subjectID = None
    frontend = None
    recordData = None
    action = 'run'
    try:
        opts, args = getopt.getopt(argv, "hcdif:e:s:", ["help", "config", "dontrecord", "info", "frontend=", "experimentFile=", "subjectID="])
    except (getopt.error, msg):
        print(msg)
        print("for help use --help")
        sys.exit(2)
    for var, val in opts:
        if var in ("--help", "-h"):
            print(__doc__)
            sys.exit(0)
        elif var in ("--experimentFile", "-e"):
            experimentFile = val
        elif var in ("--subjectID", "-s"):
            subjectID = val
        elif var in ("--frontend", "-f"):
            frontend = val
        elif var in ("--config", "-c"):
            action = 'config'
        elif var in ("--dontrecord", "-d"):
            recordData = False
        elif var in ("--info", "-i"):
            action = 'info'
    if action in ('config'):
        configure(experimentFile = experimentFile, frontend = frontend)
    elif action in ('list'):
        info(experimentFile = experimentFile, frontend = frontend)
    else:
        run(experimentFile = experimentFile, subjectID = subjectID, frontend = frontend, recordData = recordData)

if __name__ == '__main__':
    main(sys.argv[1:])

