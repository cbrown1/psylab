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
        followed by a period, followed by the output of socket.gethostname 
        (the machine name).
        
        There is no write or save functionality, which is by design. The 
        intention is for the user to create the config file by hand.

        There are several functions for getting various types of data. But 
        get_str always works, since that is how all data are stored in the file.
        Lists of ints or floats are assumed to be comma-separated
        Booleans [case-insensitive] should be (from the ConfigParser docs):
        either ['1', 'yes', 'true', 'on'] or ['0', 'no', 'false', 'off']
        
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
        """Returns the identifier for the current machine (the identifier 
            returned is the one generated, it is not read from the config file)
        """
        return self.machine

    def get_machines(self):
        """Returns all machine identifiers in file
        """
        return self.Conf.sections()

    def get_conf_filename(self):
        """Returns the name of the configuration file
        """
        #return os.path.realpath(self.conf_file)
        return self.conf_file

    def get_keys(self):
        """Returns a list containing all of the keys for this machine
        """
        return [key[0] for key in self.Conf.items(self.machine)]
#        keys = []
#        for item in self.Conf.items(self.machine):
#            keys.append(item[0])
#        return keys

    def get_keyvals(self):
        """Returns a list containing all of the key-value tuples for this machine
        """
        return self.Conf.items(self.machine)

    def get_str(self, var):
        """Returns the value of the specified key, as a string
        """
        return self.Conf.get(self.machine, var)
    
    def get_bool(self, var):
        """Returns the value of the specified key, as a boolean
        """
        return self.Conf.getboolean(self.machine, var)
    
    def get_path(self, var):
        """Returns the value of the specified key, as an expanded path
        """
        return os.path.expanduser(self.Conf.get(self.machine, var))
    
    def get_list_int(self,var):
        """Returns the value of the specified key, as a list of ints
        """
        ret = self.Conf.get(self.machine, var)
        return [int(i) for i in ret.split(',')]

    def get_list_float(self,var):
        """Returns the value of the specified key, as a list of floats
        """
        ret = self.Conf.get(self.machine, var)
        return [float(i) for i in ret.split(',')]

    def get_int(self,var):
        """Returns the value of the specified key, as an int
        """
        return int(self.Conf.get(self.machine, var))

    def get_float(self,var):
        """Returns the value of the specified key, as a float
        """
        return float(self.Conf.get(self.machine, var))
