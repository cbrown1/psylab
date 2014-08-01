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

"""Method of constant stimuli for Gustav

    This method has three properties, which should be set in pre_exp:
    
    exp.var.constant = {
        'trialsperblock' : 10,
        'startblock' : 1,
        'starttrial' : 1,
        }

    trialsperblock sets the number of trials to run for each block, or 
        combination of experimental variable levels. This parameter is required.
        
    startblock and starttrial are intended for crash recovery, and are optional.
"""

constant_vars = {
    'trialsperblock' : 10,
    'startblock' : 1,
    'starttrial' : 1,
    }

def pre_exp(exp):
    # Only set these if None, in case they were set in experiment file setup, which has run already
    if not exp.var.constant.has_key('trialsperblock'):
        raise Exception("The following constant variables must be set: \n\nexp.var.constant['trialsperblock']\n")
    if not exp.var.constant.has_key('startblock'):
        exp.var.constant['startblock'] = 1
    if not exp.var.constant.has_key('starttrial'):
        exp.var.constant['starttrial'] = 1

    if exp.logString_pre_exp == None:
        exp.logString_pre_exp = "Experiment started: $name. Date: $date, Time: $time, Subject #: $subj\n"
    if exp.logString_pre_block == None:
        exp.logString_pre_block = "\n Block $block of $blocks started at $time; Condition: $condition ; $currentvarsvals[' ; ']\n"
    if exp.logString_post_trial == None:
        exp.logString_post_trial = " Trial $trial, Response: $response\n"
    if exp.logString_post_block == None:
        exp.logString_post_block = " Block $block of $blocks ended at $time; Condition: $condition ; $currentvarsvals[' ; ']\n"
    if exp.logString_post_exp == None:
        exp.logString_post_exp = "\nExperiment ended: $name. Date: $date, Time: $time, Subject #: $subj\n"
        
    exp.run.block = exp.var.constant['startblock']-1
        
    if exp.run.block >= exp.run.nblocks - 1:
        exp.run.gustav_is_go = False

def pre_block(exp):
    if exp.run.block == exp.var.constant['startblock'] - 1:
        exp.run.trials_block = exp.var.constant['starttrial'] - 1
        exp.run.trials_exp = (exp.var.constant['trialsperblock'] * (exp.var.constant['startblock']-1)) + (exp.run.trials_block)

def post_trial(exp):
    if exp.run.trials_block == exp.var.constant['trialsperblock']-1:
        exp.run.block_on = False
    exp.run.trial_on = False

