#!/usr/bin/python
# -*- coding: utf-8 -*-

# gotoclass.py

import wx
import os
from wrapper import Cipher
from crypt_bat_bk import AES_Batch

class AES_GUI(wx.Frame):
  
    def __init__(self, parent, title):
        super(AES_GUI, self).__init__(parent, title=title,
            size=(480, 200))
        self.cipher = AES_Batch()
        self.InitUI()
        self.Centre()
        self.Show()     
        
    def InitUI(self):
    
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        input_lb = wx.StaticText(panel, label='Batch from:')
        hbox1.Add(input_lb, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)
        self.input = wx.TextCtrl(panel)
        hbox1.Add(self.input, proportion=1)
        load = wx.Button(panel, label='Load')
        load.Bind(wx.EVT_BUTTON, self.onOpenFile)
        hbox1.Add(load, flag=wx.ALIGN_RIGHT|wx.LEFT, border=10)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.ALL, border=20)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        output_lb = wx.StaticText(panel, label='Batch to:')
        hbox2.Add(output_lb, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)
        self.output = wx.TextCtrl(panel)
        hbox2.Add(self.output, proportion=1)
        load2 = wx.Button(panel, label='Load')
        load2.Bind(wx.EVT_BUTTON, self.onOpenFile2)
        hbox2.Add(load2, flag=wx.ALIGN_RIGHT|wx.LEFT, border=10)
        vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=20)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        process = wx.Button(panel, label='Process')
        process.Bind(wx.EVT_BUTTON, self.onProcess)
        hbox3.Add(process, flag=wx.ALIGN_CENTER|wx.EXPAND, proportion=1)
        vbox.Add(hbox3, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=20)

        panel.SetSizer(vbox)

    def onProcess(self, event):
        msg = self.cipher.parseBatch(self.input.GetValue(), self.output.GetValue())
        if not msg == '':
            wx.MessageBox(msg, 'Error', wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox('Completed!', 'Completed', wx.OK | wx.ICON_INFORMATION)
    def onOpenFile(self, event):
        """
        Create and show the Open FileDialog
        """

        wildcard = "All files (*.csv)|*.csv"
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir= os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            self.input.SetValue(dlg.GetPath())
        dlg.Destroy()

    def onOpenFile2(self, event):
        """
        Create and show the Open FileDialog
        """
        wildcard = "All files (*.csv)|*.csv"
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir= os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
           self.output.SetValue(dlg.GetPath())
        dlg.Destroy()


if __name__ == '__main__':
    app = wx.App()
    AES_GUI(None, title='AES Crypto Tool (Batch)')
    app.MainLoop()