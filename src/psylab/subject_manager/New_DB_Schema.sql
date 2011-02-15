/* 
An SQL Schema file to create a basic subject database. The `Protocols` table is intended to hold 
all of your IRB protocols, so that each subject can be searched/sorted on that, when it comes time 
to report. 

TO RUN:

import sqlite3
qry = open('New_DB_Schema.sql', 'r').read()
conn = sqlite3.connect('/path/to/db')
c = conn.cursor()
c.executescript(qry)
conn.commit()
c.close()
conn.close()
*/

-- The main table, to hold subject info
CREATE TABLE "Subjects" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "SubjN" INTEGER,
    "Protocol" TEXT,
    "FName" TEXT,
    "LName" TEXT,
    "DOB" TEXT,
    "Today" TEXT,
    "Gender" TEXT,
    "Email" TEXT,
    "Phone" TEXT,
    "Race" TEXT,
    "EthnicID" TEXT,
    "Consent" TEXT,
    "Audiogram" TEXT,
    "IEEE" TEXT,
    "HINT" TEXT,
    "CUNY" TEXT,
    "CID" TEXT,
    "NOTES" TEXT,
    "Contact" TEXT
);

-- A table to hold the list of IRB protocols
CREATE TABLE "Protocols" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Protocol" TEXT
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
