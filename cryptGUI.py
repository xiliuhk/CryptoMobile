#!/usr/bin/python
# -*- coding: utf-8 -*-

# gotoclass.py

import wx
import os
class AES_GUI(wx.Frame):
  
    def __init__(self, parent, title):
        super(AES_GUI, self).__init__(parent, title=title,
            size=(480, 400))
            
        self.InitUI()
        self.Centre()
        self.Show()     
        
    def InitUI(self):
    
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        taskList = ['IP', 'Cipher', 'Decipher']
        task = wx.RadioBox(panel, label='Task', choices=taskList)
        hbox0.Add(task,flag=wx.ALIGN_RIGHT|wx.ALL, border=20)
        directs = ['uplink', 'downlink']
        direction = wx.RadioBox(panel, label='Direction', choices=directs)
        hbox0.Add(direction,flag=wx.ALIGN_RIGHT|wx.ALL, border=20)
        vbox.Add(hbox0)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        key_lb = wx.StaticText(panel, label='Key')
        hbox1.Add(key_lb,flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)
        key = wx.TextCtrl(panel)
        hbox1.Add(key, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=20)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        cnt_lb = wx.StaticText(panel, label='Count')
        hbox2.Add(cnt_lb,flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)
        cnt = wx.TextCtrl(panel)
        hbox2.Add(cnt,flag=wx.ALIGN_RIGHT|wx.RIGHT, border=20)
        bearer_lb = wx.StaticText(panel, label='Bearer')
        hbox2.Add(bearer_lb,flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)
        bearer = wx.TextCtrl(panel)
        hbox2.Add(bearer)
        vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=20)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        vbox_data = wx.BoxSizer(wx.VERTICAL)
        data_lb = wx.StaticText(panel, label='Data')
        vbox_data.Add(data_lb)
        data = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        data.SetMinSize(wx.Size(-1, 105))
        vbox_data.Add(data, proportion=1,flag=wx.EXPAND|wx.BOTTOM, border=20)

        hbox_btn = wx.BoxSizer(wx.HORIZONTAL)
        load = wx.Button(panel, label='Load')
        load.Bind(wx.EVT_BUTTON, self.onOpenFile)
        hbox_btn.Add(load, flag = wx.ALIGN_LEFT|wx.RIGHT, border=40)
        process = wx.Button(panel, label='Process')
        hbox_btn.Add(process, flag = wx.ALIGN_RIGHT)
        vbox_data.Add(hbox_btn, proportion=1, flag=wx.EXPAND)
        vbox_data.SetMinSize(wx.Size(200, -1))
        hbox3.Add(vbox_data, proportion=1, flag=wx.EXPAND|wx.LEFT, border=20)

        vbox_out = wx.BoxSizer(wx.VERTICAL)
        out_lb = wx.StaticText(panel, label='Output')
        vbox_out.Add(out_lb)
        output = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        output.SetMinSize(wx.Size(-1, 100))
        vbox_out.Add(output, proportion=1, flag=wx.EXPAND|wx.BOTTOM, border=20)
        copy = wx.Button(panel, label='Copy')
        vbox_out.Add(copy, flag = wx.ALIGN_RIGHT)
        vbox_out.SetMinSize(wx.Size(200, -1))
        hbox3.Add(vbox_out, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=20)

        vbox.Add(hbox3, proportion=1)

        panel.SetSizer(vbox)


    def onOpenFile(self, event):
        """
        Create and show the Open FileDialog
        """

        wildcard = "Python source (*.py)|*.py|" \
                    "All files (*.*)|*.*"
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir= os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print "You chose the following file(s):"
            for path in paths:
                print path
        dlg.Destroy()

if __name__ == '__main__':
  
    app = wx.App()
    AES_GUI(None, title='AES Crypto Tool')
    app.MainLoop()