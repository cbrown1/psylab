# messagebox.py

import sys
from PyQt4 import QtGui, QtCore


class MessageBox(QtGui.QDialog):
    def __init__(self, fupdate, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.fupdate = fupdate
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('TEST~!')
        self.setModal=False #(QtCore.Qt.NonModal)


    def keyPressEvent(self, event):
        #if event.key() == QtCore.Qt.Key_Escape:
        #    self.close()
        #else:
        #    self.fupdate(event.key())
		self.fupdate(self, event.key())

	
def update(mb, key):
	if key < 256:
		thiskey = chr(key)
		print thiskey
	elif key == 16777216:
		print "closing..."
		mb.close()
	else:
		print "non-ascii character: " + str(key)

app = QtGui.QApplication(sys.argv)
qb = MessageBox(update)
qb.setWindowModality(QtCore.Qt.NonModal)
qb.show()
app.processEvents()
sys.exit(app.exec_())
