/*
An SQL Schema file to create a basic subject database. The `Protocols` table
is intended to hold all of your IRB protocols, so that subjects can be
searched/sorted on that, when it comes time to report. The CustomVars table
is for any additional info you want to store, eg `audio125`, `audio250`, etc.


TO RUN:

import sqlite3
qry = open('New_DB_Schema.sql', 'r').read()
conn = sqlite3.connect('Subjects.db')
c = conn.cursor()
c.executescript(qry)
conn.commit()
c.close()
conn.close()
*/

-- The main table, to hold subject info. Full-text searchable.
-- New fields will be added as needed for Protocols (a default is created
-- here) and custom vars.
CREATE VIRTUAL TABLE "Subjects" USING FTS3(
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "SubjN" INTEGER,
    "FName" TEXT  NOT NULL DEFAULT "",
    "LName" TEXT NOT NULL DEFAULT "",
    "DOB" TEXT NOT NULL DEFAULT "",
    "Today" TEXT NOT NULL DEFAULT "",
    "Gender" TEXT NOT NULL DEFAULT "",
    "Email" TEXT NOT NULL DEFAULT "",
    "Phone" TEXT NOT NULL DEFAULT "",
    "Race" TEXT NOT NULL DEFAULT "",
    "EthnicID" TEXT NOT NULL DEFAULT "",
    "Contact" TEXT NOT NULL DEFAULT "",
    "Protocol_Default" TEXT NOT NULL DEFAULT ""
);

-- NIH 'Race' Categories
CREATE TABLE "Races" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Race" TEXT
);
INSERT INTO Races (Race) VALUES ('White');
INSERT INTO Races (Race) VALUES ('Black');
INSERT INTO Races (Race) VALUES ('Asian');
INSERT INTO Races (Race) VALUES ('Pacific');
INSERT INTO Races (Race) VALUES ('Mixed/Other');

-- NIH 'Ethnic' Categories
CREATE TABLE "EthnicIDs" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "EthnicID" TEXT
);
INSERT INTO EthnicIDs (EthnicID) VALUES ('Not Hispanic');
INSERT INTO EthnicIDs (EthnicID) VALUES ('Hispanic/Latino');
INSERT INTO EthnicIDs (EthnicID) VALUES ('Unknown');

-- NIH 'Ethnic' Categories
CREATE TABLE "Genders" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Gender" TEXT
);
INSERT INTO Genders (Gender) VALUES ('Female');
INSERT INTO Genders (Gender) VALUES ('Male');

-- A table to hold the list of IRB protocols
CREATE TABLE "Protocols" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Protocol" TEXT
);
INSERT INTO Protocols (Protocol) VALUES ('Default');

-- A table to hold any custom user variables
CREATE TABLE "UserVars" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "UserVar" TEXT
);

-- A table to hold any database admin data
CREATE TABLE "Admin" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT,
    "Value" TEXT
);

-- A table to reports Subject is whether it is an individual subject report
CREATE TABLE "Reports" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT,
    "Path" TEXT,
    "Subject" TEXT
);


INSERT INTO Admin (Name,Value) VALUES ('version','0.1');
