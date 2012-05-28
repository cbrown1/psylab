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

import sys, os
import sqlite3
import datetime
import platform
import ConfigParser
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import Qt
from PyQt4 import uic
#from PySide import QtGui
#from PySide import QtCore
#from PyQt4 import uic
STDOUT = sys.stdout
form_class, base_class = uic.loadUiType("subject_manager_ui.ui")

class SubjectManager (QtGui.QWidget, form_class):
    version = '0.1'
    filename = ''
    configFilePath = 'subject_manager.ini'

    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.setWindowTitle("Subject Manager")
        self.setWindowIcon(QtGui.QIcon('images/report.png'))
        
        self.connect(self.add_pushButton, QtCore.SIGNAL("clicked()"), self.add_Process)
        self.connect(self.add_birthdate_dateEdit, QtCore.SIGNAL("dateChanged(const QDate&)"), self.doAge)
        self.connect(self.edit_pushButton, QtCore.SIGNAL("clicked()"), self.edit_Process)
        self.connect(self.edit_subject_list_comboBox, QtCore.SIGNAL("currentIndexChanged (const QString&)"), self.edit_load_subject_data)
        self.connect(self.edit_search_lineEdit, QtCore.SIGNAL("textEdited ( const QString& )"), self.edit_load_subject_list)
        #self.connect(self.edit_search_exact_checkBox, QtCore.SIGNAL("clicked ( bool )"), self.edit_search_exact_clicked)
        self.connect(self.edit_search_back_pushButton, QtCore.SIGNAL("clicked()"), self.edit_search_back)
        self.connect(self.edit_search_fwd_pushButton, QtCore.SIGNAL("clicked()"), self.edit_search_fwd)
        self.connect(self.edit_reports_run_pushButton, QtCore.SIGNAL("clicked()"), self.edit_reports_click_button)
        self.connect(self.edit_reports_listWidget, QtCore.SIGNAL("itemDoubleClicked ( QListWidgetItem * )"), self.edit_reports_click_list)

        self.connect(self.edit_user_tableWidget, QtCore.SIGNAL("itemChanged ( QTableWidgetItem *)"), self.edit_data_changed)
        self.connect(self.edit_protocol_date_dateEdit, QtCore.SIGNAL("dateChanged ( QDate *)"), self.edit_data_changed)
        self.connect(self.edit_contact_checkBox, QtCore.SIGNAL("clicked ( bool )"), self.edit_data_changed)
        self.connect(self.edit_notes_plainTextEdit, QtCore.SIGNAL("textChanged ()"), self.edit_note_changed)

        self.connect(self.edit_protocol_listWidget, QtCore.SIGNAL("currentItemChanged ( QListWidgetItem *, QListWidgetItem *)"), self.edit_protocol_selected)
        self.connect(self.edit_protocol_date_dateEdit.calendarWidget(), QtCore.SIGNAL("clicked(const QDate&)"), self.edit_protocol_dateChanged)
        self.connect(self.edit_protocol_date_remove_pushButton, QtCore.SIGNAL("clicked()"), self.edit_protocol_date_remove)
        
        self.connect(self.admin_protocols_add_pushButton, QtCore.SIGNAL("clicked()"), self.admin_protocols_add)
        self.connect(self.admin_protocols_remove_pushButton, QtCore.SIGNAL("clicked()"), self.admin_protocols_remove)
        self.connect(self.admin_user_add_pushButton, QtCore.SIGNAL("clicked()"), self.admin_user_add)
        self.connect(self.admin_user_remove_pushButton, QtCore.SIGNAL("clicked()"), self.admin_user_remove)
        self.connect(self.admin_db_create_pushButton, QtCore.SIGNAL("clicked()"), self.admin_create_db)
        self.connect(self.admin_db_open_pushButton, QtCore.SIGNAL("clicked()"), self.admin_open_db)
        self.connect(self.admin_db_export_schema_pushButton, QtCore.SIGNAL("clicked()"), self.admin_export_schema)
        self.connect(self.admin_db_import_schema_pushButton, QtCore.SIGNAL("clicked()"), self.admin_import_schema)
        self.connect(self.admin_reports_listWidget, QtCore.SIGNAL("currentItemChanged ( QListWidgetItem *, QListWidgetItem *)"), self.admin_reports_selected)
        self.connect(self.admin_reports_run_pushButton, QtCore.SIGNAL("clicked()"), self.admin_reports_run_buttonclick)
        self.connect(self.admin_reports_listWidget, QtCore.SIGNAL("itemDoubleClicked ( QListWidgetItem * )"), self.admin_reports_run_listclick)
        self.connect(self.admin_reports_script_pushButton, QtCore.SIGNAL("clicked()"), self.admin_reports_script_browse)
        
        self.connect(self.admin_reports_add_pushButton, QtCore.SIGNAL("clicked()"), self.admin_reports_add)
        self.connect(self.admin_reports_remove_pushButton, QtCore.SIGNAL("clicked()"), self.admin_reports_remove)

        self.edit_subject_protocol_dict = {}
        
        self.edit_user_tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        # Hack! Use bg color to `hide` the date in the protocol datewidget when none has been selected
        palette = QtGui.QPalette(self.edit_protocol_date_dateEdit.palette())
        self.datewidget_background_color = palette.color(QtGui.QPalette.Base).getRgb()
        self.datewidget_foreground_color = palette.color(QtGui.QPalette.WindowText).getRgb()
        self.datewidget_changed_programmatically = False
        dateedit_button_style = "QSpinBox::down-button {subcontrol-origin: border; subcontrol-position: bottom left; width: 16px; "
        dateedit_button_style += "image: url(:/images/calendar.png) 1; border-width: 1px; border-top-width: 0;} "
        #dateedit_button_style += "QSpinBox::down-arrow {image: url(:/images/calendar.png); width: 16px; height: 16px;}"
        self.edit_protocol_date_dateEdit.setStyleSheet(dateedit_button_style)

        self.admin_protocols_remove_pushButton.setIcon(QtGui.QIcon("images/delete.png"))
        self.admin_protocols_remove_pushButton.setText("")

        self.admin_protocols_add_pushButton.setIcon(QtGui.QIcon("images/add.png"))
        self.admin_protocols_add_pushButton.setText("")

        self.admin_db_create_pushButton.setIcon(QtGui.QIcon("images/database_add.png"))
        self.admin_db_create_pushButton.setStyleSheet ("text-align: left");
        
        self.admin_db_open_pushButton.setIcon(QtGui.QIcon("images/database_folder.png"))
        self.admin_db_open_pushButton.setStyleSheet ("text-align: left");
        
        self.admin_db_export_schema_pushButton.setIcon(QtGui.QIcon("images/database_save.png"))
        self.admin_db_export_schema_pushButton.setStyleSheet ("text-align: left");
        
        self.admin_db_import_schema_pushButton.setIcon(QtGui.QIcon("images/database_plain.png"))
        self.admin_db_import_schema_pushButton.setStyleSheet ("text-align: left");
        
        self.admin_user_remove_pushButton.setIcon(QtGui.QIcon("images/delete.png"))
        self.admin_user_remove_pushButton.setText("")

        self.admin_user_add_pushButton.setIcon(QtGui.QIcon("images/add.png"))
        self.admin_user_add_pushButton.setText("")

        self.admin_reports_remove_pushButton.setIcon(QtGui.QIcon("images/delete.png"))
        self.admin_reports_remove_pushButton.setText("")
        
        self.admin_reports_add_pushButton.setIcon(QtGui.QIcon("images/add.png"))
        self.admin_reports_add_pushButton.setText("")

        self.admin_reports_run_pushButton.setIcon(QtGui.QIcon("images/page_chart_go.png"))
        self.admin_reports_run_pushButton.setText("")

        self.admin_reports_script_pushButton.setIcon(QtGui.QIcon("images/folder_add.png"))
        self.admin_reports_script_pushButton.setText("")
        
        self.edit_pushButton.setIcon(QtGui.QIcon("images/user_save.png"))
        self.edit_pushButton.setText("Save")

        self.edit_protocol_date_remove_pushButton.setIcon(QtGui.QIcon("images/delete.png"))
        self.edit_protocol_date_remove_pushButton.setText("")

        self.edit_reports_run_pushButton.setIcon(QtGui.QIcon("images/page_chart_go.png"))
        self.edit_reports_run_pushButton.setText("")

        self.edit_search_back_pushButton.setIcon(QtGui.QIcon("images/back.png"))
        self.edit_search_back_pushButton.setText("")

        self.edit_search_fwd_pushButton.setIcon(QtGui.QIcon("images/fwd.png"))
        self.edit_search_fwd_pushButton.setText("")

        self.edit_find_label.setPixmap(QtGui.QPixmap("images/find.png"))
        self.edit_find_label.setText("")

        self.edit_subjects_label.setPixmap(QtGui.QPixmap("images/group.png"))
        self.edit_subjects_label.setText("")

        self.add_pushButton.setIcon(QtGui.QIcon("images/user_add.png"))
        self.add_pushButton.setText("Add")

        self.admin_user_listWidget.setAlternatingRowColors(True)
        
        palette = QtGui.QPalette(self.edit_data_changed_label.palette())
        h_back = palette.color(QtGui.QPalette.Highlight)
        h_text = palette.color(QtGui.QPalette.HighlightedText)
        self.edit_data_changed_label.setStyleSheet("QLabel {color: rgb(%i, %i, %i); background-color: rgb(%i, %i, %i); padding: 3px;border: 1px solid rgb(%i, %i, %i); border-radius: 2px;}" %
            (h_text.red(), h_text.green(), h_text.blue(), h_back.red(), h_back.green(), h_back.blue(), h_text.red(), h_text.green(), h_text.blue()))
        self.edit_data_changed_label.setVisible(False)
        
        self.about_textedit.setAlignment(Qt.Qt.AlignLeft | Qt.Qt.AlignTop)
        self.about_textedit.setText("""<h3><img src='images/report.png'>&nbsp;Subject Manager  %s</h3> 
                                 <p><i>Copyright &copy; 2010-2012 Christopher Brown &lt;cbrown1@pitt.edu&gt;</i></p> 
                                 <p>This program comes with ABSOLUTELY NO WARRANTY. This is free software, and is distributed 
                                 under the terms of the GNU GPL. You are welcome to redistribute it under certain conditions; 
                                 see http://www.gnu.org/licenses/ for more information.</p>
                                 <p>Subject Manager is part of Psylab. Bug reports, bug fixes, suggestions, enhancements, or other
                                 contributions are welcome. Go to http://code.google.com/p/psylab/ for more information and to contribute. 
                                 <p>Python Version: %s<br> 
                                 Qt Version: %s<br>
                                 PyQt Version: %s<br>
                                 SQLite Version: %s</p> 
                                 <p>Most icons taken or derived from the Silk Icon Set, found at http://www.famfamfam.com/lab/icons/silk/</p>
                                 """ % (self.version, platform.python_version(), QtCore.QT_VERSION_STR, QtCore.PYQT_VERSION_STR, sqlite3.sqlite_version)
                                )
        self.about_textedit.viewport().setAutoFillBackground(False) # <- Transparent bg
        self.about_textedit.setStyleSheet('QTextEdit {padding-top: 10px; padding-left: 10px; padding-right: 10px}')

        self.edit_data_changed_label.setToolTip("This subject's data have changed.\nClick save, or changes will be lost.")
        self.edit_search_back_pushButton.setToolTip("Select previous subject in list")
        self.edit_search_fwd_pushButton.setToolTip("Select next subject in list")
        self.edit_search_lineEdit.setToolTip("""<p>Enter search terms to filter the list of subjects</p>
                                                <p>When multiple search terms are used, the default is AND (ie., 'John Smith' will return
                                                only records containing both 'John' AND 'Smith'). You can use the OR operator (ie., 'John OR Mary'
                                                will return any record that contains either 'John' OR 'Mary'.</p>
                                                <p>The default is exact matches (ie., 'Mar' will not return records containing 'Mary'). 
                                                You can use the * wildcard to specify partial matches (ie., 'Mar*' will match both 
                                                'Mary' and 'Margaret').</p>
                                                <p>You can search for records that do not contain a term using -. (ie., 'Mary -Jones').</p>
                                                <p>You can limit the search for a term to a specific variable (ie., 'FName:John LName:Smith')</p>
                                                <p>To search a User Data variable, add 'User_' to the beginning of 
                                                the variable name ('User_R1k:5').</p>
                                                """)
        self.edit_protocol_listWidget.setToolTip("""<p>Protocols consented to by a subject</p>
                                                <p>A check means that consent for a protocol was obtained from a subject</p> 
                                                <p>Click on that protocol to see the date of consent, or enter a date and click save</p>
                                                """)
        self.edit_protocol_date_dateEdit.setToolTip("""<p>Displays or sets the date on which a subject consented to a protocol</p>
                                                    <p>If you change this value, be sure to click save or the changes will be lost</p>
                                                    """)
        self.edit_reports_listWidget.setToolTip("""<p>This is a list of reports available for individual subjects.</p> 
                                                <p>Double-click on a report to run it.</p>
                                                """)
        self.edit_reports_run_pushButton.setToolTip("Run selected Report")
        self.edit_user_tableWidget.setToolTip("""<p>This is a list of user variables and their values for each subject</p> 
                                                <p>If you change any values, be sure to click save or the changes will be lost</p>
                                                """)
        self.admin_db_create_pushButton.setToolTip("Click to create a new, empty database")
        self.admin_db_open_pushButton.setToolTip("Click to open an existing database")
        self.admin_db_export_schema_pushButton.setToolTip("Click export all data in database to an sql file")
        self.admin_db_import_schema_pushButton.setToolTip("""<p>Click to import data from an sql file</p>
                                                    <p><b>WARNING! All current data will be lost!</b></p>
                                                    <p>You should backup your DB regularly
                                                    (either by exporting the data, or by simply
                                                    copying the db file to a safe place)</p>
                                                    """)
        self.admin_protocols_add_pushButton.setToolTip("Add a new Protocol")
        self.admin_protocols_remove_pushButton.setToolTip("Delete selected Protocol")
        self.admin_reports_add_pushButton.setToolTip("Add a new Report")
        self.admin_reports_remove_pushButton.setToolTip("Delete selected Report")
        self.admin_reports_run_pushButton.setToolTip("Run selected Report")
        self.admin_user_add_pushButton.setToolTip("Add a new User Variable")
        self.admin_user_remove_pushButton.setToolTip("Delete selected User Variable")
        self.admin_reports_script_pushButton.setToolTip("Browse to select a Report script")
        self.admin_protocols_listWidget.setToolTip("""<p>The list of Protocols</p>
                                                    <p>Add new protocols, or delete unneeded ones here</p>
                                                    <p><b>WARNING! Deleting a protocol will
                                                    delete all subject data for that protocol!</b></p>
                                                    <p>You should backup your DB regularly
                                                    (either by exporting the data, or by simply
                                                    copying the db file to a safe place)</p>
                                                    """)
        self.admin_reports_listWidget.setToolTip("""<p>The list of reports</p>
                                                    <p>Add new reports, or delete unneeded ones here</p>
                                                    <p>Note that deleting a report here does not delete
                                                    the report script, only the reference to it here</p>
                                                    """)
        self.admin_reports_name_lineEdit.setToolTip("""<p>The name of a report</p>
                                                    <p>If you make any changes here, click the Plus button to
                                                    save them. Reports with the same name will be overwritten.</p>
                                                    """)
        self.admin_reports_script_lineEdit.setToolTip("""<p>The path to the script of a Report</p>
                                                    <p>If you make any changes here, click the Plus button to
                                                    save them. Reports with the same name will be overwritten.</p>
                                                    """)
        self.admin_reports_args_lineEdit.setToolTip("""<p>The command line arguments to the Report script</p>
                                                    <p>If you make any changes here, click the Plus button to
                                                    save them. Reports with the same name will be overwritten.</p>
                                                    <p>You can use $db, which will pass to the report script the full path of the database
                                                     file. This is useful when you want to make sql queries from within the report script.
                                                    You can also use any variable name from the Subjects table preceded by a '$'
                                                    (eg., $SubjN will pass to the report script the subject number of the currently 
                                                    selected subject, $FName is the subject's First Name, etc.). Using any of these
                                                    variables will cause the Report to show up in the list on Browse page (and these
                                                    reports can only be run from there when a subject is selected, since they require individual
                                                    subject data).</p>
                                                    """)
        self.admin_user_listWidget.setToolTip("""<p>The list of User Variables</p>
                                                <p>Add new user variables, or delete unneeded ones here</p>
                                                <p><b>WARNING! Deleting a user variable will
                                                delete all subject data for that variable!</b></p>
                                                <p>You should backup your DB regularly
                                                (either by exporting the data, or by simply
                                                copying the db file to a safe place)</p>
                                                """)
        self.close_pushButton.setToolTip("Close Subject Manager")

        self.admin_init()
        self.add_init()
        self.add_edit_protocol_populate()
        self.edit_user_populate()
        self.edit_load_subject_list()
        self.admin_reports_populate()
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

    #def edit_search_exact_clicked(self, state):
    #    self.edit_load_subject_list()
    #    self.edit_load_subject_data(self.edit_subject_list_comboBox.currentText())

    def edit_load_subject_list(self, search_field=None):
        search_field = unicode(self.edit_search_lineEdit.text())
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        if search_field in [None, '']:
            query = """SELECT SubjN,FName,LName FROM Subjects"""
        else:
        #    if self.edit_search_exact_checkBox.checkState() == QtCore.Qt.Checked:
             query = """SELECT SubjN,FName,LName FROM Subjects WHERE Subjects MATCH '%s'""" % search_field
        #    else:
        #        query = """SELECT SubjN,FName,LName FROM Subjects WHERE Subjects MATCH '%s*'""" % search_field
        c.execute(query)
        self.edit_subject_list_comboBox.clear()
        ind = 0
        for row in c:
            self.edit_subject_list_comboBox.insertItem(ind, QtGui.QIcon("images/user.png"), "%s, %s %s" % (row[0], row[1], row[2]))
            ind += 1
        c.close()
        conn.close()

    def edit_search_back(self):
        index = self.edit_subject_list_comboBox.currentIndex()
        if index > 0:
            index -= 1
        self.edit_subject_list_comboBox.setCurrentIndex(index)
    
    def edit_search_fwd(self):
        index = self.edit_subject_list_comboBox.currentIndex()
        if index < self.edit_subject_list_comboBox.count()-1:
            index += 1
        self.edit_subject_list_comboBox.setCurrentIndex(index)
    
    def edit_load_subject_data(self, info):
        subn = unicode(info.split(", ")[0]).strip()
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute("""SELECT FName,LName,Email,Phone,DOB,Contact,Notes FROM Subjects WHERE SubjN == '%s'""" % subn)
        subject = c.fetchone()
        if subject is not None:
            self.edit_name_label.setText("%s %s" % (subject[0],subject[1]))
            self.edit_email_label.setText("%s" % subject[2])
            self.edit_phone_label.setText("%s" % subject[3])
            self.edit_dob_label.setText("%s" % subject[4])
            self.edit_contact_checkBox.setChecked(bool(subject[5]))
            self.edit_notes_plainTextEdit.setPlainText("%s" % subject[6])
            c.execute("""SELECT Protocol FROM Protocols""")
            protocols = c.fetchall()
            self.edit_subject_protocol_dict = {}
            for protocol in protocols:
                c.execute("""SELECT Protocol_%s FROM Subjects WHERE SubjN == '%s'""" % (protocol[0],subn))
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
                c.execute("""SELECT User_%s FROM Subjects WHERE SubjN == '%s'""" % (var[0],subn))
                uservar_this = c.fetchone()
                if uservar_this[0] is not None:
                    item = QtGui.QTableWidgetItem(uservar_this[0])
                    for i in range(self.edit_user_tableWidget.rowCount()):
                        if var[0] == self.edit_user_tableWidget.item(i,0).text():
                            self.edit_user_tableWidget.setItem(i, 1, item)
                else:
                    item = QtGui.QTableWidgetItem("")
                    for i in range(self.edit_user_tableWidget.rowCount()):
                        if var[0] == self.edit_user_tableWidget.item(i,0).text():
                            self.edit_user_tableWidget.setItem(i, 1, item)
        else:
            self.edit_name_label.setText("")
            self.edit_email_label.setText("")
            self.edit_phone_label.setText("")
            self.edit_notes_plainTextEdit.setPlainText("")
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
            query += "Contact = 'True', "
        else:
            query += "Contact = 'False', "
        query += "Notes = \"%s\"" % self.edit_notes_plainTextEdit.toPlainText()

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
            item.setToolTip(row[0])
            item.setIcon(QtGui.QIcon("images/vcard.png"))
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


    def edit_note_changed(self):
        self.edit_data_changed_label.setVisible(True)

    def edit_data_changed(self, obj):
        self.edit_data_changed_label.setVisible(True)
    
    def edit_reports_click_list(self, item):
        report = item.text()
        self.edit_reports_run(report)
       
    def edit_reports_click_button(self):
        if self.edit_reports_listWidget.currentItem() is not None:
            report = self.edit_reports_listWidget.currentItem().text()
            self.edit_reports_run(report)
    
    def edit_reports_run(self, report):
            conn = sqlite3.connect(self.filename)
            c = conn.cursor()
            c.execute("""SELECT Path, Args FROM Reports WHERE Name == '%s'""" % report)
            ret = c.fetchone()
            args = ret[1].split(" ")
            subjn = unicode(self.edit_subject_list_comboBox.currentText().split(", ")[0]).strip()
            data = "SubjN,FName,LName,DOB,Today,Gender,Email,Phone,Race,EthnicID,Contact"
            datal = data.split(",")
            c.execute("""SELECT %s FROM Subjects WHERE SubjN == '%s'""" % (data, subjn))
            rets = c.fetchone()
            c.close()
            conn.close()
            for i in range(len(args)):
                args[i] = args[i].replace("$db", os.path.abspath(self.filename))
                for dat,var in zip(datal,rets):
                    args[i] = args[i].replace("$%s" % dat, var)
            sys.argv = args
            execfile(ret[0])

    def admin_init(self):
        Config = ConfigParser.ConfigParser()
        if self.filename == "":
            self.filename = 'Subjects.db'
        if not os.path.isfile(self.configFilePath):
            Config.add_section('database')
            Config.set('database','path',self.filename)
            fh = open(self.configFilePath, 'w')
            Config.write(fh)
            fh.close()
        Config.read(self.configFilePath)
        Config.set('database','path',self.filename)
        fh = open(self.configFilePath, 'w')
        Config.write(fh)
        fh.close()
        
        if not os.path.isfile(self.filename):
            self.admin_create_db()
        self.filePath_label.setText(self.filename)
        
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute("""SELECT Protocol FROM Protocols""")
        self.admin_protocols_listWidget.clear()
        for row in c:
            item = QtGui.QListWidgetItem(row[0])
            item.setIcon(QtGui.QIcon("images/table.png"))
            item.setFlags( QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled )
            self.admin_protocols_listWidget.insertItem(-1, item)
        c.execute("""SELECT UserVar FROM UserVars""")
        self.admin_user_listWidget.clear()
        for row in c:
            item = QtGui.QListWidgetItem(row[0])
            item.setIcon(QtGui.QIcon("images/vcard.png"))
            item.setFlags( QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled )
            self.admin_user_listWidget.insertItem(-1, item)
        c.close()
        conn.close()

    def admin_create_db(self):
        ret = self.get_newfile(title = 'Enter new filename to create:', file_types = "SQLite DB Files (*.db);;All files (*.*)")
        if ret != '':
            qry = open('New_DB_Schema.sql', 'r').read()
            conn = sqlite3.connect(ret)
            c = conn.cursor()
            c.executescript(qry)
            conn.commit()
            c.close()
            conn.close()
            self.filename = ret
            self.add_init()
            self.add_edit_protocol_populate()
            self.edit_user_populate()
            self.admin_init()

    def admin_open_db(self):
        ret = self.get_newfile(title = 'Select existing DB file to open:', file_types = "SQLite DB Files (*.db);;All files (*.*)")
        if ret != '':
            self.filename = ret
            self.add_init()
            self.add_edit_protocol_populate()
            self.edit_user_populate()
            self.admin_init()

    def admin_export_schema(self):
        ret = self.get_newfile(title = 'Enter a new SQL filename to save data to:', file_types = "SQL Files (*.sql);;All files (*.*)")
        if ret != '':
            conn = sqlite3.connect(self.filename);
            c = conn.cursor();
            c.execute("""SELECT name FROM sqlite_master WHERE type = 'table'""")
            tables = c.fetchall()
            c.close()
            skip = ['sqlite_sequence', 'Subjects_content', 'Subjects_segments', 'Subjects_segdir']
            fh = open(ret,'w')
            now = datetime.datetime.now()
            fh.write("-- Subject Manager database dump; db version %s\n-- This file was created at %s on %s\n\nBEGIN TRANSACTION;\n\n" % 
                                                                        (self.version, now.strftime("%H:%M"), now.strftime("%Y-%m-%d")))
            fh.close()
            for table in tables:
                if table[0] not in skip:
                    with open(ret, 'a') as f:
                        for line in self.sqlite_table_dump(conn, table[0]):
                            f.write('%s\n' % line)
                        f.write('\n')
            fh = open(ret,'a')
            fh.write('COMMIT;\n')
            fh.close()
            conn.close()

    def admin_import_schema(self):
        ret = self.get_newfile(title = 'Select SQL file to load from:', file_types = "SQL Files (*.sql);;All files (*.*)")
        if ret != '':
            confirm = self.get_yesno(title = 'Subject Manager', prompt = 'WARNING!\n\nThis will overwrite all data and cannot be undone!\nMake sure you have backed up your database!\nAre you sure you want to continue?:')
            if confirm:
                os.remove(self.filename)
                qry = open(ret, 'r').read()
                conn = sqlite3.connect(self.filename)
                c = conn.cursor()
                c.executescript(qry)
                conn.commit()
                c.close()
                conn.close()
                self.filePath_label.setText(self.filename)
                self.add_init()
                self.add_edit_protocol_populate()
                self.edit_user_populate()
                self.edit_load_subject_list()
                self.admin_init()
            
    
    def admin_protocols_add(self):
        ret = self.get_input(title = 'Subject Manager', prompt = 'Enter a protocol name.\nSpaces will be replaced with _')
        if ret != '':
            ret = ret.replace(" ","_")
            item_a = QtGui.QListWidgetItem(ret)
            item_a.setIcon(QtGui.QIcon("images/chart_pie.png"))
            item_a.setFlags( QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled )
            self.admin_protocols_listWidget.insertItem(-1, item_a)
            #self.admin_protocols_listWidget.insertItem(-1, ret)
            conn = sqlite3.connect(self.filename);
            c = conn.cursor();
            c.execute("""INSERT INTO Protocols (Protocol) VALUES ('%s')""" % ret)
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
                c.execute("""Delete from Protocols where Protocol == '%s'""" % val)
                c.close()
                conn.commit()
                conn.close()
                item = self.admin_protocols_listWidget.takeItem(self.admin_protocols_listWidget.currentRow())
                item = None
                self.sqlite_column_delete(self.filename, 'Subjects', 'Protocol_%s' % val)
                self.add_edit_protocol_populate()

    def admin_reports_run_buttonclick(self):
        if self.admin_reports_listWidget.currentItem() is not None:
            self.admin_reports_run(self.admin_reports_listWidget.currentItem())

    def admin_reports_run_listclick(self, item):
        self.admin_reports_run(item)

    def admin_reports_run(self, item):
        val = item.text()
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute("""SELECT Path, Args FROM Reports where Name == '%s'""" % val)
        ret = c.fetchone()
        c.close()
        conn.close()
        args = ret[1].split(" ")
        data = "SubjN,FName,LName,DOB,Today,Gender,Email,Phone,Race,EthnicID,Contact"
        datal = ["$%s" % i for i in data.split(",")]
        subj = False
        for arg in args:
            if arg in datal:
                subj = True
                break
        if not subj:
            for i in range(len(args)):
                args[i] = args[i].replace("$db", os.path.abspath(self.filename))
            import sys
            sys.argv = args
            execfile(ret[0])
        else:
            print "This report appears to require individual subject information, and thus should be run from the 'Browse' tab with the desired subject selected"
            
    def admin_reports_populate(self):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute("""SELECT Name, Args FROM Reports""")
        self.admin_reports_listWidget.clear()
        self.edit_reports_listWidget.clear()
        #self.add_protocol_comboBox.clear()
        for row in c:
            #if  (os.path.isfile(row[1])):
            item_a = QtGui.QListWidgetItem(row[0])
            item_a.setIcon(QtGui.QIcon("images/page_chart.png"))
            item_a.setFlags( QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled )
            self.admin_reports_listWidget.insertItem(-1, item_a)
            args = row[1].split(" ")
            data = "SubjN,FName,LName,DOB,Today,Gender,Email,Phone,Race,EthnicID,Contact"
            datal = ["$%s" % i for i in data.split(",")]
            subj = False
            for arg in args:
                if arg in datal:
                    subj = True
                    break
            if subj:
                item_e = QtGui.QListWidgetItem(row[0])
                item_e.setIcon(QtGui.QIcon("images/page_chart.png"))
                item_e.setFlags( QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled )
                self.edit_reports_listWidget.insertItem(-1, item_e)
            #self.edit_reports_listWidget.item(0).setSelected(True)
        c.close()
        conn.close()
        
    def admin_reports_selected(self):
        if self.admin_reports_listWidget.currentItem() is not None:
            val = self.admin_reports_listWidget.currentItem().text()
            conn = sqlite3.connect(self.filename)
            c = conn.cursor()
            c.execute("""SELECT Name, Path, Args FROM Reports where Name == '%s'""" % val)
            row = c.fetchone()
            self.admin_reports_name_lineEdit.setText(row[0])
            self.admin_reports_script_lineEdit.setText(row[1])
            self.admin_reports_args_lineEdit.setText(row[2])
    
    def admin_reports_add(self):
        if (self.admin_reports_name_lineEdit.text() != '') and (self.admin_reports_script_lineEdit.text() != '') and (os.path.isfile(self.admin_reports_script_lineEdit.text())):
            ret_name = unicode(self.admin_reports_name_lineEdit.text()).replace(" ","_")
            ret_path = unicode(self.admin_reports_script_lineEdit.text())
            ret_args = unicode(self.admin_reports_args_lineEdit.text())
            conn = sqlite3.connect(self.filename);
            c = conn.cursor();
            c.execute("""Delete from Reports where Name == '%s'""" % ret_name)
            c.execute("""INSERT INTO Reports (Name, Path, Args) VALUES ('%s', '%s', '%s')""" % (ret_name,ret_path,ret_args))
            conn.commit()
            c.close()
            conn.close()
            self.admin_reports_populate()

    def admin_reports_remove(self):
        if self.admin_reports_listWidget.currentItem() is not None:
            val = self.admin_reports_listWidget.currentItem().text()
            ret = self.get_yesno(title = 'Subject Manager', prompt = 'Confirm!\nAre you sure you want to remove report:\n\n' + val)
            if ret:
                conn = sqlite3.connect(self.filename)
                c = conn.cursor()
                c.execute("""Delete from Reports where Name == '%s'""" % val)
                c.close()
                conn.commit()
                conn.close()
                item = self.admin_reports_listWidget.takeItem(self.admin_protocols_listWidget.currentRow())
                item = None
                self.admin_reports_populate()
                
    def admin_reports_script_browse(self):
        ret = self.get_file(title = 'Subject Manager', default_dir = "", file_types = "Python Scripts (*.py)")
        if ret != '':
            self.admin_reports_script_lineEdit.setText(ret)

    def admin_user_add(self):
        ret = self.get_input(title = 'Subject Manager', prompt = 'Enter a user variable name with letters and numbers only.\nSpaces will be replaced with _')
        if ret != '':
            ret = ret.replace(" ","_")
            item = QtGui.QListWidgetItem(ret)
            item.setIcon(QtGui.QIcon("images/vcard.png"))
            item.setFlags( QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled )
            self.admin_user_listWidget.insertItem(-1, item)
            #self.admin_user_listWidget.insertItem(-1, ret)
            conn = sqlite3.connect(self.filename);
            c = conn.cursor();
            c.execute("""INSERT INTO UserVars (UserVar) VALUES ('%s')""" % ret)
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
                c.execute("""Delete from UserVars where UserVar == '%s'""" % val)
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
        c.execute("""SELECT MAX(CAST(SubjN AS Int)) FROM Subjects""");
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
        c.execute("""INSERT INTO Subjects ('%s') VALUES ('%s')""" % ("','".join(query_columns_list), "','".join(query_vals_list)))
        conn.commit()
        c.close()
        conn.close()
        self.add_init()
        self.edit_load_subject_list()

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

    def get_input(parent=None, title = 'User Input', prompt = 'Enter a value:', default=''):
        """Opens a simple prompt for user input, returns a string
        """
        if QtGui.QApplication.startingUp():
            app = QtGui.QApplication([])
        sys.stdout = None
        ret, ok = QtGui.QInputDialog.getText(parent, title, prompt, QtGui.QLineEdit.Normal, default)
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
        col_create_list = []
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


    def sqlite_table_dump(self, connection, table_name):
        """
        Returns an iterator to the dump of the database in an SQL text format.

        Used to produce an SQL dump of the database.  Useful to save an in-memory
        database for later restoration.  This function should not be called
        directly but instead called from the Connection method, iterdump().
        
        Author: Paul Kippes <kippesp@gmail.com>
        """

        cu = connection.cursor()
        table_name = table_name

        #yield('BEGIN TRANSACTION;')

        # sqlite_master table contains the SQL CREATE statements for the database.
        q = """
           SELECT name, type, sql
            FROM sqlite_master
                WHERE sql NOT NULL AND
                type == 'table' AND
                name == :table_name
            """
        schema_res = cu.execute(q, {'table_name': table_name})
        for table_name, type, sql in schema_res.fetchall():
            if table_name == 'sqlite_sequence':
                yield('DELETE FROM sqlite_sequence;')
            elif table_name == 'sqlite_stat1':
                yield('ANALYZE sqlite_master;')
            elif table_name.startswith('sqlite_'):
                continue
            else:
                yield('%s;' % sql)

            # Build the insert statement for each row of the current table
            res = cu.execute("PRAGMA table_info('%s')" % table_name)
            column_names = [str(table_info[1]) for table_info in res.fetchall()]
            q = "SELECT 'INSERT INTO \"%(tbl_name)s\" VALUES("
            q += ",".join(["'||quote(" + col + ")||'" for col in column_names])
            q += ")' FROM '%(tbl_name)s'"
            query_res = cu.execute(q % {'tbl_name': table_name})
            for row in query_res:
                yield("%s;" % row[0])

        # Now when the type is 'index', 'trigger', or 'view'
        #q = """
        #    SELECT name, type, sql
        #    FROM sqlite_master
        #        WHERE sql NOT NULL AND
        #        type IN ('index', 'trigger', 'view')
        #    """
        #schema_res = cu.execute(q)
        #for name, type, sql in schema_res.fetchall():
        #    yield('%s;' % sql)

        #yield('COMMIT;')


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = SubjectManager(None)
    if len(sys.argv)>1:
        form.select_tab(sys.argv[1])
    app.exec_()
