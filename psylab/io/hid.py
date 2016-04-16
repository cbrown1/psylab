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
import yaml
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

    def __init__(self, device=None, devices_file='joystick.yml', timeout=.2):

        js_file = open(devices_file, 'r')
        self.known_devices = yaml.load(js_file)
        self.dev_id = None

        if device:
            for dev in self.known_devices.keys():
                if device == self.known_devices[dev]['name']:
                    self.dev_id = dev
                    break
                elif device == dev:
                    self.dev_id = dev
                    break
                elif device == self.known_devices[dev]['path']:
                    self.dev_id = dev
                    break
                elif (self.known_devices[dev].has_key('nickname') and device == self.known_devices[dev]['nickname']):
                    self.dev_id = dev
                    break
            if not self.dev_id:
                raise Exception("Device not found: {}".format(device))
        else:
            self.device = None
            for dev in self.known_devices.keys():
                if os.path.exists(dev):
                    self.dev_id = dev
                    break
            if not self.dev_id:
                raise Exception("No valid devices found!")
        self.timeout = timeout
        self.device = self.known_devices[self.dev_id]
        self.name = self.device['name']
        self.path = self.device['path']

        if self.device.has_key('cal_min'):
            self.cal_min = self.device['cal_min']
        else:
            self.cal_min = {}
            for key, val in self.device['control_ids'].items():
                if len(val) > 2 and val[-4:] in ['Vert', 'Horz']:
                    self.cal_min[str(key)] = None

        if self.device.has_key('cal_max'):
            self.cal_max = self.device['cal_max']
        else:
            self.cal_max = {}
            for key, val in self.device['control_ids'].items():
                if len(val) > 2 and val[-4:] in ['Vert', 'Horz']:
                    self.cal_max[str(key)] = None

        if not self.device.has_key('cal_has_center'):
            self.device['cal_has_center'] = True
        self.cal_has_center = self.device['cal_has_center']
        if self.device.has_key('cal_center'):
            self.cal_center = self.device['cal_center']
        else:
            self.cal_center = {}
            for key, val in self.device['control_ids'].items():
                if len(val) > 2 and val[-4:] in ['Vert', 'Horz']:
                    self.cal_center[str(key)] = None

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
        c_js_id_h = None
        c_js_id_v = None
        # Data:
        ax_h_min = 999
        ax_h_max = -999
        ax_v_min = 999
        ax_v_max = -999

        ax_h_cen = None
        ax_v_cen = None

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
        if not c_js_id_h and not c_js_id_v:
            raise Exception("Could not find axis info on joystick {}".format(str(joystick)))

        print("Move joystick {} around its perimeter, then return to center and press button {} to end").format(str(joystick), "1")
        pipe = open(self.path, 'r')
        while wait:
            for character in pipe.read(1):
                ev.append( '{:02X}'.format(ord(character)) )
            if len(ev) == 8:
                if ev[0] in self.device['control_types'].keys():
                    if ev[0] == self.id_joystick:
                    	feedback = ""
                        if ev[2] == c_js_id_v:
                            ax_v_min = min(int(ev[4], 16), ax_v_min)
                            ax_v_max = max(int(ev[4], 16), ax_v_max)
                            if self.cal_has_center is not None:
                                ax_v_cen = int(ev[4], 16)
                            feedback += "Vert: ({:}, {:}, {:})  ".format(ax_v_min, ax_v_cen, ax_v_max)
                        elif ev[2] == c_js_id_h:
                            ax_h_min = min(int(ev[4], 16), ax_h_min)
                            ax_h_max = max(int(ev[4], 16), ax_h_max)
                            if self.cal_has_center is not None:
                                ax_h_cen = int(ev[4], 16)
                            feedback += "Horz: ({:}, {:}, {:})  ".format(ax_h_min, ax_h_cen, ax_h_max)
                        if feedback is not "":
                            print(feedback)
                    elif ev[0] == self.id_button and ev[2] == b1_id and ev[4] == '00':
                        wait = False
                ev = []
        pipe.close()
        if ax_h_min ==  999: ax_h_min = None
        if ax_h_max == -999: ax_h_max = None
        if ax_v_min ==  999: ax_v_min = None
        if ax_v_max == -999: ax_v_max = None
        if c_js_id_h:
            self.cal_min[str(c_js_id_h)] = ax_h_min
            self.cal_max[str(c_js_id_h)] = ax_h_max
            print ("Control ID: {:}; min: {}".format(c_js_id_h, ax_h_min))
            print ("Control ID: {:}; max: {}".format(c_js_id_h, ax_h_max))
            if self.cal_has_center:
                self.cal_center[str(c_js_id_h)] = ax_h_cen
                print ("Control ID: {:}; cen: {}".format(c_js_id_h, ax_h_cen))
        if c_js_id_v:
            self.cal_min[str(c_js_id_v)] = ax_v_min
            self.cal_max[str(c_js_id_v)] = ax_v_max
            print ("Control ID: {:}; min: {}".format(c_js_id_v, ax_v_min))
            print ("Control ID: {:}; max: {}".format(c_js_id_v, ax_v_max))
            if self.cal_has_center:
                self.cal_center[str(c_js_id_v)] = ax_v_cen
                print ("Control ID: {:}; cen: {}".format(c_js_id_v, ax_v_cen))

    def debug(self, dur=15, verbose=False):
        print("debug will run for {:} secs and print all activity on device: {}".format(dur, self.name))
        start = time.time()
        ev = []
        pipe = open(self.path, 'r')
        while time.time() - start < dur:
            for character in pipe.read(1):
                ev.append( '{:02X}'.format(ord(character)) )
                if len(ev) == 8:
                    if verbose:
                        print (ev)
                    else:
                        if ev[0] in self.device['control_types'].keys():
