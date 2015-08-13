# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 20:50:40 2013

@author: code-breaker
"""

import sys
import sqlite3
import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.markers as mpm
from matplotlib.widgets import Button

name = "Get_Audio"

data = {}

left_data = [None, None, None, None, None, None, None, None, None, None, None]
right_data = [None, None, None, None, None, None, None, None, None, None, None]
left_handle = [None, None, None, None, None, None, None, None, None, None, None]
right_handle = [None, None, None, None, None, None, None, None, None, None, None]

shift = 0

save_data = False
close = False

x = [125, 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000]
xpos = np.arange(0,len(x))
ypos = range(-10, 120, 5)

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

def mouse_click(event):
    # HACK! Use an axis label to identify the axes
    #global shift, af, fh
    if event.inaxes and event.inaxes.get_xlabel() == "Frequency (Hz)":
        x = find_nearest(xpos, event.xdata)
        y = find_nearest(ypos, event.ydata)
        # TODO: implement shift for no-response (plot as nr if y < -10)
        if (y > 10) and (shift > 0):
            y1 = -y
        else:
            y1 = y
        if event.button == 1:
            if left_handle[x]:
                left_handle[x][0].remove()
                left_handle[x] = None
            if y1 < -10:
                left_handle[x] = data['af'].plot(x-.1,y, marker=mpm.CARETLEFT, ms=10, ls='None', mfc='None', mec='b', mew=3)
            else:
                left_handle[x] = data['af'].plot(x,y, marker='s', ms=10, ls='None', mfc='None', mec='b', mew=3)
            left_data[x] = y1
        elif event.button == 3:
            if right_handle[x]:
                right_handle[x][0].remove()
                right_handle[x] = None
            if y1 < -10:
                right_handle[x] = data['af'].plot(x+.1,y, marker=mpm.CARETRIGHT, ms=10, ls='None', mfc='None', mec='r', mew=3)
            else:
                right_handle[x] = data['af'].plot(x,y, marker='o', ms=10, ls='None', mfc='None', mec='r', mew=3)
            right_data[x] = y1
        event.canvas.draw()

def key_press(event):
    global shift
    if event.key == 'shift':
        shift += 1
    
def key_release(event):
    global shift
    if event.key == 'shift':
        if shift > 0:
            shift -= 1

def callback_done(event):
    save_data()
    plt.close(data['fh'])
    #sys.stdout.flush()

def callback_cancel(event):
    plt.close(data['fh'])
    #sys.stdout.flush()

def is_number(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError) as e:
        return False

def proc_subject(db, SubjN):
    #global dbg, SubjNg, af, fh
    data['db'] = db
    data['SubjN'] = SubjN

    data['fh'] = plt.figure()
    
    data['af'] = data['fh'].add_axes([0.09, 0.12, 0.89, 0.81])
    data['af'].axhspan(-5,20, fc='0.7', ec='None', alpha=0.5)
    
    button_coor_done = [0.85, 0.01, 0.1, 0.06]
    button_coor_cancel = [0.72, 0.01, 0.1, 0.06]
    
    data['af'].set_ylim([-5, 115])
    data['af'].yaxis.set_ticks(range(0, 120, 10))
    data['af'].yaxis.set_ticklabels(range(0, 120, 10))
    data['af'].invert_yaxis()
    data['af'].xaxis.set_ticks(xpos)
    data['af'].xaxis.set_ticklabels(x)
    data['af'].set_xlim([-.5, xpos[-1]+.5])
    data['af'].grid(True)
    data['af'].set_ylabel('Threshold (Hearing Level)')
    data['af'].set_xlabel('Frequency (Hz)')
    
    data['fh'].canvas.mpl_connect('button_press_event', mouse_click)
    data['fh'].canvas.mpl_connect('key_press_event', key_press)
    data['fh'].canvas.mpl_connect('key_release_event', key_release)
    
    axdone = data['fh'].add_axes(button_coor_done)
    data['bd'] = Button(axdone, 'Done')
    data['bd'].on_clicked(callback_done)
    
    data['axcancel'] = data['fh'].add_axes(button_coor_cancel)
    data['bc'] = Button(data['axcancel'], 'Cancel')
    data['bc'].on_clicked(callback_cancel)
    
    conn = sqlite3.connect(data['db'])
    c = conn.cursor()
    c.execute("""SELECT FName,LName FROM Subjects WHERE SubjN == \'%s\'""" % SubjN)
    subject = list(c.fetchone())
    for i in range(len(subject)):
        if subject[i] is None:
            subject[i] = ''
    data['fh'].text(.5,.97,'%s %s' % (subject[0], subject[1]),horizontalalignment='center',fontsize='large')
    data['fh'].text(.5,.94,'Left- or right-click for each ear, hold shift for no response',horizontalalignment='center',fontsize='medium')

    c.execute("""SELECT User_L125,User_L250,User_L500,User_L750,User_L1k,
                 User_L15,User_L2k,User_L3k,User_L4k,User_L6k,User_L8k FROM Subjects WHERE SubjN == \'%s\'""" % (SubjN))
    uservar_this = list(c.fetchone())
    for i in range(len(uservar_this)):
        y = uservar_this[i]
        if y and is_number(y):
            y = float(y)
            if y < -10:
                y1 = -y
            else:
                y1 = y
            if left_handle[i]:
                left_handle[i][0].remove()
                left_handle[i] = None
            if y < -10:
                left_handle[i] = data['af'].plot(i-.1,y1, marker=mpm.CARETLEFT, ms=10, ls='None', mfc='None', mec='b', mew=3)
            else:
                left_handle[i] = data['af'].plot(i,y1, marker='s', ms=10, ls='None', mfc='None', mec='b', mew=3)
            left_data[i] = y

    c.execute("""SELECT User_R125,User_R250,User_R500,User_R750,User_R1k,
                 User_R15,User_R2k,User_R3k,User_R4k,User_R6k,User_R8k FROM Subjects WHERE SubjN == \'%s\'""" % (SubjN))
    uservar_this = list(c.fetchone())
    for i in range(len(uservar_this)):
        y = uservar_this[i]
        if y and is_number(y):
            y = float(y)
            if y < -10:
                y1 = -y
            else:
                y1 = y
            if right_handle[i]:
                right_handle[i][0].remove()
                right_handle[i] = None
            if y < -10:
                right_handle[i] = data['af'].plot(i+.1,y1, marker=mpm.CARETRIGHT, ms=10, ls='None', mfc='None', mec='r', mew=3)
            else:
                right_handle[i] = data['af'].plot(i,y1, marker='o', ms=10, ls='None', mfc='None', mec='r', mew=3)
            right_data[i] = y

    data['fh'].show()

