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

import sys, os
import time

class joystick():
    """Class to access joystick data on linux with no dependencies
        
        You will need to find the values for your hardware.
        
        Example
        -------
        >>> j = joystick()
        >>> def get_j1axh_until_b2(): # Return Horz axis value of j1 when b2 is pressed
                wait = True
                while wait:
                    c,e,d = j.listen()
                    if c == "Joystick" and e == "1 Horz":
                        # Gather horizontal axis data from joystick 1
                        print d
                        data = d
                    elif c == "Button" and e == "2" and d == "0":
                        # Wait until button 2 is released
                        wait=False
                return data
        >>> ret = get_j1axh_until_b2()
        
        Notes
        -----
        Adapted from http://blog.flip-edesign.com/?p=62
        
        Dependencies
        ------------
        linux OS
    """
    known_devices =  {'/dev/input/by-id/usb-Gravis_Eliminator_AfterShock-event-joystick':
                       {
                        'name' : "Gravis Eliminator Aftershock",
                        'control_types' : {'01': "Button",
                                           '03': "Joystick"
                                          },
                        'control_ids' :   {'00': '1 Horz', # Joysticks
                                           '01': '1 Vert',
                                           '02': '2 Vert',
                                           '03': '3 Vert',
                                           '05': '2 Horz',
                                           '07': '3 Horz',
                                           '30': '1', # Buttons
                                           '31': '2',
                                           '32': '3',
                                           '33': '4',
                                           '34': '5',
                                           '35': '6',
                                           '36': '7',
                                           '37': '8',
                                           '38': '9',
                                           '39': '10'
                                          },
                       },
                   }
    def __init__(self, device=None):
        if device:
            self.dev_name = device
        else:
            self.device = None
            for dev in self.known_devices.keys():
                if os.path.exists(dev):
                    self.dev_name = dev
                    break
            if not self.dev_name:
                raise Exception, "No valid devices found!"
        self.device = self.known_devices[self.dev_name]
        self.name = self.device['name']
        self.n_joysticks = 0
        self.n_buttons = 0
        for key,val in self.device['control_ids'].items():
            if len(val) <= 2:
                self.n_buttons += 1
            elif val[-4:] == 'Horz':
                self.n_joysticks += 1

    def calibrate_axis(self, control_id):
        """ Simple calibration routine for a specified joystick axis."

            Returns the min, max, and center values, in that order.

            Example
            -------
            ret = j.calibrate_axis('1 Horz')
        """
        ev = []
        wait = True
        ax_min = 255
        ax_max = 0
        for key, val in self.device['control_types'].items():
            if val == 'Joystick':
                j_id = key
            if val == "Button":
                b_id = key
        for key, val in self.device['control_ids'].items():
            if val == control_id:
                c_id = key
            if val == "1":
                b1_id = key
        if not c_id:
            raise Exception, "Not a valid control_id!"
        else:
            if control_id[-4:] == "Horz":
                direction = "left and right"
            else:
                direction = "up and down"
            print("Move {} {}, then return to center and press button {} when finished").format(control_id, direction, "1")
            pipe = open(self.dev_name, 'r')
            while wait:
                for character in pipe.read(1):
                    ev.append( '{:02X}'.format(ord(character)) )
                if len(ev) == 8:
                    if ev[0] in self.device['control_types'].keys():
                        if ev[0] == j_id and ev[2] == c_id:
                            data = int(ev[4], 16)
                            ax_min = min(ax_min, data)
                            ax_max = max(ax_max, data)
                        elif ev[0] == b_id and ev[2] == b1_id and ev[4] == '00':
                            wait = False
                    ev = []
            pipe.close()
            return (ax_min, ax_max, data)

    def debug(self, dur=15, verbose=False):
        print("debug will run for specified secs and print all joystick activity")
        start = time.time()
        ev = []
        pipe = open(self.dev_name, 'r')
        while time.time() - start < dur:
            for character in pipe.read(1):
                ev.append( '{:02X}'.format(ord(character)) )
                if len(ev) == 8:
                    if verbose:
                        print ev
                    else:
                        if ev[0] in self.device['control_types'].keys():
                            print("Control type: {} | Control id: {} | Data: {}".format(ev[0], ev[2], ev[4]))
                    ev = []
        pipe.close()


    def listen(self):
        """Returns state change info of the device
            
            Returns
            -------
            control_type : str
                The control type that changed (ie, Joystick or Button)
            control_id : str
                The identifier of the control that changed
                For Buttons, it will be the button number starting with 1
                For Joysticks, it will be the joystick number, followed 
                by a space, folowed by the axis along which the change occurred.
                Eg, "2 Horz" or "3 Vert"
            data : int
                The state of the change.
                For buttons, 1 = Down; 0 = Up
                For joysticks, it will be an int 0 <= 255, where 127 is roughly 
                centered, 0 is all the way to the left (or up), and 255 is fully 
                right (or down)
        """
        ev = []
        wait = True
        pipe = open(self.dev_name, 'r')
        while wait:
            for character in pipe.read(1):
                ev.append( '{:02X}'.format(ord(character)) )
            if len(ev) == 8:
                if ev[0] in self.device['control_types'].keys():
                    control_type = self.device['control_types'][ ev[0] ]
                    if ev[2] in self.device['control_ids'].keys():
                        control_id = self.device['control_ids'][ ev[2] ]
                        data = int(ev[4], 16)
                        wait = False
                    else:
                        # This shouldn't happen
                        ev = []
                else:
                    ev = []
        pipe.close()
        return (control_type, control_id, data)
