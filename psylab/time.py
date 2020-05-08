# -*- coding: utf-8 -*-

# Copyright (c) 2010-2019 Christopher Brown
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
# contributions are welcome. Go to http://github.com/cbrown1/psylab/ 
# for more information and to contribute. Or send an e-mail to: 
# cbrown1@pitt.edu.
#

import datetime

class timer():
    """ Simple high-precision timer class
        
        Use to easily time blocks of code:
        
        >>> with timer():
                for i in range(1000):
                    for j in range(1000):
                        k = j*i

        0.166001081467
        >>> 
        
        Found at:
        http://mrooney.blogspot.com/2009/07/simple-timing-of-python-code.html
        
        [2019-07-24] Modified to use timestamp functions below instead of time module
    """
    def __enter__(self): self.start = timestamp_us()
    def __exit__(self, *args): print("{:} seconds".format((timestamp_us() - self.start) / 1000000.))


"""
Timing functions taken from https://stackoverflow.com/questions/38319606/how-to-get-millisecond-and-microsecond-resolution-timestamps-in-python

The only changes [CB 2019-07-24] made from version 0.2.0 of that pasted code were to rename the functions as follows:
    - monotic_time -> timestamp_s
    - millis -> timestamp_ms
    - micros -> timestamp_us
    - delay -> wait_ms
    - delayMicroseconds -> wait_us
...and edit the examples

GS_timing.py
-create some low-level Arduino-like millis() (milliseconds) and micros() 
 (microseconds) timing functions for Python 
By Gabriel Staples
http://www.ElectricRCAircraftGuy.com 
-click "Contact me" at the top of my website to find my email address 
Started: 11 July 2016 
Updated: 13 Aug 2016 

History (newest on top): 
20160813 - v0.2.0 created - added Linux compatibility, using ctypes, so that it's compatible with pre-Python 3.3 (for Python 3.3 or later just use the built-in time functions for Linux, shown here: https://docs.python.org/3/library/time.html)
-ex: time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
20160711 - v0.1.0 created - functions work for Windows *only* (via the QPC timer)

References:
WINDOWS:
-personal (C++ code): GS_PCArduino.h
1) Acquiring high-resolution time stamps (Windows)
   -https://msdn.microsoft.com/en-us/library/windows/desktop/dn553408(v=vs.85).aspx
2) QueryPerformanceCounter function (Windows)
   -https://msdn.microsoft.com/en-us/library/windows/desktop/ms644904(v=vs.85).aspx
3) QueryPerformanceFrequency function (Windows)
   -https://msdn.microsoft.com/en-us/library/windows/desktop/ms644905(v=vs.85).aspx
4) LARGE_INTEGER union (Windows)
   -https://msdn.microsoft.com/en-us/library/windows/desktop/aa383713(v=vs.85).aspx

-*****https://stackoverflow.com/questions/4430227/python-on-win32-how-to-get-
absolute-timing-cpu-cycle-count

LINUX:
-https://stackoverflow.com/questions/1205722/how-do-i-get-monotonic-time-durations-in-python


"""

import ctypes, os 

#-------------------------------------------------------------------
#FUNCTIONS:
#-------------------------------------------------------------------
#OS-specific low-level timing functions:
if (os.name=='nt'): #for Windows:
    def timestamp_us():
        "return a high-precision timestamp in microseconds (us)"
        tics = ctypes.c_int64()
        freq = ctypes.c_int64()

        #get ticks on the internal ~2MHz QPC clock
        ctypes.windll.Kernel32.QueryPerformanceCounter(ctypes.byref(tics)) 
        #get the actual freq. of the internal ~2MHz QPC clock
        ctypes.windll.Kernel32.QueryPerformanceFrequency(ctypes.byref(freq))  

        t_us = tics.value*1e6/freq.value
        return t_us

    def timestamp_ms():
        "return a high-precision timestamp in milliseconds (ms)"
        tics = ctypes.c_int64()
        freq = ctypes.c_int64()

        #get ticks on the internal ~2MHz QPC clock
        ctypes.windll.Kernel32.QueryPerformanceCounter(ctypes.byref(tics)) 
        #get the actual freq. of the internal ~2MHz QPC clock 
        ctypes.windll.Kernel32.QueryPerformanceFrequency(ctypes.byref(freq)) 

        t_ms = tics.value*1e3/freq.value
        return t_ms

