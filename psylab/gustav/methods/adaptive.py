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
# Comments and/or additions are welcome. Send e-mail to: cbrown1@pitt.edu.
#

"""Adaptive tracking method for Gustav

    This method has several required properties that must be set in pre_exp:
    
    exp.var.dynamic = {
            'name': '',          # Name of the dynamic variable
            'units': '',         # Units of the dynamic variable (dB, etc.)
            'alternatives': 2,   # Number of alternatives
            'steps': [0, 0],     # Stepsizes to use at each reversal (len = #revs)
            'downs': 2,          # Number of 'downs'
            'ups': 1,            # Number of 'ups'
            'val_start': 0,      # Starting value
            'val_floor': 0,      # Floor; don't go below this
            'val_ceil': 0,       # Ceiling; don't go above this
            'val_floor_n': 3,    # Number of consecutive floor values at which to quit
            'val_ceil_n': 3,     # Number of consecutive ceiling values at which to quit
            'run_n_trials': 0,   # Set to non-zero to run exactly this number of trials
            'max_trials': 0,     # Set a specific maximum number of trials to run (0=ignore)
            'vals_to_avg': 0,    # The number of values (at reversal) to average
            'step': step,        # A custom step function [optional]
           }
"""
import os, codecs
import numpy as np

# TODO: change vals to types, so we can specify the type on initialize error
# TODO: Make varnames more consistent (block, trial, etc)
dynamic_vars_user = {            # These must be set by experimenter
            'name': '',          # Name of the dynamic variable
            'units': '',         # Units of the dynamic variable
            'alternatives': 2,   # Number of alternatives
            'steps': [0, 0],     # Stepsizes to use at each reversal (len = #revs)
            'downs': 2,          # Number of 'downs'
            'ups': 1,            # Number of 'ups'
            'val_start': 0,      # Starting value
            'val_floor': 0,      # Floor
            'val_ceil': 0,       # Ceiling
            'val_floor_n': 3,    # Number of consecutive floor values to quit at
            'val_ceil_n': 3,     # Number of consecutive ceiling values to quit at
            'run_n_trials': 0,   # Set to non-zero to run exactly that number of trials
            'max_trials': 0,     # Maximum number of trials to run
            'vals_to_avg': 0,    # The number of values to average
           }
dynamic_vars_block = {           # Might be useful for stimgen or at end of block
            'msg': "",           # Description of why the block ended
            'values': [],        # Array of values
            'track': [],         # 0 = no change, -1 = reversal/dn, 1 = reversal/up
            'values_at_rev': [], # Values at reversals
            'good_run': False,   # True if the run finished normally, otherwise False
           }
dynamic_vars_track = {           # Tracking stuff
            'value': 0,          # Current dynamic value
            'val_floor_count': 0,# Number of consecutive floor trials
            'val_ceil_count': 0, # Number of consecutive ceiling trials
            'prev_dir': 0,       # Previous direction; -1 = dn, 1 = up
            'init_dir': 0,       # Initial direction; -1 = dn, 1 = up
            'cur_ups': 0,        # Counter for current number of ups
            'cur_dns': 0,        # Counter for current number of downs
            'cur_step': 0,       # Whether to step this trial; -1 = dn, 1 = up, 0 = none
            'correct': 0,        # The correct response
            'cur_correct': False,# Whether the current response was correct
            'cur_status': " ",   # For each trial, one of:
                                 #  ' ' for no change
                                 #  'v' for start dn
                                 #  '^' for start up
                                 #  '+n' for rev dn, n = reversal #
                                 #  '-n' for rev up, n = reversal #
                                 #  'fn' for floor trials, n = # consecutive floor
                                 #  'cn' for ceiling trials
           }

