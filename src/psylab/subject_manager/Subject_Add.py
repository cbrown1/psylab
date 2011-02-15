# -*- coding: utf-8 -*-

import sys, datetime, sqlite3
from PyQt4 import QtGui, QtCore

filename = r'S:\Projects\PAL\Subjects\Subjects.db'

class AddSubjectUI(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.setWindowTitle("Psychoacoustics Lab @ ASU: Add Subject")
        self.setWindowIcon(QtGui.QIcon('shs_head16.png'))

        # Widgets
        OKButton = QtGui.QPushButton(self.tr("&OK"))
        cancelButton = QtGui.QPushButton(self.tr("&Cancel"))

        CurrDate = QtCore.QDate.currentDate()
        self.birth = QtGui.QDateEdit(CurrDate)
        self.birth.setDisplayFormat("yyyy-MM-dd");
        self.cons = QtGui.QDateEdit(CurrDate)
        self.cons.setDisplayFormat("yyyy-MM-dd");
        self.audio = QtGui.QDateEdit(CurrDate)
        self.audio.setDisplayFormat("yyyy-MM-dd");

        self.fname = QtGui.QLineEdit()
        self.lname = QtGui.QLineEdit()
        self.email = QtGui.QLineEdit()
        self.phone = QtGui.QLineEdit()
        self.subjn = QtGui.QLineEdit()

        self.race = QtGui.QComboBox()
        self.race.addItems(["White","Black","Asian","Pacific","Native American","Mixed/Other"])
        self.ethn = QtGui.QComboBox()
        self.ethn.addItems(["Not Hispanic","Hispanic/Latino","Unknown"])
        self.gend = QtGui.QComboBox()
        self.gend.addItems(["Female","Male"])

        self.contact = QtGui.QCheckBox('Consent to\nContact?')

        lfname = QtGui.QLabel('First Name')
        llname = QtGui.QLabel('Last Name')
        lemail = QtGui.QLabel('Email')
        lphone = QtGui.QLabel('Phone #')
        lbirth = QtGui.QLabel('Birthdate')
        lrace = QtGui.QLabel('Race')
        lethn = QtGui.QLabel('Ethnic ID')
        lcons = QtGui.QLabel('Consent')
        laudio = QtGui.QLabel('Audiogram')
        lgend = QtGui.QLabel('Gender')
        lsubjn = QtGui.QLabel('Subject #')
        self.lage = QtGui.QLabel('Age:     ')

        lfname.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        llname.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        lemail.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        lphone.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        lbirth.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        lrace.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        lethn.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        lcons.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        laudio.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        lgend.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        lsubjn.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        # Signals
        self.connect(OKButton, QtCore.SIGNAL("clicked()"), self.Process)
        self.connect(cancelButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("close()"))
        self.connect(self.birth, QtCore.SIGNAL("dateChanged(const QDate&)"), self.doAge)

        # Fonts
        f = QtGui.QFont()
        f.setPointSize(12)

        self.birth.setFont(f);
        self.cons.setFont(f);
        self.audio.setFont(f);
        self.fname.setFont(f);
        self.lname.setFont(f);
        self.email.setFont(f);
        self.phone.setFont(f);
        self.subjn.setFont(f);
        self.race.setFont(f);
        self.ethn.setFont(f);
        self.gend.setFont(f);
        OKButton.setFont(f);
        cancelButton.setFont(f);
        lfname.setFont(f);
        llname.setFont(f);
        lemail.setFont(f);
        lphone.setFont(f);
        lbirth.setFont(f);
        lrace.setFont(f);
        lethn.setFont(f);
        lcons.setFont(f);
        laudio.setFont(f);
        lgend.setFont(f);
        lsubjn.setFont(f);
        self.lage.setFont(f);

        # Layout
        grid = QtGui.QGridLayout();
        grid.setSpacing(10);

        grid.addWidget(lfname, 1, 0);
        grid.addWidget(self.fname, 1, 1, 1, 2);
        grid.addWidget(llname, 2, 0);
        grid.addWidget(self.lname, 2, 1, 1, 2);
        grid.addWidget(lemail, 3, 0);
        grid.addWidget(self.email, 3, 1, 1, 2);
        grid.addWidget(lphone, 4, 0);
        grid.addWidget(self.phone, 4, 1, 1, 2);
        grid.addWidget(lbirth, 5, 0);
        grid.addWidget(self.birth, 5, 1);
        grid.addWidget(self.lage, 5, 2);
        #grid.addWidget(self.birth, 5, 1, 1, 2);

        grid.addWidget(self.contact, 6, 2);

        grid.addWidget(lethn, 1, 3);
        grid.addWidget(self.ethn, 1, 4, 1, 3);
        grid.addWidget(lrace, 2, 3);
        grid.addWidget(self.race, 2, 4, 1, 3);
        grid.addWidget(lgend, 3, 3);
        grid.addWidget(self.gend, 3, 4, 1, 3);
        grid.addWidget(lcons, 4, 3);
        grid.addWidget(self.cons, 4, 4, 1, 3);
        grid.addWidget(laudio, 5, 3);
        grid.addWidget(self.audio, 5, 4, 1, 3);

        grid.addWidget(cancelButton, 6, 4, 1, 2);
        grid.addWidget(OKButton, 6, 6);
        grid.addWidget(lsubjn, 6, 0);
        grid.addWidget(self.subjn, 6, 1);
        self.setLayout(grid);

        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        
        conn = sqlite3.connect(filename);
        c = conn.cursor();
        c.execute("""SELECT MAX(SubjN) FROM Subjects""");
        subn = c.fetchone();
        self.subjn.setText(str(subn[0]+1));
        c.close();
        conn.close();
        self.doAge();

    def doAge(self):
        thisage = self.age(self.birth.text());
        if int(thisage) < 18:
            self.lage.setText(u"<font color='red'>Age: " + unicode(thisage) + "</font>");
        else:
            self.lage.setText(u"<font color='green'>Age: " + unicode(thisage) + "</font>");

    def Process(self):
        missing = [];
        if self.fname.text()=='':
            missing.append('First Name');
        if self.lname.text()=='':
            missing.append('Last Name');
        if self.birth.text()=='':
            missing.append('Birthday');
        if self.email.text()=='':
            missing.append('Email');
        if len(missing) > 0:
            msg = "The following required fields were left blank:\n\n";
            for field in missing:
                msg += field + "\n";
            reply = QtGui.QMessageBox.question(self, 'PAL',
             msg, QtGui.QMessageBox.Ok);
            return;
        thisage = self.age(self.birth.text())
        if int(thisage) < 18:
            reply = QtGui.QMessageBox.critical(self, 'PAL',
             "This subject appears to be under 18 years of age.\n\n" +
             "Legally, authorization from a parent or guardian\n" + 
             "is required for them to participate.\n" +
             "Do you want to continue?", 
             QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel);
            if reply == QtGui.QMessageBox.Cancel:
                return;
        conn = sqlite3.connect(filename);
        c = conn.cursor();
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
                  (unicode(self.subjn.text()),
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
                  ));
        conn.commit();
        c.execute("""SELECT MAX(SubjN) FROM Subjects""");
        subn = c.fetchone()[0];
        c.close();
        conn.close();
        if (str(subn) == self.subjn.text()):
            reply = QtGui.QMessageBox.question(self, 'PAL',
             "Subject Number Confirmed:\n\n" + str(subn), QtGui.QMessageBox.Ok);
        else:
            reply = QtGui.QMessageBox.question(self, 'PAL',
             "Something weird happened with\nthe subject number. Check with Chris\n\nEntered: " + self.subjn.text() + '\nFound: ' + str(subn), QtGui.QMessageBox.Ok);
        self.close();

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

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv);
    prog = AddSubjectUI();
    prog.show();
    sys.exit(app.exec_());