#                            ndata = self.normalize_joystick_data(ev[2], int(ev[4], 16))
                            print("Control type: {} | Control id: {} | Data: {}".format(ev[0], ev[2], ev[4]))
                    ev = []
        pipe.close()
        print("debug done")


    def normalize_joystick_data(self, control_id, data):
        """Scales the value in data to the range 0 >= 255, 
            based on the calibration values for the specified control.
        """
        minim = float(self.cal_min[control_id] )
        maxim = float(self.cal_max[control_id] )

        if self.cal_has_center:
            center = float(self.cal_center[control_id] )
            if data > center:
                #print("In: {:} | Out: {:}".format(data, np.minimum(int((data / maxim)*(255. - center) + center), 255)))
                return np.minimum(int((data / maxim)*(255. - center) + center), 255)
            else:
                #print("In: {:} | Out: {:}".format(data, np.maximum(int(((data - minim) / (center - minim)) * center), 0)))
                return np.maximum(int(((data - minim) / (center - minim)) * center), 0)
        else:
            #print("In: {:} | Out: {:}".format(data, np.maximum(int(((data - minim) / (maxim - minim)) * maxim), 0)))
            return np.maximum(int(((data - minim) / (maxim - minim)) * maxim), 0)

    def start(self):
        self.pipe = os.open( self.path, os.O_RDONLY | os.O_NONBLOCK )
#        self.pipe = open(self.path, 'rb', buffering=0)

    def stop(self):
        os.close(self.pipe)
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

        timeout_start = time.time()
        while time.time() - timeout_start < self.timeout:
            try:
                rawdata = os.read(self.pipe, 1024)
            except:
                # No data read
                pass
            else:
                ev = []
                i = 0
                for character in rawdata:
                    ev.append( '{:02X}'.format(ord(character)) )
                    # When we have 8 characters, check if it is a meaningful event
                    if len(ev) == 8:
                        if ev[0] in self.device['control_types'].keys():
                            control_type = self.device['control_types'][ ev[0] ]
                            if ev[2] in self.device['control_ids'].keys():
                                control_id = str(self.device['control_ids'][ ev[2] ])
                                data = int(ev[4], 16)
                                if ev[0] == self.id_joystick and cal and self.cal_min.has_key(control_id) and self.cal_max.has_key(control_id):
                                    data = self.normalize_joystick_data(control_id, data)
                                return control_type, control_id, data
                            else:
                                # This shouldn't happen
                                ev = []
                        else:
                            ev = []
        # Timed out. Return Nones
        return ret

    def get_known_device_names(self):
        ret = []
        for key,val in self.known_devices.iteritems():
            ret.append(val['name'])
        return ret
