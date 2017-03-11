#! /usr/bin/env python
#coding=utf-8

import wx


class SZQNTrayIcon(wx.TaskBarIcon):
    def __init__(self):
        wx.TaskBarIcon.__init__(self)#,parent,id)    # it turns out that the constructor of TaskBarIcon class doesnt need parent or id
        self.SetIcon(wx.Icon('icon.png', wx.BITMAP_TYPE_ANY), "S.Z.'s Note!")
                
        
    def menuData(self):
        menudata = (('New Note',"Create a new quick note.",self.OnNew),
                    ('Show Notes',"Show all quick notes on top of other programs.",self.OnShow),
                    ('Hide Notes',"Hide all quick notes.",self.OnHide),
                    ('Clear Notes',"Delete all quick notes.",self.OnClear),
                    ('Separator'),
                    ('About',"About S.Z.'s Quite Note.",self.OnAbout),
                    ('Quit',"Quit the program without saving.",self.OnQuit))
        return menudata
        
        
    def CreatePopupMenu(self):
        menu = wx.Menu()
        for eachItem in self.menuData():
            if eachItem=='Separator':
                menu.AppendSeparator()
            else:
                name = eachItem[0]
                hint = eachItem[1]
                handler = eachItem[2]
                menuItem = menu.Append(-1,name,hint)   # Add menuitem to this menu
                self.Bind(wx.EVT_MENU,handler,menuItem)   # Bind menuitem with correspond function
        return menu
    
                
    # all event bind functions below are redirected to mainframe object, as the main frame is the container of main record
    def OnNew(self,evt):
        self.mainframe.OnNew()
        
    def OnShow(self,evt):
        self.mainframe.OnShow()
    
    def OnHide(self,evt):
        self.mainframe.OnHide()
    
    def OnClear(self,evt):
        self.mainframe.OnClear()
    
    def OnAbout(self,evt):
        self.mainframe.OnAbout()
    
    def OnQuit(self,evt):
        self.mainframe.OnQuit()
        self.Destroy()
        