# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 16:42:30 2010

@author: cabrown4
"""

import serial

def set_atten(com='COM1', dev=1, atten=0):

    #  temp = (unsigned int)(Level*10.0+0.05);
    #  cmd[0] = PA4_ATT;
    #  cmd[1] = temp >> 8;
    #  cmd[2] = temp;
    #    Result = xbusSendCmdData ( port, DevLocNum, &cmd[0], 3, heiPA4MsTimeout);      

    s = serial.Serial(com, baudrate=38400, timeout=1)
    
    d = chr(3+dev) # device ID's start at 4
    
    c = chr(0x20)  # command for set atten
    
    hb = chr(0x03) # high byte of atten*10
    
    lb = chr(0xE7) # low byte of atten*10
    
    cs = chr(0x0A) # Checksum of 
    
    # set dev 5 (Rack 1, position 2) to 99.9:
    command = d+c+hb+lb+cs
    command = chr(0x05)+chr(0x44)+chr(0x20)+chr(0x03)+chr(0xE7)+chr(0x0A)
    s.write(command)
    
