/*
# Copyright (c) 2011-2012 Christopher Brown
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
# along with Psylab.  If not, see <http://www.gnu.org/licenses/>.
#
# Bug reports, bug fixes, suggestions, enhancements, or other 
# contributions are welcome. Go to http://code.google.com/p/psylab/ 
# for more information and to contribute. Or send an e-mail to: 
# cbrown1@pitt.edu.
#
*/

/*
An SQL Schema file to create a basic subject database. This is the same 
as the default schema ('New_DB_Schema.spl'), with some example data added 
for debug purposes. 

TO RUN:

import sqlite3
qry = open('New_DB_Schema_debug.sql', 'r').read()
conn = sqlite3.connect('Subjects.db')
c = conn.cursor()
c.executescript(qry)
conn.commit()
c.close()
conn.close()
*/

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE "Races" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Race" TEXT
);
INSERT INTO "Races" VALUES(1,'White');
INSERT INTO "Races" VALUES(2,'Black');
INSERT INTO "Races" VALUES(3,'Asian');
INSERT INTO "Races" VALUES(4,'Pacific');
INSERT INTO "Races" VALUES(5,'Mixed/Other');
CREATE TABLE "EthnicIDs" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "EthnicID" TEXT
);
INSERT INTO "EthnicIDs" VALUES(1,'Not Hispanic');
INSERT INTO "EthnicIDs" VALUES(2,'Hispanic/Latino');
INSERT INTO "EthnicIDs" VALUES(3,'Unknown');
CREATE TABLE "Genders" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Gender" TEXT
);
INSERT INTO "Genders" VALUES(1,'Female');
INSERT INTO "Genders" VALUES(2,'Male');
CREATE TABLE "Protocols" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Protocol" TEXT
);
INSERT INTO "Protocols" VALUES(2,'Binaural');
INSERT INTO "Protocols" VALUES(3,'Reverb');
INSERT INTO "Protocols" VALUES(4,'EAS');
CREATE TABLE "UserVars" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "UserVar" TEXT
);
INSERT INTO "UserVars" VALUES(1,'L125');
INSERT INTO "UserVars" VALUES(2,'L250');
INSERT INTO "UserVars" VALUES(4,'L500');
INSERT INTO "UserVars" VALUES(5,'L750');
INSERT INTO "UserVars" VALUES(6,'L1k');
INSERT INTO "UserVars" VALUES(7,'L15');
INSERT INTO "UserVars" VALUES(8,'L2k');
INSERT INTO "UserVars" VALUES(9,'L3k');
INSERT INTO "UserVars" VALUES(10,'L4k');
INSERT INTO "UserVars" VALUES(11,'L6k');
INSERT INTO "UserVars" VALUES(12,'L8k');
INSERT INTO "UserVars" VALUES(13,'R125');
INSERT INTO "UserVars" VALUES(14,'R250');
INSERT INTO "UserVars" VALUES(15,'R500');
INSERT INTO "UserVars" VALUES(16,'R750');
INSERT INTO "UserVars" VALUES(17,'R1k');
INSERT INTO "UserVars" VALUES(18,'R15');
INSERT INTO "UserVars" VALUES(19,'R2k');
INSERT INTO "UserVars" VALUES(20,'R3k');
INSERT INTO "UserVars" VALUES(21,'R4k');
INSERT INTO "UserVars" VALUES(22,'R6k');
INSERT INTO "UserVars" VALUES(23,'R8k');
INSERT INTO "UserVars" VALUES(24,'Audio_Date');
INSERT INTO "UserVars" VALUES(25,'Audio_Tester');
CREATE VIRTUAL TABLE "Subjects" USING FTS3(
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "SubjN" INTEGER,
    "FName" TEXT NOT NULL,
    "LName" TEXT NOT NULL,
    "DOB" TEXT NOT NULL,
    "Today" TEXT NOT NULL,
    "Gender" TEXT NOT NULL,
    "Email" TEXT NOT NULL,
    "Phone" TEXT NOT NULL,
    "Race" TEXT NOT NULL,
    "EthnicID" TEXT NOT NULL,
    "Contact" TEXT NOT NULL,
    "Notes" TEXT NOT NULL DEFAULT "",
    "Protocol_Binaural" TEXT NOT NULL,
    "Protocol_Reverb" TEXT NOT NULL,
    "Protocol_EAS" TEXT NOT NULL,
    "User_L125" TEXT NOT NULL,
    "User_L250" TEXT NOT NULL,
    "User_L500" TEXT NOT NULL,
    "User_L750" TEXT NOT NULL,
    "User_L1k" TEXT NOT NULL,
    "User_L15" TEXT NOT NULL,
    "User_L2k" TEXT NOT NULL,
    "User_L3k" TEXT NOT NULL,
    "User_L4k" TEXT NOT NULL,
    "User_L6k" TEXT NOT NULL,
    "User_L8k" TEXT NOT NULL,
    "User_R125" TEXT NOT NULL,
    "User_R250" TEXT NOT NULL,
    "User_R500" TEXT NOT NULL,
    "User_R750" TEXT NOT NULL,
    "User_R1k" TEXT NOT NULL,
    "User_R15" TEXT NOT NULL,
    "User_R2k" TEXT NOT NULL,
    "User_R3k" TEXT NOT NULL,
    "User_R4k" TEXT NOT NULL,
    "User_R6k" TEXT NOT NULL,
    "User_R8k" TEXT NOT NULL,
    "User_Audio_Date" TEXT NOT NULL,
    "User_Audio_Tester" TEXT NOT NULL
);

-- A table for reports
CREATE TABLE "Reports" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT,
    "Path" TEXT,
    "Args" TEXT,
    "Subject" TEXT
);
INSERT INTO "Reports" VALUES(NULL,'Audio','report_audiogram.py','$db $SubjN','True');
INSERT INTO "Reports" VALUES(NULL,'Enrollment','report_EnrollmentQuery.py','$db','False');

CREATE TABLE "Admin" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT,
    "Value" TEXT
);
INSERT INTO "Subjects" VALUES(NULL,'1','John','Smith','1955-02-15','2011-03-04','Male','john.smith@hotmail.com','123-456-7890','White','Not Hispanic','True','','','2011-03-04','','5','5','5','10','10','20','15','20','25','25','30', '45','50','60','70','70','80','85','90','-110','-110','-70','2012-02-12','CAB');
INSERT INTO "Subjects" VALUES(NULL,'2','Mary','Jones','1965-10-22','2011-03-04','Female','mary.jones@yahoo.com','111-222-3333','Black','Hispanic/Latino','True','','2011-04-15','','','0','5','5','10','5','5','10','10','20','5','10', '0','0','0','0','5','5','0','10','15','10','5','2012-03-27','KHT');
INSERT INTO "Subjects" VALUES(NULL,'3','Thomas','Jefferson','1743-04-13','2011-03-04','Male','jefferson@whitehouse.gov','456-765-4321','White','Not Hispanic','True','','2012-07-22','','','20','25','25','20','35','45','50','50','45','55','50', '10','20','35','30','35','45','40','40','45','40','45','2011-03-04','KHT');
INSERT INTO "Subjects" VALUES(NULL,'4','Margaret','Thatcher','1743-04-13','2011-03-04','Male','jefferson@whitehouse.gov','456-765-4321','White','Not Hispanic','True','','2012-07-22','','','20','25','25','20','35','45','50','50','45','55','50', '10','20','35','30','35','45','40','40','45','40','45','2011-03-04','KHT');

INSERT INTO "Admin" VALUES(1,'version','0.1');

COMMIT;
