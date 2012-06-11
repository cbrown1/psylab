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
import time
import psylab
from gustav_forms import qt_adaptive as theForm
#from brian import hears as bh
#import brian as b
import medussa as m

def setup(exp,run,var,stim,user):

    if os.name == 'posix':
        basedir = r'/home/code-breaker/Python'
    else:
        basedir = r'C:\Users\code-breaker\Documents\Python'
        basedir = r'C:\Documents and Settings\cabrown4\My Documents\Python'
        #basedir = r'P:\Python'

    # General Experimental Variables
    exp.name = '_ILD_x_freq'
    exp.method = 'adaptive' # 'constant' for constant stimuli, or 'adaptive' for a staircase procedure (SRT, etc)
    exp.prompt = '<- = 1        |        2 = ->' # Prompt for subject
    exp.frontend = 'qt'
    exp.logFile = os.path.join(basedir,'logs','$name_$date.log')
    exp.logConsole = True
    exp.debug = False
    exp.recordData = True
    exp.dataFile = os.path.join(basedir,'data','$name_$subj.py')
    # The method class writes to the datafile, so don't overwrite the string here 
    exp.dataString_post_block = None
    exp.cacheTrials = False
    exp.validKeys = '1,2'.split(",")
    exp.quitKey = '/'
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
                              'process':'manual',  # 'auto' = Load stimulus info automatically (default)
                              'order':  'r,1:500', #
                              'repeat': True,    # If we run out of files, should we start over?
                              'equate': 3,  # A custom value
                            }

