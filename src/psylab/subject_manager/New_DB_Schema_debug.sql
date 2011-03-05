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
CREATE TABLE "CustomVars" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "CustomVar" TEXT
);
INSERT INTO "CustomVars" VALUES(1,'AUDIO125');
INSERT INTO "CustomVars" VALUES(2,'AUDIO250');
INSERT INTO "CustomVars" VALUES(4,'AUDIO500');
INSERT INTO "CustomVars" VALUES(5,'AUDIO750');
INSERT INTO "CustomVars" VALUES(6,'AUDIO1000');
INSERT INTO "CustomVars" VALUES(7,'AUDIO1500');
INSERT INTO "CustomVars" VALUES(8,'AUDIO2000');
INSERT INTO "CustomVars" VALUES(9,'AUDIO3000');
INSERT INTO "CustomVars" VALUES(10,'AUDIO4000');
INSERT INTO "CustomVars" VALUES(11,'AUDIO6000');
INSERT INTO "CustomVars" VALUES(12,'AUDIO8000');
CREATE VIRTUAL TABLE "Subjects" USING FTS3(ID,SubjN,FName,LName,DOB,Today,Gender,Email,Phone,Race,EthnicID,Contact,Protocol_Binaural,Protocol_Reverb,Protocol_EAS,Custom_AUDIO125,Custom_AUDIO250,Custom_AUDIO500,Custom_AUDIO750,Custom_AUDIO1000,Custom_AUDIO1500,Custom_AUDIO2000,Custom_AUDIO3000,Custom_AUDIO4000,Custom_AUDIO6000,Custom_AUDIO8000);
INSERT INTO "Subjects" VALUES(NULL,'1','John','Smith','1955-02-15','2011-03-04','Male','john.smith@hotmail.com','123-456-7890','White','Not Hispanic','True',NULL,'2011-03-04',NULL,'0','0','5','10','10','20','15','20','25','25','30');
INSERT INTO "Subjects" VALUES(NULL,'2','Mary','Jones','1965-10-22','2011-03-04','Female','mary.jones@yahoo.com','111-222-3333','Black','Hispanic/Latino','True','2011-03-04',NULL,NULL,'0','0','0','5','0','5','5','10','5','5','10');
CREATE TABLE "Admin" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT,
    "Value" TEXT
);
INSERT INTO "Admin" VALUES(1,'version','0.1');
COMMIT;
