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
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# Comments and/or additions are welcome. Send e-mail to: cbrown1@pitt.edu.
#

from PyQt4 import QtGui, QtCore
from .pylabconfig import Ui_Dialog
import sys
from copy import deepcopy
STDOUT = sys.stdout

name = 'qt'

def show_config(exp,run,var,stim,user):
    app = QtGui.QApplication([])
    config = ConfigDialog(app,exp,run,var,stim,user)
    config.show()
    app.exec_()

class ConfigDialog(QtGui.QWidget):

    def __init__(self, app,exp,run,var,stim,user):
        self.exp = exp
        self.run = run
        self.stim = stim
        self.var = var
        self.user = user
        self.app = app
        self.run.pylab_is_go = False # True tells pylab to run experiment (False == cancel)

        QtGui.QWidget.__init__(self, None)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.settings2form()

        self.connect(self.ui.Run,  QtCore.SIGNAL( 'clicked ()' ), self.run_experiment )
        self.connect(self.ui.Cancel,  QtCore.SIGNAL( 'clicked ()' ), self.cancel_experiment )
        self.connect(self.ui.DataPath_Get,  QtCore.SIGNAL( 'clicked ()' ), self.getDataPath )
        self.connect(self.ui.Stimulus_Names, QtCore.SIGNAL("itemSelectionChanged ()"), self.stim_select)
        self.connect(self.ui.Stimulus_PathToFiles, QtCore.SIGNAL("textChanged(QString)"), self.stim_selectPath)
        self.connect(self.ui.Stimulus_PathToText, QtCore.SIGNAL("textChanged (QString)"), self.stim_selectText)
        self.connect(self.ui.Stimulus_Order, QtCore.SIGNAL("textChanged (QString)"), self.stim_selectOrder)
        self.connect(self.ui.Stimulus_FileMask, QtCore.SIGNAL("textChanged (QString)"), self.stim_selectMask)
        self.connect(self.ui.Stimulus_Type, QtCore.SIGNAL("currentIndexChanged (QString)"), self.stim_selectType)
        self.connect(self.ui.Stimulus_Load, QtCore.SIGNAL("currentIndexChanged (QString)"), self.stim_selectLoad)
        self.connect(self.ui.Stimulus_Repeat, QtCore.SIGNAL("stateChanged (int)"), self.stim_selectRepeat)

    def settings2form(self):
        # Experiment:
        self.ui.InputMethod.clear()
        self.ui.ExperimentalMethod.clear()
        self.ui.Name.setText(self.exp.name)
        self.ui.ExperimentalMethod.addItems(self.exp.methodTypes)
        self.ui.Comments.setPlainText(self.exp.comments)
        self.ui.Subject.setText(self.exp.subjID)
        self.ui.RecordData.setChecked(self.exp.recordData)
        self.ui.DataPath.setText(self.exp.dataPath)
        self.ui.TrialsPerBlock.setValue(self.run.trialsperblock)
        self.ui.InputMethod.addItems(self.exp.responseTypes)
        self.ui.InputChars.setText(self.exp.validKeys)

        # Stimuli
        self.stimsets = deepcopy(self.stim.sets) #self.stim is a ref, so make a real copy to store changes, in case of cancel
        self.stimsetlist = []
        for stimset in self.stimsets:
            self.stimsetlist.append(stimset)
        self.ui.Stimulus_Load.clear()
        self.ui.Stimulus_Load.addItems(self.exp.stimLoadTypes)
        self.ui.Stimulus_Type.clear()
        self.ui.Stimulus_Type.addItems(self.exp.stimTypes)
        self.ui.Stimulus_Names.reset()
        self.ui.Stimulus_Names.addItems(self.stimsetlist)
        #self.ui.Stimulus_Names.setCurrentRow(0)

    def form2settings(self):
        # Experiment:
        self.exp.name = str(self.ui.Name.text())
        self.exp.comments = str(self.ui.Comments.toPlainText())
        self.exp.subjn = str(self.ui.Subject.text())
        self.exp.method = str(self.ui.ExperimentalMethod.currentText())
        self.exp.recordData = self.ui.RecordData.isChecked()
        self.exp.dataPath = str(self.ui.DataPath.text())
        self.exp.responseMethod = str(self.ui.InputMethod.currentText())
        self.exp.validKeys = str(self.ui.InputChars.text())
        self.run.trialsperblock = int(self.ui.TrialsPerBlock.value())

        self.stim.sets.clear()
        for i in range(self.ui.Stimulus_Names.count()):
            selected_name =  str(self.ui.Stimulus_Names.item(i).text())
            self.stim.sets[selected_name] = {}
            self.stim.sets[selected_name]['type'] = self.stimsets[selected_name]['type']
            if self.stimsets[selected_name].has_key('load'):
                self.stim.sets[selected_name]['load'] = self.stimsets[selected_name]['load']
            if self.stimsets[selected_name].has_key('path'):
                self.stim.sets[selected_name]['path'] = self.stimsets[selected_name]['path']
            if self.stimsets[selected_name].has_key('text'):
                self.stim.sets[selected_name]['text'] = self.stimsets[selected_name]['text']
            if self.stimsets[selected_name].has_key('repeat'):
                self.stim.sets[selected_name]['repeat'] = self.stimsets[selected_name]['repeat']
            if self.stimsets[selected_name].has_key('order'):
                self.stim.sets[selected_name]['order'] = self.stimsets[selected_name]['order']
            if self.stimsets[selected_name].has_key('mask'):
                self.stim.sets[selected_name]['mask'] = self.stimsets[selected_name]['mask']
            if self.exp.debug:
                print("SET: " + selected_name)
                for key in self.stim.sets[selected_name]:
                    print("    " + key + " : "),
                    print(self.stim.sets[selected_name][key])

    def stim_selectPath(self, t):
        #print "Path changed: " + str(t)
        selected_name =  str(self.ui.Stimulus_Names.selectedItems()[0].text())
        self.stimsets[selected_name]['path'] = str(t)
    def stim_selectText(self, t):
        #print "Text changed: " + str(t)
        selected_name =  str(self.ui.Stimulus_Names.selectedItems()[0].text())
        self.stimsets[selected_name]['text'] = str(t)

    def stim_selectOrder(self, t):
        #print "Order changed: " + str(t)
        selected_name =  str(self.ui.Stimulus_Names.selectedItems()[0].text())
        self.stimsets[selected_name]['order'] = str(t)

    def stim_selectMask(self, t):
        #print "Mask changed: " + str(t)
        selected_name =  str(self.ui.Stimulus_Names.selectedItems()[0].text())
        self.stimsets[selected_name]['mask'] = str(t)

    def stim_selectRepeat(self, i):
        #print "Repeat changed: " + str(i)
        selected_name =  str(self.ui.Stimulus_Names.selectedItems()[0].text())
        self.stimsets[selected_name]['repeat'] = self.ui.Stimulus_Repeat.isChecked()

    def stim_selectLoad(self, t):
        #print "Load changed: " + t
        selected_name =  str(self.ui.Stimulus_Names.selectedItems()[0].text())
        self.stimsets[selected_name]['load'] = str(t)

    def stim_selectType(self, t):
        #print "Type changed: " + t
        selected_name =  str(self.ui.Stimulus_Names.selectedItems()[0].text())
        self.stimsets[selected_name]['type'] = str(t)

    def getDataPath(self):
        ret = get_folder(parent=None, title = 'Select Folder to Store Data', default_dir = str(self.ui.DataPath.text()))
        if ret != "":
            self.ui.DataPath.setText(ret)

    def run_experiment(self):
        self.form2settings()
        self.run.pylab_is_go = True
        self.app.exit()

    def cancel_experiment(self):
        self.app.exit()

    def stim_select(self):
        selected_name =  str(self.ui.Stimulus_Names.selectedItems()[0].text())
        self.ui.Stimulus_Type.setCurrentIndex(self.exp.stimTypes.index(self.stimsets[selected_name]['type']))
        if self.stimsets[selected_name].has_key('path'):
            self.ui.Stimulus_PathToFiles.setText(self.stimsets[selected_name]['path'])
        else:
            self.ui.Stimulus_PathToFiles.setText("")
        if self.stimsets[selected_name].has_key('text'):
            self.ui.Stimulus_PathToText.setText(self.stimsets[selected_name]['text'])
        else:
            self.ui.Stimulus_PathToText.setText("")
        if self.stimsets[selected_name].has_key('mask'):
            self.ui.Stimulus_FileMask.setText(self.stimsets[selected_name]['mask'])
        else:
            self.ui.Stimulus_FileMask.setText("")
        if self.stimsets[selected_name].has_key('order'):
            self.ui.Stimulus_Order.setText(str(self.stimsets[selected_name]['order']))
        else:
            self.ui.Stimulus_Order.setText("")
        if self.stimsets[selected_name].has_key('repeat'):
            self.ui.Stimulus_Repeat.setChecked(self.stimsets[selected_name]['repeat'])
        else:
            self.ui.Stimulus_Repeat.setChecked(False)
        if self.stimsets[selected_name].has_key('load'):
            self.ui.Stimulus_Load.setCurrentIndex(self.exp.stimLoadTypes.index(self.stimsets[selected_name]['load']))
        else:
            self.ui.Stimulus_Load.setCurrentIndex(0)