def step(exp):
    """ The step function
        
        Increments dynamic['value'] as needed, using the appropriate value from dynamic['steps']
        
        You can create your own custom step function in your gustav experiment 
        script by creating the function, then specifying it:

        def step(exp):
            exp.var.dynamic['value'] += exp.var.dynamic['cur_step'] * exp.var.dynamic['steps'][exp.var.dynamic['n_reversals']]
            exp.var.dynamic['value'] = max(exp.var.dynamic['value'], exp.var.dynamic['val_floor'])
            exp.var.dynamic['value'] = min(exp.var.dynamic['value'], exp.var.dynamic['val_ceil'])
        exp.var.dynamic['step'] = step
    """
    exp.var.dynamic['value'] += exp.var.dynamic['cur_step'] * exp.var.dynamic['steps'][exp.var.dynamic['n_reversals']]
    exp.var.dynamic['value'] = max(exp.var.dynamic['value'], exp.var.dynamic['val_floor'])
    exp.var.dynamic['value'] = min(exp.var.dynamic['value'], exp.var.dynamic['val_ceil'])


def track(exp):
    """ The tracking function
    """
    exp.var.dynamic['values'].append(exp.var.dynamic['value'])
    if exp.var.dynamic['cur_correct']:                         #It's a down
        exp.var.dynamic['cur_dns'] += 1                        # Increment dns
        exp.var.dynamic['cur_ups'] = 0                         # Reset ups
        if exp.var.dynamic['cur_dns'] == exp.var.dynamic['downs']: # If we have the right number of dns
            exp.var.dynamic['cur_step'] = -1                   #  Set current step
            exp.var.dynamic['cur_dns'] = 0                     #  Reset dns
            if exp.var.dynamic['prev_dir'] == -1:              #  If previous direction was dn
                exp.var.dynamic['track'].append(0)             #   No reversal
                exp.var.dynamic['cur_status'] = " "
            elif exp.var.dynamic['prev_dir'] == 0:             #  No previous direction (must be start)
                exp.var.dynamic['prev_dir'] = -1               #   Set prev_dir
                exp.var.dynamic['track'].append(0)             #   Don't record this as a change
                exp.var.dynamic['init_dir'] = -1               #   Set initial direction
                exp.var.dynamic['cur_status'] = "v"
            else:                                          #  Otherwise, its a reversal
                exp.var.dynamic['prev_dir'] = -1               #   Set prev_dir
                exp.var.dynamic['track'].append(-1)            #   Record reversal
                exp.var.dynamic['n_reversals'] += 1            #   Count it
                exp.var.dynamic['values_at_rev'].append(exp.var.dynamic['value'])
                exp.var.dynamic['cur_status'] = "-{:}".format(len(exp.var.dynamic['values_at_rev']))
        else:
            exp.var.dynamic['cur_step'] = 0                    #  No current step
            exp.var.dynamic['track'].append(0)                 #   No reversal
            exp.var.dynamic['cur_status'] = " "
    else:                                                      #It's an up
        exp.var.dynamic['cur_dns'] = 0                         # Reset dns
        exp.var.dynamic['cur_ups'] += 1                        # Increment ups
        if exp.var.dynamic['cur_ups'] == exp.var.dynamic['ups']: # If we have the right number of ups
            exp.var.dynamic['cur_step'] = 1                    #  Set current step
            exp.var.dynamic['cur_ups'] = 0                     #  Reset ups
            if exp.var.dynamic['prev_dir'] == 1:               #  If previous direction was up
                exp.var.dynamic['track'].append(0)             #   No reversal
                exp.var.dynamic['cur_status'] = " "
            elif exp.var.dynamic['prev_dir'] == 0:             #  If no previous direction (must be start)
                exp.var.dynamic['prev_dir'] = 1                #   Set prev_dir
                exp.var.dynamic['track'].append(0)             #   Don't record this as a change
                exp.var.dynamic['init_dir'] = 1                #   Set initial direction
                exp.var.dynamic['cur_status'] = "^"
            else:                                          #  Otherwise, its a reversal
                exp.var.dynamic['prev_dir'] = 1                #   Set prev_dir
                exp.var.dynamic['track'].append(1)             #   Record reversal
                exp.var.dynamic['n_reversals'] += 1            #   Count it
                exp.var.dynamic['values_at_rev'].append(exp.var.dynamic['value'])
                exp.var.dynamic['cur_status'] = "+{:}".format(len(exp.var.dynamic['values_at_rev']))
        else:                                                  # Not a reversal
            exp.var.dynamic['cur_step'] = 0                    #   No current step
            exp.var.dynamic['track'].append(0)                 #   No reversal
            exp.var.dynamic['cur_status'] = " "


