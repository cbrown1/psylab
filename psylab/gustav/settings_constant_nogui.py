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

# A Gustav settings file!

import os
import inspect
import numpy as np
import psylab
import qtForm_speech as theForm

def setup(exp,run,var,stim,user):

    # Crash Recovery
    run.startblock = 1;
    run.starttrial = 1;

    if os.name == 'posix':
        basedir = r'/home/code-breaker/Python'
    else:
        basedir = r'C:\Documents and Settings\cabrown4\My Documents\Python'

    # General Experimental Variables
    exp.name = '_SomeExperiment'
    exp.method = 'constant' # 'constant' for constant stimuli, or 'adaptive' for a staircase procedure (SRT, etc)
    exp.consoleString_Trial = ''; #Write this string to the console after every trial
    exp.consoleString_Block = "Block $block ; Condition: $condition ; $currentvarsvals[' ; ']\n"; #Write this string to the console before every block
    exp.frontend = 'term'
    exp.logFile = os.path.join(basedir,'logs','$name_$date.log')
    exp.debug = True
    exp.recordData = True
    exp.dataFile = os.path.join(basedir,'data','$name.csv')
    exp.cacheTrials = False
    exp.validKeys = '0,1,2,3,4,5,6,7,8,9';  # comma-delimited list of valid responses
    exp.note = 'CI Pilot data'
    exp.comments = '''ci_fmam: CI Pilot data
    When processing involves speech in lf region, freq is the lowpass cutoff of
    the acoustic speech, and atten is a /-delimited list of attenuation values
    for broadband, 200 and 150Hz lp. For tones, freq is the downward shift of
    mean f0, and atten is a /-delimited list of attenuation values for shifts
    of 0, -25, -50, -75,-100 & -125.
    '''

    """STIMULUS SETS
        If you generate all your stimuli on the fly, you don't need any of these.

        The only required property is `type`, which should be either `manual`
        or `soundfiles`. If it is manual, the experimenter is responsible for
        handling it.

        If `type` is set to `soundfiles`, each set needs two additional settings:

        `path` is the full path to the folder containing the files

        `fs` is the playback sampling frequency

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
                stimuli automatically as well. default is `auto`

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
                              'type':   'soundfiles',
                              'path':   os.path.join(basedir,'stim','CUNYf'),
                              'fs'  :   44100,
                              'text':   os.path.join(basedir,'stim','CUNYf','CUNY.txt'),
                              'txtfmt': 'file kw text',
                              'mask':   '*.wav; *.WAV',
                              'load':   'auto',  # 'auto' = Load stimuli automatically (default)
                              'order':  '1:10', #
                              'repeat': True,    # If we run out of files, should we start over?
                              'equate': 3,  # A custom value
                            };
    stim.sets['Babble'] = {
                              'type':   'soundfiles',
                              'path':   os.path.join(basedir,'stim','babble'),
                              'fs'  :   44100,
                              'mask':   '*.wav; *.WAV',
                              'load':   'manual',  # 'manual' = Just get names, don't load
                              'order':  'random', #
                              'repeat': True,    #
                            };
    stim.sets['SSNoise'] = {
                              'type': 'manual',
                              };

    """EXPERIMENT VARIABLES
        There are 2 kinds of variables: factorial and ordered

        Levels added as 'factvars' variables will be factorialized with each
        other. So, if you have 2 fact variables A & B, each with 3 levels, you
        will end up with 9 conditions: A1B1, A1B2, A1B3, A2B1 etc..

        Levels added as 'listvars' variables will simply be listed (in parallel
        with the corresponding levels from the other variables) in the order
        specified. So, if you have 2 'listvars' variables A & B, each with 3
        levels, you will end up with 3 conditions: A1B1, A2B2, and A3B3. All
        'listvars' variables must have either the same number of levels, or
        exactly one level. When only one level is specified, that level will
        be used in all 'listvars' conditions. Eg., A1B1, A2B1, A3B1, etc.

        You can use both types of variables in the same experiment, but both
        factvars and listvars must contain exactly the same set of variable
        names. Factvars levels are processed first, listvars levels are added at
        the end.

        Each variable (whether factvars or listvars) should have 3 properties:

        'name' is the name of the variable, as a string

        'type' is either 'manual' or 'stim'. 'manual' variables are ones that
                the experimenter will handle in the stimgen. 'stim' variables
                are ones that will load stimulus files. One usecase would be
                eg., if you preprocess your stimuli and want to read the same
                files, but from different directories depending on the
                treatment.

        'levels' should be a list of strings that identify each level of interest

        for file in stim['masker_files']:
            masker,fs,enc = utils.wavread(file)
            stim['masker'] += masker
        stim['masker'] = stim['masker'][0:stim['masker_samples_needed']]
    """
    # TODO: for python 2.7, change these to ordered dicts, where name is the key
    # and the dict {type, levels} is the val
    var.factvars.append( {  'name' : 'freq',
                            'type' : 'manual',
                          'levels' : [
                                        '0',
                                        '-25',
                                        '-50',
                                        '-75',
                                        '-100',
                                        '-125',
                                      ]
                        });

    var.factvars.append( {  'name' : 'processing',
                            'type' : 'manual',
                          'levels' : [
                                        'E',
                                        'E/A',
                                        'E/Tfmam',
                                      ]
                        });

    var.factvars.append( {  'name' : 'excursion',
                            'type' : 'manual',     # This variable will be processed manually in stimgen (default behavior)
                          'levels' : [
                                        '1',
                                        '.5',
                                      ]
                        });

    var.factvars.append( {  'name' : 'target',
                            'type' : 'stim',    # This variable will be drawn from stim. 'levels' must be stim set names
                          'levels' : [
                                        'CUNYf',
                                      ]
                        });

    var.factvars.append( {  'name' : 'masker',
                            'type' : 'stim',
                          'levels' : [
                                        'Babble',
                                      ]
                        });

    var.factvars.append( {  'name' : 'snr',
                            'type' : 'manual',
                          'levels' : [
                                        '3',
                                      ]
                        });

    var.listvars.append( {  'name' : 'freq',
                            'type' : 'manual',
                          'levels' : [
                                        '300',
                                      ]
                        });

    var.listvars.append( {  'name' : 'processing',
                            'type' : 'manual',
                          'levels' : [
                                        'E',
                                      ]
                        });

    var.listvars.append( {  'name' : 'excursion',
                            'type' : 'manual',
                          'levels' : [
                                        '1',
                                        '3',
                                        '5',
                                        '7',
                                      ]
                        });

    var.listvars.append( {  'name' : 'target',
                            'type' : 'stim',
                          'levels' : [
                                        'CUNYf',
                                      ]
                        });

    var.listvars.append( {  'name' : 'masker',
                            'type' : 'stim',
                          'levels' : [
                                        'Babble',
                                      ]
                        });

    var.listvars.append( {  'name' : 'snr',
                            'type' : 'manual',
                          'levels' : [
                                        '3',
                                      ]
                        });

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
    var.order = 'menu';

    """IGNORE CONDITIONS
        A list of condition numbers to ignore. These conditions will not be
        reflected in the total number of conditions to be run, etc. They will
        simply be skipped as they are encountered during a session.
    """
    var.ignore = []

    """USER VARIABLES
        Add any additional variables you need here
    """
    user.prebuff = 150;
    user.postbuff = 150;


"""CUSTOM PROMPT
    If you want a custom response prompt, define a function for it
    here. run.response should receive the response as a string, and
    if you want to cancel the experiment, set both run.block_on and
    run.pylab_is_go to False
