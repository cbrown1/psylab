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

'''Adaptive tracking method for Gustav

'''
import os, codecs
from inspect import getmembers
import numpy as np

# TODO: change vals to types, so we can specify the type on initialize error
# TODO: Make varnames more consistent (block, trial, etc)
dynamic_vars_user = {            # These must be set by experimenter
            'name': '',          # Name of the dynamic variable
            'units': '',         # Units of the dynamic variable
            'intervals': 2,      # Number of intervals
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
            'good_run': False,   # True if the run did finished normally, otherwise False
           }
dynamic_vars_track = {           # These vals are used for tracking
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

def step(cur_step,exp,run,var,stim,user):
    if len(var.dynamic['values_at_rev']) == 0:
        # If there are no reversals yet, use first step
        var.dynamic['value'] += cur_step * var.dynamic['steps'][0]
    else:
        var.dynamic['value'] += cur_step * var.dynamic['steps'][len(var.dynamic['values_at_rev'])-1]
    var.dynamic['value'] = max(var.dynamic['value'], var.dynamic['val_floor'])
    var.dynamic['value'] = min(var.dynamic['value'], var.dynamic['val_ceil'])


def track(exp,run,var,stim,user):
    var.dynamic['values'].append(var.dynamic['value'])
    if var.dynamic['cur_correct']:
        var.dynamic['cur_dns'] += 1                        # Increment dns
        var.dynamic['cur_ups'] = 0                         # Reset ups
        if var.dynamic['cur_dns'] == var.dynamic['downs']: # If we have the right number of dns
            var.dynamic['cur_step'] = -1                   #  Set current step
            var.dynamic['cur_dns'] = 0                     #  Reset dns
            if var.dynamic['prev_dir'] == -1:              #  If previous direction was dn
                var.dynamic['track'].append(0)             #   No reversal
                var.dynamic['cur_status'] = " "
            elif var.dynamic['prev_dir'] == 0:             #  If no previous direction (must be start)
                var.dynamic['prev_dir'] = -1               #   Set prev_dir
                var.dynamic['track'].append(0)             #   Don't record this as a change
                var.dynamic['init_dir'] = -1               #   Set initial direction
                var.dynamic['cur_status'] = "v"
            else:                                          #  Otherwise, its a reversal
                var.dynamic['prev_dir'] = -1               #   Set prev_dir
                var.dynamic['track'].append(-1)            #   Record reversal
                var.dynamic['values_at_rev'].append(var.dynamic['value'])
                var.dynamic['cur_status'] = "-%g" % len(var.dynamic['values_at_rev'])
        else:
            var.dynamic['cur_step'] = 0                    #  No current step
            var.dynamic['track'].append(0)                 #   No reversal
            var.dynamic['cur_status'] = " "
    else:
        var.dynamic['cur_dns'] = 0                         # Reset dns
        var.dynamic['cur_ups'] += 1                        # Increment ups
        if var.dynamic['cur_ups'] == var.dynamic['ups']:   # If we have the right number of ups
            var.dynamic['cur_step'] = 1                    #  Set current step
            var.dynamic['cur_ups'] = 0                     #  Reset ups
            if var.dynamic['prev_dir'] == 1:               #  If previous direction was up
                var.dynamic['track'].append(0)             #   No reversal
                var.dynamic['cur_status'] = " "
            elif var.dynamic['prev_dir'] == 0:             #  If no previous direction (must be start)
                var.dynamic['prev_dir'] = 1                #   Set prev_dir
                var.dynamic['track'].append(0)             #   Don't record this as a change
                var.dynamic['init_dir'] = 1                #   Set initial direction
                var.dynamic['cur_status'] = "^"
            else:                                          #  Otherwise, its a reversal
                var.dynamic['prev_dir'] = 1                #   Set prev_dir
                var.dynamic['track'].append(1)             #   Record reversal
                var.dynamic['values_at_rev'].append(var.dynamic['value'])
                var.dynamic['cur_status'] = "+%g" % len(var.dynamic['values_at_rev'])
        else:
            var.dynamic['cur_step'] = 0                    #  No current step
            var.dynamic['track'].append(0)                 #   No reversal
            var.dynamic['cur_status'] = " "


def finish_trial(exp, run, var, stim, user):
    '''Check for various end-of-block situations
    '''
    if var.dynamic['value'] == var.dynamic['val_floor']:
        if var.dynamic['cur_step'] == -1:
            var.dynamic['val_floor_count'] += 1
            var.dynamic['cur_status'] = "f%g" % var.dynamic['val_floor_count']
        elif  not var.dynamic['cur_correct']:
            var.dynamic['val_floor_count'] = 0
        if var.dynamic['val_floor_count'] == var.dynamic['val_floor_n']:
            run.block_on = False
            var.dynamic['msg'] = '%g consecutive floor trials reached' % var.dynamic['val_floor_n']
    else:
        var.dynamic['val_floor_count'] = 0
    if var.dynamic['value'] == var.dynamic['val_ceil']:
        if var.dynamic['cur_step'] == 1:
            var.dynamic['val_ceil_count'] += 1
            var.dynamic['cur_status'] = "c%g" % var.dynamic['val_ceil_count']
        elif var.dynamic['cur_correct']:  # At ceil, correct, but not a step. So reset ceil_count
            var.dynamic['val_ceil_count'] = 0
        if var.dynamic['val_ceil_count'] == var.dynamic['val_ceil_n']:
            run.block_on = False
            var.dynamic['msg'] = '%g consecutive ceiling trials reached' % var.dynamic['val_ceil_n']
    else:
        var.dynamic['val_ceil_count'] = 0

    if run.block_on:
        if var.dynamic['run_n_trials'] > 0 and run.trial == var.dynamic['run_n_trials']:
            run.block_on = False
            var.dynamic['good_run'] = True
            var.dynamic['msg'] = '%g trials reached' % var.dynamic['run_n_trials']
        elif var.dynamic['max_trials'] > 0 and run.trial == var.dynamic['max_trials']:
            run.block_on = False
            var.dynamic['good_run'] = True
            var.dynamic['msg'] = 'A maximum of %g trials reached' % var.dynamic['max_trials']
        elif len(var.dynamic['values_at_rev']) == len(var.dynamic['steps']):
            run.block_on = False
            var.dynamic['good_run'] = True
            var.dynamic['msg'] = '%g reversals reached' % len(var.dynamic['steps'])

def pre_block(exp, run, var, stim, user):
    missing_vars = ''
    for key,val in dynamic_vars_user.items():
        if not var.dynamic.has_key(key):
            missing_vars += "var.dynamic['" + key + "']\n"
    if missing_vars != '':
            raise Exception, "The following dynamic variables must be set: \n\n%s" % missing_vars
    d = var.dynamic.copy()
    var.dynamic = dynamic_vars_block.copy()
    var.dynamic.update(dynamic_vars_track.copy())
    var.dynamic.update(d.copy())
    if hasattr(exp.settings, 'step'):
        exp.dynamic_step = exp.settings.step
    else:
        exp.dynamic_step = step
    var.dynamic['value'] = var.dynamic['val_start']
    var.dynamic['values'] = []
    var.dynamic['track'] = []
    var.dynamic['values_at_rev'] = []
    var.dynamic['prev_dir'] = 0
    var.dynamic['init_dir'] = 0

def post_trial(exp, run, var, stim, user):
    var.dynamic['cur_correct'] = str(run.response)==str(var.dynamic['correct'])
    track(exp, run, var, stim, user)
    finish_trial(exp, run, var, stim, user)
    exp.dynamic_step(var.dynamic['cur_step'], exp, run, var, stim, user)

    run.trial_on = False

def post_block(exp, run, var, stim, user):
    if var.dynamic['good_run']:
        var.dynamic['mean'] = np.mean(var.dynamic['values_at_rev'][var.dynamic['vals_to_avg']*-1:])
        var.dynamic['sd'] = np.std(var.dynamic['values_at_rev'][var.dynamic['vals_to_avg']*-1:])
    else:
        var.dynamic['mean'] = np.nan
        var.dynamic['sd'] = np.nan

def record_block_data(exp,run,var,stim,user):
    if os.path.isfile(exp.dataFile):
        f = codecs.open(exp.dataFile, encoding='utf-8', mode='a')
    else:
        f = codecs.open(exp.dataFile, encoding='utf-8', mode='w')
        f.write(u"# -*- coding: utf-8 -*-\n\n# A datafile created by Gustav\n\n")
    f.write(u"block_%s_%s = {\n" % (run.date.replace("-","_"), run.time.replace(":","_")))
    f.write(u"    'name' : '%s',\n" % exp.name)
    f.write(u"    'note' : '%s',\n" % exp.note)
    f.write(u"    'subjid' : '%s',\n" % exp.subjID)
    f.write(u"    'date' : '%s',\n" % run.date)
    f.write(u"    'time' : '%s',\n" % run.time)
    f.write(u"    'host' : '%s',\n" % exp.host)

    f.write(u"    'variables' : {\n")
    for key, val in var.current.items():
        f.write(u"        '%s' : %r,\n" % (key, val))
    f.write(u"    },\n")

    items = getmembers(user)
    f.write(u"    'user' : {\n")
    for key, val in items:
        if key[:2] != "__":
            f.write(u"        '%s' : %r,\n" % (key, val))
    f.write(u"    },\n")

    f.write(u"    'dynamic' : {\n")
    for key, val in var.dynamic.items():
        if key not in exp.method.dynamic_vars_track:
            f.write(u"        '%s' : %r,\n" % (key, val))
    f.write(u"    },\n}\n\n")
    f.close()
