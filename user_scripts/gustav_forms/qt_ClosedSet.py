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
        self.app.processEvents()

    class Dialog(QtGui.QDialog):

        def __init__(self, choices, parent=None):
            QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowTitleHint)
            #self.setWindowIcon(QtGui.QIcon('icon.png'))
            self.goodResponse = False
            self.waitingForResponse = False
            self.response = None
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
            self.default_button_stylesheet_nobg = "font-size: 16px; font-weight: bold; border: 4px solid gray; border-radius: 10px;} QPushButton:pressed {background-color: lightGray;}"
            self.default_button_stylesheet += self.default_button_stylesheet_nobg

            self.bbox = QtGui.QHBoxLayout()
            self.bbox_group = []
            i = 0
            for choice_group in choices:
                thisgroup = []
                thisVLayout = QtGui.QVBoxLayout()
                for choice in choice_group:
                    button = QtGui.QPushButton(choice)
                    button.clicked.connect(self.responseButtonEvent)
                    button.setObjectName(str(i) + "_" + choice)
                    button.setFixedHeight(40)
                    button.setFixedWidth(80)
                    button.setCheckable(True)
                    button.setStyleSheet(self.default_button_stylesheet)
                    thisVLayout.addWidget(button)
                    thisgroup.append(button)
                self.bbox_group.append(thisgroup)
                self.bbox.addLayout(thisVLayout)
                i += 1
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

            self.setWindowTitle("Closed Set!")
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
            self.setFocus()
            obj = self.sender().objectName()
            group,choice = obj.split("_")
            self.radioCheck(int(group), choice)
            self.isGoodResponse()
            if self.goodResponse:
                self.response = self.getAllText()
                self.waitingForResponse = False

        def keyDown(self, key):
            if self.waitingForResponse:
                if key < 256:
                    thiskey = chr(key).lower()
                    if thiskey == self.quitKey:
                        # Close...
                        self.response = None
                        self.waitingForResponse = False

        def keyUp(self, key):
            if key == QtCore.Qt.Key_Control:
                ctrlDown = False
            elif key == QtCore.Qt.Key_Shift:
                shiftDown = False
            elif key == QtCore.Qt.Key_Alt:
                altDown = False

        def radioCheck(self, group, choice):
            if self.waitingForResponse:
                for item in self.bbox_group[group]:
                    if item.text() == choice:
                        item.setChecked(True)
                        stylesheet = "QPushButton {background-color: yellow; " + self.default_button_stylesheet_nobg
                    else:
                        item.setChecked(False)
                        stylesheet = self.default_button_stylesheet
                    item.setStyleSheet(stylesheet)

        def isGoodResponse(self):
            all = True
            for group in  self.bbox_group:
                thisGroup = False
                for item in group:
                    thisGroup = thisGroup or item.isChecked()
                all = all and thisGroup
            self.goodResponse = all

        def getAllText(self):
            resp = []
            for group in self.bbox_group:
                for item in group:
                    if item.isChecked():
                        resp.append(unicode(item.text()))
            return " ".join(resp)

        def resetForm(self):
            self.response = None
            self.goodResponse = False
            for group in self.bbox_group:
                for item in group:
                    item.setChecked(False)
                    stylesheet = self.default_button_stylesheet
                    item.setStyleSheet(stylesheet)

    # End Dialog

    def get_resp(self, prompt=None):
        """Waits modally for a full response
        """
        if prompt:
            self.dialog.task.setText(prompt)
        self.dialog.waitingForResponse = True
        while self.dialog.waitingForResponse:
            self.app.processEvents()
            time.sleep(.1)
        ret = self.dialog.response
        self.dialog.resetForm()
        self.update_form()
        return ret

    def updateInfo_task(self, s):
        self.dialog.task.setText(s)
        self.update_form()

    def updateInfo_BlockCount(self, s):
        self.dialog.blocks.setText(s)
        self.update_form()

    def resetForm(self):
        self.dialog.resetForm()
        self.update_form()

    def update_form(self):
        # have to call this twice or some widgets won't update
        self.app.processEvents()
        self.app.processEvents()

