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

-- The main table, to hold subject info. New fields will be added as needed
-- for Protocols (a default is created here) and custom vars
CREATE TABLE "Subjects" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "SubjN" INTEGER,
    "FName" TEXT,
    "LName" TEXT,
    "DOB" TEXT,
    "Today" TEXT,
    "Gender" TEXT,
    "Email" TEXT,
    "Phone" TEXT,
    "Race" TEXT,
    "EthnicID" TEXT,
    "Contact" TEXT,
    "Protocol_Default" TEXT
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
CREATE TABLE "CustomVars" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "CustomVar" TEXT
);

-- A table to hold any database admin data
CREATE TABLE "Admin" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT,
    "Value" TEXT
);
INSERT INTO Admin (Name,Value) VALUES ('version','0.1');
