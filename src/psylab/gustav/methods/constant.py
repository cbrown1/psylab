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


