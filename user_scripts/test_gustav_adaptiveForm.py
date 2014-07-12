# -*- coding: utf-8 -*-

from gustav_forms import qt_Adaptive as theForm
import time

validKeys = '1,2'.split(',')
correctKey = '1'

quitKeys = '/,q'.split(',')

interface = theForm.Interface(validKeys)

interface.app.processEvents()
ret = interface.get_resp("Which interval?")
if str(ret) in validKeys:
    resp = ret
elif str(ret) in quitKeys:
    print("Cancelled by user")
    resp = None

interface.button_light([1,2], None)
if correctKey.lower() == resp.lower():
    color = 'green'
else:
    color = 'red'
for i in range(3):
    interface.button_light([correctKey], color)
    time.sleep(.1)
    interface.button_light([correctKey], None)
    time.sleep(.05)

print(resp)

