# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 14:58:02 2014

@author: code-breaker
"""

import sys
from PyQt4 import QtGui, QtCore, Qt

class UI_Lateralization(QtGui.QWidget):
    
    def __init__(self):
        super(UI_Lateralization, self).__init__()
        
        self.initUI()
        
    def getPos(self , event):
        #x = event.pos().x()
        #y = event.pos().y() 
        response = float(event.pos().x())/self.width()
        response = round(response * 21)-10
        print("Response: %f" % (response))

    def initUI(self):               
        
        # Load image
        self.imraw = QtGui.QPixmap("smileyface_pirate.jpg")
        x = self.imraw.width()
        y = self.imraw.height()
        if x > 500 or y > 500:
            self.imraw = self.imraw.scaled(500,500, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
            x = self.imraw.width()
            y = self.imraw.height()
        self.image = QtGui.QLabel(self)
        self.image.setBackgroundRole(QtGui.QPalette.Base)
        self.image.setSizePolicy(QtGui.QSizePolicy.Ignored,
                QtGui.QSizePolicy.Ignored)
        
        # Draw mid-saggital line
        self.imagep = QtGui.QPainter(self.imraw)
        self.imagep.setPen(QtGui.QPen(QtGui.QColor(128, 128, 128), 6, QtCore.Qt.DotLine, QtCore.Qt.SquareCap, QtCore.Qt.BevelJoin));
        self.imagep.drawLine(int(x/2),0,int(x/2.),y)
        self.image.setPixmap(self.imraw)

        # Create response area
        self.clickArea = QtGui.QLabel(self)
        self.clickArea.setGeometry(QtCore.QRect(5, int(y/4), x-10, 35))
        self.clickArea.setAutoFillBackground(True)
        self.clickArea.setStyleSheet("border-style: outset; border-width: 3px; border-color: rgba(20,20,20,120); background-color: rgba(60,60,60,120); color: rgba(255,255,255,255);")
        self.clickArea.mousePressEvent = self.getPos
        self.clickArea.setAlignment(QtCore.Qt.AlignCenter)
        self.clickArea.setAlignment(QtCore.Qt.AlignHCenter)

        self.listenPrompt = QtGui.QLabel(self)
        self.listenPrompt.setGeometry(QtCore.QRect(0, 0, x, y))
        self.listenPrompt.setStyleSheet("qproperty-alignment: AlignCenter; background-color: rgba(100,20,20,255); color: rgba(255,255,255,255); font: bold 36px;")
        self.listenPrompt.setText('Listen!')
        self.listenPrompt.setVisible(False)

        self.resize(x, y)
        self.setWindowTitle('Gustav!')
        self.show()
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = UI_Lateralization()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()