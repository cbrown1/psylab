# -*- coding: utf-8 -*-

# A Gustav settings file!

import os
import numpy as np
import time
import psylab
import qtForm_adaptive as theForm
#from brian import hears as bh
#import brian as b
import medussa as m

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
    exp.name = '_ILD_x_freq'
    exp.method = 'adaptive' # 'constant' for constant stimuli, or 'adaptive' for a staircase procedure (SRT, etc)
    exp.prompt = 'Which is more to the left?' # Prompt for subject
    exp.frontend = 'qt'
    exp.logFile = os.path.join(basedir,'logs','$name_$date.log')
    exp.logConsole = True
    exp.debug = False
    exp.recordData = True
    exp.dataFile = os.path.join(basedir,'data','$name_$subj.py')
    exp.dataString_trial = ''
    exp.dataString_block = ''
    exp.dataString_exp = ''
    exp.dataString_header = ''
    exp.cacheTrials = False
    exp.validKeys = '1,2';  # comma-delimited list of valid responses
    exp.note = "ILD Sensitivity; overall vs 'natural' ILDs"
    exp.comments = '''\
    user.ild_nat and flat are the amounts of attenuation in each of 32 
    filterbands, used to create the ild. The nat function is zero up to 
    about 1000 Hz, then increases in 1 dB steps thereafter. The flat 
    function is set to a 'spectrum level' the yeilds an integral that is 
    equivalent to the nat function. Thus, both functions yeild the same 
    overall ILD, the difference being that the nat function concentrates  
    all of the ILD into the high frequency region. The tracking variable 
    attenuates these values, thus reducing the ild (integrals remain equal). 
    '''

    """STIMULUS SETS
        If you generate all your stimuli on the fly, you don't need any of these.

        The only required property is 'type', which should be either 'manual'
        or 'soundfiles'. If it is manual, the experimenter is responsible for
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
    stim.sets['CNC'] = {
                              'type':   'soundfiles',
                              'path':   os.path.join(basedir,'stim','CNC','gammatone_32'),
                              'fs'  :   44100,
                              'text':   '', #os.path.join(basedir,'stim','CUNYf','CUNY.txt'),
                              'txtfmt': 'file kw text',
                              'mask':   '*.wav; *.WAV',
                              'load':   'manual',  # 'auto' = Load stimuli automatically (default)
                              'order':  '1:500', #
                              'repeat': True,    # If we run out of files, should we start over?
                              'equate': 3,  # A custom value
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
    var.factvars.append( {  'name' : 'ILD_type',
                            'type' : 'manual',   
                          'levels' : [
                                        'Natural',
                                        'Flat',
                                      ]
                        });
    
    var.factvars.append( {  'name' : 'target',
                            'type' : 'stim',    # This variable will be drawn from stim. 'levels' must be stim set names
                          'levels' : [
                                        'CNC',
                                      ]
                        });

    var.dynamic = { 'name': 'ild_coeff', # Name of the dynamic variable
                    'units': 'dB',       # Units of the dynamic variable
                    'intervals': 2,      # Number of intervals
                    #'steps': [2, 2, 1, 1, 1, 1, 1, 1], # Stepsizes to use at each reversal (#revs = len)
                    'steps': [2, 2], # Stepsizes to use at each reversal (#revs = len)
                    'downs': 2,          # Number of 'downs'
                    'ups': 1,            # Number of 'ups'
                    'val_start': -10,     # Starting value
                    'val_floor': -30,    # Floor
                    'val_ceil': 0,       # Ceiling
                    'val_floor_n': 3,    # Number of consecutive floor values to quit at
                    'val_ceil_n': 3,     # Number of consecutive ceiling values to quit at
                    'run_n_trials': 0,   # Set to non-zero to run exactly that number of trials
                    'max_trials': 60,    # Maximum number of trials to run
                    'vals_to_avg': 6,    # The number of values to average
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

    '''USER VARIABLES
        Add any additional variables you need here
    '''
    user.fs = 44100
    user.isi = 250 # ms
    user.ild_nat = np.hstack((np.zeros(14), np.linspace(1,18,18)))
    user.ild_flat = np.ones(32)*5.34375
    user.cfs = np.array([   64. ,    97.5,   134.9,   176.5,   222.9,   274.6,   332.2,   396.4,   467.9,
                           547.6,   636.5,   735.5,   845.9,   968.9,  1105.9,  1258.7,  1428.9,  1618.6,
                          1830. ,  2065.6,  2328.2,  2620.8,  2947. ,  3310.4,  3715.4,  4166.8,  4669.8,
                          5230.4,  5855.1,  6551.4,  7327.3,  8192. ,])

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
    fb_wf,fs = m.read_file(stim.current['CNC']['file'])
    if var.current['ILD_type'] == 'Natural':
        ild_fun = psylab.signal.atten(user.ild_nat, -var.dynamic['value'])
    elif var.current['ILD_type'] == 'Flat':
        ild_fun = psylab.signal.atten(user.ild_flat, -var.dynamic['value'])
    fb_wf = fb_wf[:,7:26]
    ild_fun = ild_fun[7:26]
    
    fb_wf_ild_l_1 = fb_wf
    fb_wf_ild_r_1 = psylab.signal.atten(fb_wf, ild_fun)
    fb_wf_ild_l_2 = psylab.signal.atten(fb_wf, ild_fun)
    fb_wf_ild_r_2 = fb_wf
    
    fb_wf_ild_l_1 = psylab.signal.vocoder(fb_wf_ild_l_1.sum(axis=1), user.fs, 8, 350, 5500, noise=True, compression_ratio=1, gate=-5)
    fb_wf_ild_r_1 = psylab.signal.vocoder(fb_wf_ild_r_1.sum(axis=1), user.fs, 8, 350, 5500, noise=True, compression_ratio=1, gate=-5)
    fb_wf_ild_l_2 = psylab.signal.vocoder(fb_wf_ild_l_2.sum(axis=1), user.fs, 8, 350, 5500, noise=True, compression_ratio=1, gate=-5)
    fb_wf_ild_r_2 = psylab.signal.vocoder(fb_wf_ild_r_2.sum(axis=1), user.fs, 8, 350, 5500, noise=True, compression_ratio=1, gate=-5)
    
    isi = np.zeros(psylab.signal.ms2samp(user.isi,user.fs))
    var.dynamic['correct'] = np.random.randint(1, var.dynamic['intervals']+1)
    if var.dynamic['correct'] == 1:
        channel_l = np.hstack((fb_wf_ild_l_1, isi, fb_wf_ild_l_2))
        channel_r = np.hstack((fb_wf_ild_r_1, isi, fb_wf_ild_r_2))
    else:
        channel_l = np.hstack((fb_wf_ild_l_2, isi, fb_wf_ild_l_1))
        channel_r = np.hstack((fb_wf_ild_r_2, isi, fb_wf_ild_r_1))
        
    stim.out = np.vstack((channel_r, channel_l)).T # place channels in reverse order because of transpose
    
    s = exp.audiodev.open_array(stim.out,user.fs)
    s.play()
    exp.interface.button_light('1', 'yellow', float(fb_wf.shape[0])/user.fs)
    time.sleep(user.isi/1000.)
    exp.interface.button_light('2', 'yellow', float(fb_wf.shape[0])/user.fs)
    
def present_trial(exp, run, var, stim, user):
    # TODO: settings.present_trial not being picked up by gustav
    print "\n\n\n     PRESENT!!!\n\n\n"
    s = exp.audiodev.open_array(stim.out,user.fs)
    s.play()
    exp.interface.button_light(0, 'yellow', len(stim.out)/user.fs)
    time.sleep(user.isi/1000.)
    exp.interface.button_light(1, 'yellow', len(stim.out)/user.fs)

def post_trial(exp, run, var, stim, user):
    if run.gustav_is_go:
        if str(var.dynamic['correct']).lower() == run.response.lower():
            exp.interface.button_flash(str(var.dynamic['correct']).lower(), 'green')
        else:
            exp.interface.button_flash(str(var.dynamic['correct']).lower(), 'red')

def pre_exp(exp,run,var,stim,user):
    exp.interface = theForm.adaptive_interface(exp, run, exp.validKeys_)
    exp.audiodev = m.open_device()

def post_exp(exp,run,var,stim,user):
    exp.interface.dialog.close()

def pre_block(exp,run,var,stim,user):
    exp.interface.dialog.blocks.setText("Block %g of %g" % (run.block+1, var.nblocks))
    

def present_trial(exp,run,var,stim,user):
    pass

if __name__ == '__main__':
    import inspect
    fname = inspect.getfile( inspect.currentframe() )
    psylab.gustav.run(settingsFile=fname)
