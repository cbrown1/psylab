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
# Psylab is a collection of Python modules for handling various aspects 
# of psychophysical experimentation. Python is a powerful programming  
# language that is free, open-source, easy-to-learn, and cross-platform, 
# thus making it extremely well-suited to scientific applications. 
# There are countless modules written by other scientists that are  
# freely available, making Python a good choice regardless of your  
# particular field. Consider using Python as your scientific platform.
# 

# A Gustav experiment file!

import os, sys
import numpy as np
import psylab
from gustav_forms import qt_speech as theForm
import medussa as m

def setup(exp,run,var,stim,user):

    if os.name == 'posix':
        basedir = os.path.expanduser(os.path.join('~','Python'))
    else:
        basedir = os.path.expanduser(os.path.join('~','Documents','Python')) # Win7
        basedir = os.path.expanduser(os.path.join('~','My Documents','Python'))

    # General Experimental Variables
    exp.name = 'SNR_exp'
    exp.method = 'constant' # 'constant' for constant stimuli, or 'adaptive' for a staircase procedure (SRT, etc)
    # TODO: move logstring and datastring vars out of exp and into either method or experiment, so they can be properly enumerated at startup

    exp.logFile = os.path.join(basedir,'logs','$name_$date.log')
    exp.dataFile = os.path.join(basedir,'data','$name.csv')
    exp.recordData = True
    exp.dataString_header = "# A datafile created by Gustav!\n# \n# Experiment: $name\n# \n\nS,Trial,Date,Block,Condition,@currentvars[],KWP,KWC\n"
    exp.dataString_post_trial = "$subj,$trial,$date,$block,$condition,$currentvars[],$user[kwp],$response\n"
    exp.logString_pre_block = "\n Block $block of $blocks started at $time; Condition: $condition ; $currentvarsvals[' ; ']\n"
    exp.logString_post_trial = " Trial $trial, target stimulus: $user[trial_stimbase], KWs correct: $response / possible: $user[trial_kwp] ($user[block_kwc] / $user[block_kwp]: $user[block_pc] %)\n"
    exp.logString_post_block = " Block $block of $blocks ended at $time; Condition: $condition ; $currentvarsvals[' ; ']\n"
    exp.frontend = 'qt'
    exp.debug = False
    # CUSTOM: A comma-delimited list of valid single-char responses. This experiment is designed to have 
    # the experimenter do the scoring, and enter the score on each trial.
    exp.validKeys = '0,1,2,3,4,5,6,7,8,9'.split(',')
    exp.quitKey = '/'
    exp.note = 'CI Pilot data'
    exp.comments = '''ci_fmam: CI Pilot data
    When processing involves speech in lf region, freq is the lowpass cutoff of
    the acoustic speech, and atten is a /-delimited list of attenuation values
    for broadband, 200 and 150Hz lp. For tones, freq is the downward shift of
    mean f0, and atten is a /-delimited list of attenuation values for shifts
    of 0, -25, -50, -75,-100 & -125.
    '''

    # DEPRECATED! Use tools.consecutive_files or synched_consecutive_files instead
    """STIMULUS SETS
        If you generate all your stimuli on the fly, you don't need any of these.

        The only required property is `type`, which should be either `manual`
        or `files`. If it is 'files', the function stim.get_next will be called 
        on each trial, and you can access the current token at 
        stim.current[setname]. In this case, you must also set the `path` 
        variable. If it is manual, the experimenter is responsible for
        keeping track of file order, etc., but you can call stim.get_next yourself
        as needed (you'll still need to set `path`), in which case 
        stim.current[setname] will be accessible. In all cases, the experimenter 
        is responsible for loading the stimuli. 

        If `type` is set to `files`, an additional setting is required:

        `path` is the full path to the folder containing the files

        There are several optional settings for soundfiles:

        `text` is the full path to a text file that specifies text for each token.
                There should be one line per token, and the format can be
                specified (see below).

        `txtfmt` If you're using a text file, you can specify the format here.
                  You can specify 3 values, `file`, `kw`, and `text`. The default
                  format is `file,kw,text` which in your file would look like:
                  `CUNY001,4,They LOOKED UP at the BLUE SKY.` where CUNY001 is
                  the filename [no extension], 4 is the number of keywords, and
                  the rest of the line is the text. The text should always be
                  last on the line, and the delimiter can be a comma or a space.

        `mask` is a list of filemasks (e.g., '*.wav; *.WAV'). default = '*.*'

        `load` is `manual` to simply keep track of filenames, or `auto` to load
                stimuli automatically as well. default is `auto` * DEPRECATED! *

        `order` is the presentation order: `random`, `natural`, or a print
                range style string, which should be a comma-separated list of
                values, which can be either a single number, or a colon-delimited
                range. Make the first item in the list the string `random` to
                randomize the list. default is `natural`

        `repeat` is whether to run through the list again if we run out. If this
                is True and `order` is random, a new random order will be
                generated each time. If this is false, you must ensure that there
                are enough stimulus files available. default is False
    """

    stim.sets['CUNYf'] = {
                              'type':   'files',
                              'path':   os.path.join(basedir,'stim','CUNY_F1'),
                              'text':   os.path.join(basedir,'stim','CUNY_F1.txt'),
                              'txtfmt': 'file kw text',
                              'mask':   '*.wav; *.WAV',
                              'process':'auto',  # 'auto' = Load stimulus info automatically (default)
                              'order':  '1:866', #
                              'repeat': False,    # If we run out of files, should we start over?
                              'equate': 3,  # A custom value
                            }
    stim.sets['Babble'] = {
                              'type':   'files',
                              'path':   os.path.join(basedir,'stim','noise'),
                              'mask':   '*.wav; *.WAV',
                              'process':'manual',  # 'manual' = Just get names, don't load
                              'order':  'random', #
                              'repeat': True,    #
                            }
    stim.sets['SSNoise'] = {
                              'type': 'manual',
                              }

    """EXPERIMENT VARIABLES
        There are 2 kinds of variables: factorial and ordered

        Levels added as 'factorial' variables will be factorialized with each
        other. So, if you have 2 fact variables A & B, each with 3 levels, you
        will end up with 9 conditions: A1B1, A1B2, A1B3, A2B1 etc..

        Levels added as 'covariable' variables will simply be listed (in parallel
        with the corresponding levels from the other variables) in the order
        specified. So, if you have 2 'covariable' variables A & B, each with 3
        levels, you will end up with 3 conditions: A1B1, A2B2, and A3B3. All
        'covariable' variables must have either the same number of levels, or
        exactly one level. When only one level is specified, that level will
        be used in all 'covariable' conditions. Eg., A1B1, A2B1, A3B1, etc.

        You can use both types of variables in the same experiment, but both
        factorial and covariable must contain exactly the same set of variable
        names. factorial levels are processed first, covariable levels are added
        at the end.

        Each variable (whether factorial or covariable) should have 3 properties:

        'name' is the name of the variable, as a string

        'type' is either 'manual' or 'stim'. 'manual' variables are ones that
                the experimenter will handle in the stimgen. 'stim' variables
                are ones that will load stimulus files. One usecase would be
                eg., if you preprocess your stimuli and want to read the same
                files, but from different directories depending on the
                treatment.

        'levels' should be a list of strings that identify each level of interest

    """
    # TODO: for python 2.7, change these to ordered dicts, where name is the key
    # and the dict {type, levels} is the val
    var.factorial.append( {  'name' : 'SNR',
                            'type' : 'manual',
                          'levels' : [
                                        '5',
                                        '0',
                                        '-5',
                                        '-10',
                                      ]
                        })

    var.factorial.append( {  'name' : 'target',
                            'type' : 'stim',    # This variable will be drawn from stim. 'levels' must be stim set names
                          'levels' : [
                                        'CUNYf',
                                      ]
                        })

    var.factorial.append( {  'name' : 'masker',
                            'type' : 'stim',
                          'levels' : [
                                        'Babble',
                                      ]
                        })

    var.constant = {
        'trialsperblock' : 10,
        'startblock' : 1,
        'starttrial' : 1,
        }

    """CONDITION PRESENTATION ORDER
        Use 'prompt' to prompt for condition on each block, 'random' to randomize
        condition order, 'menu' to be able to choose from a list of conditions at
        the start of a run, 'natural' to use natural order (1:end), or a
        print-range style string to specify the order ('1-10, 12, 15'). You can
        make the first item in the print range 'random' to randomize the specified
        range.
    """
    var.order = 'menu'

    """IGNORE CONDITIONS
        A list of condition numbers to ignore. These conditions will not be
        reflected in the total number of conditions to be run, etc. They will
        simply be skipped as they are encountered during a session.
    """
    var.ignore = []

    """USER VARIABLES
        Add any additional variables you need here
    """
    user.prebuff = 150
    user.postbuff = 150
    user.fs = 44100
    # Placeholders. Values will be set in pre or post trial, then used for logging / saving data.
    user.trial_kwp = 0
    user.trial_stimbase = ''
    user.block_kwp = 0.
    user.block_kwc = 0.
    user.block_pc = 0.