def get_file(parent=None, title = 'Open File', default_dir = "", file_types = "All files types (*.*)"):
   """Opens a file dialog, returns file path as a string

       To specify filetypes, use the (qt) format:
       "Python or Plain Text Files (*.py *.txt);;All files (*.*)"
   """
   if QtGui.QApplication.startingUp():
       app = QtGui.QApplication([])
   sys.stdout = None # Avoid the "Redirecting output to win32trace
                     # remote collector" message from showing in stdout
   ret = QtGui.QFileDialog.getOpenFileName(parent, title, default_dir, file_types)
   sys.stdout = STDOUT
   return str(ret)

def get_folder(parent=None, title = 'Open Folder', default_dir = ""):
    """Opens a folder dialog, returns the path as a string
    """
    if QtGui.QApplication.startingUp():
        app = QtGui.QApplication([])
    sys.stdout = None
    ret = QtGui.QFileDialog.getExistingDirectory(parent, title, default_dir)
    sys.stdout = STDOUT
    return str(ret)

def get_input(parent=None, title = 'User Input', prompt = 'Enter a value:'):
    """Opens a simple prompt for user input, returns a string
    """
    if QtGui.QApplication.startingUp():
        app = QtGui.QApplication([])
    sys.stdout = None
    ret, ok = QtGui.QInputDialog.getText(parent, title, prompt)
    sys.stdout = STDOUT
    if ok:
        return str(ret)
    else:
        return ''

