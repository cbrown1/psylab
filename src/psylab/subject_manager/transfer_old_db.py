import sqlite3

db_from = r'C:\Documents and Settings\cabrown4\My Documents\subjects.db'
db_to = r'C:\Documents and Settings\cabrown4\My Documents\projects\psylab\src\psylab\subject_manager\Subjects.db'

con1 = sqlite3.connect(db_from)
con2 = sqlite3.connect(db_to)

c1 = con1.cursor()
c2 = con2.cursor()

##                 0  1     2     3     4   5     6      7     8     9    10       11      12        13      14
c1.execute("SELECT ID,SubjN,FName,LName,DOB,Today,Gender,Email,Phone,Race,EthnicID,Consent,Audiogram,Contact,NOTES FROM subjects")

recs = c1.fetchall()

for rec in recs:
    print rec[0]
    if rec[13] == 'Y':
        Contact = 'True'
    else:
        Contact = 'False'
    qry = "INSERT INTO Subjects VALUES(%i,'%s',\"%s\",\"%s\",'%s','%s','%s'," % (rec[0], rec[1], rec[2], rec[3], rec[4], rec[5], rec[6]) 
    
    qry = qry + "'%s','%s','%s','%s','%s',\"%s\",'','','%s'," % (rec[7], rec[8], rec[9], rec[10], Contact, rec[14], rec[11])
    
    qry = qry + "'','','','','','','','','','','','','','','','','','','','','','','%s','');" % rec[12]
    
    c2.execute(qry)
    
con2.commit()

c1.close()
con1.close()

c2.close()
con2.close()
