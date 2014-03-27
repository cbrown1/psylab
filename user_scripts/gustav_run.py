# -*- coding: utf-8 -*-
"""
gustav_run.py

Allows you to run a gustav experiment script by clicking on a desktop icon. 

The command line should look something like:
python2.7 -i /home/User/Python/gustav_run.py /home/User/Python/gustav_exp.py

@author: Psylab
"""

import os, sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))

os.system("python2.7 %s" % sys.argv[1])

