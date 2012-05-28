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
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# Comments and/or additions are welcome. Send e-mail to: cbrown1@pitt.edu.
#

'''Method of constant stimuli for Gustav

'''
import os, codecs

#def initialize(exp,run,var,stim,user):
#    pass

# TODO: add trialsperblock, startblock, starttrial

def pre_exp(exp, run, var, stim, user):
    # Only set these if empty, in case they were set in settings file setup, which has run already
    if exp.logString_pre_exp == "":
        exp.logString_pre_exp = "Experiment $name started at $time\n"
    if exp.logString_pre_block == "":
        exp.logString_pre_block = "\n Block $block of $blocks started at $time; Condition: $condition ; $currentvarsvals[' ; ']\n"
    if exp.logString_post_trial == "":
        exp.logString_post_trial = " Trial $trial, Response: $response\n"
    if exp.logString_post_block == "":
        exp.logString_post_block = " Block $block of $blocks ended at $time; Condition: $condition ; $currentvarsvals[' ; ']\n"
    if exp.logString_post_exp == "":
        exp.logString_post_exp = "\nExperiment $name ended at $time\n"
    run.block = var.constant['startblock']-1
    if run.block == run.nblocks - 1:
        run.gustav_is_go = False
    # Check if there are enough stimuli
    # Move to settingsfile? Are stim issues really method related?
    for stimset in stim.stimvars:
        if stim.sets[stimset]['type'] != 'manual':
            if not stim.sets[stimset]['repeat']:
                if var.constant['trialsperblock']*var.nlevels_total > stim.sets[stimset]['n']:
                    raise Exception,  "Not enough stimulus files for stimset: " + stimset + "\nNeeded for design: " + str(run.trialsperblock*var.nlevels_total) + "\nAvailable: " + str(stim.sets[stimset]['n'])

def post_trial(exp, run, var, stim, user):
    run.stim_index = run.trials_exp # Not used atm
    if run.trials_block == var.constant['trialsperblock']-1:
        run.block_on = False
    run.trial_on = False