def pre_exp(exp,run,var,stim,user):
    exp.interface = theForm.Interface(exp, run)
    exp.interface.updateInfo_Exp(exp.name+", "+exp.note)
    expvars = "Conditions: %r\nRecord Data: %r" % (var.orderarray, exp.recordData)
    exp.interface.updateInfo_expVariables(expvars)
    exp.audiodev = m.open_device()

def pre_block(exp,run,var,stim,user):
    user.block_kwp = 0
    user.block_kwc = 0
    user.block_pc = 0.
    exp.interface.updateInfo_BlockCount("Block %g of %g" % (run.block+1, run.nblocks))
    exp.interface.updateInfo_Block("Block %g of %g | Condition # %g" % (run.block+1, run.nblocks, run.condition+1))
    exp.interface.updateInfo_blockVariables(exp.utils.get_expanded_vals_in_string("$currentvarsvals['\n']",exp,run,var,stim,user))

"""PRE_TRIAL
    This function gets called on every trial to generate the stimulus, do
    any other processing you need, and present the stimulus. All settings
    and variables are available. For the current level of a variable, use
    var.current['varname']. The stimulus waveform can be played back
    using exp.utils.wavplay.
"""
def pre_trial(exp,run,var,stim,user):
    target_name = var.current['target']
    masker_name = var.current['masker']
    p = "Trial "+ str(run.trials_exp+1) + ", " + stim.current[target_name].filebase+" KW: "+str(stim.current[target_name].info['kw']) +"\n"+stim.current[target_name].info['text']
    target, fs = m.read_file(stim.current[target_name].filename)
    masker = np.zeros((1,1))
    masker_dur = psylab.signal.ms2samp((user.prebuff + user.postbuff), fs) + len(target)
    while len(masker) < masker_dur:
        stim.get_next(exp,stim,masker_name)
        thistoken,fs = m.read_file(stim.current[masker_name].filename)
        masker = np.concatenate((masker,thistoken))
    masker = masker[0:masker_dur]
    masker_rms = psylab.signal.rms(masker)
    target_rms = psylab.signal.rms(target)
    snr = float(var.current['SNR'])
    if snr > 0:
        masker = psylab.signal.atten(masker, snr)
    else:
        target = psylab.signal.atten(target,-snr)
    stim.out = psylab.signal.mix(target,masker,offsets=[0,user.prebuff])
    
    exp.interface.updateInfo_Trial(p)
    user.trial_kwp = stim.current[target_name].info['kw']
    user.trial_stimbase = stim.current[target_name].filebase

