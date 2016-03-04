# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 16:01:24 2014

@author: code-breaker
"""
import time
import numpy as np
from gustav_forms import qt_LateralizationFusion_Joystick as theForm

# The form uses psylab.io.hid, which requires linux!
# Make sure a joystick (or atari paddle) is plugged in.

bg_image = 'gustav_forms/Images/SmileyFaces/SmileyFace-Headphones.svg'
icon = 'stim/People/Small/Female_07.svg'

# Output of form is 0 <= r <= 1. 
# Convert to location (eg. -18<= l <= 18) with l = r*n-d 
locs = 37.
n = locs-1
d = n/2.


interface = theForm.Interface(bg_image, icon)
interface.prompt = "Where did you hear it?"
interface.set_text_block("Block 1 of 1")

interface.set_text_trial("Trial 1 of 3")
resp = interface.get_resp()
print(np.round(resp*n-d)) 

time.sleep(1)
interface.set_text_trial("Trial 2 of 3")
resp = interface.get_resp()
print(np.round(resp*n-d))

time.sleep(1)
interface.set_text_trial("Trial 3 of 3")
resp = interface.get_resp()
print(np.round(resp*n-d))