def finish_trial(exp):
    '''Check for various end-of-block situations
    '''
    if exp.var.dynamic['value'] == exp.var.dynamic['val_floor']:
        if exp.var.dynamic['cur_step'] == -1:
            exp.var.dynamic['val_floor_count'] += 1
            exp.var.dynamic['cur_status'] = "f{:}".format(exp.var.dynamic['val_floor_count'])
        elif  not exp.var.dynamic['cur_correct']:
            exp.var.dynamic['val_floor_count'] = 0
        if exp.var.dynamic['val_floor_count'] == exp.var.dynamic['val_floor_n']:
            exp.run.block_on = False
            exp.var.dynamic['msg'] = "{:} consecutive floor trials reached".format(exp.var.dynamic['val_floor_n'])
    else:
        exp.var.dynamic['val_floor_count'] = 0
    if exp.var.dynamic['value'] == exp.var.dynamic['val_ceil']:
        if exp.var.dynamic['cur_step'] == 1:
            exp.var.dynamic['val_ceil_count'] += 1
            exp.var.dynamic['cur_status'] = "c{:}".format(exp.var.dynamic['val_ceil_count'])
        elif exp.var.dynamic['cur_correct']:  # At ceil, correct, but not a step. So reset ceil_count
            exp.var.dynamic['val_ceil_count'] = 0
        if exp.var.dynamic['val_ceil_count'] == exp.var.dynamic['val_ceil_n']:
            exp.run.block_on = False
            exp.var.dynamic['msg'] = "{:} consecutive ceiling trials reached".format(exp.var.dynamic['val_ceil_n'])
    else:
        exp.var.dynamic['val_ceil_count'] = 0

    if exp.run.block_on:
        if exp.var.dynamic['run_n_trials'] > 0 and exp.run.trials_block == exp.var.dynamic['run_n_trials']:
            exp.run.block_on = False
            exp.var.dynamic['good_run'] = True
            exp.var.dynamic['msg'] = "{:} trials reached".format(exp.var.dynamic['run_n_trials'])
        elif exp.var.dynamic['max_trials'] > 0 and exp.run.trials_block == exp.var.dynamic['max_trials']:
            exp.run.block_on = False
            exp.var.dynamic['good_run'] = True
            exp.var.dynamic['msg'] = "A maximum of {:} trials reached".format(exp.var.dynamic['max_trials'])
        elif exp.var.dynamic['n_reversals'] == len(exp.var.dynamic['steps'])-1: # -1 because we added one to len in pre_exp
            exp.run.block_on = False
            exp.var.dynamic['good_run'] = True
            exp.var.dynamic['msg'] = "{:} reversals reached".format(len(exp.var.dynamic['steps'])-1)

def pre_block(exp):
    missing_vars = ''
    for key,val in dynamic_vars_user.items():
        if not exp.var.dynamic.has_key(key):
            missing_vars += "exp.var.dynamic['{}']\n".format(key)
    if missing_vars != '':
            raise Exception("The following dynamic variables must be set: \n\n{}".format(missing_vars))
    d = exp.var.dynamic.copy()
    exp.var.dynamic = dynamic_vars_block.copy()
    exp.var.dynamic.update(dynamic_vars_track.copy())
    exp.var.dynamic.update(d.copy())
    if exp.var.dynamic.has_key('step'):
        exp.dynamic_step = exp.var.dynamic['step']
    else:
        exp.dynamic_step = step
    exp.var.dynamic['value'] = exp.var.dynamic['val_start']
    exp.var.dynamic['values'] = []
    exp.var.dynamic['track'] = []
    exp.var.dynamic['values_at_rev'] = []
    exp.var.dynamic['prev_dir'] = 0
    exp.var.dynamic['init_dir'] = 0
    exp.var.dynamic['n_reversals'] = 0