#    stim.sets['Noise'] = {
#                              'type':   'soundfiles',
#                              'path':   os.path.join(basedir,'stim','noise','gammatone_32'),
#                              'fs'  :   44100,
#                              'text':   '', #os.path.join(basedir,'stim','CUNYf','CUNY.txt'),
#                              'txtfmt': 'file kw text',
#                              'mask':   '*.wav; *.WAV',
#                              'load':   'manual',  # 'auto' = Load stimulus info automatically (default)
#                              'order':  'r,1:50', #
#                              'repeat': True,    # If we run out of files, should we start over?
#                              'equate': 3,  # A custom value
#                            }

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
    var.factorial.append( {  'name' : 'ILD_type',
                            'type' : 'manual',   
                          'levels' : [
                                        'Natural',
                                        'Flat_rms',
                                        'Flat_max',
                                      ]
                        })
    
    var.factorial.append( {  'name' : 'target',
                            'type' : 'stim',    # This variable will be drawn from stim. 'levels' must be stim set names
                          'levels' : [
                                        'CNC',
                                        #'Noise',
                                      ]
                        })

    var.dynamic = { 'name': 'ild_coeff', # Name of the dynamic variable
                    'units': 'dB',       # Units of the dynamic variable
                    'intervals': 2,      # Number of intervals
                    'steps': [.1, .1, .02, .02, .02, .02, .02, .02], # Stepsizes to use at each reversal (#revs = len)
                    #'steps': [2, 2], # Stepsizes to use at each reversal (#revs = len)
                    'downs': 2,          # Number of 'downs'
                    'ups': 1,            # Number of 'ups'
                    'val_start': .2,    # Starting value
                    #'val_start': 0,     # Starting value
                    'val_floor': 0,      # Floor
                    'val_ceil': 1,       # Ceiling
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
    #user.ild_nat = np.hstack((np.zeros(14), np.linspace(1,18,18)))
    # Starting values:
        
#    user.ild_nat = np.array([    1.57,   2.04,   1.58,   1.35,   1.16,   2.13,  -0.24,   3.01,
#                                 2.92,   1.79,   4.1 ,   4.75,   3.88,   6.49,   3.9 ,   3.86,
#                                 4.96,   6.99,  10.1 ,  15.16,  19.5 ,  21.38,  19.76,  17.58,
#                                14.41,  13.2 ,  17.87,  17.05,  16.36,  22.64,  26.18,  34.09])
#    user.cfs = np.array([   64. ,    97.5,   134.9,   176.5,   222.9,   274.6,   332.2,   396.4,   467.9,
#                           547.6,   636.5,   735.5,   845.9,   968.9,  1105.9,  1258.7,  1428.9,  1618.6,
#                          1830. ,  2065.6,  2328.2,  2620.8,  2947. ,  3310.4,  3715.4,  4166.8,  4669.8,
#                          5230.4,  5855.1,  6551.4,  7327.3,  8192. ,])
    user.ild_nat = np.array([    1.57,   1.48,  -0.47,  -2.26,   3.33,   1.99,   2.  ,   3.37,
                                 3.89,   1.94,   3.84,   4.21,   3.34,   4.62,   4.48,   2.41,
                                 2.85,   4.42,   5.33,   8.55,  12.32,  13.03,  13.27,  13.43,
                                13.19,  12.95,  11.79,  14.29,  17.78,  22.05,  23.72,  29.18])
    user.cfs = np.array([    128.  ,   166.31,   208.73,   255.7 ,   307.72,   365.32,
                             429.11,   499.74,   577.95,   664.57,   760.48,   866.68,
                             984.29,  1114.53,  1258.75,  1418.44,  1595.29,  1791.11,
                            2007.97,  2248.1 ,  2514.01,  2808.46,  3134.53,  3495.61,
                            3895.44,  4338.2 ,  4828.5 ,  5371.42,  5972.64,  6638.4 ,
                            7375.63,  8192.  ])
    user.rms = 0.03592662

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
        elif str(ret) == exp.quitKey:
            run.block_on = False
            run.gustav_is_go = False
            var.dynamic['msg'] = "Cancelled by user"
            break

"""PRE_TRIAL
    This function gets called on every trial to generate the stimulus, and
    do any other processing you need. All settings and variables are
    available. For the current level of a variable, use
    var.current['varname']. The stimulus waveform can be played back
    using exp.utils.wavplay.
"""
def pre_trial(exp,run,var,stim,user):

    targ = var.current['target']
    fb_wf,fs = m.read_file(stim.current[targ].filename)
    
    if var.current['ILD_type'] == 'Natural':
        ild_fun = user.ild_nat_useable * var.dynamic['value']
    elif var.current['ILD_type'] in [ 'Flat_rms', 'Flat_max' ]:
        ild_fun = user.ild_flat_useable * var.dynamic['value']
    fb_wf = fb_wf[:,user.useable_channels]
    #ild_fun = ild_fun[user.useable_channels]
    
    fb_wf_ild_l_1 = fb_wf
    fb_wf_ild_r_1 = psylab.signal.atten(fb_wf, ild_fun)
    fb_wf_ild_l_2 = psylab.signal.atten(fb_wf, ild_fun)
    fb_wf_ild_r_2 = fb_wf
    
    #fb_wf_ild_l_1 = psylab.signal.vocoder(fb_wf_ild_l_1.sum(axis=1), user.fs, 8, 350, 5500, noise=True, compression_ratio=1, gate=-5)
    #fb_wf_ild_r_1 = psylab.signal.vocoder(fb_wf_ild_r_1.sum(axis=1), user.fs, 8, 350, 5500, noise=True, compression_ratio=1, gate=-5)
    #fb_wf_ild_l_2 = psylab.signal.vocoder(fb_wf_ild_l_2.sum(axis=1), user.fs, 8, 350, 5500, noise=True, compression_ratio=1, gate=-5)
    #fb_wf_ild_r_2 = psylab.signal.vocoder(fb_wf_ild_r_2.sum(axis=1), user.fs, 8, 350, 5500, noise=True, compression_ratio=1, gate=-5)
    
    fb_wf_ild_l_1 = fb_wf_ild_l_1.sum(axis=1)
    fb_wf_ild_r_1 = fb_wf_ild_r_1.sum(axis=1)
    fb_wf_ild_l_2 = fb_wf_ild_l_2.sum(axis=1)
    fb_wf_ild_r_2 = fb_wf_ild_r_2.sum(axis=1)
        
    
    isi = np.zeros(psylab.signal.ms2samp(user.isi,user.fs))
    var.dynamic['correct'] = np.random.randint(1, var.dynamic['intervals']+1)
    if var.dynamic['correct'] == 1:
        channel_l = np.hstack((fb_wf_ild_l_2, isi, fb_wf_ild_l_1))
        channel_r = np.hstack((fb_wf_ild_r_2, isi, fb_wf_ild_r_1))
    else:
        channel_l = np.hstack((fb_wf_ild_l_1, isi, fb_wf_ild_l_2))
        channel_r = np.hstack((fb_wf_ild_r_1, isi, fb_wf_ild_r_2))
        
    stim.out = np.vstack((channel_r, channel_l)).T # place channels in reverse order because of transpose
    #s = exp.audiodev.open_array(stim.out,user.fs)
    #s.play()
    #exp.interface.button_light('1', 'yellow', float(fb_wf.shape[0])/user.fs)
    #time.sleep(user.isi/1000.)
    #exp.interface.button_light('2', 'yellow', float(fb_wf.shape[0])/user.fs)
    
def present_trial(exp, run, var, stim, user):
    #pass
    #s = exp.audiodev.open_array(stim.out,user.fs)
    #s.play()
    m.play_array(stim.out,user.fs)
    #exp.interface.button_light([1,2], 'yellow')
    #m.play_array(stim.out,user.fs)
    exp.interface.button_light([1,2], 'green')

def post_trial(exp, run, var, stim, user):
    exp.interface.button_light([1,2], None)
    #if run.gustav_is_go:
    #    if str(var.dynamic['correct']).lower() == run.response.lower():
    #        exp.interface.button_flash(str(var.dynamic['correct']).lower(), 'green')
    #    else:
    #        exp.interface.button_flash(str(var.dynamic['correct']).lower(), 'red')

def pre_exp(exp,run,var,stim,user):
    exp.interface = theForm.adaptive_interface(exp, run, exp.validKeys_)
    #exp.audiodev = m.open_device()

def post_exp(exp,run,var,stim,user):
    exp.interface.dialog.close()

def pre_block(exp,run,var,stim,user):
    exp.interface.dialog.blocks.setText("Block %g of %g" % (run.block+1, run.nblocks+1))
    # Only use bands available by CI users
    user.useable_channels = np.where((user.cfs>350) & (user.cfs<5500))[0]
    user.cfs_useable = user.cfs[user.useable_channels]
    # Grab those corresponding ild values
    user.ild_nat_useable = user.ild_nat[user.useable_channels]
    # Now compute a flat ILD for that number of bands equal to the overal natural ild
    if var.current['ILD_type'] == 'Flat_rms':
        user.ild_flat_useable = np.ones(user.useable_channels.shape[0]) * (user.ild_nat_useable.sum()/user.useable_channels.shape[0])
    elif var.current['ILD_type'] == 'Flat_max':
        user.ild_flat_useable = np.ones(user.useable_channels.shape[0]) * (user.ild_nat_useable.max())

if __name__ == '__main__':
    argv = sys.argv[1:]
    argv.append("--experimentFile=%s" % os.path.realpath(__file__))
    psylab.gustav.main(argv)

