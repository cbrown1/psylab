# -*- coding: utf-8 -*-
# messagebox.py

import sys
from PyQt4 import QtGui, QtCore
import time

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
            self.char = ''
            self.waitingForResponse = False

            vbox = QtGui.QVBoxLayout()
            vbox.addStretch(1)

            self.task = QtGui.QLabel(exp.prompt)
            f = self.task.font()
            f.setPointSize(14);
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

    def updateInfo_BlockCount(self, s):
        self.dialog.blocks.setText(s)
