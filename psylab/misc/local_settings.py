# -*- coding: utf-8 -*-

# Copyright (c) 2014 Christopher Brown
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

import os
import socket
try:
    # Python2
    import ConfigParser
except ImportError:
    # Python3
    import configparser as ConfigParser

class local_settings:
    """A simple class for retrieving machine-specific settings info from ini files

        Uses ConfigParser to read settings file, which should look something like:
        
            [posix.shrsft163.shrs.pitt.edu]
            name=Chris''s Office
            audio_id =0,0,2
            workdir=~/Copy/Python
            stimdir=~/Copy/Lab/stim
            
            [posix.shrsft129.shrs.pitt.edu]
            name=Right Booth
            audio_id=7,7,8
            workdir=~/Copy/Python
            stimdir=~/Copy/Lab/stim

        ...where each section name should consist of os.name ('posix' or 'nt')
        followed by a period, followed by socket.gethostname (machine name)

        There are several functions for getting various types of data. But 
        get_str always works, since that is how all data are stored in the file.
        Lists of ints or floats are assumed to be comma-separated
        
        Example usage:
        
        import local_settings
        machine = local_settings.local_settings()
        name = machine.get_str('name')

    """
    def __init__(self, conf_file=None, machine=None):
        if conf_file:
            self.conf_file = conf_file
        else:
            self.conf_file = 'psylab.conf'
        
        if machine:
            self.machine = machine
        else:
            self.machine = os.name + "." + socket.gethostname()
        self.Conf = ConfigParser.ConfigParser()
        self.Conf.read(self.conf_file)

    def get_machine(self):
        return self.machine

    def get_keys(self):
        keys = []
        for item in self.Conf.items(self.machine):
            keys.append(item[0])
        return keys

    def get_str(self, var):
        return self.Conf.get(self.machine, var)
    
    def get_path(self, var):
        return os.path.expanduser(self.Conf.get(self.machine, var))
    
    def get_list_int(self,var):
        ret = self.Conf.get(self.machine, var)
        return [int(i) for i in ret.split(',')]

    def get_list_float(self,var):
        ret = self.Conf.get(self.machine, var)
        return [float(i) for i in ret.split(',')]

    def get_int(self,var):
        return int(self.Conf.get(self.machine, var))

    def get_float(self,var):
        return float(self.Conf.get(self.machine, var))
