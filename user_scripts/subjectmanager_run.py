# -*- coding: utf-8 -*-
"""
subjectmanager_run.py

This script is intended to allow you to run subjectmanager by double clicking on a desktop icon. 
The idea is that you point python to this script, which should be in the directory containing the 
conf file. 

@author: Psylab
"""

import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

import psylab.subject_manager as sm
sm.run()
