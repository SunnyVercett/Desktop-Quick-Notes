#! /usr/bin/env python
#coding=utf-8

import wx


class NotePatchFrame(wx.Frame):
    def __init__(self,parent=None,id=-1,color=(255,255,200),pos=(400,300),size=(400,400), 
                content="Welcome to a new note! \nDouble click this note to edit its text. \nOr right click to show options.", 
                font=None, fontColor=(0,0,0), onTop=False):
                    
        self.frameStyle = wx.DEFAULT_FRAME_STYLE^wx.CAPTION|wx.FRAME_NO_TASKBAR
        wx.Frame.__init__(self,parent,id,pos=pos,size=size,style=self.frameStyle)
        
        # set up a series of default values
        self.bAlwaysOnTop = onTop
        self.tFramePos = pos
        self.tBackColor = color
        self.tPatchSize = size
        self.sContent = content
        self.tFontColor = fontColor
        
        self.tMousePos = self.ScreenToClient(wx.GetMousePosition())
        self.bChangeText = False
        if font==None:    # putting this wx.Font object as a argument will cause an error, so put it here
            self.font = wx.Font(16,wx.ROMAN,wx.NORMAL,wx.NORMAL)
            self.iFontSize = 16
        else:
            self.font = font
            self.iFontSize = self.font.GetPointSize()
        
        self.setContextMenu()
        self.SetMinSize((200,200))
        self.SetBackgroundColour(self.tBackColor)
        if self.bAlwaysOnTop:
            self.SetWindowStyle(frameStyle|wx.STAY_ON_TOP)
        
        # set up the elements in the frame
        self.textDisplay = wx.StaticText(parent=self,id=-1,label=self.sContent,pos=(5,5),style=wx.TE_MULTILINE|wx.ST_ELLIPSIZE_END)
        self.textDisplay.SetForegroundColour(self.tFontColor)
        self.textDisplay.SetBackgroundColour(self.tBackColor)
        self.textDisplay.SetFont(self.font)
        
        self.textEdit = wx.TextCtrl(parent=self,id=-1,value=self.sContent,pos=(3,3),style=wx.TE_MULTILINE)
        self.textEdit.SetForegroundColour(self.tFontColor)
        self.textEdit.SetBackgroundColour(self.tBackColor)
        self.textEdit.SetFont(self.font)
        self.textEdit.Hide()
        
        self.SetTextSize()
        
        self.finishButton = wx.Button(parent=self,id=-1,size=(200,60),label='Finish')
        self.SetButtonPos()
        
        # bind events
        # event 1 - drag the note patch
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.textDisplay.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.textDisplay.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.textDisplay.Bind(wx.EVT_MOTION, self.OnMouseMove)
        
        # event 2 - start to edit the content
        #self.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.textDisplay.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)    # double click on the test alse trigger the changing text event
        
        # event 3 - finish editing
        self.Bind(wx.EVT_BUTTON,self.OnFinish,self.finishButton)
        
        # event 4 - right click to open a context menu
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        self.textDisplay.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        
        # event 5 - resize the frame
        self.Bind(wx.EVT_SIZE, self.OnResize)
                
        
    def setContextMenu(self):
        contextMenuItems = (('Edit','Edit the content of this note.',self.OnEdit),
                            ('Font','Change the font of the text in this note.',self.OnFont),
                            ('Color','Change the background color of the text in this note.',self.OnColor),
                            'S',
                            ('C_Always on top','Toggle whether this note is always on top.',self.OnAlwaysOnTop),
                            'S',
                            ('Delete','Renove this note.',self.OnDelete),
                            )
                            
        self.contextMenu = wx.Menu()
        for eachItem in contextMenuItems:
            if eachItem=='S':    # otherwise it's a tuple
                self.contextMenu.AppendSeparator()
            elif eachItem[0][0:2]=='C_':
                name = eachItem[0][2:]
                hint = eachItem[1]
                handler = eachItem[2]
                menuItem = self.contextMenu.AppendCheckItem(-1,name,hint)
            else:
                name = eachItem[0]
                hint = eachItem[1]
                handler = eachItem[2]
                menuItem = self.contextMenu.Append(-1,name,hint)   # Add menu item to this menu
            self.Bind(wx.EVT_MENU,handler,menuItem)   # Bind menu item with correspond function

            # this is a script-specialized operation
            if eachItem[0]=='C_Always on top':
                self.alwaysOnTopMenuItemId = menuItem.GetId()
                self.contextMenu.Check(self.alwaysOnTopMenuItemId, self.bAlwaysOnTop)
                
    
    def SetTextSize(self):
        textLines = 1+self.sContent.count('\n')
        self.textEditSize = (self.tPatchSize[0]-20,5*textLines*self.iFontSize)
        if self.textEditSize[1]>self.tPatchSize[1]-100:
            self.textEditSize = self.tPatchSize[0]-20,self.tPatchSize[1]-100
        self.textEdit.SetSize(self.textEditSize)
        
        self.textDisplaySize = self.tPatchSize[0]-20,self.tPatchSize[1]-10
        self.textDisplay.SetSize(self.textDisplaySize)
        
    
    def SetButtonPos(self):
        pos_x = (self.Size.x-220)/2
        pos_y = self.textEdit.Size.y+10
        self.finishButton.SetPosition((pos_x,pos_y))
    
    
    def startEditing(self):
        self.textDisplay.Hide()
        self.textEdit.Show()
        self.bChangeText = True
        self.finishButton.Show()
        
    
    def finishEditing(self):
        self.sContent = self.textEdit.GetValue()
        self.textEdit.Hide()    # a wild guess works
        self.textDisplay.Show() 
        self.textDisplay.SetLabel(self.sContent)
        self.SetTextSize()
        self.SetButtonPos()
        self.bChangeText = False        
    
    
    def OnLeftDown(self,evt):
        if self.bChangeText:
            self.finishEditing()
        else:
            self.tMousePos = (evt.GetX(),evt.GetY())
            self.CaptureMouse()

    
    def OnMouseMove(self,evt):
        if not self.bChangeText:
            if evt.LeftIsDown() and self.HasCapture():
            # hasCapture() unexpectedly solve the problem that the frame moves after quiting edit mode with a click
            # it's just a wild try and i dont expect at all that it will work
                tMousePos2 = self.ClientToScreen(evt.GetPosition())
                track = (tMousePos2.x-self.tMousePos[0], tMousePos2.y-self.tMousePos[1])
                self.Move(track)
            self.tFramePos = self.GetPosition()
            
    
    def OnLeftUp(self,evt):
        if self.HasCapture():
            self.ReleaseMouse()

    
    def OnRightClick(self,evt):
        if not self.bChangeText:    # is not changing text, then this context menu is openable
            pos = evt.GetPosition()
            self.PopupMenu(self.contextMenu, pos)
            
            
    def OnDoubleClick(self,evt):
        self.startEditing()
        
        
    def OnEdit(self,event):
        self.startEditing()
        
        
    def OnFinish(self,evt):
        self.finishEditing()
        
        
    def OnFont(self,event):
        fontDialog = wx.FontDialog(parent=self,data=wx.FontData())
        if fontDialog.ShowModal() == wx.ID_OK:
            data = fontDialog.GetFontData()
            self.font = data.GetChosenFont()
            self.tFontColor = data.GetColour()
            self.sFontName = self.font.GetFaceName()
            self.iFontSize = self.font.GetPointSize()
        fontDialog.Destroy()
        self.textDisplay.SetFont(self.font)
        self.textDisplay.SetForegroundColour(self.tFontColor)    # the color of the text, not the backfround
        self.textEdit.SetFont(self.font)
        self.textEdit.SetForegroundColour(self.tFontColor)    # the color of the text, not the backfround
        self.SetTextSize()
        self.SetButtonPos()
        self.textDisplay.Show()
        self.textEdit.Hide()
        self.finishButton.Hide()
        
        
    def OnColor(self,event):
        colorDialog = wx.ColourDialog(parent=self)
        colorDialog.GetColourData().SetChooseFull(True)
        if colorDialog.ShowModal()==wx.ID_OK:
            data = colorDialog.GetColourData()
            self.tBackColor = data.GetColour().Get()
            # this frame is refreshed on the next event, so here's a forced refresh to show the color change
        colorDialog.Destroy()
        self.SetBackgroundColour(self.tBackColor)
        self.textDisplay.SetBackgroundColour(self.tBackColor)
        self.textEdit.SetBackgroundColour(self.tBackColor)
        self.Refresh(eraseBackground=True)
        
    
    def OnAlwaysOnTop(self,event):
        self.bAlwaysOnTop = self.contextMenu.IsChecked(self.alwaysOnTopMenuItemId)
        if self.bAlwaysOnTop:
            self.SetWindowStyle(self.frameStyle|wx.STAY_ON_TOP)
        else:
            self.SetWindowStyle(self.frameStyle)
        self.Refresh(eraseBackground=True)
    
    
    def OnDelete(self,event):
        parentFrame = self.GetParent()
        if parentFrame!=None:    # has a parent
            parentFrame.OnNoteDelete(self)
        
        self.Destroy()
        
        
    def OnResize(self,event):
        newSize = event.GetSize()    # a tuple
        self.tPatchSize = (newSize[0], newSize[1])
        self.SetTextSize()        
        self.SetButtonPos()
        
    
    
    
if __name__=="__main__":
    app = wx.App()
    frame = NotePatchFrame()
    frame.Show()
    app.MainLoop()