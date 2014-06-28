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
# language that is free, open-source, easy to learn, and cross-platform, 
# thus making it extremely well-suited to scientific applications. 
# There are countless other freely-available Python modules written by    
# scientists in many different fields, making Python a good choice   
# regardless of your particular field. Consider using Python as your 
# scientific platform.
# 

# A Gustav experiment file!

import os, sys
import inspect
import numpy as np
import psylab

def setup(exp,run,var,stim,user):

    if os.name == 'posix':
        basedir = r'/home/code-breaker/Python'
    else:
        basedir = r'C:\Documents and Settings\cabrown4\My Documents\Python'

    # General Experimental Variables
    exp.name = '_Constant_nogui'
    exp.method = 'constant' # 'constant' for constant stimuli, or 'adaptive' for a staircase procedure (SRT, etc)
    exp.recordData = True
    exp.dataFile = os.path.join(basedir,'data','$name.csv')
    exp.dataString_header = "# A datafile created by Gustav!\n# \n# Experiment: $name\n# \n\nS,Trial,Date,Block,Condition,@currentvars[],KWP,KWC\n"
    exp.dataString_post_trial = "$subj,$trial,$date,$block,$condition,$currentvars[],$user[kwp],$response\n"
    exp.logFile = os.path.join(basedir,'logs','$name_$date.log')
    exp.logString_pre_block = "\n Block $block of $blocks started at $time; Condition: $condition ; $currentvarsvals[' ; ']\n"
    exp.logString_pre_trial = ''; # trial info is written in the pre_trial function
    exp.logString_post_trial = ''; 
    exp.logString_post_block = " Block $block ; Condition: $condition ; $currentvarsvals[' ; ']\n";
    exp.frontend = 'term'
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
        prior to each trial, and you can access the current token at 
        stim.current[setname]. In this case, you must also set the `path` 
        variable. If type is manual, nothing will occur automatically. `manual`
        stim sets are useful if you have a level of an experimental variable 
        that is stimulus-based, and another level of that variable that is 
        not. For example, you might want a masker variable to be both a talker
        (files on disk, type='files') and speech-shaped noise which you generate
        digitally as needed (type='manual').  
        
        If `type` is set to `files`, an additional setting is required:

        `path` is the full path to the folder containing the files

        There are several optional settings when `type` is `files`:

        `text` is the full path to a text file containing info on each token.
                There should be one line per token, and the format can be
                specified (see below).

        `txtfmt` If you're using a text file, specify the format here.
                The comma-delimited values you list here will be used as keys
                to the info dictionary in stim.current to allow you to retrieve
                the info. For example, if you set txtfmt to be `file,kw,text`,
                and your file looks like `CUNY001,4,They LOOKED UP at the BLUE SKY.`, 
                then you can use stim.current[stimname].info['kw'] to get the value 
                4, and stim.current[stimname].info['text'] will be `They LOOKED...`.
                One txtfmt value needs to be 'file', and the corresponding text in
                the textfile should be the filename (without the extension), as that
                is how the info is connected to a token.

        `mask` is a list of filemasks (e.g., '*.wav; *.WAV'). default = '*.*'

        `process` is either `manual` or `auto`. default = `auto`. When its `auto`,
                the function stim.get_next will be called once before the start of 
                every trial, which simply loads information for the next stimulus
                token in the list into stim.current[stimname] (useful if you need 
                exactly 1 stim token per trial). If `manual`, stim.get_next will 
                not be called, and you will have to call it yourself as needed
                (useful if you need something other than exactly 1 stim token per
                trial). 

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
                              'process': 'auto',
                              'order':  '1:10', #
                              'repeat': True,    # If we run out of files, should we start over?
                              'equate': 3,  # A custom value
                            }
    stim.sets['Babble'] = {
                              'type':   'files',
                              'path':   os.path.join(basedir,'stim','noise'),
                              'mask':   '*.wav; *.WAV',
                              'process': 'auto',
                              'order':  'random', #
                              'repeat': True,    #
                            }
    stim.sets['SSNoise'] = {
                              'type': 'manual',
                              }

    """EXPERIMENT VARIABLES
        There are 2 kinds of variables: factorial and covariable

        Levels added as 'factorial' variables will be factorialized with each
        other. So, if you have 2 fact variables A & B, each with 3 levels, you
        will end up with 9 conditions: A1B1, A1B2, A1B3, A2B1 etc..

        Levels added as 'covariable' variables will simply be listed, in 
        parallel with the corresponding levels from the other variables, in the 
        order specified. So, if you have 2 'covariable' variables A & B, each 
        with 3 levels, you will end up with 3 conditions: A1B1, A2B2, and A3B3. 
        All 'covariable' variables must have either the same number of levels, 
        or exactly one level. When only one level is specified, that level will
        be used in all 'covariable' conditions. Eg., A1B1, A2B1, A3B1, etc.

        You can use both types of variables in the same experiment, but both
        factorial and covariable must contain exactly the same set of variable
        names. factorial levels are processed first, covariable levels are 
        added at the end (and then the entire list gets randomized, etc).

        Each variable (whether factorial or covariable) should have 3 
        properties:
        
        'name' is the name of the variable, as a string. Should be unique for 
                the experiment.

        'type' is either 'manual' or 'stim'. 'manual' variables are ones that
                the experimenter will handle in the stimgen. 'stim' variables
                are ones that will load stimulus files. One usecase would be
                eg., if you preprocess your stimuli and want to read the same
                files, but from different directories depending on the
                treatment.

        'levels' should be a list of strings that identify each level of 
                interest

    """
    # TODO: for python 2.7, change these to ordered dicts, where name is the key
    # and the dict {type, levels} is the val
    var.factorial.append( {  'name' : 'freq',
                            'type' : 'manual',
                          'levels' : [
                                        '0',
                                        '-25',
                                        '-50',
                                        '-75',
                                        '-100',
                                        '-125',
                                      ]
                        })

    var.factorial.append( {  'name' : 'processing',
                            'type' : 'manual',
                          'levels' : [
                                        'E',
                                        'E/A',
                                        'E/Tfmam',
                                      ]
                        })

    var.factorial.append( {  'name' : 'excursion',
                            'type' : 'manual',     # This variable will be processed manually in stimgen (default behavior)
                          'levels' : [
                                        '1',
                                        '.5',
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

    var.factorial.append( {  'name' : 'snr',
                            'type' : 'manual',
                          'levels' : [
                                        '3',
                                      ]
                        })

    var.covariable.append( {  'name' : 'freq',
                            'type' : 'manual',
                          'levels' : [
                                        '300',
                                      ]
                        })

    var.covariable.append( {  'name' : 'processing',
                            'type' : 'manual',
                          'levels' : [
                                        'E',
                                      ]
                        })

    var.covariable.append( {  'name' : 'excursion',
                            'type' : 'manual',
                          'levels' : [
                                        '1',
                                        '3',
                                        '5',
                                        '7',
                                      ]
                        })

    var.covariable.append( {  'name' : 'target',
                            'type' : 'stim',
                          'levels' : [
                                        'CUNYf',
                                      ]
                        })

    var.covariable.append( {  'name' : 'masker',
                            'type' : 'stim',
                          'levels' : [
                                        'Babble',
                                      ]
                        })

    var.covariable.append( {  'name' : 'snr',
                            'type' : 'manual',
                          'levels' : [
                                        '3',
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

    """PROMPT FOR VARIABLE
        Add the name of a variable to this and you will be prompted for the 
        level to run prior to each block during testing. The default value 
        is the value of that variable in that condition at runtime.
    """
    var.prompt = ['snr']

    """USER VARIABLES
        Add any additional variables you need here
    """
    user.prebuff = 150
    user.postbuff = 150
    user.kwp = '0'


"""CUSTOM PROMPT
    If you want a custom response prompt, define a function for it
    here. run.response should receive the response as a string, and
    if you want to cancel the experiment, set both run.block_on and
    run.pylab_is_go to False
"""
def prompt_response(exp,run,var,stim,user):
    #while True:
    target_name = var.current['target']
    # The prompt is the trial feedback.
    user.kwp = str(stim.current[var.current['target']].info['kw']) # TODO: stim isn't getting set before pre-trial? 
    p = "  Trial "+ str(run.trials_exp+1) + ", " + stim.current[target_name].filebase+" KW: "+str(stim.current[target_name].info['kw']) +" "+stim.current[target_name].info['text']
    exp.utils.log(exp,run,var,stim,user,p)
    while True:
        ret = exp.frontend.get_char()
        if ret in exp.validKeys:
            run.response = ret
            break
        elif ret == exp.quitKey:
            run.block_on = False
            run.gustav_is_go = False
            break

"""PRE_TRIAL
    This function gets called on every trial to generate the stimulus, do
    any other processing you need, and present the stimulus. All settings
    and variables are available. For the current level of a variable, use
    var.current['varname']. The stimulus waveform can be played back
    using exp.utils.wavplay.
"""
def pre_trial(exp,run,var,stim,user):
    stim.stimarray = np.zeros((1))

def post_trial(exp,run,var,stim,user):
    exp.utils.log(exp,run,var,stim,user, " | Correct: %s\n" % run.response)

if __name__ == '__main__':
    argv = sys.argv[1:]
    argv.append("--experimentFile=%s" % os.path.realpath(__file__))
    psylab.gustav.main(argv)

