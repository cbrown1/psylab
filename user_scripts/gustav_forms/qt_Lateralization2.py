# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 14:58:02 2014

@author: code-breaker
"""

import os, sys
from PyQt4 import QtGui, QtCore, Qt
import numpy as np
import psylab.audio

#class Interface():
#
class UI_Lateralization(QtGui.QWidget):
    
    form_w = 0
    form_h = 0

    respIcon_w = 0
    respIcon_h = 0

    respArea_x = 0
    respArea_y = 0
    respArea_w = 0
    respArea_h = 0

    response = 0
    click_x = 0
    click_y = 0

    feedback = False
    
    def __init__(self, feedback, bg_image):
        super(UI_Lateralization, self).__init__()
        
        self.waitingForResponse = False
        if feedback:
            self.feedback = True
            if os.path.isfile(feedback):
                self.respIcon_file = os.path.join(feedback)
            else:
                self.icon_randomize = True
                self.icon_folder = feedback
                if self.icon_randomize:
                    self.icon_set = psylab.audio.signal_io.get_consecutive_files(self.icon_folder,
                                                                                 file_ext='.png',
                                                                                 random = True)
        if bg_image:
            self.form_bgImage = bg_image
        else:
            self.form_bgImage = os.path.join("Images","SmileyFaces","smileyface_headphones.jpg")

        self.initUI()

    
    def feedback_show(self):
        x = self.click_x - round(self.respIcon_w/2)+self.respArea_x
        x = np.maximum(x,0)
        x = np.minimum(x,self.form_w)
        y = (self.respArea_h/2) - round(self.respIcon_h/2)+self.respArea_y
        y = np.maximum(y,0)
        y = np.minimum(y,self.form_h)
        if self.icon_randomize:
            self.iconImage.setVisible(False)
            respIconraw = QtGui.QPixmap(os.path.join(self.icon_folder,self.icon_set.get_next()))
#            if respIconraw.width() > 48 or respIconraw.height() > 48:
#                respIconraw = respIconraw.scaled(48,48, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
            self.iconImage.setPixmap(respIconraw)
            self.iconImage.update()
        self.iconImage.setGeometry(x,y,self.respIcon_w, self.respIcon_h)
        self.iconImage.setVisible(True)
        
        
    def feedback_hide(self):
        self.iconImage.setVisible(False)

    def responseClick(self , event):
        self.click_x = event.pos().x()
        self.click_y = event.pos().y()
        response = float(event.pos().x())/self.width()
        self.response = round(response * 21)-10
        if self.feedback:
            self.feedback_show()
        self.waitingForResponse = False

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

        # Create response area
        self.respArea_x = 5
        self.respArea_y = int(self.form_h/4)
        self.respArea_w = self.form_w-10
        self.respArea_h = 35
        self.respArea = QtGui.QLabel(self)
        self.respArea.setGeometry(QtCore.QRect(self.respArea_x, self.respArea_y, self.respArea_w, self.respArea_h))
        self.respArea.setAutoFillBackground(True)
        self.respArea.setStyleSheet("border-style: outset; border-width: 3px; border-color: rgba(20,20,20,120); background-color: rgba(60,60,60,120); color: rgba(255,255,255,255);")
        self.respArea.mousePressEvent = self.responseClick
        self.respArea.setAlignment(QtCore.Qt.AlignCenter)
        self.respArea.setAlignment(QtCore.Qt.AlignHCenter)

        if self.icon_randomize:
            respIconraw = QtGui.QPixmap(os.path.join(self.icon_folder,self.icon_set.get_next()))
        else:
            respIconraw = QtGui.QPixmap(self.respIcon_file)
        self.respIcon_w = respIconraw.width()
        self.respIcon_h = respIconraw.height()
        self.iconImage = QtGui.QLabel(self)
        self.iconImage.setBackgroundRole(QtGui.QPalette.Base)
        self.iconImage.setSizePolicy(QtGui.QSizePolicy.Ignored,
                QtGui.QSizePolicy.Ignored)
        self.iconImage.setPixmap(respIconraw)
        self.iconImage.setVisible(False)

        self.listenPrompt = QtGui.QLabel(self)
        self.listenPrompt.setGeometry(QtCore.QRect(0, 0, self.form_w, self.form_h))
        self.listenPrompt.setStyleSheet("qproperty-alignment: AlignCenter; background-color: rgba(100,20,20,255); color: rgba(255,255,255,255); font: bold 36px;")
        self.listenPrompt.setText('Listen!')
        self.listenPrompt.setVisible(False)

        self.setFixedSize(self.form_w, self.form_h)
        self.setWindowTitle('Gustav!')
        self.show()

#    def __init__(self, exp, run, feedback=None, bg_image=None):
#        app = QtGui.QApplication(sys.argv)
#        ex = UI_Lateralization(feedback, bg_image)
#        sys.exit(app.exec_())
#
#
#    def feedback_hide(self):
#        self.dialog.feedback_hide()
#
#    def get_resp(self):
#        """Waits modally for a response
#        """
#        self.dialog.waitingForResponse = True
#        while self.dialog.waitingForResponse:
#            self.app.processEvents()
#            time.sleep(.1)
#        curresp = self.dialog.response
#        self.dialog.response= 0
#        return curresp
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = UI_Lateralization('/home/code-breaker/Projects/psylab/user_scripts/gustav_forms/Images/Animals',
    '/home/code-breaker/Projects/psylab/user_scripts/gustav_forms/Images/SmileyFaces/smileyface_headphones.jpg')
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()