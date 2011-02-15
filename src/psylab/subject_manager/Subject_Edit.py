#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, datetime, time, sqlite3
from PyQt4 import QtGui, QtCore

filename = r'S:\Projects\PAL\Subjects\Subjects.db'

class AddSubjectUI(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.setWindowTitle("Psychoacoustics Lab @ ASU: Edit Subject")
        self.setWindowIcon(QtGui.QIcon('shs_head16.png'))

        # Widgets
        OKButton = QtGui.QPushButton(self.tr("&Apply"))
        cancelButton = QtGui.QPushButton(self.tr("&Close"))
        upButton = QtGui.QPushButton(self.tr("&Up"))
        dnButton = QtGui.QPushButton(self.tr("&Dn"))

        self.subjn = QtGui.QLineEdit()
        self.subjn.setValidator(QtGui.QIntValidator(self.subjn));
        self.ieee = QtGui.QLineEdit()
        self.hint = QtGui.QLineEdit()
        self.cuny = QtGui.QLineEdit()
        self.cid = QtGui.QLineEdit()
        self.note = QtGui.QLineEdit()
        
        self.contact = QtGui.QCheckBox('Consent to\nContact?')
        
        self.dname = QtGui.QLabel('')
        lname = QtGui.QLabel('Name')
        lsubjn = QtGui.QLabel('Subject #')
        lIEEE = QtGui.QLabel('IEEE')
        lHINT = QtGui.QLabel('HINT')
        lCUNY = QtGui.QLabel('CUNY')
        lCID = QtGui.QLabel('CID')
        lNOTE = QtGui.QLabel('Notes')

        lname.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        lsubjn.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        lIEEE.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        lHINT.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        lCUNY.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        lCID.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        lNOTE.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        # Signals
        self.connect(OKButton, QtCore.SIGNAL("clicked()"), self.Process)
        self.connect(cancelButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("close()"))
        self.connect(upButton, QtCore.SIGNAL("clicked()"), self.up)
        self.connect(dnButton, QtCore.SIGNAL("clicked()"), self.dn)
        self.connect(self.subjn, QtCore.SIGNAL("editingFinished()"), self.change)

        # Fonts
        f = QtGui.QFont()
        f.setPointSize(12)

        self.dname.setFont(f);
        self.subjn.setFont(f);
        self.ieee.setFont(f);
        self.hint.setFont(f);
        self.cuny.setFont(f);
        self.cid.setFont(f);
        self.note.setFont(f);
        lname.setFont(f);
        lsubjn.setFont(f);
        lIEEE.setFont(f);
        lHINT.setFont(f);
        lCUNY.setFont(f);
        lCID.setFont(f);
        lNOTE.setFont(f);
        OKButton.setFont(f);
        cancelButton.setFont(f);
        upButton.setFont(f);
        dnButton.setFont(f);
        
        # Layout
        grid = QtGui.QGridLayout();
        grid.setSpacing(10);

        grid.addWidget(self.subjn, 1, 1);
        grid.addWidget(lIEEE, 3, 0);
        grid.addWidget(self.ieee, 3, 1, 1, 2);
        grid.addWidget(lCUNY, 4, 0);
        grid.addWidget(self.cuny, 4, 1, 1, 2);
        grid.addWidget(lNOTE, 5, 0, 1, 1);
        grid.addWidget(self.note, 5, 1, 1 ,4);
        grid.addWidget(self.contact, 5, 5, 1 ,2);
        grid.addWidget(cancelButton, 6, 5);
        grid.addWidget(OKButton, 6, 6);
        grid.addWidget(lHINT, 3, 3, 1, 2);
        grid.addWidget(self.hint, 3, 5, 1 ,2);
        grid.addWidget(lCID, 4, 3, 1, 2);
        grid.addWidget(self.cid, 4, 5, 1 ,2);

        grid.addWidget(dnButton, 1, 0);
        grid.addWidget(upButton, 1, 2);
        grid.addWidget(lname, 1, 3);
        grid.addWidget(self.dname, 1, 5, 1, 2);
        self.setLayout(grid);

        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

        #import os
        #if not os.path.exists(filename):
            #reply = QtGui.QMessageBox.information(self, 'PAL',
             #"The database file was not found.\n\n" +
             #"You can click OK to create a new one,\n" + 
             #"but this is probably an error.\n" +
             #"Best thing to do is click cancel,\n" + 
             #"and talk to Chris.", 
             #QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel);
            #if reply == QtGui.QMessageBox.Cancel:
                #sys.exit(app.exec_());
            #else:
                #conn = sqlite3.connect(filename);
                #c = conn.cursor();
                #c.execute("""CREATE TABLE "Subjects" (
                 #"ID" INTEGER PRIMARY KEY AUTOINCREMENT,
                 #"SubjN" INTEGER,
                 #"FName" TEXT,
                 #"LName" TEXT,
                 #"DOB" TEXT,
                 #"Today" TEXT,
                 #"Gender" TEXT,
                 #"Email" TEXT,
                 #"Phone" TEXT,
                 #"Race" TEXT,
                 #"EthnicID" TEXT,
                 #"Consent" TEXT,
                 #"Audiogram" TEXT,
                 #"IEEE" TEXT,
                 #"HINT" TEXT,
                 #"CUNY" TEXT,
                 #"CID" TEXT,
                 #"NOTES" TEXT
                 #);""")
                #conn.commit();
                #c.close();
                #conn.close();

        self.subjn.setText('1');
        self.update()
        #conn = sqlite3.connect(filename);
        #c = conn.cursor();
        #c.execute("""SELECT MAX(SubjN) FROM Subjects""");
        #subn = c.fetchone();
        #self.subjn.setText(str(subn[0]+1));
        #c.close();
        #conn.close();
        #self.doAge();

    def update(self):
        subjn = str(self.subjn.text());
        conn = sqlite3.connect(filename);
        c = conn.cursor();
        c.execute("""SELECT * FROM Subjects WHERE SubjN=?""",(str(subjn[:]),));
        row = c.fetchone();
        self.subjn.setText(str(row[1]));
        self.dname.setText(str(row[2]) + ' ' + str(row[3]));
        self.ieee.setText(row[13]);
        self.cuny.setText(row[15]);
        self.hint.setText(row[14]);
        self.cid.setText(row[16]);
        self.note.setText(row[17]);
        if row[18] == 'Y':
            self.contact.setCheckState(QtCore.Qt.Checked)
        else:
            self.contact.setCheckState(QtCore.Qt.Unchecked)
        c.close();
        conn.close();

    def change(self):
        subjn = self.subjn.text();
        if subjn != '':
            conn = sqlite3.connect(filename);
            c = conn.cursor();
            c.execute("""SELECT SubjN FROM Subjects WHERE SubjN>=?""",(str(subjn),));
            subjn = c.fetchone()[0];
            c.execute("""SELECT MAX(SubjN) FROM Subjects""");
            maxsn = c.fetchone()[0];
            c.close();
            conn.close();
            if int(subjn) < 1 | int(subjn) > int(maxsn):
                subjn = '1';
            self.subjn.setText(str(subjn));
            self.update();


    def up(self):
        subjn = int(self.subjn.text());
        if subjn != '':
            conn = sqlite3.connect(filename);
            c = conn.cursor();
            c.execute("""SELECT SubjN FROM Subjects WHERE SubjN>?""",(str(subjn),));
            ret = c.fetchone();
            if ret is not None:
                subjn = ret[0];
        c.execute("""SELECT MAX(SubjN) FROM Subjects""");
        maxsn = c.fetchone()[0];
        c.close();
        conn.close();
        if int(subjn) < 1:
            subjn = '1';
        self.subjn.setText(str(subjn));
        self.update();

    def dn(self):
        subjn = self.subjn.text();
        if subjn != '':
            if int(subjn) > 1:
                conn = sqlite3.connect(filename);
                c = conn.cursor();
                c.execute("""SELECT SubjN FROM Subjects WHERE SubjN<?""",(str(subjn),));
                subjn = c.fetchall()[-1][0];
            else:
                subjn = str(1);

        self.subjn.setText(str(subjn));
        self.update();

    def Process(self):
        subjn = str(self.subjn.text());
        conn = sqlite3.connect(filename);
        c = conn.cursor();
        c.execute("""SELECT * FROM Subjects WHERE SubjN=?""",(str(subjn[:]),));
        row = c.fetchone();
        line = datetime.date.today().isoformat() + " " + time.strftime("%H:%M:%S", time.localtime()) + " ";
        for item in row:
            line = line + "~" + str(item);
        line = line + "\n";
        try:
          import codecs
          fin = None
          fin = codecs.open(r'S:\Projects\PAL\Subjects\Subjects.log', encoding='utf8', mode='a')
          fin.write(line)
        except:
          print "error writing file"
        finally:
          if fin != None:
            fin.close()
        if self.contact.isChecked():
            contact = 'Y';
        else:
            contact = 'N';
        c.execute("""UPDATE Subjects SET IEEE=?, CUNY=?, HINT=?, CID=?, Notes=?, Contact=? WHERE SubjN=?""",
         (unicode(self.ieee.text()), 
         unicode(self.cuny.text()), 
         unicode(self.hint.text()), 
         unicode(self.cid.text()), 
         unicode(self.note.text()), 
         unicode(contact), 
         unicode(subjn[:]),));
        conn.commit();
        c.close();
        conn.close();

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv);
    prog = AddSubjectUI();
    prog.show();
    sys.exit(app.exec_());
