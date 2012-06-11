# -*- coding: utf-8 -*-

# Copyright (c) 2012 Christopher Brown
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
import numpy as np
import time
import psylab
from gustav_forms import qt_ClosedSet as theForm
#from brian import hears as bh
#import brian as b
import medussa as m

def setup(exp,run,var,stim,user):

    if os.name == 'posix':
        basedir = os.path.expanduser(os.path.join('~','Python'))
    else:
        basedir = os.path.expanduser(os.path.join('~','Documents','Python')) # Win7
        basedir = os.path.expanduser(os.path.join('~','My Documents','Python'))

    # General Experimental Variables
    exp.name = 'CSS_exp'
    exp.prompt = 'Select one word from each column'
    exp.method = 'constant' # 'constant' for constant stimuli, or 'adaptive' for a staircase procedure (SRT, etc)
    # TODO: move logstring and datastring vars out of exp and into either method or experiment, so they can be properly enumerated at startup
    exp.logFile = os.path.join(basedir,'logs','$name_$date.log')
    exp.dataFile = os.path.join(basedir,'data','$name.csv')
    exp.recordData = True
    """DATA & LOG STRINGS
        Data strings are written to the file specified in exp.dataFile. Log  
        strings are written to the console and to the log file specified in 
        'gustav_logfile_$date.log'. You don't need to specify any particular
        one, only the ones that make sense for the particular experiment. 
        Note also that the method classes have reasonable default strings 
        specified, but the ones in the experiment file have priority. If you 
        don't want a method string used, set that string to "". 
        
        Each type of string can be written at various points in the experiment
        by specifying any of the following:
        
        dataString_pre_exp           logString_pre_exp
        dataString_pre_block         logString_pre_block
        dataString_pre_trial         logString_pre_trial
        dataString_post_trial        logString_post_trial
        dataString_post_block        logString_post_block
        dataString_post_exp          logString_post_exp
        dataString_header (only written if dataFile does not exist)
        
        For each string, there are a number of variables that you can use, 
        that will be expanded just prior to being written. They are:
        
        Var ref:         : Will be replaced with:
        $name            : The name of the experiment
        $host            : The name of the machine that the exp is being run on
        $subj            : The subject id
        $resp            : The current response
        $trial           : The current trial number
        $trial_block     : The current trial number within the current block
        $block           : The current block number
        $condition       : The current condition number
        $conditions      : The total number of conditions
        $time            : The time the session started
        $date            : The date the session started
        $stim_kw[name]   : The current kw value for the specified stimulus set
        $stim_file[name] : The current filename for the specified stimulus set
        $stim_text[name] : The current text for the specified stimulus set
        $stim_ind[name]  : The current file ind for the specified stimulus set
        $var[varname]    : varname is the name of one of your variables
        $currentvars[';']: A delimited list of the current levels of all vars
                            The delimiter can be specified (use empty brackets
                            to specify default: ',')
        $currentvarsvals : Same as currentvars, but you will get 'var = val'
                            instead of just 'val'
        @currentvars     : Same as currentvars, but you will get var names 
                            instead of values (eg., for datafile header). 
        $user[varname]   : The value of a user variables
        
    """
    exp.dataString_header = u"# A datafile created by Gustav!\n# \n# Experiment: $name\n# \n\nS,Trial,Date,Block,Condition,@currentvars[],KWP,KWC\n"
    exp.dataString_pre_exp = ''
    exp.dataString_pre_block = ''
    exp.dataString_post_trial = u"$subj,$trial,$date,$block,$condition,$currentvars[],$user[kwp],$response\n"
    exp.logString_pre_block = "\n Block $block of $blocks started at $time; Condition: $condition ; $currentvarsvals[' ; ']\n"
    exp.logString_post_trial = " Trial $trial, response: $response\n"
    exp.logString_post_block = " Block $block of $blocks ended at $time; Condition: $condition ; $currentvarsvals[' ; ']\n"

    exp.frontend = 'qt'
    exp.debug = False
    exp.quitKey = '/'
    exp.note = 'A closed-set speech experiment'
    exp.comments = '''This is an example of a closed-set speech experiment. 
    The interface is designed for the subject to run herself. 
    '''

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
                              'order':  '1:866', #
                              'repeat': False,    # If we run out of files, should we start over?
                              'equate': 3,  # A custom value
                            }
    stim.sets['Babble'] = {
                              'type':   'files',
                              'path':   os.path.join(basedir,'stim','noise'),
                              'mask':   '*.wav; *.WAV',
                              'process': 'manual', # we may need more than 1
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
    user.choices = [['Bill', 'Joe',  'Ruth', 'Rick',  'Kate', 'Mike', 'Jack', 'Ned',  'Tom',  'Lynn'],
                    ['took', 'gave', 'lost', 'found', 'had',  'bought', 'sold', 'saw', 'got', 'brought'],
                    ['no',  'two',  'three', 'four', 'five', 'six',  'eight', 'nine', 'ten', 'twelve'],
                    ['red', 'blue', 'green', 'brown', 'gray', 'black', 'white', 'beige', 'tan', 'dark'],
                    ['clips', 'pens', 'cards', 'toys', 'wires', 'gloves', 'hats', 'socks', 'blocks', 'tops']
                   ]

def prompt_response(exp,run,var,stim,user):
    """CUSTOM PROMPT
        If you want a custom response prompt, define a function for it
        here. run.response should receive the response as a string, and
        if you want to cancel the experiment, set both run.block_on and
        run.pylab_is_go to False
    """
    exp.interface.app.processEvents()
    ret = exp.interface.get_response()
    if ret:
        run.response = ret
    else:
        run.block_on = False
        run.gustav_is_go = False

def pre_trial(exp,run,var,stim,user):
    """PRE_TRIAL
        This function gets called on every trial to generate the stimulus, and
        do any other processing you need. All settings and variables are
        available. For the current level of a variable, use
        var.current['varname']. 
    """
    target_name = var.current['target']
    masker_name = var.current['masker']
    p = "Trial "+ str(run.trials_exp+1) + ", " + stim.current[target_name].filebase + " KW: "+str(stim.current[target_name].info['kw']) +"\n"+stim.current[target_name].info['text']
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
    
def present_trial(exp, run, var, stim, user):
    exp.interface.updateInfo_task('Listen...')
    # Wait a half-second, otherwise trial start is too quick
    time.sleep(.5)
    # Create a playback stream from the generated stimulus
    s = exp.audiodev.open_array(stim.out,user.fs)
    # Play it
    s.play()
    while s.is_playing:
        time.sleep(.1)
    exp.interface.updateInfo_task(exp.prompt)

def post_trial(exp, run, var, stim, user):
    # In case the subject has clicked during playback
    exp.interface.resetForm()
    if run.gustav_is_go:
        pass

def pre_exp(exp,run,var,stim,user):
    exp.interface = theForm.Interface(exp, run, user.choices)
    exp.audiodev = m.open_device()

def post_exp(exp,run,var,stim,user):
    exp.interface.dialog.close()

def pre_block(exp,run,var,stim,user):
    exp.interface.dialog.blocks.setText("Block %g of %g" % (run.block+1, run.nblocks+1))

if __name__ == '__main__':
    argv = sys.argv[1:]
    argv.append("--experimentFile=%s" % os.path.realpath(__file__))
    psylab.gustav.main(argv)

