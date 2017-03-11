#! /usr/bin/env python
#coding=utf-8

import wx
import os

from noteFrame import *
from aboutFrame import *


class QuickNoteMainFrame(wx.Frame):
    def __init__(self,parent=None,id=-1):
        screenResolution = wx.GetDisplaySize()
        frameStyle = wx.FRAME_NO_TASKBAR|wx.MINIMIZE
        wx.Frame.__init__(self,parent,id,pos=(screenResolution.x/2-160,screenResolution.y/2-120),size=(320,240),style=frameStyle)
        
        #self.SZCreateMenuBar()
        
        self.filename = "./lastNotes.szz"
        self.thisPos = (400,300)
        self.dNoteDict = {}
        self.iNoteCount = 0
        
        try:
            self.OnStart()
        except IOError:
            pass
        
        
    def menuData(self):
        menudata = (('File',
                        ('New Note',"Create a new quick note.",self.OnNew),
                        ('Clear',"Delete all quick notes.",self.OnClear),
                        ('Separator'),
                        ('Quit',"Quit the program without saving.",self.OnQuit)
                    ),
                    ('Edit',
                        ('Options',"View and change the options of notes.",self.OnOption)
                    ),
                    ('Help',
                        ('About',"About S.Z.'s Quite Note.",self.OnAbout)
                    ))
        return menudata
    
    
    def SZCreateMenuBar(self):
        self.menubar = wx.MenuBar()
        for eachMenu in self.menuData():
            menuLabel = eachMenu[0]
            menuItems = eachMenu[1:]
            menu = self.SZCreateMenu(menuLabel,menuItems)
            self.menubar.Append(menu,menuLabel)   # Add this menu to menubar
        self.SetMenuBar(self.menubar)
    
    
    def SZCreateMenu(self,menuLabel,menuItems):
        menu = wx.Menu()
        for eachItem in menuItems:
            if eachItem=='Separator':
                menu.AppendSeparator()
            else:
                name = eachItem[0]
                hint = eachItem[1]
                handler = eachItem[2]
                menuItem = menu.Append(-1,name,hint)   # Add menuitem to this menu
                self.Bind(wx.EVT_MENU,handler,menuItem)   # Bind menuitem with correspond function
        return menu
    
    
    def writeFile(self,_list):
        f = open(self.filename, 'w')
        for eachItem in _list:
            try:
                assert type(eachItem)==type({0:'a'})    # ensure that _list is a list of dictionaries
            except AssertionError:
                raise AssertionError
            
            for eachKey in eachItem:
                f.write("%s::::%s,,,," %(eachKey,eachItem[eachKey]))
                # in case the content of a note has the same symbol. symbol :::: or ,,,, is much more rare 
            f.write("\n")
        f.close()
        
        
    def readFile(self):
        f = open(self.filename, 'r')
        _list = []
        
        for line in f:
            _dict = {}
            line = line.split(',,,,')
            for element in line:
                if '\n' in element:
                    continue    # skip the \n at the end of each line
                
                element = element.split('::::')
                key = element[0]
                value = eval(element[1])    # read a string and convert it to the type according to its format
                    
                _dict[key] = value
                
            _list += [_dict]
            
        while {} in _list:
            del _list[_list.index({})]
            
        return _list
        
        
    def OnNoteDelete(self,child):    # the delete operation is conducted in a sibling
        self.iNoteCount -= 1
        for eachNoteKey in self.dNoteDict:
            if self.dNoteDict[eachNoteKey] is child:    # be noted the use of 'is'
            # only to use a dictionary will make the memory address in main record equal to the note frame
                del self.dNoteDict[eachNoteKey]
                break
        
        
    def OnStart(self):
        lStartList = self.readFile()    # type conversion is completed in this function
        
        for eachNote in lStartList:
            assert type(eachNote)==type({0:0})
            
            color = eachNote['color']
            size = eachNote['size']
            pos = eachNote['pos']
            content = eachNote['content'].replace('SZSaysNewline','\n')
            # font description
            fontDescription = eachNote['fontDescription']    # a tuple
            fontSize = fontDescription[0]
            fontFamily = fontDescription[1]
            fontStyle = fontDescription[2]
            fontWeight = fontDescription[3]
            fontUnderlined = fontDescription[4]
            fontFaceName = fontDescription[5]
            fontEncoding = fontDescription[6]
            # font description ends
            fontColor = eachNote['fontColor']
            onTop = eachNote['onTop']
            
            font = wx.Font(fontSize,fontFamily,fontStyle,fontWeight,fontUnderlined,fontFaceName,fontEncoding)
            thisNote = NotePatchFrame(parent=self, color=color, pos=pos, size=size, 
                                    content=content, font=font, fontColor=fontColor, onTop=onTop)
            thisNote.Show()
            
            self.iNoteCount += 1
            noteName = 'note%d' %self.iNoteCount
            self.dNoteDict[noteName] = thisNote
        
        if self.iNoteCount==0:
            thisNote = NotePatchFrame(parent=self)
            thisNote.Show()
            self.iNoteCount += 1
            noteName = 'note%d' %self.iNoteCount
            self.dNoteDict[noteName] = thisNote
            
        
    def OnNew(self):
        newNote = NotePatchFrame(parent=self,pos=self.thisPos)
        newNote.Show()
        
        nextPos_x = self.thisPos[0]+50
        nextPos_y = self.thisPos[1]+50
        self.thisPos = (nextPos_x,nextPos_y)
        
        self.iNoteCount += 1
        noteName = 'note%d' %self.iNoteCount
        self.dNoteDict[noteName] = newNote
        
        
    def OnShow(self):
        for eachKey in self.dNoteDict:
            eachNote = self.dNoteDict[eachKey]
            eachNote.Show()
            eachNote.SetFocus()
        
        
    def OnHide(self):
        for eachKey in self.dNoteDict:
            eachNote = self.dNoteDict[eachKey]
            eachNote.Hide()
        
    
    def OnClear(self):
        for eachNoteKey in self.dNoteDict:
            self.dNoteDict[eachNoteKey].NoteDelete()
            # call Close() on every note, or every note should have a close method
            
        self.iNoteCount = 0
        self.dNoteDict.clear()
        
        
    def OnQuit(self):
        lQuitList = []
        for eachNoteKey in self.dNoteDict:
            dQuitDict = {}
            dQuitDict['color'] = self.dNoteDict[eachNoteKey].tBackColor
            dQuitDict['size'] = self.dNoteDict[eachNoteKey].tPatchSize
            dQuitDict['pos'] = self.dNoteDict[eachNoteKey].GetPosition()
            dQuitDict['content'] = "'%s'" %self.dNoteDict[eachNoteKey].sContent.replace('\n','SZSaysNewline')
            # font description
            fontSize = self.dNoteDict[eachNoteKey].font.GetPointSize()
            fontFamily = self.dNoteDict[eachNoteKey].font.GetFamily()
            fontStyle = self.dNoteDict[eachNoteKey].font.GetStyle()
            fontWeight = self.dNoteDict[eachNoteKey].font.GetWeight()
            fontUnderlined = self.dNoteDict[eachNoteKey].font.GetUnderlined()
            fontFaceName = self.dNoteDict[eachNoteKey].font.GetFaceName()
            fontEncoding = self.dNoteDict[eachNoteKey].font.GetEncoding()
            dQuitDict['fontDescription'] = (fontSize,fontFamily,fontStyle,fontWeight,fontUnderlined,fontFaceName,fontEncoding)
            # font description ends
            #dQuitDict['font'] = self.dNoteDict[eachNoteKey].font
            dQuitDict['fontColor'] = self.dNoteDict[eachNoteKey].tFontColor
            dQuitDict['onTop'] = self.dNoteDict[eachNoteKey].bAlwaysOnTop
            
            lQuitList += [dQuitDict]
            
            self.dNoteDict[eachNoteKey].Close(True)
            # call Close() on every note, or every note should have its own close method
        
        self.writeFile(lQuitList)
        self.Close()
        #self.trayIcon.Destroy()
        # has the trayIcon attribute, but this access will be denied, because the frame has always been deleted
    
    
    def OnOption(self,evt):
        pass
    
    
    def OnAbout(self):
        aboutFrame = AboutDialog(parent=self)
        aboutFrame.Show()
    
    
    
    
if __name__=='__main__':
    app = wx.App()
    frame = QuickNoteMainFrame()
    frame.Show()
    app.MainLoop()