def get_item(parent=None, title = 'User Input', prompt = 'Choose One:', items = [], current = 0, editable = False):
    """Opens a simple prompt to choose an item from a list, returns a string
    """
    if QtGui.QApplication.startingUp():
        app = QtGui.QApplication([])
    sys.stdout = None
    ret, ok = QtGui.QInputDialog.getItem(parent, title, prompt, items, current, editable)
    sys.stdout = STDOUT
    if ok:
        return str(ret)
    else:
        return ''

def get_yesno(parent=None, title = 'User Input', prompt = 'Yes or No:'):
    """Opens a simple yes/no message box, returns a bool
    """
    if QtGui.QApplication.startingUp():
        app = QtGui.QApplication([])
    sys.stdout = None
    ret = QtGui.QMessageBox.question(parent, title, prompt, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
    sys.stdout = STDOUT
    if ret == QtGui.QMessageBox.Yes:
        return True
    else:
        return False

def show_message(parent=None, title = 'Title', message = 'Message', msgtype = 'Information'):
    """Opens a simple message box

      msgtype = 'Information', 'Warning', or 'Critical'
    """
    if QtGui.QApplication.startingUp():
        app = QtGui.QApplication([])
    sys.stdout = None
    if msgtype == 'Information':
        QtGui.QMessageBox.information(parent, title, message)
    elif msgtype == 'Warning':
        QtGui.QMessageBox.warning(parent, title, message)
    elif msgtype == 'Critical':
        QtGui.QMessageBox.critical(parent, title, message)
    sys.stdout = STDOUT

