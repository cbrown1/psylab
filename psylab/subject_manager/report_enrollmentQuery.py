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
# along with Psylab.  If not, see <http://www.gnu.org/licenses/>.
#
# Comments and/or additions are welcome. Send e-mail to: cbrown1@pitt.edu.
#

name = "Enrollment"

#import sys
#import datetime
import sqlite3, os, sys
import guidata
guidata.qapplication()
import guidata.dataset.datatypes as dt
import guidata.dataset.dataitems as di

protocols = []

def proc_main(db):
    d = {}
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("""SELECT Protocol FROM Protocols""")
    for row in c:
        protocols.append(row[0])

    class Processing(dt.DataSet):
        """Enrollment Query"""
        global protocols
        start = di.DateItem("Start Date")
        end = di.DateItem("End Date")
        protocol = di.ChoiceItem("Protocol", protocols)
        
    param = Processing()
    param.edit()

    #startdate=r'2010-01-01'
    #enddate = '2010-12-31'
    startdate = str(param.start)
    enddate = str(param.end)
    protocol = protocols[param.protocol]

    c.execute("""SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s'""" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        raise Exception("SQLError: No records found")
    d['all'] = fetch[0]


    ######################################################### GENDER

    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND Gender = 'Male'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['allm'] = 0
    else: 
        d['allm'] = fetch[0]
    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND Gender = 'Female'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['allf'] = 0
    else: 
        d['allf'] = fetch[0]


    ######################################################### ETHNIC (Hispanic, etc)

    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND Gender = 'Male' AND EthnicID = 'Hispanic/Latino'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['allhm'] = 0
    else: 
        d['allhm'] = fetch[0]
    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND Gender = 'Female' AND EthnicID = 'Hispanic/Latino'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['allhf'] = 0
    else: 
        d['allhf'] = fetch[0]

    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND Gender = 'Male' AND EthnicID = 'Not Hispanic'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['allnhm'] = 0
    else: 
        d['allnhm'] = fetch[0]
    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND Gender = 'Female' AND EthnicID = 'Not Hispanic'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['allnhf'] = 0
    else: 
        d['allnhf'] = fetch[0]

    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND Gender = 'Male' AND EthnicID = 'Unknown'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['alluhm'] = 0
    else: 
        d['alluhm'] = fetch[0]
    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND Gender = 'Female' AND EthnicID = 'Unknown'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['alluhf'] = 0
    else: 
        d['alluhf'] = fetch[0]


    ######################################################### RACE - ALL

    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND Gender = 'Male' AND Race = 'White'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['allwm'] = 0
    else: 
        d['allwm'] = fetch[0]
    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND Gender = 'Female' AND Race = 'White'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['allwf'] = 0
    else: 
        d['allwf'] = fetch[0]

    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND Gender = 'Male' AND Race = 'Black'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['allbm'] = 0
    else: 
        d['allbm'] = fetch[0]
    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND Gender = 'Female' AND Race = 'Black'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['allbf'] = 0
    else: 
        d['allbf'] = fetch[0]

    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND Gender = 'Male' AND Race = 'Asian'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['allam'] = 0
    else: 
        d['allam'] = fetch[0]
    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND Gender = 'Female' AND Race = 'Asian'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['allaf'] = 0
    else: 
        d['allaf'] = fetch[0]

    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND Gender = 'Male' AND Race = 'Pacific'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['allpm'] = 0
    else: 
        d['allpm'] = fetch[0]
    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND Gender = 'Female' AND Race = 'Pacific'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['allpf'] = 0
    else: 
        d['allpf'] = fetch[0]

    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND Gender = 'Male' AND Race = 'Native American'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['allnm'] = 0
    else: 
        d['allnm'] = fetch[0]
    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND Gender = 'Female' AND Race = 'Native American'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['allnf'] = 0
    else: 
        d['allnf'] = fetch[0]

    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND Gender = 'Male' AND Race = 'Mixed/Other'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['allmm'] = 0
    else: 
        d['allmm'] = fetch[0]
    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND Gender = 'Female' AND Race = 'Mixed/Other'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['allmf'] = 0
    else: 
        d['allmf'] = fetch[0]


    ######################################################### RACE - WITHIN HISPANIC

    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND EthnicID = 'Hispanic/Latino' AND Gender = 'Male' AND Race = 'White'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['hwm'] = 0
    else: 
        d['hwm'] = fetch[0]
    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND EthnicID = 'Hispanic/Latino' AND Gender = 'Female' AND Race = 'White'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['hwf'] = 0
    else: 
        d['hwf'] = fetch[0]

    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND EthnicID = 'Hispanic/Latino' AND Gender = 'Male' AND Race = 'Black'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['hbm'] = 0
    else: 
        d['hbm'] = fetch[0]
    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND EthnicID = 'Hispanic/Latino' AND Gender = 'Female' AND Race = 'Black'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['hbf'] = 0
    else: 
        d['hbf'] = fetch[0]

    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND EthnicID = 'Hispanic/Latino' AND Gender = 'Male' AND Race = 'Asian'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['ham'] = 0
    else: 
        d['ham'] = fetch[0]
    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND EthnicID = 'Hispanic/Latino' AND Gender = 'Female' AND Race = 'Asian'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['haf'] = 0
    else: 
        d['haf'] = fetch[0]

    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND EthnicID = 'Hispanic/Latino' AND Gender = 'Male' AND Race = 'Pacific'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['hpm'] = 0
    else: 
        d['hpm'] = fetch[0]
    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND EthnicID = 'Hispanic/Latino' AND Gender = 'Female' AND Race = 'Pacific'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['hpf'] = 0
    else: 
        d['hpf'] = fetch[0]

    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND EthnicID = 'Hispanic/Latino' AND Gender = 'Male' AND Race = 'Native American'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['hnm'] = 0
    else: 
        d['hnm'] = fetch[0]
    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND EthnicID = 'Hispanic/Latino' AND Gender = 'Female' AND Race = 'Native American'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['hnf'] = 0
    else: 
        d['hnf'] = fetch[0]

    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND EthnicID = 'Hispanic/Latino' AND Gender = 'Male' AND Race = 'Mixed/Other'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['hmm'] = 0
    else: 
        d['hmm'] = fetch[0]
    c.execute("SELECT COUNT(*) FROM Subjects WHERE Protocol_%s > '%s' AND Protocol_%s <= '%s' AND EthnicID = 'Hispanic/Latino' AND Gender = 'Female' AND Race = 'Mixed/Other'" % (protocol,startdate,protocol,enddate))
    fetch = c.fetchone()
    if fetch == None: 
        d['hmf'] = 0
    else: 
        d['hmf'] = fetch[0]

    c.close()
    conn.close()

    data = "<html><head><style rel='stylesheet' type='text/css'>td{text-align:right;}</style></head><body>\n"
    data += "<h2>Protocol: "+protocol+"</h2>\n"
    data += "<h3>Start Date: "+startdate+"</h3>\n"
    data += "<h3>End Date: "+enddate+"</h3>\n<table>\n"
    data +="<tr><th>&nbsp;</th><th>Female</th><th>Male</th><th>Total</th></tr>\n"
    data += "<tr><td>Hispanic</td><td>"+str(d['allhf'])+"</td><td>"+str(d['allhm'])+"</td><td><em>"+str(d['allhm']+d['allhf'])+"</em></td></tr>\n"
    data += "<tr><td>Not Hisp</td><td>"+str(d['allnhf'])+"</td><td>"+str(d['allnhm'])+"</td><td><em>"+str(d['allnhm']+d['allnhf'])+"</em></td></tr>\n"
    data += "<tr><td>Unknown</td><td>"+str(d['alluhf'])+"</td><td>"+str(d['alluhm'])+"</td><td><em>"+str(d['alluhm']+d['alluhf'])+"</em></td></tr>\n"
    data += "<tr><th>Total</th><td><em>"+str(d['allf'])+"</em></th><td><em>"+str(d['allm'])+"</em></td><td><em>"+str(d['allm']+d['allf'])+"</em></td></tr>\n"
    data += "<tr><td colspan=4>&nbsp;</td>\n"

    data += "<tr><td>Native</td><td>"+str(d['allnf'])+"</td><td>"+str(d['allnm'])+"</td><td><em>"+str(d['allnm']+d['allnf'])+"</em></td></tr>\n"
    data += "<tr><td>Asian</td><td>"+str(d['allaf'])+"</td><td>"+str(d['allam'])+"</td><td><em>"+str(d['allam']+d['allaf'])+"</em></td></tr>\n"
    data += "<tr><td>Pacific</td><td>"+str(d['allpf'])+"</td><td>"+str(d['allpm'])+"</td><td><em>"+str(d['allpm']+d['allpf'])+"</em></td></tr>\n"
    data += "<tr><td>Black</td><td>"+str(d['allbf'])+"</td><td>"+str(d['allbm'])+"</td><td><em>"+str(d['allbm']+d['allbf'])+"</em></td></tr>\n"
    data += "<tr><td>White</td><td>"+str(d['allwf'])+"</td><td>"+str(d['allwm'])+"</td><td><em>"+str(d['allwm']+d['allwf'])+"</em></td></tr>\n"
    data += "<tr><td>Mixed/Other</td><td>"+str(d['allmf'])+"</td><td>"+str(d['allmm'])+"</td><td><em>"+str(d['allmm']+d['allmf'])+"</em></td></tr>\n"
    data += "<tr><th>Total</th><td><em>"+str(d['allf'])+"</em></td><td><em>"+str(d['allm'])+"</em></td><td><em>"+str(d['allm']+d['allf'])+"</em></td></tr>\n"
    data += "<tr><td colspan=4>&nbsp;</td>\n"
    data += "<tr><td colspan=2 align='left'><b>Within Hispanic</b></td><td colspan=4>&nbsp;</td>\n"

    data += "<tr><td>Native</td><td>"+str(d['hnf'])+"</td><td>"+str(d['hnm'])+"</td><td><em>"+str(d['hnm']+d['hnf'])+"</em></td></tr>\n"
    data += "<tr><td>Asian</td><td>"+str(d['haf'])+"</td><td>"+str(d['ham'])+"</td><td><em>"+str(d['ham']+d['haf'])+"</em></td></tr>\n"
    data += "<tr><td>Pacific</td><td>"+str(d['hpf'])+"</td><td>"+str(d['hpm'])+"</td><td><em>"+str(d['hpm']+d['hpf'])+"</em></td></tr>\n"
    data += "<tr><td>Black</td><td>"+str(d['hbf'])+"</td><td>"+str(d['hbm'])+"</td><td><em>"+str(d['hbm']+d['hbf'])+"</em></td></tr>\n"
    data += "<tr><td>White</td><td>"+str(d['hwf'])+"</td><td>"+str(d['hwm'])+"</td><td><em>"+str(d['hwm']+d['hwf'])+"</em></td></tr>\n"
    data += "<tr><td>Mixed/Other</td><td>"+str(d['hmf'])+"</td><td>"+str(d['hmm'])+"</td><td><em>"+str(d['hmm']+d['hmf'])+"</em></td></tr>\n"
    data += "<tr><th>Total</th><td><em>"+str(d['allhf'])+"</em></td><td><em>"+str(d['allhm'])+"</em></td><td><em>"+str(d['allhm']+d['allhf'])+"</em></td></tr>\n"

    data += "</table></body></html>\n"
    outfile = 'EnrollmentData_%s_%s_%s.html' % (protocol,startdate,enddate)
    f=open(outfile, 'w')
    f.write(data)
    f.close()
    if os.name == "nt":
        os.system(outfile)
    elif os.name == "posix":
        os.system("xdg-open " + outfile)
    elif os.name == "mac":
        os.system("open " + outfile)


if __name__ == "__main__":
    db = sys.argv[0].strip("\"").strip("\'")
    proc_main(db)
    
