import sys, sqlite3

from PyQt4 import QtCore, QtGui
from subject_manager import Ui_Form

FILE = "Subjects.db"

class MainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        # Load the form we created in QT Designer
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        ## Setup the Edit tab
        # Populate the uid_combobox with uids
        self.ui.uid_comboBox.insertItems(0, self.get_subject_uids())
        
        # Reflect changes
        self.update_edit_tab()
        
        # When we pick a new ID, change the other forms
        self.connect(self.ui.uid_comboBox,
                     QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.update_edit_tab)
        
        # Initialize the Save button
        self.connect(self.ui.edit_save_pushButton,
                     QtCore.SIGNAL('clicked()'),
                     self.save_edit)

        ## Setup the Add tab
        # Wait on this...
        
        
    def get_subject_uids(self):
        conn = sqlite3.connect(FILE)
        c = conn.cursor()
        c.execute("select id from subjects")        
        result = [str(x[0]) for x in c]        
        c.close()
        return result

    def update_edit_tab(self):
        conn = sqlite3.connect(FILE)
        c = conn.cursor()
        c.execute("select * from subjects where id = %s" % (self.ui.uid_comboBox.itemText(self.ui.uid_comboBox.currentIndex())))

        row = c.fetchone()
        
        self.ui.name_label.setText(str(row[2]) + ' ' + str(row[3]))
        self.ui.ieee_lineEdit.setText(row[13])
        self.ui.cuny_lineEdit.setText(row[15])
        self.ui.hint_lineEdit.setText(row[14])
        self.ui.cid_lineEdit.setText(row[16])
        self.ui.notes_lineEdit.setText(row[17])
        if row[18] == 'Y':
            self.ui.contact_edit_checkBox.setCheckState(QtCore.Qt.Checked)
        else:
            self.ui.contact_edit_checkBox.setCheckState(QtCore.Qt.Unchecked)

        c.close()

    def save_edit(self):
        conn = sqlite3.connect(FILE)
        c = conn.cursor()

        c.execute("update Subjects set ieee=?, cuny=?, hint=?, cid=?, notes=?, contact=? where id=?",
         (unicode(self.ui.ieee_lineEdit.text()), 
         unicode(self.ui.cuny_lineEdit.text()), 
         unicode(self.ui.hint_lineEdit.text()), 
         unicode(self.ui.cid_lineEdit.text()), 
         unicode(self.ui.notes_lineEdit.text()), 
         unicode(self.ui.contact_edit_checkBox), 
         unicode(self.ui.uid_comboBox.itemText(self.ui.uid_comboBox.currentIndex()))))

        conn.commit()
        c.close()
        conn.close()

    def add_subject(self):
        missing = [];
        if self.ui.first_name_lineEdit.text()=='':
            missing.append('First Name')
        if self.ui.last_name_lineEdit.text()=='':
            missing.append('Last Name')
        if self.ui.birthdate_dateEdit.text()=='':
            missing.append('Birthday')
        if self.iu.email_lineEdit.text()=='':
            missing.append('Email')
        if len(missing) > 0:
            msg = "The following required fields were left blank:\n\n";
            for field in missing:
                msg += field + "\n";
            reply = QtGui.QMessageBox.question(self, 'PAL',
             msg, QtGui.QMessageBox.Ok)
            return
        thisage = self.age(self.ui.birthdate_dateEdit.text())
        if int(thisage) < 18:
            reply = QtGui.QMessageBox.critical(self, 'PAL',
             "This subject appears to be under 18 years of age.\n\n" +
             "Legally, authorization from a parent or guardian\n" + 
             "is required for them to participate.\n" +
             "Do you want to continue?", 
             QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Cancel:
                return

        conn = sqlite3.connect(FILE)
        c = conn.cursor()

        if self.ui.contact_add_checkBox.isChecked():
            contact = 'Y'
        else:
            contact = 'N'

        # Insert the data
        c.execute("""insert into subjects
                  values (NULL,?,?,?,?,?,?,?,?,?,?,?,?,'','','','','',?)""",
                  (unicode(self.subjn.text()),
                  unicode(self.ui.first_name_lineEdit.text()),
                  unicode(self.ui.last_name_lineEdit.text()),
                  unicode(self.ui.birthdate_dateEdit.text()),
                  unicode(self.ui.age(self.ui.birthdate_dateEdit.text())),
                  unicode(self.ui.gender_comboBox.currentText()),
                  unicode(self.ui.email_lineEdit.text()),
                  unicode(self.ui.phone_lineEdit.text()),
                  unicode(self.ui.race_comboBox.currentText()),
                  unicode(self.ui.ethnic_id_comboBox.currentText()),
                  unicode(self.ui.consent_dateEdit.text()),
                  unicode(self.ui.audiogram_dateEdit.text()),
                  unicode(contact)
                  ))
        conn.commit()

        c.execute("""SELECT MAX(SubjN) FROM Subjects""")
        subn = c.fetchone()[0]
        c.close()
        conn.close()

        if (str(subn) == self.subjn.text()):
            reply = QtGui.QMessageBox.question(self, 'PAL',
             "Subject Number Confirmed:\n\n" + str(subn), QtGui.QMessageBox.Ok);
        else:
            reply = QtGui.QMessageBox.question(self, 'PAL',
             "Something weird happened with\nthe subject number. Check with Chris\n\nEntered: " + self.subjn.text() + '\nFound: ' + str(subn), QtGui.QMessageBox.Ok)
        self.close()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainForm()
    window.show()
    sys.exit(app.exec_())