elif (os.name=='posix'): #for Linux:

    #Constants:
    CLOCK_MONOTONIC_RAW = 4 # see <linux/time.h> here: https://github.com/torvalds/linux/blob/master/include/uapi/linux/time.h

    #prepare ctype timespec structure of {long, long}
    class timespec(ctypes.Structure):
        _fields_ =\
        [
            ('tv_sec', ctypes.c_long),
            ('tv_nsec', ctypes.c_long)
        ]

    #Configure Python access to the clock_gettime C library, via ctypes:
    #Documentation:
    #-ctypes.CDLL: https://docs.python.org/3.2/library/ctypes.html
    #-librt.so.1 with clock_gettime: https://docs.oracle.com/cd/E36784_01/html/E36873/librt-3lib.html #-
    #-Linux clock_gettime(): http://linux.die.net/man/3/clock_gettime
    librt = ctypes.CDLL('librt.so.1', use_errno=True)
    clock_gettime = librt.clock_gettime
    #specify input arguments and types to the C clock_gettime() function
    # (int clock_ID, timespec* t)
    clock_gettime.argtypes = [ctypes.c_int, ctypes.POINTER(timespec)]

    def timestamp_s():
        "return a high-precision timestamp in seconds (sec)"
        t = timespec()
        #(Note that clock_gettime() returns 0 for success, or -1 for failure, in
        # which case errno is set appropriately)
        #-see here: http://linux.die.net/man/3/clock_gettime
        if clock_gettime(CLOCK_MONOTONIC_RAW , ctypes.pointer(t)) != 0:
            #if clock_gettime() returns an error
            errno_ = ctypes.get_errno()
            raise OSError(errno_, os.strerror(errno_))
        return t.tv_sec + t.tv_nsec*1e-9 #sec 

    def timestamp_us():
        "return a high-precision timestamp in microseconds (us)"
        return timestamp_s()*1e6 #us 

    def timestamp_ms():
        "return a high-precision timestamp in milliseconds (ms)"
        return timestamp_s()*1e3 #ms 

#Other timing functions:
def wait_ms(delay_ms):
    "Wait (block) for delay_ms milliseconds (ms) using a high-precision timer"
    t_start = timestamp_ms()
    while (timestamp_ms() - t_start < delay_ms):
      pass #do nothing 
    return

def wait_us(delay_us):
    "Wait (block) for delay_us microseconds (us) using a high-precision timer"
    t_start = timestamp_us()
    while (timestamp_us() - t_start < delay_us):
      pass #do nothing 
    return 

def get_week_number(strdate, fmt='%Y-%m-%d'):
    """Returns the week of the year in which a date occurs

    """
    return datetime.datetime.strptime(strdate,fmt).date().strftime("%V")

def seconds_to_time(seconds):
    """Returns a string representation of time given a number of seconds

        If seconds is an int, the format of the string returned is 'hh:mm:ss'
        If it is a float with a decimal, the return string format is 'hh:mm:ss.sss'
        where sss is milliseconds

    """

    secs, d = divmod(seconds, 1)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    ret = '{:02d}:{:02d}:{:02d}'.format(int(h), int(m), int(s))
    if d > 0:
        ret = "{}.{:03d}".format(ret, round(d*1000))
    return ret


def time_to_seconds(strtime):
    """Returns a number of seconds as an int from a time string

        strtime format can be in the form hh:mm:ss.ms; the only required params are mm and ss
    """
    # return int(sum(x * int(t) for x, t in zip([3600, 60, 1, .001], strtime.split(":"))))
    if "." in strtime:
        t,ms = strtime.split(".")
    else:
        t = strtime
        ms = "000"
    sec = float(sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(strtime.split(":")))))
    return sec + (float(ms)/1000.) 

#-------------------------------------------------------------------
#EXAMPLES:
#-------------------------------------------------------------------
if __name__ == "__main__": #if running this module as a stand-alone program

    #print loop execution time 100 times, using micros()
    tStart = timestamp_us() #us
    for x in range(0, 100):
        tNow = timestamp_us() #us
        dt = tNow - tStart #us; delta time 
        tStart = tNow #us; update 
        print("dt(us) = " + str(dt))

    #print loop execution time 100 times, using timestamp_ms()
    print("\n")
    tStart = timestamp_ms() #ms
    for x in range(0, 100):
        tNow = timestamp_ms() #ms
        dt = tNow - tStart #ms; delta time 
        tStart = tNow #ms; update 
        print("dt(ms) = " + str(dt))

    #print a counter once per second, for 5 seconds, with ms resolution
    print("\nstart (ms)")
    tStart = timestamp_ms() #us
    for i in range(1,6):
        wait_ms(1000)
        print(timestamp_ms() - tStart)

    #print a counter once per second, for 5 seconds, with us resolution
    print("\nstart (us)")
    tStart = timestamp_us() #us
    for i in range(1,6):
        wait_us(1000000)
        print(timestamp_us() - tStart)
