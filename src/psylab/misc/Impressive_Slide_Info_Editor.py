# -*- coding: utf-8 -*-

import sys, os
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
STDOUT = sys.stdout
form_class, base_class = uic.loadUiType("Impressive_Slide_Info_Editor_ui.ui")

class MyWidget (QtGui.QWidget, form_class):

    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.setWindowTitle("Impressive InfoFile Editor")
        self.slide_viewer_label.setSizePolicy(QtGui.QSizePolicy.Ignored,
                QtGui.QSizePolicy.Ignored)
        self.slide_viewer_label.setScaledContents(True)
        self.scrollArea.setWidgetResizable(True)

        self.connect(self.select_slides_pushButton, QtCore.SIGNAL("clicked()"), self.select_slides)

        #self.fileDir = r'C:\Documents and Settings\cabrown4\My Documents\_writing\2011 Talk - UofA Colloquium\slides'
        #self.fileMask = ['.png']
        #self.fileList = self.listDirectory(self.fileDir, self.fileMask)
        #self.load_image(self.fileList[0])
        self.fileDir = r''
        self.fileMask = ['.png','.jpg','.JPG']
        self.fileList = {}



    def select_slides(self):
        self.fileDir = self.get_folder(title = 'Open Folder', default_dir = "")
        if self.fileDir != '':
            fileList = self.listDirectory(self.fileDir, self.fileMask)
            for file in fileList:
                self.fileList[os.path.splitext(os.path.basename(file))[0]] = file
            self.slide_selector_comboBox.clear()
            for key,val in self.fileList.items():
                self.slide_selector_comboBox.insertItem(-1, key)
            self.load_image(self.fileList[os.path.splitext(os.path.basename(fileList[0]))[0]])


    def load_image(self, fileName):
        image = QtGui.QImage(fileName)
        if image.isNull():
            QtGui.QMessageBox.information(self, "Image Viewer",
                    "Cannot load %s." % fileName)
            return

        self.slide_viewer_label.setPixmap(QtGui.QPixmap.fromImage(image))


    def listDirectory(self, directory, fileExtList):
        "get list of file info objects for files of particular extensions"
        fileList = [os.path.normcase(f)
                    for f in os.listdir(directory)]
        if fileExtList is not None:
            fileList = [os.path.join(directory, f)
                       for f in fileList
                        if os.path.splitext(f)[1] in fileExtList]
        return fileList


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

    def get_newfile(parent=None, title = 'Open File', default_dir = "", file_types = "All files types (*.*)"):
        """Opens a file dialog, returns file path as a string

            To specify filetypes, use the (qt) format:
            "Python or Plain Text Files (*.py *.txt);;All files (*.*)"
        """
        if QtGui.QApplication.startingUp():
            app = QtGui.QApplication([])
        sys.stdout = None # Avoid the "Redirecting output to win32trace
                            # remote collector" message from showing in stdout
        ret = QtGui.QFileDialog.getSaveFileName(parent, title, default_dir, file_types)
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


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = MyWidget(None)
    form.show()
    app.exec_()