def post_trial(exp):
    exp.var.dynamic['cur_correct'] = str(exp.run.response)==str(exp.var.dynamic['correct'])
    track(exp)
    finish_trial(exp)
    exp.dynamic_step(exp)

    exp.run.trial_on = False

def post_block(exp):
    if exp.var.dynamic['good_run']:
        exp.var.dynamic['mean'] = np.mean(exp.var.dynamic['values_at_rev'][exp.var.dynamic['vals_to_avg']*-1:])
        exp.var.dynamic['sd'] = np.std(exp.var.dynamic['values_at_rev'][exp.var.dynamic['vals_to_avg']*-1:])
    else:
        exp.var.dynamic['mean'] = np.nan
        exp.var.dynamic['sd'] = np.nan


def pre_exp(exp):
    # Repeat the first step, to be used at reversal 0 (the start)
    exp.var.dynamic['steps'].insert(0, exp.var.dynamic['steps'][0])

    # Only set these if None, in case they were set in experiment file setup, which has run already
    if exp.logString_pre_exp == None:
        exp.logString_pre_exp = "Experiment $name started at $time\n"
    if exp.logString_pre_block == None:
        exp.logString_pre_block = "\n Block $block of $blocks started at $time; Condition: $condition ; $currentvarsvals[' ; ']\n"
    if exp.logString_pre_trial == None:
        exp.logString_pre_trial = "  Trial $trial_block, dynamic: $dynamic[value] $dynamic[units], alternative: $dynamic[correct], "
    if exp.logString_post_trial == None:
        exp.logString_post_trial = "Response: $response $dynamic[cur_status]\n"
    if exp.logString_post_block == None:
        exp.logString_post_block = " Mean: $dynamic[mean], SD: $dynamic[sd], Result: $dynamic[msg]\n Block $block of $blocks ended at $time; Condition: $condition ; $currentvarsvals[' ; ']\n"
    if exp.logString_post_exp == None:
        exp.logString_post_exp = "\nExperiment $name ended at $time\n"


def save_data_block(exp):
    """ Write data for a run (a block) in a pythonic way

        The files are written so as to be an executable python script, 
        and the data for runs are stored in python classes.
    """
    if os.path.isfile(exp.dataFile):
        f = codecs.open(exp.dataFile, encoding='utf-8', mode='a')
    else:
        f = codecs.open(exp.dataFile, encoding='utf-8', mode='w')
        f.write("# -*- coding: utf-8 -*-\n\n# A datafile created by Gustav!\n\n")
        f.write("# Experiment: {}\n\n'''{}\n'''\n\n".format(exp.name, exp.comments))
        
    f.write("class block_{}_{} ():\n".format(exp.run.date.replace("-","_"), exp.run.time.replace(":","_")))
    indent="    "
    f.write(exp.utils.obj_to_str(exp.name,'name',indent))
    f.write(exp.utils.obj_to_str(exp.note,'note',indent))
    f.write(exp.utils.obj_to_str(exp.subjID,'subjID',indent))
    f.write(exp.utils.obj_to_str(exp.run.date,'date',indent))
    f.write(exp.utils.obj_to_str(exp.run.time,'time',indent))
    f.write(exp.utils.obj_to_str(exp.host,'host',indent))
    f.write(exp.utils.obj_to_str(exp.var.current,'variables',indent))
    f.write(exp.utils.obj_to_str(exp.user,'user',indent))
    f.write(exp.utils.obj_to_str(exp.var.dynamic,'dynamic',indent))
    f.write("\n")
    f.close()
