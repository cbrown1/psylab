#!/usr/bin/python
# -*- coding: utf-8 -*-

# calendar.py

import sys
import sqlite3
import datetime
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
form_class, base_class = uic.loadUiType("subject_manager.ui")

class MyWidget (QtGui.QWidget, form_class):
    filename = 'Subjects.db'

    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.filePath_label.setText(self.filename)
        now = datetime.datetime.now()
        eighteenyears = datetime.timedelta(days=18*365)
        self.add_birthdate_dateEdit.setDate(now - eighteenyears)
        self.add_audiogram_dateEdit.setDate(now)
        self.add_consent_dateEdit.setDate(now)

        self.connect(self.add_pushButton, QtCore.SIGNAL("clicked()"), self.add_Process)
        self.connect(self.edit_pushButton, QtCore.SIGNAL("clicked()"), self.edit_Process)
        self.connect(self.add_birthdate_dateEdit, QtCore.SIGNAL("dateChanged(const QDate&)"), self.doAge)

        conn = sqlite3.connect(self.filename);
        c = conn.cursor();
        c.execute("""SELECT MAX(SubjN) FROM Subjects""");
        subn = c.fetchone();
        self.add_subject_lineEdit.setText(str(subn[0]+1));
        c.close();
        conn.close();
        self.doAge();

    def edit_Process(self):
        pass

    def add_Process(self):
        missing = [];
        if self.add_name_first_lineEdit.text()=='':
            missing.append('First Name')
        if self.add_name_last_lineEdit.text()=='':
            missing.append('Last Name')
        if self.add_birthdate_lineEdit.text()=='':
            missing.append('Birthday')
        if self.add_email_lineEdit.text()=='':
            missing.append('Email')
        if len(missing) > 0:
            msg = "The following required fields were left blank:\n\n";
            msg = "\n".join(missing)
            reply = QtGui.QMessageBox.question(self, 'PAL', msg, QtGui.QMessageBox.Ok)
            return
        thisage = self.age(self.birth.text())
        if int(thisage) < 18:
            reply = QtGui.QMessageBox.critical(self, 'PAL',
             "This subject appears to be under 18 years of age.\n\n" +
             "Legally, authorization from a parent or guardian\n" +
             "is required for them to participate.\n" +
             "Do you want to continue?",
             QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Cancel:
                return;
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
#        c.execute("""SELECT Consent FROM Subjects WHERE FName=? AND LName=? AND DOB=?""",
#                  (unicode(self.fname.text()),unicode(self.lname.text()),unicode(self.birth.text())));
#        cns = c.fetchone();
#        if len(cns) != "":
#            reply = QtGui.QMessageBox.information(self, 'PAL',
#             "This subject appears to be in the database.\n\n" +
#             "A match was found based on first name,\n" +
#             "last name, and birthdate.\n" +
#             "Informed Consent was obtained on " + cns[0] +
#             "Do you want to continue?",
#             QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel);
#            if reply == QtGui.QMessageBox.Cancel:
#                return;
        if self.contact.isChecked():
            contact = 'Y';
        else:
            contact = 'N';
        c.execute("""insert into subjects
                  values (NULL,?,?,?,?,?,?,?,?,?,?,?,?,'','','','','',?)""",
                  (unicode(self.add_subject_lineEdit.text()),
                  unicode(self.fname.text()),
                  unicode(self.lname.text()),
                  unicode(self.birth.text()),
                  unicode(self.age(self.birth.text())),
                  unicode(self.gend.currentText()),
                  unicode(self.email.text()),
                  unicode(self.phone.text()),
                  unicode(self.race.currentText()),
                  unicode(self.ethn.currentText()),
                  unicode(self.cons.text()),
                  unicode(self.audio.text()),
                  unicode(contact)
                  ))
        conn.commit()
        c.execute("""SELECT MAX(SubjN) FROM Subjects""")
        subn = c.fetchone()[0]
        c.close()
        conn.close()
        if (str(subn) == self.add_subject_lineEdit.text()):
            reply = QtGui.QMessageBox.question(self, 'PAL',
             "Subject Number Confirmed:\n\n" + str(subn), QtGui.QMessageBox.Ok)
        else:
            reply = QtGui.QMessageBox.question(self, 'PAL',
             "Something weird happened with\nthe subject number. Check with Chris\n\nEntered: " + self.add_subject_lineEdit.text() + '\nFound: ' + str(subn), QtGui.QMessageBox.Ok)
        self.close()

    def doAge(self):
        thisage = self.age(self.add_birthdate_dateEdit.text());
        if int(thisage) < 18:
            self.add_age_label.setText(u"<font color='red'>Age: " + unicode(thisage) + "</font>");
        else:
            self.add_age_label.setText(u"<font color='green'>Age: " + unicode(thisage) + "</font>");

    def days_previous_month(self, y, m):
        from calendar import monthrange as _monthrange;
        m -= 1;
        if m == 0:
            y -= 1;
            m = 12;
        _, days = _monthrange(y, m);
        return days;

    def age(self,dob):
        time_format = "%Y-%m-%d";
        today1 = datetime.date.today();
        dob1 = datetime.datetime.strptime(str(dob), time_format);
        y = today1.year - dob1.year;
        m = today1.month - dob1.month;
        d = today1.day - dob1.day;
        while m <0 or d <0:
            while m <0:
                y -= 1;
                m = 12 + m;  # m is negative
            if d <0:
                m -= 1;
                days = self.days_previous_month(today1.year, today1.month);
                d = max(0, days - dob1.day) + today1.day;
        return y;


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = MyWidget(None)
    form.show()
    tabtxt = ['Add','Edit','Browse','Reports','Admin']
    for i in range(len(tabtxt)):
        form.tabWidget.setTabText(i,tabtxt[i])
    if len(sys.argv)>1:
        form.tabWidget.setCurrentIndex(tabtxt.index(sys.argv[1]))
    app.exec_()
