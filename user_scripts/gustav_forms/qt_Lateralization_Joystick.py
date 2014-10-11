# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 14:58:02 2014

@author: code-breaker
"""

import os, sys
import time
from PyQt4 import QtGui, QtCore, Qt
import numpy as np
import psylab
import psylab.io.hid


class Interface():
    """Lateralization form that accepts joystick input
    
        Move the joystick left or right to indicate lateral position, then
        push button 1 to enter response.
        
        Uses psylab.io.hid to access joystick data, which depends on linux
        
        Will use the first joystick it finds, then reads the horizontal axis 
        of Joystick 1, and waits for Button 1 to enter response. Atari Paddles 
        (tennis/pong) will work as well as joysticks. 
    """
    prompt = ""
    joystick = psylab.io.hid.joystick()
    
    def __init__(self, bg_image, icon, parent=None):
        pass
        self.app = QtGui.QApplication([]) # D
        self.dialog = self.Dialog(bg_image, icon) # D
        self.dialog.show() # D
        self.dialog.setFixedSize(self.dialog.width(),self.dialog.height()) # <- Must be done after show  # D
        self.app.processEvents() # D

#    class Dialog(QtGui.QWidget):
    class Dialog(QtGui.QDialog):
        
        def __init__(self, bg_image, icon, parent=None):
    #        super(Dialog, self).__init__()
            QtGui.QDialog.__init__(self, parent, QtCore.Qt.Window) # D
            #self.setWindowIcon(QtGui.QIcon('shs_head16.png')) # D

            self.char = ''
            self.waitingForResponse = False
            self.respIsClick = False

            self.form_w = 0
            self.form_h = 0
        
            self.respIcon_file = icon
            self.respIcon_w = 0
            self.respIcon_h = 0
        
            self.respArea_x = 0
            self.respArea_y = 0
            self.respArea_w = 0
            self.respArea_h = 0
            self.response = 0
            self.click_x = 0
            self.click_y = 0
            
            if bg_image:
                self.form_bgImage = bg_image
            else:
                self.form_bgImage = os.path.join("Images","SmileyFaces","smileyface_headphones.jpg")
    
            self.initUI()
            
            
        def update_position(self, x):

            x = round(x * self.respArea_w) - round(self.respIcon_w/2)+self.respArea_x
            y = (self.respArea_h/2) - round(self.respIcon_h/2)+self.respArea_y
            self.iconImage.setGeometry(x,y,self.respIcon_w, self.respIcon_h)
            self.iconImage.setVisible(True)
            self.update()
            self.repaint()
            
            
        def feedback_show(self):
            x = self.click_x - round(self.respIcon_w/2)+self.respArea_x
            x = np.maximum(x,0)
            x = np.minimum(x,self.form_w)
            y = (self.respArea_h/2) - round(self.respIcon_h/2)+self.respArea_y
            y = np.maximum(y,0)
            y = np.minimum(y,self.form_h)
            self.respArea.setText("")
            if self.icon_folder:
                self.iconImage.setVisible(False)
                respIconraw = QtGui.QPixmap(os.path.join(self.icon_folder,self.icon_set.get_filename()))
    #            if respIconraw.width() > 48 or respIconraw.height() > 48:
    #                respIconraw = respIconraw.scaled(48,48, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
                self.iconImage.setPixmap(respIconraw)
                self.iconImage.update()
            self.iconImage.setGeometry(x,y,self.respIcon_w, self.respIcon_h)
            self.iconImage.update()
            self.iconImage.setVisible(True)
            self.update()
            self.repaint()
            
        def keyPressEvent(self, keyevent):
            self.response = keyevent.key()
            self.waitingForResponse = False
            
        def feedback_hide(self):
            self.iconImage.setVisible(False)
            
        def response_hide(self):
            if self.feedback:
                self.iconImage.setVisible(False)
                self.iconImage.update()
            self.respArea.setVisible(False)
            self.respArea.update()
            self.repaint()
    
        def response_click(self , event):
            self.click_x = event.pos().x()
            self.click_y = event.pos().y()
            response = float(event.pos().x())/self.width()
            # Transform response from 0-1 to +-responses/2 (if resp==21, then -10 - +10)
            self.response = round(response * (self.responses-1))-np.floor(self.responses/2.)
            self.respIsClick = True
            self.waitingForResponse = False
        
        def solicit_resp(self, prompt=""):
            self.iconImage.setVisible(False)
            self.respArea.setText(prompt)
            self.respArea.setVisible(True)
            self.respIsClick = False
            self.waitingForResponse = True
            
    
        def set_text_block(self,text):
            self.label_block.setText(text)
    
        def initUI(self):               
            
            # Load Background Image
            self.setWindowIcon(QtGui.QIcon('shs_head16.png'))
            self.bgImageraw = QtGui.QPixmap(self.form_bgImage)
            self.form_w = self.bgImageraw.width()
            self.form_h = self.bgImageraw.height()
            if self.form_w > 500 or self.form_h > 500:
                self.bgImageraw = self.bgImageraw.scaled(500,500, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
                self.form_w = self.bgImageraw.width()
                self.form_h = self.bgImageraw.height()
            self.bgimage = QtGui.QLabel(self)
            self.bgimage.setBackgroundRole(QtGui.QPalette.Base)
            self.bgimage.setSizePolicy(QtGui.QSizePolicy.Ignored,
                    QtGui.QSizePolicy.Ignored)
            
            # Draw mid-saggital line
            self.bgimagep = QtGui.QPainter(self.bgImageraw)
            self.bgimagep.setPen(QtGui.QPen(QtGui.QColor(128, 128, 128), 6, QtCore.Qt.DotLine, QtCore.Qt.SquareCap, QtCore.Qt.BevelJoin));
            self.bgimagep.drawLine(int(self.form_w/2),0,int(self.form_w/2.),self.form_h)
            self.bgimage.setPixmap(self.bgImageraw)
            self.bgimagep.end()
    
            # Create response area
            self.respArea_x = 5
            self.respArea_y = int(self.form_h/4)
            self.respArea_w = self.form_w-10
            self.respArea_h = 35
            self.respArea = QtGui.QLabel(self)
            self.respArea.setGeometry(QtCore.QRect(self.respArea_x, self.respArea_y, self.respArea_w, self.respArea_h))
            self.respArea.setAutoFillBackground(True)
            self.respArea.setStyleSheet("border-style: outset; border-width: 3px; border-color: rgba(20,20,20,120); background-color: rgba(60,60,60,120); color: rgba(255,255,255,255); font-size: 20px")
            self.respArea.mousePressEvent = self.response_click
            self.respArea.setAlignment(QtCore.Qt.AlignCenter)
            #self.respArea.setAlignment(QtCore.Qt.AlignHCenter)
            self.respArea.setVisible(False)
    
            respIconraw = QtGui.QPixmap(self.respIcon_file)
            self.respIcon_w = respIconraw.width()
            self.respIcon_h = respIconraw.height()
            self.iconImage = QtGui.QLabel(self)
            self.iconImage.setBackgroundRole(QtGui.QPalette.Base)
            self.iconImage.setSizePolicy(QtGui.QSizePolicy.Ignored,
                    QtGui.QSizePolicy.Ignored)
            self.iconImage.setPixmap(respIconraw)
            self.iconImage.setVisible(False)
    
            self.label_block = QtGui.QLabel(self)
            self.label_block.setGeometry(QtCore.QRect(10, self.form_h-30, 100, 25))
            self.label_block.setStyleSheet("border-style: outset; border-width: 2px; border-color: rgba(20,20,20,100); background-color: rgba(255,255,255,255); color: rgba(0,0,0,255);")
            
            self.label_trial = QtGui.QLabel(self)
            self.label_trial.setGeometry(QtCore.QRect(self.form_w-110, self.form_h-30, 100, 25))
            self.label_trial.setStyleSheet("border-style: outset; border-width: 2px; border-color: rgba(20,20,20,100); background-color: rgba(255,255,255,255); color: rgba(0,0,0,255);")
            
            self.setFixedSize(self.form_w, self.form_h)
            self.setWindowTitle('Gustav!')
            self.setModal = False # D
            self.setFocus() # D
    #        self.show()
    # End Dialog

    def get_resp(self,prompt=None):
        """Waits modally for a response click
        """
        if prompt:
            self.prompt = prompt
        self.dialog.respArea.setText(self.prompt)
        self.dialog.respArea.setVisible(True)
        self.dialog.update()
        self.dialog.repaint()
        self.app.processEvents()
        time.sleep(.01)

        wait = True
        while wait:
            c,e,d = self.joystick.listen()
#            print c,e,d
            if c == "Joystick" and e == "1 Horz":
                # Gather data from paddle 1
                self.data = float(d)/255.
                self.dialog.update_position(self.data)
            elif c == "Button" and e == "1" and d == 0:
                # Wait until button 1 is released (data==0)
                wait=False
            self.app.processEvents()
            time.sleep(.01)
        self.dialog.respArea.setVisible(False)
        self.dialog.iconImage.setVisible(False)
        self.app.processEvents()
        self.dialog.update()
        self.dialog.repaint()

        return self.data


#        while True:
#            self.dialog.solicit_resp(self.prompt)
#            while self.dialog.waitingForResponse:
#                self.app.processEvents()
#                time.sleep(.1)
#            resp = self.dialog.response
#            if self.dialog.respIsClick:
#                self.dialog.feedback_show()
#                self.app.processEvents()
#                time.sleep(self.feedback_dur)
#                self.dialog.response_hide()
#                self.app.processEvents()
#                break
#            elif resp < 128: # US keyboard
#                resp = chr(resp)
#                break
#        return resp

    def set_text_block(self, text):
        self.dialog.label_block.setText(text)

    def set_text_trial(self, text):
        self.dialog.label_trial.setText(text)
    
    def update(self):
        self.dialog.update()
        self.dialog.repaint()
        self.app.processEvents()
        
#def main():
#    pass # D
#    app = QtGui.QApplication(sys.argv)
#    ex = Dialog('/home/code-breaker/Projects/psylab/user_scripts/gustav_forms/Images/SmileyFaces/smileyface_headphones.jpg',
#                           '/home/code-breaker/Projects/psylab/user_scripts/gustav_forms/Images/Butterflies')
#    #ex = Interface()
#    sys.exit(app.exec_())

#if __name__ == '__main__':
#    main()