#        c.execute("""SELECT User_L125,User_L250,User_L500,User_L750,User_L1k,
#                     User_L15,User_L2k,User_L3k,User_L4k,User_L6k,User_L8k FROM Subjects WHERE SubjN == \'%s\'""" % (SubjN))
#        uservar_this = c.fetchone()
#        left = []
#        for var in uservar_this:
#            if var and is_number(var):
#                left.append(float(var))
#            else:
#                left.append(np.nan)
#        plot_data(af,left,'left')
#
#        c.execute("""SELECT User_R125,User_R250,User_R500,User_R750,User_R1k,
#                     User_R15,User_R2k,User_R3k,User_R4k,User_R6k,User_R8k FROM Subjects WHERE SubjN == \'%s\'""" % (SubjN))
#        uservar_this = c.fetchone()
#        right = []
#        for var in uservar_this:
#            if var and is_number(var):
#                right.append(float(var))
#            else:
#                right.append(np.nan)
#        plot_data(af,right,'right')
    
    
    # TODO: get previous audio data from db and add to fig

def save_data():
    #global dbg, SubjNg
    query = "UPDATE Subjects SET "
    items = ["User_Audio_Date = '%s'" % time.strftime("%Y-%m-%d")]
    vars = ['125', '250', '500', '750', '1k', '15', '2k', '3k', '4k', '6k', '8k']
    for i in range(len(vars)):
        if left_data[i] is not None:
            items.append("User_l%s = '%i'" % (vars[i], left_data[i]))
        else:
            items.append("User_l%s = ''" % vars[i])
    for i in range(len(vars)):
        if right_data[i] is not None:
            items.append("User_r%s = '%i'" % (vars[i], right_data[i]))
        else:
            items.append("User_r%s = ''" % vars[i])
    query += ", ".join(items)
    query += " WHERE SubjN = '%s';" % data['SubjN']

    conn = sqlite3.connect(data['db'])
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    c.close()
    conn.close()

    plt.close(data['fh'])
