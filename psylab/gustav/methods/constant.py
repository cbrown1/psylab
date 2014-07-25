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
# Comments and/or additions are welcome. Send e-mail to: cbrown1@pitt.edu.
#

'''Method of constant stimuli for Gustav

'''

#def initialize(exp,run,var,stim,user):
#    pass

def pre_exp(exp):
    # Only set these if None, in case they were set in experiment file setup, which has run already
    if exp.logString_pre_exp == None:
        exp.logString_pre_exp = "Experiment $name started at $time\n"
    if exp.logString_pre_block == None:
        exp.logString_pre_block = "\n Block $block of $blocks started at $time; Condition: $condition ; $currentvarsvals[' ; ']\n"
    if exp.logString_post_trial == None:
        exp.logString_post_trial = " Trial $trial, Response: $response\n"
    if exp.logString_post_block == None:
        exp.logString_post_block = " Block $block of $blocks ended at $time; Condition: $condition ; $currentvarsvals[' ; ']\n"
    if exp.logString_post_exp == None:
        exp.logString_post_exp = "\nExperiment $name ended at $time\n"
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

