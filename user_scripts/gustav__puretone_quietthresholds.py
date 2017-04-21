# -*- coding: utf-8 -*-

# A Gustav settings file!

import os, sys
import numpy as np
import time
import socket
import psylab
from gustav_forms import qt_Adaptive as theForm
#from brian import hears as bh
#import brian as b
import medussa as m
#import signal_io

def setup(exp):

    if os.name == 'posix':
        basedir = r'/home/cbrown'
#        stimdir = r'/home/code-breaker/SpiderOak Hive/Lab/stim'
    else:
        basedir = r'C:\Users\code-breaker\Documents\Python'
        basedir = r'C:\Documents and Settings\cabrown4\My Documents\Python'
        #basedir = r'P:\Python'

    # General Experimental Variables
    exp.name = '_quiet_thresholds_'
    exp.method = 'adaptive' # 'constant' for constant stimuli, or 'adaptive' for a staircase procedure (SRT, etc)
    exp.prompt = 'Which interval?' # Prompt for subject
    exp.frontend = 'qt'
    exp.logFile = os.path.join(basedir,'logs','$name_$date.log')
    exp.logConsole = True
    exp.debug = False
    exp.recordData = True
    exp.dataFile = os.path.join(basedir,'data','exp_$subj.py')
    exp.dataString_trial = ''
    exp.dataString_block = ''
    exp.dataString_exp = ''
    exp.dataString_header = ''
    exp.cacheTrials = False
    exp.validKeys = '1,2';  # comma-delimited list of valid responses
    exp.quitKey = '/'
    exp.note = "Quiet thresholds of pure tones"
    exp.comments = '''\
    '''

    """STIMULUS SETS
        If you generate all your stimuli on the fly, you don't need any of these.

        The only required property is 'type', which should be either 'manual'
        or 'files'. If it is manual, the experimenter is responsible for
        handling it.

        If 'type is set to 'soundfiles', each set needs two additional settings:

        'path' is the full path to the folder containing the files

        'fs' is the playback sampling frequency

        There are several optional settings for soundfiles:

        'text' is the full path to a text file that specifies text for each token.
                There should be one line per token, and the format can be
                specified (see below).

        'txtfmt' If you're using a text file, you can specify the format here.
                  You can specify 3 values, 'file', 'kw', and 'text'. The default
                  format is 'file,kw,text' which in your file would look like:
                  'CUNY001,4,They LOOKED UP at the BLUE SKY.' where CUNY001 is
                  the filename [no extension], 4 is the number of keywords, and
                  the rest of the line is the text. The text should always be
                  last on the line, and the delimiter can be a comma or a space.

        'mask' is a list of filemasks (e.g., '*.wav; *.WAV'). default = '*.*'

        'load' is 'manual' to simply keep track of filenames, or 'auto' to load
                stimuli automatically as well. default is 'auto'

        'order' is the presentation order: 'random', 'natural', or a print
                range style string, which should be a comma-separated list of
                values, which can be either a single number, or a colon-delimited
                range. Make the first item in the list the string 'random' to
                randomize the list. default is 'natural'

        'repeat' is whether to run through the list again if we run out. If this
                is True and 'order' is random, a new random order will be
                generated each time. If this is false, you must ensure that there
                are enough stimulus files available. default is False
    """

#    stim.sets['CNC'] = {
#                              'type':   'files',
#                              'path':   os.path.join(stimdir,'CNC'),
#                              'text':   '', #os.path.join(basedir,'stim','CUNYf','CUNY.txt'),
#                              'txtfmt': 'file kw text',
#                              'mask':   '*.wav; *.WAV',
#                              'process':   'auto',  # 'auto' = Load stimuli automatically (default)
#                              'order':  'r,1:500', #
#                              'repeat': True,   # If we run out of files, should we start over?
#                              'equate': 3,  # A custom value
#                              'gammatone_folder' : os.path.join(stimdir,'gammatone_32','CNC'),
#                            };

#    stim.sets['Noise'] = {
#                              'type':   'soundfiles',
#                              'path':   os.path.join(basedir,'stim','noise','gammatone_32'),
#                              'fs'  :   44100,
#                              'text':   '', #os.path.join(basedir,'stim','CUNYf','CUNY.txt'),
#                              'txtfmt': 'file kw text',
#                              'mask':   '*.wav; *.WAV',
#                              'load':   'manual',  # 'auto' = Load stimuli automatically (default)
#                              'order':  'r,1:50', #
#                              'repeat': True,    # If we run out of files, should we start over?
#                              'equate': 3,  # A custom value
#                            };

    exp.stim.cal = {'250': 112,
                    '500': 112,
                    '1000': 112,
                    '4000': 112}

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

    exp.var.factorial['frequency'] = [
                                        '500',
                                        '4000',
                                      ]

#    var.factorial.append( {  'name' : 'target',
#                            'type' : 'stim',    # This variable will be drawn from stim. 'levels' must be stim set names
#                          'levels' : [
#                                        'CNC',
#                                        #'Noise',
#                                      ]
#                        });

    def step(exp):
    	cur_step = exp.var.dynamic['cur_step']
    	n_reversals = exp.var.dynamic['n_reversals']
    	print(n_reversals)
    	print(exp.var.dynamic['steps'])
    	step = exp.var.dynamic['steps'][n_reversals]
    	exp.var.dynamic['value'] += cur_step * step
