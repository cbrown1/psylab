# -*- coding: utf-8 -*-
# messagebox.py

import sys
from PyQt4 import QtGui, QtCore
import time
from datetime import datetime

class Interface():
    def __init__(self, exp, run, choices):
        self.app = QtGui.QApplication([])
        self.dialog = self.Dialog(exp, run, choices)
        self.dialog.show()
        self.dialog.setFixedSize(self.dialog.width(),self.dialog.height()) # <- Must be done after show

    class Dialog(QtGui.QDialog):

        def __init__(self, exp, run, choices, parent=None):
            QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowTitleHint)
            self.setWindowIcon(QtGui.QIcon('shs_head16.png'))
            self.setFixedWidth(400)
            self.char = ''
            self.waitingForResponse = False

            self.ctimer = QtCore.QTimer()
            QtCore.QObject.connect(self.ctimer, QtCore.SIGNAL("timeout()"), self.updateClock)
            self.ctimer.start(1000)
            vbox = QtGui.QVBoxLayout()
            #vbox.addStretch(1)

            headerBox = QtGui.QHBoxLayout()

            self.isPlaying = QtGui.QLabel('PlayBack!')
            self.isPlaying.setStyleSheet("QWidget { background-color: 'red'; border: 1px solid darkRed; margin-left: 10; margin-right: 10; margin-top: 8; margin-bottom: 8 }")
            f = self.isPlaying.font()
            f.setPointSize(14)
            self.isPlaying.setFont(f)
            headerBox.addWidget(self.isPlaying)
            headerBox.addStretch(1)

            self.isPlaying.setVisible(False)

            self.timeLabel = QtGui.QLabel()
            f = self.timeLabel.font()
            f.setPointSize(14)
            self.timeLabel.setFont(f)
            headerBox.addWidget(self.timeLabel)
            vbox.addLayout(headerBox)

            self.expLabel = QtGui.QLabel()
            f = self.expLabel.font()
            f.setPointSize(14)
            self.expLabel.setFont(f)
            self.expLabel.setStyleSheet("QWidget { background-color: 'blue'; }")
            vbox.addWidget(self.expLabel)

            self.blockLabel = QtGui.QLabel()
            f = self.blockLabel.font()
            f.setPointSize(14);
            self.blockLabel.setFont(f)
            self.blockLabel.setStyleSheet("QWidget { background-color: 'green'; }")
            vbox.addWidget(self.blockLabel)

            self.trialLabel = QtGui.QLabel()
            f = self.trialLabel.font()
            f.setPointSize(16);
            self.trialLabel.setFont(f)
            self.trialLabel.setFixedHeight(60)
            self.trialLabel.setStyleSheet("QWidget { background-color: 'darkYellow'; }")
            vbox.addWidget(self.trialLabel)

            scoreBox = QtGui.QHBoxLayout()

            self.trialScore = QtGui.QLabel()
            f = self.trialScore.font()
            f.setPointSize(14);
            self.trialScore.setFont(f)
            self.trialScore.setFixedHeight(60)
            self.trialScore.setStyleSheet("QWidget { background-color: 'cyan'; }")
            scoreBox.addWidget(self.trialScore)

            self.blockScore = QtGui.QLabel()
            f = self.blockScore.font()
            f.setPointSize(14);
            self.blockScore.setFont(f)
            self.blockScore.setFixedHeight(60)
            self.blockScore.setStyleSheet("QWidget { background-color: 'magenta'; }")
            scoreBox.addWidget(self.blockScore)

            vbox.addLayout(scoreBox)

            ConditionBox = QtGui.QHBoxLayout()

            self.blockVariables = QtGui.QLabel()
            f = self.blockVariables.font()
            f.setPointSize(14);
            self.blockVariables.setFont(f)
            self.blockVariables.setFixedHeight(120)
            self.blockVariables.setStyleSheet("QWidget { background-color: 'cyan'; }")
            ConditionBox.addWidget(self.blockVariables)

            self.expVariables = QtGui.QLabel()
            f = self.expVariables.font()
            f.setPointSize(14);
            self.expVariables.setFont(f)
            self.expVariables.setFixedHeight(120)
            self.expVariables.setStyleSheet("QWidget { background-color: 'magenta'; }")
            ConditionBox.addWidget(self.expVariables)

            vbox.addLayout(ConditionBox)

            cbox = QtGui.QHBoxLayout()

            self.blocks = QtGui.QLabel("")
            cbox.addWidget(self.blocks)

            cbox.addStretch(1)

            cancelButton = QtGui.QPushButton("Cancel")
            cancelButton.clicked.connect(self.closeEvent)
            cbox.addWidget(cancelButton)

            vbox.addLayout(cbox)
            self.setLayout(vbox)

            self.exp = exp
            self.run = run

            self.setWindowTitle("Gustav!")
            self.setModal=False

        def updateClock(self):
            now = datetime.now()
            self.timeLabel.setText('%02i:%02i:%02i' % (now.hour,now.minute,now.second))

        def closeEvent(self, event):
            # fake a quit:
            self.waitingForResponse = True
            self.keyDown(self.exp, self.run, ord(self.exp.quitKeys[0]))

        def keyPressEvent(self, event):
            self.keyDown(self.exp, self.run, event.key())

        def keyReleaseEvent(self, event):
            self.keyUp(self.exp, event.key())

        def keyDown(self, exp, run, key):
            if self.waitingForResponse:
                if key < 256:
                    thiskey = chr(key).lower()
                    if thiskey in self.exp.quitKeys:
                        # Close Gustav...
                        self.char = thiskey
                        self.waitingForResponse = False
                    elif thiskey in self.exp.validKeys_:
                        self.char = thiskey
                        self.waitingForResponse = False

        def keyUp(self, exp, key):
            if key == QtCore.Qt.Key_Control:
                ctrlDown = False
            elif key == QtCore.Qt.Key_Shift:
                shiftDown = False
            elif key == QtCore.Qt.Key_Alt:
                altDown = False


    # End Dialog

    def get_char(self):
        """Waits modally for a keypress
        """
        self.dialog.waitingForResponse = True
        sys.stdout.flush() # In case the output of a prior print statement has been buffered
        while self.dialog.waitingForResponse:
            self.app.processEvents()
            time.sleep(.1)
        curchar = self.dialog.char
        self.dialog.char = ''
        return curchar

    def showPlaying(self, playing):
        self.isPlaying.setVisible(playing)

    def button_flash(self, button, color):
        """Flashes the specified button on and off several times with the specified color
        """
        stylesheet = "QPushButton {background-color: " + color + "; " + self.dialog.default_button_stylesheet_nobg
        for i in range(3):
            self.dialog.button_dict[button].setStyleSheet(stylesheet)
            self.app.processEvents()
            time.sleep(.12)
            self.dialog.button_dict[button].setStyleSheet(self.dialog.default_button_stylesheet)
            self.app.processEvents()
            time.sleep(.06)

    def button_light(self, button, color, dur):
        """Turns the specified button on then off with the specified color
        """
        stylesheet = "QPushButton {background-color: " + color + "; " + self.dialog.default_button_stylesheet_nobg
        self.dialog.button_dict[button].setStyleSheet(stylesheet)
        self.app.processEvents()
        time.sleep(dur)
        self.dialog.button_dict[button].setStyleSheet(self.dialog.default_button_stylesheet)
        self.app.processEvents()
