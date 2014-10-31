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
import select
import time
import numpy as np

class joystick():
    """Class to access joystick data on linux with no dependencies
        
        You will need to find the values for your hardware. You can use 
        joystick.debug to help. 
        
        This approach will only work with older-style joysticks. It does not 
        work with xinput and perhaps some other newer types. If it shows up
        in /dev/input/by-id/, it should work. 
        
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
    known_devices =  {
                        '/dev/input/by-id/usb-Gravis_Eliminator_AfterShock-event-joystick':
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
                                           '39': '10',
                                          },
                                              # H-Low, H-Hi, H-C, V-Lo, V-Hi, V-C
                        'joystick_cal' : {'1': (12,    232,  122, 17,   232,  127),
                                          '2': (12,    232,  112, 7,    232,  132),
                                          '3': (0,     255,  127, 0,    255,  127),
                                         },
                       },
                       
                        '/dev/input/by-id/usb-Microntek_USB_Joystick-event-joystick':
                        {
                        'name' : "USB Gamepad",
                        'control_types' : {'01': "Button",
                                           '03': "Joystick"
                                          },
                        'control_ids' :   {'00': '1 Horz', # Joysticks
                                           '01': '1 Vert',
                                           '02': '2 Horz',
                                           '05': '2 Vert',
                                           '10': '3 Horz',
                                           '11': '3 Vert',
                                           '20': '1', # Buttons
                                           '21': '2',
                                           '22': '3',
                                           '23': '4',
                                           '24': '5',
                                           '25': '6',
                                           '26': '7',
                                           '27': '8',
                                           '28': '9',
                                           '29': '10',
                                           '2A': '11',
                                           '2B': '12',
                                          },
                        'joystick_cal' : None, 
                       },
                       '/dev/input/by-id/usb-retronicdesign.com_Paddles_Retro_Adapter_v3.0_000000-event-joystick':
                       {
                        'name' : "Atari 2600 Paddles",
                        'control_types' : {'01': "Button",
                                           '03': "Joystick"
                                          },
                        'control_ids' :   {'00': '1 Horz', # Joysticks
                                           '01': '2 Horz',
                                           '20': '1', # Buttons
                                           '28': '2',
                                          },
                        'joystick_cal' : None, #Paddles seem to work better without calibration
                       },
                       '/dev/input/by-id/usb-retronicdesign.com_Retro_Joystick_Adapter_v3.0_000000-event-joystick':
                       {
                        'name' : "Atari 2600 Joystick",
                        'control_types' : {'01': "Button",
                                           '03': "Joystick"
                                          },
                        'control_ids' :   {'00': '1 Horz', # Joysticks
                                           '01': '2 Horz',
                                           '20': '1', # Buttons
                                           '28': '2',
                                          },
                        'joystick_cal' : None, #Paddles seem to work better without calibration
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
        self.joystick_cal = self.device['joystick_cal']
        self.n_joysticks = 0
        self.n_buttons = 0
        self.pipe = None
        for key,val in self.device['control_types'].items():
            if val == 'Joystick':
                self.id_joystick = key
            elif val == 'Button':
                self.id_button = key
        for key,val in self.device['control_ids'].items():
            if len(val) <= 2:
                self.n_buttons += 1
            elif val[-4:] == 'Horz':
                self.n_joysticks += 1


    def calibrate_joystick(self, joystick=1):
        """ Simple calibration routine for the specified joystick.
        
            Returns the calibration data as a tuple, and also stores and uses 
            it (cal data are applied by default).

            Returns
            -------
            h_min : int
                The horizontal axis minimum (left-most)
            h_max : int
                The horizontal axis maximum (right-most)
            h_center : int
                The horizontal axis center
            v_min : int
                The vertical axis minimum (top-most)
            v_max : int
                The vertical axis minimum (bottom-most)
            v_center : int
                The vertical axis center

            Example
            -------
            ret = j.calibrate_joystick(1) # Calibrate joystick 1
        """
        ev = []
        wait = True
        # Data:
        ax_h_cen = None
        ax_h_min = 999
        ax_h_max = -999
        ax_v_cen = None
        ax_v_min = 999
        ax_v_max = -999
        # Get ids for button 1 (for exit) and for the h and v axes of specified joystick
        for key, val in self.device['control_ids'].items():
            if val == "1":
                b1_id = key
            elif len(val) > 2 and val[-4:] in ['Vert', 'Horz']:
                n,ax = val.split(" ")
                if int(n) == int(joystick):
                    if ax == 'Vert':
                        c_js_id_v = key
                    elif ax == 'Horz':
                        c_js_id_h = key
        if not c_js_id_h or not c_js_id_v:
            raise Exception, "Could not find axis info on joystick {}".format(str(joystick))
        else:
            print("Move joystick {} around its perimeter, then return to center and press button {} to end.").format(str(joystick), "1")
            pipe = open(self.dev_name, 'r')
            while wait:
                for character in pipe.read(1):
                    ev.append( '{:02X}'.format(ord(character)) )
                if len(ev) == 8:
                    if ev[0] in self.device['control_types'].keys():
                        if ev[0] == self.id_joystick:
                            if ev[2] == c_js_id_v:
                                ax_v_cen = int(ev[4], 16)
                                ax_v_min = min(ax_v_min, ax_v_cen)
                                ax_v_max = max(ax_v_max, ax_v_cen)
                            elif ev[2] == c_js_id_h:
                                ax_h_cen = int(ev[4], 16)
                                ax_h_min = min(ax_h_min, ax_h_cen)
                                ax_h_max = max(ax_h_max, ax_h_cen)
                        elif ev[0] == self.id_button and ev[2] == b1_id and ev[4] == '00':
                            wait = False
                    ev = []
            pipe.close()
            if ax_h_min ==  999: ax_h_min = None
            if ax_h_max == -999: ax_h_max = None
            if ax_v_min ==  999: ax_v_min = None
            if ax_v_max == -999: ax_v_max = None
            
            self.known_devices[self.dev_name]['joystick_cal'][str(joystick)] = (ax_h_min, ax_h_max, ax_h_cen, ax_v_min, ax_v_max, ax_v_cen)
            return (ax_h_min, ax_h_max, ax_h_cen, ax_v_min, ax_v_max, ax_v_cen)


    def debug(self, dur=15, verbose=False):
        print("debug will run for {:} secs and print all activity on device: {}".format(dur, self.name))
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
        print("debug done")


    def normalize_joystick_data(self, control_id, data):
        """Scales the value in data to the range 0 >= 255, 
            based on the calibration values for the specified control.
        """
        joystick,ax = control_id.split(" ")
        if ax == "Horz":
            id_coeff = -1
        else:
            id_coeff = 2
        minim = float(self.joystick_cal[joystick][(1+id_coeff)])
        maxim = float(self.joystick_cal[joystick][(2+id_coeff)])
        center = float(self.joystick_cal[joystick][3+id_coeff])
        if data > center:
            return np.minimum(int((data / maxim)*(255. - center) + center), 255)
        else:
            return np.maximum(int(((data - minim) / (center - minim)) * center), 0)

    def start(self):
        self.pipe = open(self.dev_name, 'r')
        # remove any pending events
        while 1:
            (r, w, e) = select.select([self.pipe], [], [], 0)
            if not r:
                break
            c = self.pipe.read(8)

    def stop(self):
        self.pipe.close()
        self.pipe = None

    def listen(self, cal=True):
        """Returns state change info of the device
        
            Parameters
            ----------
            cal : bool
                Whether to return normalized (calibrated) joystick data. 
                [default = True]
            
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
        ret = None,None,None
        if not self.pipe:
            self.start()
        (r, w, e) = select.select([self.pipe], [], [], 0)
        if r:
            c = self.pipe.read(8)
            ev = []
            for character in c:
                ev.append( '{:02X}'.format(ord(character)) )
            if ev[0] in self.device['control_types'].keys():
                control_type = self.device['control_types'][ ev[0] ]
                if ev[2] in self.device['control_ids'].keys():
                    control_id = self.device['control_ids'][ ev[2] ]
                    data = int(ev[4], 16)
                    if ev[0] == self.id_joystick and cal and self.device['joystick_cal']:
                        data = self.normalize_joystick_data(control_id, data)
                    ret = (control_type, control_id, data)
                else:
                    # This shouldn't happen
                    ev = []
            else:
                ev = []
        return ret