#        exp.var.dynamic['value'] += exp.var.dynamic['cur_step'] * exp.var.dynamic['steps'][exp.var.dynamic['n_reversals']]
        exp.var.dynamic['value'] = max(exp.var.dynamic['value'], exp.var.dynamic['val_floor'])
        exp.var.dynamic['value'] = min(exp.var.dynamic['value'], exp.var.dynamic['val_ceil'])


    exp.var.dynamic = { 'name': 'Level',     # Name of the dynamic variable
                    'units': 'dBSPL',    # Units of the dynamic variable
                    'alternatives': 2,   # Number of alternatives
                    'steps': [5, 5, 2, 2, 2, 2, 2, 2], # Stepsizes to use at each reversal (#revs = len)
                    #'steps': [2, 2],    # Stepsizes to use at each reversal (#revs = len)
                    'downs': 1,          # Number of 'downs'
                    'ups': 1,            # Number of 'ups'
                    'val_start': 50,     # Starting value
                    #'val_start': 0,     # Starting value
                    'val_floor': 0,      # Floor
                    'val_ceil': 70,      # Ceiling
                    'val_floor_n': 3,    # Number of consecutive floor values to quit at
                    'val_ceil_n': 3,     # Number of consecutive ceiling values to quit at
                    'run_n_trials': 0,   # Set to non-zero to run exactly that number of trials
                    'max_trials': 60,    # Maximum number of trials to run
                    'vals_to_avg': 6,    # The number of values to average
                    'step': step,        # A custom step function. Signature: def step(exp)
                    'max_level': 80,
                   }

    """CONDITION PRESENTATION ORDER
        Use 'prompt' to prompt for condition on each block, 'random' to randomize
        condition order, 'menu' to be able to choose from a list of conditions at
        the start of a run, 'natural' to use natural order (1:end), or a
        print-range style string to specify the order ('1-10, 12, 15'). You can
        make the first item in the print range 'random' to randomize the specified
        range.
    """
    exp.var.order = 'menu'

    """IGNORE CONDITIONS
        A list of condition numbers to ignore. These conditions will not be
        reflected in the total number of conditions to be run, etc. They will
        simply be skipped as they are encountered during a session.
    """
    exp.var.ignore = []

    '''USER VARIABLES
        Add any additional variables you need here
    '''
    exp.user.fs = 44100
    exp.user.isi = 250 # ms
    exp.user.interval = 500

"""CUSTOM PROMPT
    If you want a custom response prompt, define a function for it
    here. run.response should receive the response as a string, and
    if you want to cancel the experiment, set both run.block_on and
    run.pylab_is_go to False
"""
def prompt_response(exp):
    while True:
        #ret = exp.utils.getchar()
        exp.interface.app.processEvents()
        ret = exp.interface.get_resp()
        if str(ret) in exp.validKeys:
            exp.run.response = ret
            break
        elif str(ret) in exp.quitKeys:
            exp.run.block_on = False
            exp.run.gustav_is_go = False
            exp.var.dynamic['msg'] = "Cancelled by user"
            break;

"""PRE_TRIAL
    This function gets called on every trial to generate the stimulus, and
    do any other processing you need. All settings and variables are
    available. For the current level of a variable, use
    var.current['varname'].
"""
def pre_trial(exp):
    isi = np.zeros(psylab.signal.ms2samp(exp.user.isi,exp.user.fs))
    interval_noi = np.zeros(exp.user.interval/1000.*exp.user.fs)
    interval_sig = psylab.signal.tone(float(exp.var.current['frequency']),exp.user.fs,exp.user.interval)
    interval_sig = psylab.signal.ramps(interval_sig,exp.user.fs)
    #print ("Cal: {}".format(exp.stim.cal[exp.var.current['frequency']]))
    #print ("Val: {}; Atten: {}".format(exp.var.dynamic['value'], exp.stim.cal[exp.var.current['frequency']]-exp.var.dynamic['value']))
    interval_sig = psylab.signal.atten(interval_sig,exp.stim.cal[exp.var.current['frequency']]-exp.var.dynamic['value'])

    exp.var.dynamic['correct'] = np.random.randint(1, exp.var.dynamic['alternatives']+1)
    if exp.var.dynamic['correct'] == 1:
        exp.stim.out = np.hstack((interval_sig, isi, interval_noi))
    else:
        exp.stim.out = np.hstack((interval_noi, isi, interval_sig))


def present_trial(exp):
    #pass
    #m.play_array(stim.out,user.fs)
    exp.interface.button_light([1,2], None)
    time.sleep(.1)
    s = exp.audiodev.open_array(exp.stim.out,exp.user.fs)
    s.play()
    exp.interface.button_light([1], 'yellow')
    time.sleep(exp.user.interval/1000.)
    exp.interface.button_light([1], None)
    time.sleep(exp.user.isi/1000.)
    exp.interface.button_light([2], 'yellow')
    time.sleep(exp.user.interval/1000.)
    exp.interface.button_light([2], None)
    time.sleep(.1)

def post_trial(exp):
    exp.interface.button_light([1,2], None)
    if exp.run.gustav_is_go:
        if str(exp.var.dynamic['correct']).lower() == exp.run.response.lower():
            color = 'green'
        else:
            color = 'red'
        for i in range(3):
            exp.interface.button_light([exp.var.dynamic['correct']], color)
            time.sleep(.1)
            exp.interface.button_light([exp.var.dynamic['correct']], None)
            time.sleep(.05)

def pre_exp(exp):
    exp.interface = theForm.Interface(exp.validKeys.split(","))
    exp.audiodev = m.open_device()

def post_exp(exp):
    exp.interface.dialog.close()

def pre_block(exp):
    exp.interface.dialog.blocks.setText("Block %g of %g" % (exp.run.block+1, exp.var.nblocks+1))

if __name__ == '__main__':
    argv = sys.argv[1:]
    argv.append("--experimentFile=%s" % os.path.realpath(__file__))
    psylab.gustav.main(argv)
#    import inspect
#    fname = inspect.getfile( inspect.currentframe() )
#    psylab.gustav.run(settingsFile=fname)
