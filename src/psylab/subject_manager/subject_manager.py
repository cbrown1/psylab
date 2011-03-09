# -*- coding: utf-8 -*-

import sys, os
import sqlite3
import datetime
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
#from PySide import QtGui
#from PySide import QtCore
#from PyQt4 import uic
STDOUT = sys.stdout
form_class, base_class = uic.loadUiType("subject_manager_ui.ui")

class MyWidget (QtGui.QWidget, form_class):
    filename = 'Subjects.db'

    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.setWindowTitle("Subject Manager")
        self.filePath_label.setText(self.filename)

        self.connect(self.add_pushButton, QtCore.SIGNAL("clicked()"), self.add_Process)
        self.connect(self.add_birthdate_dateEdit, QtCore.SIGNAL("dateChanged(const QDate&)"), self.doAge)
        self.connect(self.edit_pushButton, QtCore.SIGNAL("clicked()"), self.edit_Process)
        self.connect(self.edit_all_pushButton, QtCore.SIGNAL("clicked()"), self.edit_all)
        self.connect(self.edit_subject_list_comboBox, QtCore.SIGNAL("currentIndexChanged (const QString&)"), self.edit_load_subject_data)
        self.connect(self.edit_search_lineEdit, QtCore.SIGNAL("textEdited ( const QString& )"), self.edit_load_subject_list)
        self.connect(self.edit_search_exact_checkBox, QtCore.SIGNAL("clicked ( bool )"), self.edit_load_subject_list)
        self.connect(self.edit_user_tableWidget, QtCore.SIGNAL("itemChanged ( QTableWidgetItem *)"), self.edit_data_changed)
        self.connect(self.edit_protocol_date_dateEdit, QtCore.SIGNAL("dateChanged ( QDate *)"), self.edit_data_changed)
        self.connect(self.edit_contact_checkBox, QtCore.SIGNAL("clicked ( bool )"), self.edit_data_changed)
        self.connect(self.edit_protocol_listWidget, QtCore.SIGNAL("currentItemChanged ( QListWidgetItem *, QListWidgetItem *)"), self.edit_protocol_selected)
        self.connect(self.edit_protocol_date_dateEdit.calendarWidget(), QtCore.SIGNAL("clicked(const QDate&)"), self.edit_protocol_dateChanged)
        self.connect(self.edit_protocol_date_remove_pushButton, QtCore.SIGNAL("clicked()"), self.edit_protocol_date_remove)
        self.connect(self.admin_protocols_add_pushButton, QtCore.SIGNAL("clicked()"), self.admin_protocols_add)
        self.connect(self.admin_protocols_remove_pushButton, QtCore.SIGNAL("clicked()"), self.admin_protocols_remove)
        self.connect(self.admin_user_add_pushButton, QtCore.SIGNAL("clicked()"), self.admin_user_add)
        self.connect(self.admin_user_remove_pushButton, QtCore.SIGNAL("clicked()"), self.admin_user_remove)
        self.connect(self.admin_create_db_pushButton, QtCore.SIGNAL("clicked()"), self.admin_create_db)

        self.edit_subject_protocol_dict = {}

        # Hack! Use bg color to `hide` the date in the protocol datewidget when none has been selected
        palette = QtGui.QPalette(self.edit_protocol_date_dateEdit.palette())
        self.datewidget_background_color = palette.color(QtGui.QPalette.Base).getRgb()
        self.datewidget_foreground_color = palette.color(QtGui.QPalette.WindowText).getRgb()
        self.datewidget_changed_programmatically = False
        dateedit_button_style = "QSpinBox::down-button {subcontrol-origin: border; subcontrol-position: bottom left; width: 16px; "
        dateedit_button_style += "image: url(:/icons/calendar.png) 1; border-width: 1px; border-top-width: 0;} "
        #dateedit_button_style += "QSpinBox::down-arrow {image: url(:/icons/calendar.png); width: 16px; height: 16px;}"
        self.edit_protocol_date_dateEdit.setStyleSheet(dateedit_button_style)

        self.admin_protocols_remove_pushButton.setIcon(QtGui.QIcon("icons/delete.png"))
        self.admin_protocols_remove_pushButton.setIconSize(QtCore.QSize(13, 13))
        self.admin_protocols_remove_pushButton.setText("")
        self.admin_protocols_add_pushButton.setIcon(QtGui.QIcon("icons/add.png"))
        self.admin_protocols_add_pushButton.setIconSize(QtCore.QSize(13, 13))
        self.admin_protocols_add_pushButton.setText("")

        self.admin_user_remove_pushButton.setIcon(QtGui.QIcon("icons/delete.png"))
        self.admin_user_remove_pushButton.setIconSize(QtCore.QSize(13, 13))
        self.admin_user_remove_pushButton.setText("")
        self.admin_user_add_pushButton.setIcon(QtGui.QIcon("icons/add.png"))
        self.admin_user_add_pushButton.setIconSize(QtCore.QSize(13, 13))
        self.admin_user_add_pushButton.setText("")

        self.admin_reports_remove_pushButton.setIcon(QtGui.QIcon("icons/delete.png"))
        self.admin_reports_remove_pushButton.setIconSize(QtCore.QSize(13, 13))
        self.admin_reports_remove_pushButton.setText("")
        self.admin_reports_add_pushButton.setIcon(QtGui.QIcon("icons/add.png"))
        self.admin_reports_add_pushButton.setIconSize(QtCore.QSize(13, 13))
        self.admin_reports_add_pushButton.setText("")

        self.edit_protocol_date_remove_pushButton.setIcon(QtGui.QIcon("icons/delete.png"))
        self.edit_protocol_date_remove_pushButton.setIconSize(QtCore.QSize(13, 13))
        self.edit_protocol_date_remove_pushButton.setText("")

        palette = QtGui.QPalette(self.edit_data_changed_label.palette())
        h_back = palette.color(QtGui.QPalette.Highlight)
        h_text = palette.color(QtGui.QPalette.HighlightedText)
        self.edit_data_changed_label.setStyleSheet("QLabel {color: rgb(%i, %i, %i); background-color: rgb(%i, %i, %i); padding: 3px;border: 1px solid rgb(%i, %i, %i); border-radius: 2px;}" %
            (h_text.red(), h_text.green(), h_text.blue(), h_back.red(), h_back.green(), h_back.blue(), h_text.red(), h_text.green(), h_text.blue()))
        self.edit_data_changed_label.setVisible(False)

        self.admin_init()
        self.add_init()
        self.add_edit_protocol_populate()
        self.edit_user_populate()
        self.edit_load_subject_list()
        self.show()
        self.setFixedSize(self.width(),self.height()) # <- Must be done after show

    def edit_Init(self):
        self.datewidget_changed_programmatically = True
        self.edit_protocol_date_dateEdit.setDate(datetime.datetime.now())
        self.datewidget_changed_programmatically = False
        for i in range(self.edit_protocol_listWidget.count()):
            item = self.edit_protocol_listWidget.item(i)
            if self.edit_subject_protocol_dict[item.text()] != "":
                self.edit_protocol_listWidget.item(i).setCheckState(QtCore.Qt.Checked)
        self.edit_data_changed_label.setVisible(False)

    def edit_load_subject_list(self, search_field=None):
        search_field = unicode(self.edit_search_lineEdit.text())
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        if search_field in [None, '']:
            print "No search"
            query = """SELECT SubjN,FName,LName FROM Subjects"""
        else:
            if self.edit_search_exact_checkBox.checkState() == QtCore.Qt.Checked:
                print "Exact search"
                query = """SELECT SubjN,FName,LName FROM Subjects WHERE Subjects MATCH \'%s\'""" % search_field
            else:
                print "Wildcard search"
                query = """SELECT SubjN,FName,LName FROM Subjects WHERE Subjects MATCH \'%s*\'""" % search_field
        c.execute(query)
        self.edit_subject_list_comboBox.clear()
        ind = 0
        for row in c:
            self.edit_subject_list_comboBox.insertItem(ind, "%3s, %s %s" % (row[0], row[1], row[2]))
            ind += 1
        c.close()
        conn.close()

    def edit_load_subject_data(self, info):
        subn = unicode(info.split(", ")[0]).strip()
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute("""SELECT FName,LName,Email,Phone,Contact FROM Subjects WHERE SubjN == \'%s\'""" % subn)
        subject = c.fetchone()
        if subject is not None:
            self.edit_name_label.setText("%s %s" % (subject[0],subject[1]))
            self.edit_email_label.setText("%s" % subject[2])
            self.edit_phone_label.setText("%s" % subject[3])
            self.edit_contact_checkBox.setChecked(bool(subject[4]))
            c.execute("""SELECT Protocol FROM Protocols""")
            protocols = c.fetchall()
            self.edit_subject_protocol_dict = {}
            for protocol in protocols:
                c.execute("""SELECT Protocol_%s FROM Subjects WHERE SubjN == \'%s\'""" % (protocol[0],subn))
                protocol_date = c.fetchone()
                for i in range(self.edit_protocol_listWidget.count()):
                    if protocol[0] == self.edit_protocol_listWidget.item(i).text():
                        if protocol_date[0] not in [None, '']:
                            self.edit_protocol_listWidget.item(i).setCheckState(QtCore.Qt.Checked)
                            self.edit_subject_protocol_dict[unicode(self.edit_protocol_listWidget.item(i).text())] = protocol_date[0]
                        else:
                            self.edit_protocol_listWidget.item(i).setCheckState(QtCore.Qt.Unchecked)
                            self.edit_subject_protocol_dict[unicode(self.edit_protocol_listWidget.item(i).text())] = ""

            c.execute("""SELECT UserVar FROM UserVars""")
            vars = c.fetchall()
            rowcount = 0
            for var in vars:
                c.execute("""SELECT User_%s FROM Subjects WHERE SubjN == \'%s\'""" % (var[0],subn))
                uservar_this = c.fetchone()
                if uservar_this[0] is not None:
                    item = QtGui.QTableWidgetItem(uservar_this[0])
                    for i in range(self.edit_user_tableWidget.rowCount()):
                        if var[0] == self.edit_user_tableWidget.item(i,0).text():
                            self.edit_user_tableWidget.setItem(i, 1, item)
        else:
            self.edit_name_label.setText("")
            self.edit_email_label.setText("")
            self.edit_phone_label.setText("")
            self.edit_contact_checkBox.setChecked(False)
            for i in range(self.edit_protocol_listWidget.count()):
                self.edit_protocol_listWidget.item(i).setCheckState(QtCore.Qt.Unchecked)
            for i in range(self.edit_user_tableWidget.rowCount()):
                item = QtGui.QTableWidgetItem("")
                self.edit_user_tableWidget.setItem(i, 1, item)
        c.close()
        conn.close()
        self.edit_data_changed_label.setVisible(False)


    def edit_Process(self):
        query = "UPDATE Subjects SET "
        subn = unicode(self.edit_subject_list_comboBox.currentText().split(", ")[0]).strip()
        for k,v in self.edit_subject_protocol_dict.items():
            if v != "":
                query += "Protocol_%s = '%s', " % (k, v)
            else:
                query += "Protocol_%s = '%s', " % (k, "None")
        for i in range(self.edit_user_tableWidget.rowCount()):
            if self.edit_user_tableWidget.item(i,1):
                query += "User_%s = '%s', " % (unicode(self.edit_user_tableWidget.item(i,0).text()), unicode(self.edit_user_tableWidget.item(i,1).text()))
            else:
                query += "User_%s = '%s', " % (unicode(self.edit_user_tableWidget.item(i,0).text()), "None")
        if self.edit_contact_checkBox.checkState() == QtCore.Qt.Checked:
            query += "Contact = 'True' "
        else:
            query += "Contact = 'False' "

        query += "WHERE SubjN = '%s';" % subn

        #print query

        self.edit_data_changed_label.setVisible(False)
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        c.close()
        conn.close()

    def edit_user_populate(self):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute("""SELECT UserVar FROM UserVars""")
        self.edit_user_tableWidget.clear()
        self.edit_user_tableWidget.setHorizontalHeaderLabels(["Name","Value"])
        rowcount = 0
        for row in c:
            item = QtGui.QTableWidgetItem(row[0])
            item.setFlags( QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled )
            self.edit_user_tableWidget.setRowCount(rowcount+1)
            self.edit_user_tableWidget.setItem(rowcount, 0, item)
            rowcount += 1
        c.close()
        conn.close()

    def add_edit_protocol_populate(self):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute("""SELECT Protocol FROM Protocols""")
        self.edit_protocol_listWidget.clear()
        self.add_protocol_comboBox.clear()
        for row in c:
            item = QtGui.QListWidgetItem(row[0])
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setFlags( QtCore.Qt.ItemIsSelectable | # QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable |
                                    QtCore.Qt.ItemIsEnabled )
            self.edit_protocol_listWidget.insertItem(-1, item)
            self.add_protocol_comboBox.insertItem(-1, row[0])
            self.edit_subject_protocol_dict[row[0]] = ''
        c.close()
        conn.close()
        self.add_protocol_comboBox.setCurrentIndex(0)
        self.edit_protocol_listWidget.setCurrentRow(0)

    def edit_protocol_selected(self, current, prev): #, current_item):
        if (self.edit_protocol_listWidget.currentItem() is not None) and (self.edit_protocol_listWidget.currentItem().checkState() == QtCore.Qt.Checked):
            #self.edit_protocol_date_dateEdit.setStyleSheet("QDateEdit::lineEdit {color: rgb(%i, %i, %i); padding: 0px;}" %
            self.edit_protocol_date_dateEdit.setStyleSheet("QDateEdit {color: rgb(%i, %i, %i); padding: 0px;}" %
                (self.datewidget_foreground_color[0], self.datewidget_foreground_color[1], self.datewidget_foreground_color[2]))
            self.edit_protocol_date_dateEdit.setDate(QtCore.QDate.fromString(self.edit_subject_protocol_dict[unicode(self.edit_protocol_listWidget.currentItem().text())], "yyyy-MM-dd"))
        else:
            #self.edit_protocol_date_dateEdit.setStyleSheet("QDateEdit::lineEdit {color: rgb(%i, %i, %i); padding: 0px;}" %
            self.edit_protocol_date_dateEdit.setStyleSheet("QDateEdit {color: rgb(%i, %i, %i); padding: 0px;}" %
                (self.datewidget_background_color[0], self.datewidget_background_color[1], self.datewidget_background_color[2]))
            self.datewidget_changed_programmatically = True # stupid datewidget doesn't know the difference
            self.edit_protocol_date_dateEdit.setDate(datetime.datetime.now())
            self.datewidget_changed_programmatically = False

    def edit_protocol_dateChanged(self, newdate):
        if not self.datewidget_changed_programmatically:
            self.edit_data_changed_label.setVisible(True)
            self.edit_protocol_listWidget.currentItem().setCheckState(QtCore.Qt.Checked)
            #self.edit_protocol_date_dateEdit.setStyleSheet("QDateEdit::down-button {color: rgb(%i, %i, %i); padding: 0px;}" %
            self.edit_protocol_date_dateEdit.setStyleSheet("QDateEdit {color: rgb(%i, %i, %i); padding: 0px;}" %
                (self.datewidget_foreground_color[0], self.datewidget_foreground_color[1], self.datewidget_foreground_color[2]))
            self.edit_subject_protocol_dict[self.edit_protocol_listWidget.currentItem().text()] = self.edit_protocol_date_dateEdit.date().toString('yyyy-MM-dd')

    def edit_protocol_date_remove(self):
        self.edit_data_changed_label.setVisible(True)
        self.edit_protocol_listWidget.currentItem().setCheckState(QtCore.Qt.Unchecked)
        self.edit_subject_protocol_dict[self.edit_protocol_listWidget.currentItem().text()] = ""
        #self.edit_protocol_date_dateEdit.setStyleSheet("QDateEdit::lineEdit {color: rgb(%i, %i, %i); padding: 0px;}" %
        self.edit_protocol_date_dateEdit.setStyleSheet("QDateEdit {color: rgb(%i, %i, %i); padding: 0px;} QDateEdit::down-arrow {color: rgb(%i, %i, %i); padding: 0px;} " %
            (self.datewidget_background_color[0], self.datewidget_background_color[1], self.datewidget_background_color[2],
             self.datewidget_background_color[0], self.datewidget_background_color[1], self.datewidget_background_color[2]))

    def edit_data_changed(self, obj):
        self.edit_data_changed_label.setVisible(True)

    def edit_all(self):
        edit_all_dialog = QtgGui.QDialog()

    def admin_init(self):
        if not os.path.isfile(self.filename):
            self.admin_create_db()

        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute("""SELECT Protocol FROM Protocols""")
        self.admin_protocols_listWidget.clear()

        for row in c:
            self.admin_protocols_listWidget.insertItem(-1, row[0])
        c.execute("""SELECT UserVar FROM UserVars""")
        self.admin_user_listWidget.clear()
        for row in c:
            self.admin_user_listWidget.insertItem(-1, row[0])
        c.close()
        conn.close()

    def admin_create_db(self):
        ret = self.get_newfile(title = 'Select existing DB file to open, or enter new filename to create:')
        if ret != '':
            self.filename = ret
            self.filePath_label.setText(ret)
            if not os.path.isfile(self.filename):
                qry = open('New_DB_Schema_debug.sql', 'r').read()
                conn = sqlite3.connect(ret)
                c = conn.cursor()
                c.executescript(qry)
                conn.commit()
                c.close()
                conn.close()
                self.select_tab('Admin')
            self.add_init()
            self.add_edit_protocol_populate()
            self.edit_user_populate()
            self.admin_init()

    def admin_protocols_add(self):
        ret = self.get_input(title = 'Subject Manager', prompt = 'Enter a protocol name.\nSpaces will be replaced with _')
        if ret != '':
            ret = ret.replace(" ","_")
            self.admin_protocols_listWidget.insertItem(-1, ret)
            conn = sqlite3.connect(self.filename);
            c = conn.cursor();
            c.execute("""INSERT INTO Protocols (Protocol) VALUES (\'%s\')""" % ret)
            conn.commit()
            c.close()
            conn.close()
            self.sqlite_column_add(self.filename, 'Subjects', 'Protocol_%s' % ret)
            self.add_edit_protocol_populate()

    def admin_protocols_remove(self):
        if self.admin_protocols_listWidget.currentItem() is not None:
            val = self.admin_protocols_listWidget.currentItem().text()
            ret = self.get_yesno(title = 'Subject Manager', prompt = 'All data will be permanently lost!\nAre you sure you want to remove protocol:\n\n'+ val)
            if ret:
                conn = sqlite3.connect(self.filename)
                c = conn.cursor()
                c.execute("""Delete from Protocols where Protocol == \'%s\'""" % val)
                c.close()
                conn.commit()
                conn.close()
                item = self.admin_protocols_listWidget.takeItem(self.admin_protocols_listWidget.currentRow())
                item = None
                self.sqlite_column_delete(self.filename, 'Subjects', 'Protocol_%s' % val)
                self.add_edit_protocol_populate()

    def admin_user_add(self):
        ret = self.get_input(title = 'Subject Manager', prompt = 'Enter a user variable name.\nSpaces will be replaced with _')
        if ret != '':
            ret = ret.replace(" ","_")
            self.admin_user_listWidget.insertItem(-1, ret)
            conn = sqlite3.connect(self.filename);
            c = conn.cursor();
            c.execute("""INSERT INTO UserVars (UserVar) VALUES (\'%s\')""" % ret)
            conn.commit()
            c.close()
            conn.close()
            self.sqlite_column_add(self.filename, 'Subjects', 'User_%s' % ret)
            self.edit_user_populate()

    def admin_user_remove(self):
        if self.admin_user_listWidget.currentItem() is not None:
            val = self.admin_user_listWidget.currentItem().text()
            ret = self.get_yesno(title = 'Subject Manager', prompt = 'All data will be permanently lost!\nAre you sure you want to remove user variable:\n\n'+ val)
            if ret:
                conn = sqlite3.connect(self.filename)
                c = conn.cursor()
                c.execute("""Delete from UserVars where UserVar == \'%s\'""" % val)
                c.close()
                conn.commit()
                conn.close()
                item = self.admin_user_listWidget.takeItem(self.admin_user_listWidget.currentRow())
                item = None
                self.sqlite_column_delete(self.filename, 'Subjects', 'User_%s' % val)
                self.edit_user_populate()

    def add_init(self):
        conn = sqlite3.connect(self.filename);
        c = conn.cursor();
        c.execute("""SELECT MAX(SubjN) FROM Subjects""");
        subn = c.fetchone();
        if subn[0] is None:
            self.add_subject_lineEdit.setText('1')
        else:
            self.add_subject_lineEdit.setText(unicode(int(subn[0])+1));

        c.execute("""SELECT EthnicID FROM EthnicIDs""")
        self.add_ethnic_id_comboBox.clear()
        for row in c:
            self.add_ethnic_id_comboBox.insertItem(-1, row[0])

        c.execute("""SELECT Race FROM Races""")
        self.add_race_comboBox.clear()
        for row in c:
            self.add_race_comboBox.insertItem(-1, row[0])

        c.execute("""SELECT Gender FROM Genders""")
        self.add_gender_comboBox.clear()
        for row in c:
            self.add_gender_comboBox.insertItem(-1, row[0])

        c.close();
        conn.close();
        
        self.add_fname_lineEdit.setText('')
        self.add_lname_lineEdit.setText('')
        self.add_email_lineEdit.setText('')
        self.add_phone_lineEdit.setText('')

        now = datetime.datetime.now()
        eighteenyears = datetime.timedelta(days=18*365)
        self.add_birthdate_dateEdit.setDate(now - eighteenyears)
        self.doAge();

    def add_Process(self):
        # Check for missing data
        missing = [];
        if self.add_fname_lineEdit.text()=='':
            missing.append('First Name')
        if self.add_lname_lineEdit.text()=='':
            missing.append('Last Name')
        if self.add_birthdate_dateEdit.text()=='':
            missing.append('Birthday')
        if self.add_email_lineEdit.text()=='':
            missing.append('Email')
        if len(missing) > 0:
            msg = "The following required fields were left blank:\n\n";
            msg = "\n".join(missing)
            reply = QtGui.QMessageBox.question(self, 'Subject Manager', msg, QtGui.QMessageBox.Ok)
            return
        # Check for adult
        thisage = self.age(self.add_birthdate_dateEdit.text())
        if int(thisage) < 18:
            reply = QtGui.QMessageBox.critical(self, 'Subject Manager',
             "This subject appears to be under 18 years of age.\n\n" +
             "Legally, authorization from a parent or guardian\n" +
             "is required for this individual to participate.\n" +
             "Do you want to continue?",
             QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Cancel:
                return;
        # Check for duplicate
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute("""SELECT SubjN FROM Subjects WHERE FName='%s' AND LName='%s' AND DOB='%s'""" %
                  (unicode(self.add_fname_lineEdit.text()),unicode(self.add_lname_lineEdit.text()),unicode(self.add_birthdate_dateEdit.text())));
        s = c.fetchone();
        if s != None:
            reply = QtGui.QMessageBox.information(self, 'Subject Manager',
             "This subject appears to be in the database.\n\n" +
             "A match was found based on first name,\n" +
             "last name, and birthdate.\n\n" +
             "The subject number is %s.\n\n" +
             "OK to add this subject anyway?" % cns[0],
             QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Cancel:
                return;
        # Check for unique subject number
        c.execute("""SELECT MAX(SubjN) FROM Subjects""")
        subj_new = unicode(self.add_subject_lineEdit.text()).strip()
        subj_db = unicode(int(c.fetchone()[0]) + 1)
        if (subj_new == subj_db):
            reply = QtGui.QMessageBox.question(self, 'Subject Manager',
             "Subject Number Confirmed:\n\n" + subj_new, QtGui.QMessageBox.Ok)
        else:
            subj_new = unicode(int(subj_new)+1)
            reply = QtGui.QMessageBox.question(self, 'Subject Manager',
             "The subject number entered is not unique.\nMaybe a subject was added very recently?\n\nThe new subject number is now: " + subj_new,
              QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Cancel:
                return;

        # We can now gather data and enter it into db
        query_columns_list = ["SubjN", "FName", "LName", "DOB", "Today", "Gender", "Email", "Phone", "Race", "EthnicID", "Contact"]
        
        query_vals_list = [subj_new, unicode(self.add_fname_lineEdit.text()),unicode(self.add_lname_lineEdit.text()),unicode(self.add_birthdate_dateEdit.text()), 
            unicode(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')), unicode(self.add_gender_comboBox.currentText()), unicode(self.add_email_lineEdit.text()),
            unicode(self.add_phone_lineEdit.text()), unicode(self.add_race_comboBox.currentText()), unicode(self.add_ethnic_id_comboBox.currentText()), unicode(self.add_contact_checkBox.checkState())]
        
        c.execute("""SELECT Protocol FROM Protocols""")
        for row in c:
            query_columns_list.append("Protocol_%s" % row[0])
            if row[0] == self.add_protocol_comboBox.currentText():
                query_vals_list.append(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d'))
            else:
                query_vals_list.append('')

        c.execute("""SELECT UserVar FROM UserVars""")
        for row in c:
            query_columns_list.append("User_%s" % row[0])
            query_vals_list.append('')
         
        #print "\'"+"\',\'".join(query_columns_list)+"\'"
        #print "\'"+"\',\'".join(query_vals_list)+"\'"
        c.execute("""INSERT INTO Subjects (\'%s\') VALUES (\'%s\')""" % ("\',\'".join(query_columns_list), "\',\'".join(query_vals_list)))
        conn.commit()
        c.close()
        conn.close()
        self.add_init()
        #self.close()

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

    def select_tab(self, tabText):
        for i in range(self.tabWidget.count()):
            if self.tabWidget.tabText(i) == tabText:
                self.tabWidget.setCurrentIndex(i)


    def sqlite_column_add(self, db_file, table, column, default='ff123'):

        """ALTER TABLE YourTable RENAME TO OldTable;
        CREATE TABLE YourTable (/* old cols */, NewColumn DATETIME NOT NULL);
        INSERT INTO YourTable SELECT *, '2000-01-01 00:00:00' FROM OldTable;
        DROP TABLE OldTable;
        """
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("""PRAGMA table_info(%s);""" % table)
        col_create_list = []
        cols = []
        for row in c:
            col_create_list.append("'%s' TEXT DEFAULT '%s'" % (row[1], row[2]))
            cols.append(row[1])
        if column not in cols:
            colstr_old = ",".join(cols)
            cols.append(column)
            colstr_new = ",".join(cols)
            col_create_list.append("'%s' TEXT DEFAULT '%s'" % (column, default))
            col_create_str = ",".join(col_create_list)
            c.execute("""CREATE TEMPORARY TABLE %s_backup(%s);""" % (table, colstr_new))
            c.execute("""INSERT INTO %s_backup (%s) SELECT %s FROM %s""" % (table, colstr_old, colstr_old, table))
            c.execute("""DROP TABLE %s;""" % table)
            c.execute("""CREATE VIRTUAL TABLE %s USING FTS3(%s);""" % (table, col_create_str))
            c.execute("""INSERT INTO %s SELECT %s FROM %s_backup;""" % (table, colstr_new, table))
            c.execute("""DROP TABLE %s_backup;""" % table)
            conn.commit()
        c.close()
        conn.close()

    def sqlite_column_delete(self, db_file, table, column):
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("""PRAGMA table_info(%s);""" % table)
        col_list = []
        cols = []
        rows = c.fetchall()
        for row in rows:
            cols.append(row[1])
        if column in cols:
            for row in rows:
                if row[1] != column:
                    col_create_list.append("'%s' TEXT DEFAULT '%s'" % (row[1], row[2]))
            col_create_str = ",".join(col_create_list)
            cols.remove(column)
            colstr = ",".join(cols)
            c.execute("""CREATE TEMPORARY TABLE %s_backup(%s);""" % (table, colstr))
            c.execute("""INSERT INTO %s_backup SELECT %s FROM %s;""" % (table, colstr, table))
            c.execute("""DROP TABLE %s;""" % table)
            c.execute("""CREATE VIRTUAL TABLE %s USING FTS3(%s);""" % (table, col_create_str))
            c.execute("""INSERT INTO %s SELECT %s FROM %s_backup;""" % (table, colstr, table))
            c.execute("""DROP TABLE %s_backup;""" % table)
            conn.commit()
        c.close()
        conn.close()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = MyWidget(None)
    if len(sys.argv)>1:
        form.select_tab(sys.argv[1])
    app.exec_()