def present_trial(exp, run, var, stim, user):
    exp.interface.showPlaying(True)
    m.play_array(stim.out,user.fs)
    exp.interface.showPlaying(False)

"""CUSTOM PROMPT
    If you want a custom response prompt, define a function for it
    here. run.response should receive the response as a string, and
    if you want to cancel the experiment, set both run.block_on and
    run.pylab_is_go to False
"""


def prompt_response(exp,run,var,stim,user):
    while True:
        ret = exp.interface.get_char()
        if ret in exp.validKeys:
            run.response = ret
            break
        elif ret in ['/','q']:
            run.block_on = False
            run.gustav_is_go = False
            break

def post_trial(exp,run,var,stim,user):
    if run.gustav_is_go:
        user.block_kwp += int(user.trial_kwp)
        user.block_kwc += int(run.response)
        user.block_pc = round(float(user.block_kwc) / float(user.block_kwp) * 100, 1)
        trial_pc = round(float(run.response) / float(user.trial_kwp) * 100, 1)
        t = 'Trial: %s / %s (%s %%)\n' % (run.response, user.trial_kwp, trial_pc)
    else:
        t = 'Trial unfinished (Exp cancelled)\n'
    blockPercent = round(user.block_kwc / user.block_kwp * 100, 1)
    exp.interface.updateInfo_TrialScore(t + 'Total: %0.0f / %0.0f (%0.1f %%)' % 
    (user.block_kwc, user.block_kwp, user.block_pc))

def post_block(exp,run,var,stim,user):
    exp.interface.updateInfo_BlockScore("Prev Condition # %g\nScore: %s / %s (%s %%)" % 
    (run.condition+1, user.block_kwc, user.block_kwp, user.block_pc))

def post_exp(exp,run,var,stim,user):
    exp.interface.dialog.isPlaying.setText("Finished")
    exp.interface.showPlaying(True)
    #exp.interface.dialog.close()

if __name__ == '__main__':
    argv = sys.argv[1:]
    argv.append("--experimentFile=%s" % os.path.realpath(__file__))
    psylab.gustav.main(argv)

