# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 16:01:24 2014

@author: code-breaker
"""

from gustav_forms import qt_Lateralization as theForm

feedback = 'gustav_forms/Images/Animals'
bg_image = 'gustav_forms/Images/SmileyFaces/smileyface_headphones.jpg'

interface = theForm.Interface(bg_image, feedback)
interface.prompt = "Where did you hear it?"
interface.set_text_block("Block 1 of 10")
interface.set_text_trial("Trial 3 of 10")
resp = interface.get_resp()
print(resp)

