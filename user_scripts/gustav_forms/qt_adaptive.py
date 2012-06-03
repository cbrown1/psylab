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

import sys
from PyQt4 import QtGui, QtCore
import time

class Interface():
    def __init__(self, exp, run, choices):
        self.app = QtGui.QApplication([])
        self.dialog = self.Dialog(exp, run, choices)
        self.dialog.show()
        self.dialog.setFixedSize(self.dialog.width(),self.dialog.height()) # <- Must be done after show
        self.app.processEvents()

    class Dialog(QtGui.QDialog):

        def __init__(self, exp, run, choices, parent=None):
            QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowTitleHint)
            self.setWindowIcon(QtGui.QIcon('shs_head16.png'))
            self.char = ''
            self.waitingForResponse = False

            vbox = QtGui.QVBoxLayout()
            vbox.addStretch(1)

            self.task = QtGui.QLabel(exp.prompt)
            f = self.task.font()
            f.setPointSize(14)
            self.task.setAlignment(QtCore.Qt.AlignHCenter)
            self.task.setFont(f)
            vbox.addWidget(self.task)
            self.default_button_stylesheet = "QPushButton {background-color: white; "
            self.default_button_stylesheet_nobg = "font-size: 20px; font-weight: bold; border: 4px solid gray; border-radius: 10px;} QPushButton:pressed {background-color: lightGray;}"
            self.default_button_stylesheet += self.default_button_stylesheet_nobg

            self.bbox = QtGui.QHBoxLayout()
            self.button_dict = {}
            for choice in choices:
                self.button_dict[choice] = QtGui.QPushButton(choice)
                self.button_dict[choice].clicked.connect(self.responseButtonEvent)
                self.button_dict[choice].setObjectName(choice)
                self.button_dict[choice].setFixedHeight(120)
                self.button_dict[choice].setFixedWidth(120)
                self.button_dict[choice].setStyleSheet(self.default_button_stylesheet)
                self.bbox.addWidget(self.button_dict[choice])

            vbox.addLayout(self.bbox)

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
            self.setFocus()

        def closeEvent(self, event):
            # fake a quit:
            self.waitingForResponse = True
            self.keyDown(self.exp, self.run, ord(self.exp.quitKeys[0]))

        def keyPressEvent(self, event):
            self.keyDown(self.exp, self.run, event.key())

        def keyReleaseEvent(self, event):
            self.keyUp(self.exp, event.key())

        def responseButtonEvent(self):
            self.keyDown(self.exp, self.run, ord(str(self.sender().objectName())))

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


    # End AdaptiveDialog

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

    def button_light(self, button, color):
        """Turns the specified button(s) on or off with the specified color (use None for off)
        """
        self.app.processEvents()
        if color is None:
            stylesheet = self.dialog.default_button_stylesheet
        else:
            stylesheet = "QPushButton {background-color: " + color + "; " + self.dialog.default_button_stylesheet_nobg
        button = list(button)

        for b in button:
            self.dialog.button_dict[str(b)].setStyleSheet(stylesheet)
        self.app.processEvents()
        self.app.processEvents() # have to call twice to actually update widgets correctly

    def updateInfo_BlockCount(self, s):
        self.dialog.blocks.setText(s)