"""
def prompt_response(exp,run,var,stim,user):
    while True:
        # The prompt is the trial feedback.
        p = "  Trial "+ str(run.trials_exp+1) + ", " + stim.current['CUNYf']['filebase'] +" - "+stim.current['CUNYf']['txt']+" KW: "+str(stim.current['CUNYf']['kw'])+", Resp: "
        ret = exp.term.get_input(None, "Gustav!",p)

        #TODO: Switch to get_char
        #ret = exp.gui.get_input(None, "Gustav!","How many keywords? ")
        if ret in exp.validKeys_:
            run.response = ret
            #exp.utils.log(exp,run,var,stim,user, p+ret+'\n', exp.logFile, False) # Since there's no other feedback, log trial info manually
            break
        elif ret in exp.quitKeys:
            run.block_on = False
            run.gustav_is_go = False
            break;

"""PRE_TRIAL
    This function gets called on every trial to generate the stimulus, do
    any other processing you need, and present the stimulus. All settings
    and variables are available. For the current level of a variable, use
    var.current['varname']. The stimulus waveform can be played back
    using exp.utils.wavplay.
"""
def pre_trial(exp,run,var,stim,user):
    stim.stimarray = np.zeros((1))


if __name__ == '__main__':
    import inspect
    fname = inspect.getfile( inspect.currentframe() )
    psylab.gustav.run(settingsFile=fname)
