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
An SQL Schema file to add audiometric fields to the subject database that are
compatible with the audiogram report.

TO RUN:

import sqlite3
qry = open('DB_Schema_Audiometry.sql', 'r').read()
conn = sqlite3.connect('Subjects.db')
c = conn.cursor()
c.executescript(qry)
conn.commit()
c.close()
conn.close()
*/

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
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

ALTER TABLE "Subjects" ADD COLUMN "User_L125" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_L250" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_L500" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_L750" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_L1k" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_L15" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_L2k" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_L3k" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_L4k" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_L6k" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_L8k" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_R125" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_R250" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_R500" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_R750" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_R1k" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_R15" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_R2k" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_R3k" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_R4k" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_R6k" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_R8k" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_Audio_Date" TEXT NOT NULL;
ALTER TABLE "Subjects" ADD COLUMN "User_Audio_Tester" TEXT NOT NULL;

INSERT INTO "Reports" VALUES(NULL,'Audio','report_audiogram.py','$db $SubjN','True');
INSERT INTO "Reports" VALUES(NULL,'Enrollment','report_EnrollmentQuery.py','$db','False');

COMMIT;
