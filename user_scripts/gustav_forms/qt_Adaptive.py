# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import time

class Interface():
    def __init__(self, choices):
        self.app = QtGui.QApplication([])
        self.dialog = self.Dialog(choices)
        self.dialog.show()
        self.dialog.setFixedSize(self.dialog.width(),self.dialog.height()) # <- Must be done after show
        self.app.processEvents()

    class Dialog(QtGui.QDialog):

        def __init__(self, choices, parent=None):
            QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowTitleHint)
            #self.setWindowIcon(QtGui.QIcon('icon.png'))
            self.char = ''
            self.waitingForResponse = False
            self.quitKey = '/'

            vbox = QtGui.QVBoxLayout()
            vbox.addStretch(1)

            self.task = QtGui.QLabel()
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

            self.setWindowTitle("Adapt!")
            self.setModal=False
            self.setFocus()

        def closeEvent(self, event):
            # fake a quit:
            self.waitingForResponse = True
            self.keyDown(ord(self.quitKey))

        def keyPressEvent(self, event):
            self.keyDown(event.key())

        def keyReleaseEvent(self, event):
            self.keyUp(event.key())

        def responseButtonEvent(self):
            self.keyDown(ord(str(self.sender().objectName())))

        def keyDown(self,key):
            if self.waitingForResponse:
                if key < 256:
                    thiskey = chr(key).lower()
                    self.char = thiskey
                    self.waitingForResponse = False

        def keyUp(self, key):
            if key == QtCore.Qt.Key_Control:
                ctrlDown = False
            elif key == QtCore.Qt.Key_Shift:
                shiftDown = False
            elif key == QtCore.Qt.Key_Alt:
                altDown = False


    # End AdaptiveDialog

    def get_resp(self, prompt=None):
        """Waits modally for a keypress
        """
        if prompt:
            self.dialog.task.setText(prompt)
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
