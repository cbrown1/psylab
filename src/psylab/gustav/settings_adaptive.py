# -*- coding: utf-8 -*-

# A Gustav settings file!

import os
import inspect
import numpy as np
import psylab
import qtForm_adaptive as theForm
#import qtForm_speech as theForm

def setup(exp,run,var,stim,user):

    # Crash Recovery
    run.startblock = 1
    run.starttrial = 1

    if os.name == 'posix':
        basedir = r'/home/code-breaker/Python'
    else:
        basedir = r'C:\Users\code-breaker\Documents\Python'
        basedir = r'C:\Documents and Settings\cabrown4\My Documents\Python'

    # General Experimental Variables
    exp.name = '_QuietThresholds'
    exp.method = 'adaptive' # 'constant' for constant stimuli, or 'adaptive' for a staircase procedure (SRT, etc)
    exp.prompt = 'Which interval?' # Prompt for subject
    exp.frontend = 'qt'
    exp.logFile = os.path.join(basedir,'logs','$name_$date.log')
    exp.logConsole = True
    exp.debug = True
    exp.recordData = True
    exp.dataFile = os.path.join(basedir,'data','$name.py')
    exp.dataString_trial = ''
    exp.dataString_block = "user = { '$currentvarsvals[' : "
    exp.dataString_exp = ''
    exp.dataString_header = ''
    exp.cacheTrials = False
    exp.validKeys = '1,2';  # comma-delimited list of valid responses
    exp.note = 'A demonstration of the adaptive method'
    exp.comments = """Quiet Thresholds
    Derives quiet thresholds for pure tones.
    """

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


    """EXPERIMENT VARIABLES
        There are 2 kinds of variables: factorial and ordered

        Levels added as `factvars` variables will be factorialized with each
        other. So, if you have 2 fact variables A & B, each with 3 levels, you
        will end up with 9 conditions: A1B1, A1B2, A1B3, A2B1 etc..

        Levels added as `listvars` variables will simply be listed (in parallel
        with the corresponding levels from the other variables) in the order
        specified. So, if you have 2 `listvars` variables A & B, each with 3
        levels, you will end up with 3 conditions: A1B1, A2B2, and A3B3. All
        `listvars` variables must have either the same number of levels, or
        exactly one level. When only one level is specified, that level will
        be used in all `listvars` conditions. Eg., A1B1, A2B1, A3B1, etc.

        You can use both types of variables in the same experiment, but both
        factvars and listvars must contain exactly the same set of variable
        names. Factvars levels are processed first, listvars levels are added at
        the end.

        Each variable (whether factvars or listvars) should have 3 properties:

        `name` is the name of the variable, as a string

        `type` is either `manual` or `stim`. `manual` variables are ones that
                the experimenter will handle in the stimgen. `stim` variables
                are ones that will load stimulus files. One usecase would be
                eg., if you preprocess your stimuli and want to read the same
                files, but from different directories depending on the
                treatment.

        `levels` should be a list of strings that identify each level of interest

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
                                        '125',
                                        '250',
                                        '500',
                                        '1000',
                                        '2000',
                                        '4000',
                                      ]
                        });

    var.dynamic = { 'name': 'level',     # Name of the dynamic variable
                    'units': 'dB',       # Units of the dynamic variable
                    'intervals': 2,      # Number of intervals
                    'steps': [5, 5, 2, 2, 2, 2, 2, 2], # Stepsizes to use at each reversal (#revs = len)
                    'downs': 2,          # Number of 'downs'
                    'ups': 1,            # Number of 'ups'
                    'val_start': 70,     # Starting value
                    'val_floor': 0,      # Floor
                    'val_ceil': 80,      # Ceiling
                    'val_floor_n': 3,    # Number of consecutive floor values to quit at
                    'val_ceil_n': 3,     # Number of consecutive ceiling values to quit at
                    'run_n_trials': 0,   # Set to non-zero to run exactly that number of trials
                    'max_trials': 60,    # Maximum number of trials to run
                    'vals_to_avg': 6,    # The number of values to average
                   }

    """CONDITION PRESENTATION ORDER
        Use `prompt` to prompt for condition on each block, `random` to randomize
        condition order, `menu` to be able to choose from a list of conditions at
        the start of a run, `natural` to use natural order (1:end), or a
        print-range style string to specify the order ('1-10, 12, 15'). You can
        make the first item in the print range `random` to randomize the specified
        range.
    """
    var.order = 'natural'

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
    user.dur = 500 # ms
    user.isi = 250 # ms


"""CUSTOM PROMPT
    If you want a custom response prompt, define a function for it
    here. run.response should receive the response as a string, and
    if you want to cancel the experiment, set both run.block_on and
    run.pylab_is_go to False
"""
def prompt_response(exp,run,var,stim,user):
    while True:
        #ret = exp.utils.getchar()
        exp.interface.app.processEvents()
        ret = exp.interface.get_char()
        if str(ret) in exp.validKeys_:
            run.response = ret
            break
        elif str(ret) in exp.quitKeys:
            run.block_on = False
            run.gustav_is_go = False
            var.dynamic['msg'] = "Cancelled by user"
            break;

"""PRE_TRIAL
    This function gets called on every trial to generate the stimulus, and
    do any other processing you need. All settings and variables are
    available. For the current level of a variable, use
    var.current['varname']. The stimulus waveform can be played back
    using exp.utils.wavplay.
"""
def pre_trial(exp,run,var,stim,user):
    var.dynamic['correct'] = np.random.random_integers(1,var.dynamic['intervals'])
    tone = psylab.signal.tone(int(var.current['freq']), user.fs, user.dur)
    tone = psylab.signal.ramps(tone, user.fs)
    tone = psylab.signal.atten(tone, 90-int(var.dynamic['value']))
    quiet = np.zeros(tone.size)
    isi = np.zeros(user.isi/1000*user.fs)
    if var.dynamic['correct'] == 1:
        stim.stimarray = tone #np.vstack((tone, isi, quiet))
    else:
        stim.stimarray = tone #np.vstack((quiet, isi, tone))

def post_trial(exp, run, var, stim, user):
    if run.gustav_is_go:
        if str(var.dynamic['correct']).lower() == run.response.lower():
            exp.interface.button_flash(str(var.dynamic['correct']).lower(), 'green')
        else:
            exp.interface.button_flash(str(var.dynamic['correct']).lower(), 'red')

def pre_exp(exp,run,var,stim,user):
    exp.interface = theForm.Interface(exp, run, exp.validKeys_)

def post_exp(exp,run,var,stim,user):
    exp.interface.dialog.close()

def pre_block(exp,run,var,stim,user):
    exp.interface.dialog.blocks.setText("Block %g of %g" % (run.block+1, run.nblocks))

def present_trial(exp,run,var,stim,user):
    pass

if __name__ == '__main__':
    fname = inspect.getfile( inspect.currentframe() )
    psylab.gustav.run(settingsFile=fname)
