#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 21:13:43 2020

@author: niels
"""

from PyQt5 import QtCore, QtWidgets, uic


import sys
from math import floor
from pygame import mixer  # Load the popular external library

mixer.init()
mixer.music.load('alarm01.wav')

class WindowThread(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self,parent)
        #os.chdir("Y:\Experimental Control\Python Experimental Control")
        uic.loadUi('design.ui', self)
        
        self.init = 0        
        self.elapsedWorkSeconds = 0
        self.elapsedWorkMinutes = 0
        self.displayedWorkSeconds = 0
        self.displayedWorkMinutes = 0
        self.earnedBreakSeconds = 0
        self.earnedBreakMinutes = 0
        self.displayedBreakSeconds = 0
        self.displayedBreakMinutes = 0
        
        self.working = False
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
                
        self.doWork.clicked.connect(self.startWork)
        self.doBreak.clicked.connect(self.startBreak)
        self.reset.clicked.connect(self.resetTimes)
        self.pause.clicked.connect(self.timer.stop)
        #self.reset.clicked.connect(mixer.music.play)
        
        self.timer.timeout.connect(self.updateDisplay)
        
    def startBreak(self):
        if(not(self.timer.isActive())):
            self.timer.start()
        self.working = False
        self.displayedWorkMinutes += self.elapsedWorkMinutes
        if (self.elapsedWorkMinutes >= self.breakMinutesThreshold.value()):
            if(self.displayedBreakMinutes < 0 and (self.displayedBreakMinutes+self.earnedBreakMinutes) >=0):
                self.displayedBreakMinutes += self.earnedBreakMinutes-1
                self.displayedBreakSeconds += 60
            else:
                self.displayedBreakMinutes += self.earnedBreakMinutes
        self.displayedWorkSeconds += self.elapsedWorkSeconds
        if (self.displayedWorkSeconds >= 60):
            self.displayedWorkMinutes += floor(self.displayedWorkSeconds/60)
            self.displayedWorkSeconds -= 60*floor(self.displayedWorkSeconds/60)
        self.elapsedWorkMinutes = 0
        self.elapsedWorkSeconds = 0
        
    def startWork(self):
        if(not(self.timer.isActive())):
            self.timer.start()
        self.working = True
        
    
    def displayTime(self, lcd_min, lcd_sec, minutes, seconds):
        tmp = minutes
        tmp2 = seconds
        if (seconds >= 60):
           tmp += floor(seconds/60)
           tmp2 -= 60*floor(seconds/60)
        lcd_min.display("{}".format(tmp))
        lcd_sec.display("{}".format(tmp2))
        
    
    
    def updateDisplay(self):
        if (self.working):
            self.elapsedWorkSeconds += 1
            if (self.elapsedWorkSeconds >= 60):
                self.elapsedWorkSeconds = 0
                self.elapsedWorkMinutes += 1
            self.displayTime(self.workMinutes, self.workSeconds, self.displayedWorkMinutes+self.elapsedWorkMinutes, self.displayedWorkSeconds+self.elapsedWorkSeconds)
            
            self.earnedBreakMinutes = floor(self.elapsedWorkMinutes/self.breakMinutesCost.value())
            if (self.elapsedWorkMinutes >= self.breakMinutesThreshold.value()):
                self.displayTime(self.breakMinutes, self.breakSeconds, self.displayedBreakMinutes+self.earnedBreakMinutes, self.displayedBreakSeconds)
        else:
            if(self.displayedBreakMinutes==0 and self.displayedBreakSeconds==0):
                mixer.music.play(3)
                        
            if(self.displayedBreakMinutes >= 1):
                if (self.displayedBreakSeconds <= 0):
                    self.displayedBreakSeconds = 59
                    self.displayedBreakMinutes -= 1
                else:
                    self.displayedBreakSeconds -= 1
            else:                    
                if (self.displayedBreakSeconds <= -59):
                    self.displayedBreakSeconds = 0
                    self.displayedBreakMinutes -= 1
                else:
                    self.displayedBreakSeconds -= 1
            self.displayTime(self.breakMinutes, self.breakSeconds, self.displayedBreakMinutes, self.displayedBreakSeconds)

    
            
    def resetTimes(self):
        self.timer.stop()
        self.elapsedWorkSeconds = 0
        self.elapsedWorkMinutes = 0
        self.displayedWorkSeconds = 0
        self.displayedWorkMinutes = 0
        self.earnedBreakSeconds = 0
        self.earnedBreakMinutes = 0
        self.displayedBreakSeconds = 0
        self.displayedBreakMinutes = 0
        self.displayTime(self.workMinutes, self.workSeconds, self.displayedWorkMinutes, self.displayedWorkSeconds)
        self.displayTime(self.breakMinutes, self.breakSeconds, self.displayedBreakMinutes, self.displayedBreakSeconds)


    

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = WindowThread()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()