#! /usr/bin/env python
#coding=utf-8

import wx.html


class AboutDialog(wx.Dialog):
    text = '''
    <html>
    <body bgcolor="#CCC660">
    <center>
    <table bgcolor="4545D1" width="100%" cellspacing="0" cellpadding="0" border="1">
    <tr>
        <td align="center"><hl>S.Z.'s Quick Note!</hl></td>
    </tr>
    </table>
    </center>
    <p><b>S.Z.'s Quick Note </b>is a little program developed by... somebody.</p>
    <p>Any question or suggestion, please contact s.vercett@gmail.com</p>
    '''
    
    def __init__(self,parent=None):
        wx.Dialog.__init__(self,parent,-1,"About SZ Note",size=(440,400))
        html = wx.html.HtmlWindow(self)
        html.SetPage(self.text)
        button = wx.Button(self,wx.ID_OK,"Okay")
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html,1,wx.EXPAND|wx.ALL,5)
        sizer.Add(button,0,wx.ALIGN_CENTER|wx.ALL,5)
        
        self.SetSizer(sizer)
        self.Layout()
        