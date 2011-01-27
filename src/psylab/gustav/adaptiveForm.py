# -*- coding: utf-8 -*-
# messagebox.py

import sys
from PyQt4 import QtGui, QtCore
import time


# Wrap these in a class, so they are accessible in messagebox:
ctrlDown = False
shiftDown = False
altDown = False

class MessageBox(QtGui.QDialog):
    def __init__(self, exp, run, keyDown, keyUp, parent=None):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowTitleHint)
        self.setWindowIcon(QtGui.QIcon('shs_head16.png'))
        
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)

        self.task = QtGui.QLabel(exp.prompt)
        f = self.task.font()
        f.setPointSize(14);
        self.task.setFont(f)
        vbox.addWidget(self.task)
        bbox = QtGui.QHBoxLayout()
        self.default_button_stylesheet = "QPushButton {background-color: white; "
        self.default_button_stylesheet_nobg = "font-size: 20px; font-weight: bold; border: 4px solid gray; border-radius: 10px;} QPushButton:pressed {background-color: lightGray;}"
        self.default_button_stylesheet += self.default_button_stylesheet_nobg
        self.button_dict = {}
        self.button_dict["1"] = QtGui.QPushButton("1")
        self.button_dict["1"].clicked.connect(self.responseButtonEvent)
        self.button_dict["1"].setObjectName("1")
        self.button_dict["1"].setFixedHeight(120)
        self.button_dict["1"].setFixedWidth(120)
        self.button_dict["1"].setStyleSheet(self.default_button_stylesheet)
        bbox.addWidget(self.button_dict["1"])

        self.button_dict["2"] = QtGui.QPushButton('2')
        self.button_dict["2"].clicked.connect(self.responseButtonEvent)
        self.button_dict["2"].setObjectName("2")
        self.button_dict["2"].setFixedHeight(120)
        self.button_dict["2"].setFixedWidth(120)
        self.button_dict["2"].setStyleSheet(self.default_button_stylesheet)
        bbox.addWidget(self.button_dict["2"])

        vbox.addLayout(bbox)

        cancelButton = QtGui.QPushButton("Cancel")
        cancelButton .clicked.connect(self.closeEvent)
        cbox = QtGui.QHBoxLayout()
        cbox.addStretch(1)
        cbox.addWidget(cancelButton)

        vbox.addLayout(cbox)

        self.setLayout(vbox)

        self.exp = exp
        self.run = run
        self.keyDown = keyDown
        self.keyUp = keyUp
        #self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle(exp.exp_name)
        self.setModal=False #(QtCore.Qt.NonModal)
        #self.setFixedSize(self.width(),self.height())

    def closeEvent(self, event):
        self.exp.waitingForResponse = False
        self.run.block_on = False
        self.run.gustav_is_go = False

    def keyPressEvent(self, event):
        self.keyDown(self, self.exp, self.run, event.key())

    def keyReleaseEvent(self, event):
        self.keyUp(self, self.exp, event.key())

    def responseButtonEvent(self):
        self.keyDown(self, self.exp, self.run, ord(str(self.sender().objectName())))


def keyDown(mb, exp, run, key):
    if exp.waitingForResponse:
        if key < 256:
            #if shiftDown:
            #    thiskey = chr(key)
            #else:
            #    thiskey = chr(key).lower()
            thiskey = chr(key).lower()
            if thiskey in exp.quitKeys:
                # Close Gustav...
                run.block_on = False
                run.gustav_is_go = False
                mb.close()
            elif thiskey in exp.validKeys_:
                print thiskey
                exp.waitingForResponse = False
                run.response = thiskey
        #elif key == QtCore.Qt.Key_Escape:
        elif key == QtCore.Qt.Key_Control:
            ctrlDown = True
        elif key == QtCore.Qt.Key_Shift:
            shiftDown = True
        elif key == QtCore.Qt.Key_Alt:
            altDown = True
        else:
            print "non-ascii character: " + str(key)

def keyUp(mb, exp, key):
    if key == QtCore.Qt.Key_Control:
        ctrlDown = False
    elif key == QtCore.Qt.Key_Shift:
        shiftDown = False
    elif key == QtCore.Qt.Key_Alt:
        altDown = False

class exp:
    '''Experimental settings
    '''
    exp_name = 'gustav'
    quitKeys = ['q', '/']
    responseTypes = ['key', 'text'] # 'key' or 'text'. If key, be sure to set'validresponses'
    methodTypes = ['constant', 'staircase']
    stimLoadTypes = ['auto', 'manual']
    stimTypes = ['soundfiles', 'manual']
    varTypes = ['stim', 'manual', 'dynamic']
    frontendTypes = ['qt', 'tk']
    prompt = 'Which Interval?'
    validKeys = '1, 2'  # list of valid responses
    waitingForResponse = False
exp.validKeys_ = [key.strip() for key in exp.validKeys.split(',')]

class run:
    '''Settings associated with the details of running the experiment
    '''
    time = ''
    date = ''
    startblock = 1
    starttrial = 1
    trialsperblock = 1
    btrial = 0     # Current trial count within a block
    trial = 0      # Current total trial count
    block = 0      # Current block (treatment) count
    blocks = 0     # Current total block count
    condition = 0  # Current condition
    block_on = True
    trial_on = True
    gustav_is_go = True
    response = ''


def get_char(exp, app):
    exp.waitingForResponse = True
    while exp.waitingForResponse:
        app.processEvents()
        time.sleep(.1)
    
def button_flash(dialog, button, color):
    stylesheet = "QPushButton {background-color: " + color + "; " + dialog.default_button_stylesheet_nobg
    for i in range(3):
        dialog.button_dict[button].setStyleSheet(stylesheet)
        app.processEvents()
        time.sleep(.12)
        dialog.button_dict[button].setStyleSheet(dialog.default_button_stylesheet)
        app.processEvents()
        time.sleep(.06)

def button_light(dialog, button, color, dur):
    stylesheet = "QPushButton {background-color: " + color + "; " + dialog.default_button_stylesheet_nobg
    dialog.button_dict[button].setStyleSheet(stylesheet)
    app.processEvents()
    time.sleep(dur)
    dialog.button_dict[button].setStyleSheet(dialog.default_button_stylesheet)
    app.processEvents()

app = QtGui.QApplication(sys.argv)
dialog = MessageBox(exp, run, keyDown, keyUp)
dialog.show()
dialog.setFixedSize(dialog.width(),dialog.height()) # <- Must be done after show
app.processEvents()

# Getting/setting the position:
#print dialog.geometry()
#dialog.setGeometry()

while run.gustav_is_go:
    get_char(exp,app)
    if run.block_on:
        button_flash(dialog, run.response, 'green')
