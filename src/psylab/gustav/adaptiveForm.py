# -*- coding: utf-8 -*-
# messagebox.py

import sys
from PyQt4 import QtGui, QtCore
import time

ctrlDown = False

class MessageBox(QtGui.QDialog):
    def __init__(self, exp, keyDown, keyUp, parent=None):
        QtGui.QDialog.__init__(self, parent)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)

        self.task = QtGui.QLabel(exp.prompt)
        vbox.addWidget(self.task)

        self.b1 = QtGui.QPushButton('1')
        self.b1.clicked.connect(self.doResponse)
        self.b1.setObjectName("1")
        self.b1.setFixedHeight(100)

        self.b2 = QtGui.QPushButton('2')
        self.b2.clicked.connect(self.doResponse)
        self.b2.setObjectName("2")
        self.b2.setFixedHeight(100)

        bbox = QtGui.QHBoxLayout()
        bbox.addWidget(self.b1)
        bbox.addWidget(self.b2)

        vbox.addLayout(bbox)

        cancelButton = QtGui.QPushButton("Cancel")
        cancelButton .clicked.connect(self.closeEvent)
        cbox = QtGui.QHBoxLayout()
        cbox.addStretch(1)
        cbox.addWidget(cancelButton)

        vbox.addLayout(cbox)

        self.setLayout(vbox)

        self.exp = exp
        self.keyDown = keyDown
        self.keyUp = keyUp
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle(exp.exp_name)
        self.setModal=False #(QtCore.Qt.NonModal)

    def closeEvent(self, event):
        self.exp.waitingForResponse = False

    def keyPressEvent(self, event):
        self.keyDown(self, self.exp, event.key())

    def keyReleaseEvent(self, event):
        self.keyUp(self, self.exp, event.key())

    def doResponse(self):
        self.keyDown(self, self.exp, ord(str(self.sender().objectName())))


def keyDown(mb, exp, key):
    if exp.waitingForResponse:
        if key < 256:
            thiskey = chr(key)
            if thiskey in exp.quitKeys:
                # Close Gustav...
                mb.close()
            elif thiskey in exp.validKeys_:
                print thiskey
                exp.waitingForResponse = False
        #elif key == 16777216: # esc key
        elif key == 16777249:
            ctrlDown = True
        else:
            print "non-ascii character: " + str(key)

def keyUp(mb, exp, key):
    if key == 16777249:
        ctrlDown = False

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


app = QtGui.QApplication(sys.argv)
dialog = MessageBox(exp, keyDown, keyUp)
dialog.show()

# Both work:
#dialog.b1.setStyleSheet("QWidget {background-color: #00FF00}")
dialog.b1.setStyleSheet("QWidget {background-color: green}")

exp.waitingForResponse = True
while exp.waitingForResponse:
    app.processEvents()
    time.sleep(.1)
