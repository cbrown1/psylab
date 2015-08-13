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

import os
from random import shuffle
import sys
import getopt
import numpy as np
from . import utils

def configure(experimentFile = None, frontend = None):

    exp = utils.exp()
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

    experiment.setup( exp )

    exp.frontend.show_config( exp )


def info(experimentFile = None, frontend = None):

    exp = utils.exp()
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

    experiment.setup( exp )

    exp.utils.process_variables(var)
    print(exp.utils.get_variable_strtable(var))

def run(experimentFile = None, subjectID = None, frontend = None, recordData = None):

    exp = utils.exp()
    exp.utils = utils

    sys.path.append( os.path.dirname( os.path.realpath( __file__ ) ) )

    if experimentFile == None:
        experimentFile = exp.term.get_file(None, "Open Gustav Experiment File", "", "Python or Plain Text Files (*.py *.txt);;All files (*.*)")
        if experimentFile == '':
            exp.utils.log(exp, "Gustav cancelled at user request (Prompt for Experiment File)")
            return

    if subjectID == None:
        exp.subjID = exp.term.get_input(parent=None, title = "Gustav!", prompt = 'Enter a Subject ID:')
        q = exp.quitKeys
        q.append('')
        if exp.subjID in q:
            exp.utils.log(exp, "Gustav cancelled at user request (Prompt for Subject ID)")
            return
    else:
        exp.subjID = str(subjectID)

    exp.experimentPath,exp.experimentFile = os.path.split(experimentFile)
    exp.experimentBase = os.path.splitext(exp.experimentFile)[0]
    exp.experimentFilePath = os.path.join(exp.experimentPath,exp.experimentFile)
    sys.path.append(exp.experimentPath)
    exp.experiment = __import__(exp.experimentBase)

    exp.experiment.setup( exp )

    exp.method_str = exp.method
    try:
        methodi = __import__('methods',globals(), locals(), exp.method_str)
    except ImportError:
        raise Exception("Error importing experimental method: " + exp.method_str)
    exp.method = getattr(methodi, exp.method_str)

    exp.utils.initialize_experiment( exp )
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
                exp.utils.log(exp, "Gustav cancelled at user request (Prompt to record data)")
                return
            else:
                exp.utils.log(exp, "WARNING: No data will be recorded!")
    else:
        exp.utils.log(exp, "WARNING: No data will be recorded!")
    if exp.var.order == 'menu':
        exp.utils.menu_condition( exp )

    if exp.run.gustav_is_go == False:
        exp.utils.log(exp, "Gustav cancelled at user request (Prompt to select conditions)")
        return
    ret = exp.frontend.get_yesno(None, title = "Gustav!", prompt = "Ready to begin testing?")
    if not ret:
        exp.utils.log(exp, "Gustav cancelled at user request (Prompt to begin testing)")
        return

    exp.utils.update_time(exp.run)
    if not os.path.isfile(exp.dataFile):
        exp.utils.save_data(exp, 'header')
    exp.utils.do_event(exp, 'pre_exp')
    exp.run.trials_exp = 0
    exp.run.gustav_is_go = True
    while exp.run.gustav_is_go:
        if exp.var.order == 'prompt':
            exp.prompt_condition(exp)
        else:
            exp.run.condition = exp.var.orderarray[exp.run.block]
        if exp.var.order == 'prompt' or exp.run.condition+1 not in exp.var.ignore:
            exp.run.trials_block = 0
            exp.utils.get_current_variables(exp)
            exp.utils.do_event(exp, 'pre_block')
            exp.run.block_on = True
            while exp.run.block_on:
                exp.run.trial_on = True
                while exp.run.trial_on:
                    exp.utils.do_event(exp, 'pre_trial')
                    exp.present_trial(exp)
                    exp.prompt_response(exp)
                    exp.utils.do_event(exp, 'post_trial')
                    exp.run.trials_block += 1
                    exp.run.trials_exp += 1

            exp.utils.do_event(exp, 'post_block')
            exp.run.block += 1
            if exp.var.order != 'prompt' and exp.run.block == exp.run.nblocks:
                exp.run.gustav_is_go = False

    # End gustav_is_go loop
    exp.utils.do_event(exp, 'post_exp')

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

