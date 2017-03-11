#! /usr/bin/env python
#coding=utf-8

import wx
from mainFrame import *
from trayIcon import *


class SZQNApp(wx.App):
    def OnInit(self):    # must subclass the 'app' class and overwrite the OnInit() function
        self.frame = QuickNoteMainFrame()
        self.trayIcon = SZQNTrayIcon()
        self.trayIcon.mainframe = self.frame
        #self.frame.Show()    # do not show the frame. the frame just exist, to contain the main record and amin record length, and act as note frames' parent
        self.frame.trayIcon = self.trayIcon
        self.SetTopWindow(self.frame)    # without this the app just ends upon starting
        return True    # OnInit() function must return a boolean variable
        
    
    
if __name__=='__main__':
    app = SZQNApp()
    app.MainLoop()
