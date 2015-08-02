#!/usr/bin/python
# -*- coding: utf-8 -*-

# gotoclass.py

import wx
import os
from wrapper import Cipher

class AES_GUI(wx.Frame):
  
    def __init__(self, parent, title):
        self.cipher = Cipher()
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
        self.task = wx.RadioBox(panel, label='Task', choices=taskList)
        hbox0.Add(self.task,flag=wx.ALIGN_RIGHT|wx.ALL, border=20)
        directs = ['uplink', 'downlink']
        self.direction = wx.RadioBox(panel, label='Direction', choices=directs)
        hbox0.Add(self.direction,flag=wx.ALIGN_RIGHT|wx.ALL, border=20)
        vbox.Add(hbox0)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        key_lb = wx.StaticText(panel, label='Key')
        hbox1.Add(key_lb,flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)
        self.key = wx.TextCtrl(panel)
        hbox1.Add(self.key, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=20)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        cnt_lb = wx.StaticText(panel, label='Count')
        hbox2.Add(cnt_lb,flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)
        self.cnt = wx.TextCtrl(panel)
        hbox2.Add(self.cnt,flag=wx.ALIGN_RIGHT|wx.RIGHT, border=20)
        bearer_lb = wx.StaticText(panel, label='Bearer')
        hbox2.Add(bearer_lb,flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)
        self.bearer = wx.TextCtrl(panel)
        hbox2.Add(self.bearer)
        load = wx.Button(panel, label='Clear')
        load.Bind(wx.EVT_BUTTON, self.onClear)
        hbox2.Add(load,flag=wx.ALIGN_RIGHT|wx.LEFT, border=10)
        vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=20)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        vbox_data = wx.BoxSizer(wx.VERTICAL)
        data_lb = wx.StaticText(panel, label='Data')
        vbox_data.Add(data_lb)
        self.data = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.data.SetMinSize(wx.Size(-1, 105))
        vbox_data.Add(self.data, proportion=1,flag=wx.EXPAND|wx.BOTTOM, border=20)

        hbox_btn = wx.BoxSizer(wx.HORIZONTAL)
        load = wx.Button(panel, label='Load')
        load.Bind(wx.EVT_BUTTON, self.onOpenFile)
        hbox_btn.Add(load, flag = wx.ALIGN_LEFT|wx.RIGHT, border=40)
        process = wx.Button(panel, label='Process')
        process.Bind(wx.EVT_BUTTON, self.onProcess)

        hbox_btn.Add(process, flag = wx.ALIGN_RIGHT)
        vbox_data.Add(hbox_btn, proportion=1, flag=wx.EXPAND)
        vbox_data.SetMinSize(wx.Size(200, -1))
        hbox3.Add(vbox_data, proportion=1, flag=wx.EXPAND|wx.LEFT, border=20)

        vbox_out = wx.BoxSizer(wx.VERTICAL)
        out_lb = wx.StaticText(panel, label='Output')
        vbox_out.Add(out_lb)
        self.output = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.output.SetMinSize(wx.Size(-1, 100))
        vbox_out.Add(self.output, proportion=1, flag=wx.EXPAND|wx.BOTTOM, border=20)
        copy = wx.Button(panel, label='Copy')
        copy.Bind(wx.EVT_BUTTON, self.onCopy)
        vbox_out.Add(copy, flag = wx.ALIGN_RIGHT)
        vbox_out.SetMinSize(wx.Size(200, -1))
        hbox3.Add(vbox_out, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=20)

        vbox.Add(hbox3, proportion=1)

        panel.SetSizer(vbox)

    def onProcess(self, event):
        task = self.task.GetStringSelection()
        direct = self.direction.GetStringSelection()
        key = self.key.GetValue()
        count = int(self.cnt.GetValue(), 16)
        bearer = int(self.bearer.GetValue())
        data = self.data.GetValue()

        if task == 'IP':
            self.output.SetValue(self.cipher.IP(key, count, direct, bearer, data))
        elif task == 'Cipher':
            self.output.SetValue(self.cipher.encrypt(key, count, direct, bearer, data))
        else:
            self.output.SetValue(self.cipher.decrypt(key, count, direct, bearer, data))

    def onClear(self, event):
        for ctrlText in [self.key, self.cnt, self.bearer, self.data, self.output]:
            ctrlText.SetValue('')

    def onOpenFile(self, event):
        """
        Create and show the Open FileDialog
        """

        wildcard = "All files (*.*)|*.*"
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir= os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            file = open(dlg.GetPath(), 'r')
            self.data.SetValue(file.read())
            file.close()
        dlg.Destroy()

    def onCopy(self, event):
        """"""
        self.dataObj = wx.TextDataObject()
        self.dataObj.SetText(self.output.GetValue())
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(self.dataObj)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Unable to open the clipboard", "Error")

if __name__ == '__main__':
  
    app = wx.App()
    AES_GUI(None, title='AES Crypto Tool')
    app.MainLoop()