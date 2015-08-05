#!/usr/bin/python
# -*- coding: utf-8 -*-

# gotoclass.py

import wx
import os
from wrapper import Cipher
import sys

class AES_GUI(wx.Frame):

    def __init__(self, parent, title):
        self.cipher = Cipher()
        super(AES_GUI, self).__init__(parent, title=title,
            size=(960, 840))

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        taskList = ['IP Check', 'SRB Cipher', 'SRB Decipher', 'IP + SRB Cipher', 'SRB Decipher + IP',
                    'DRB Cipher', 'DRB Decipher']
        self.task = wx.RadioBox(panel, label='Task', choices=taskList)
        hbox0.Add(self.task,flag=wx.ALIGN_RIGHT|wx.ALL, border=20)
        vbox.Add(hbox0)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        directs = ['uplink', 'downlink']
        self.direction = wx.RadioBox(panel, label='Direction', choices=directs)
        hbox2.Add(self.direction,flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)
        cnt_lb = wx.StaticText(panel, label='Count')
        hbox2.Add(cnt_lb,flag=wx.ALIGN_RIGHT|wx.RIGHT|wx.TOP, border=20)
        self.cnt = wx.TextCtrl(panel)
        hbox2.Add(self.cnt,flag=wx.ALIGN_RIGHT|wx.RIGHT|wx.TOP, border=20)
        bearer_lb = wx.StaticText(panel, label='Bearer')
        hbox2.Add(bearer_lb,flag=wx.ALIGN_RIGHT|wx.RIGHT|wx.TOP, border=20)
        self.bearer = wx.TextCtrl(panel)
        hbox2.Add(self.bearer,flag=wx.ALIGN_RIGHT|wx.TOP, border=20)
        vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=20)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        key_lb = wx.StaticText(panel, label='   IP Key')
        hbox1.Add(key_lb,flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)
        self.key = wx.TextCtrl(panel)
        hbox1.Add(self.key, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=20)

        hbox1_SRB = wx.BoxSizer(wx.HORIZONTAL)
        key_lb_SRB = wx.StaticText(panel, label='SRB Key')
        hbox1_SRB.Add(key_lb_SRB,flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)
        self.key_SRB = wx.TextCtrl(panel)
        hbox1_SRB.Add(self.key_SRB, proportion=1)
        vbox.Add(hbox1_SRB, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=20)

        hbox1_DRB = wx.BoxSizer(wx.HORIZONTAL)
        key_lb_DRB = wx.StaticText(panel, label='DRB Key')
        hbox1_DRB.Add(key_lb_DRB,flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)
        self.key_DRB = wx.TextCtrl(panel)
        hbox1_DRB.Add(self.key_DRB, proportion=1)
        vbox.Add(hbox1_DRB, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=20)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        data_lb = wx.StaticText(panel, label='  Stream')
        hbox3.Add(data_lb,flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)
        self.data = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.data.SetMinSize(wx.Size(-1, 180))
        hbox3.Add(self.data, proportion=1,flag=wx.EXPAND|wx.BOTTOM, border=20)
        vbox.Add(hbox3, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=20)

        hbox3_btn = wx.BoxSizer(wx.HORIZONTAL)
        load = wx.Button(panel, label='Load')
        load.Bind(wx.EVT_BUTTON, self.onOpenFile)
        hbox3_btn.Add(load, flag = wx.ALIGN_RIGHT|wx.LEFT, border=52)
        clear = wx.Button(panel, label='Clear')
        clear.Bind(wx.EVT_BUTTON, self.onClearData)
        hbox3_btn.Add(clear,flag=wx.ALIGN_RIGHT|wx.LEFT, border=10)
        vbox.Add(hbox3_btn, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=20)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        output_lb = wx.StaticText(panel, label='  Output')
        hbox4.Add(output_lb,flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)
        self.output = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.output.SetMinSize(wx.Size(-1, 180))
        hbox4.Add(self.output, proportion=1,flag=wx.EXPAND|wx.BOTTOM, border=20)
        vbox.Add(hbox4, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=20)

        hbox4_btn = wx.BoxSizer(wx.HORIZONTAL)
        process = wx.Button(panel, label='Process')
        process.Bind(wx.EVT_BUTTON, self.onProcess)
        hbox4_btn.Add(process, flag = wx.ALIGN_RIGHT|wx.LEFT, border=52)
        copy = wx.Button(panel, label='Copy')
        copy.Bind(wx.EVT_BUTTON, self.onCopy)
        hbox4_btn.Add(copy, flag = wx.ALIGN_RIGHT|wx.LEFT, border=10)
        clear = wx.Button(panel, label='Clear All')
        clear.Bind(wx.EVT_BUTTON, self.onClear)
        hbox4_btn.Add(clear,flag=wx.ALIGN_RIGHT|wx.LEFT, border=180)
        vbox.Add(hbox4_btn, proportion=1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=20)

        panel.SetSizer(vbox)

    def onProcess(self, event):
        try:
            task = self.task.GetStringSelection()
            direct = self.direction.GetStringSelection()
            if (self.cnt.GetValue()==''):
                wx.MessageBox('Count required!', 'Error')
                return
            else:
                count = int(self.cnt.GetValue(), 16)
            if (self.bearer.GetValue()==''):
                wx.MessageBox('Bearer required!', 'Error')
                return
            else:
                bearer = int(self.bearer.GetValue())
            if (self.data.GetValue()==''):
                wx.MessageBox('Data required!', 'Error')
                return
            else:
                data = self.data.GetValue().replace('0x', '')

            if task == 'IP Check':
                if self.key.GetValue() == '':
                    wx.MessageBox('IP Key required!', 'Error')
                    return
                else:
                    key = self.key.GetValue().replace('0x', '')
                self.output.SetValue(self.cipher.IP(key, count, direct, bearer, data))
            elif task == 'SRB Cipher':
                if self.key_SRB.GetValue() == '':
                    wx.MessageBox('SRB Key required!', 'Error')
                    return
                else:
                    key = self.key_SRB.GetValue().replace('0x', '')
                self.output.SetValue(self.cipher.encrypt(key, count, direct, bearer, data))
            elif task == 'SRB Decipher':
                if self.key_SRB.GetValue() == '':
                    wx.MessageBox('SRB Key required!', 'Error')
                    return
                else:
                    key = self.key_SRB.GetValue().replace('0x', '')
                self.output.SetValue(self.cipher.decrypt(key, count, direct, bearer, data))
            elif task == 'DRB Cipher':
                if self.key_DRB.GetValue() == '':
                    wx.MessageBox('SRB Key required!', 'Error')
                    return
                else:
                    key = self.key_DRB.GetValue().replace('0x', '')
                self.output.SetValue(self.cipher.encrypt(key, count, direct, bearer, data))
            elif task == 'DRB Cipher':
                if self.key_DRB.GetValue() == '':
                    wx.MessageBox('SRB Key required!', 'Error')
                    return
                else:
                    key = self.key_DRB.GetValue().replace('0x', '')
                self.output.SetValue(self.cipher.decrypt(key, count, direct, bearer, data))
            elif task == 'IP + SRB Cipher':
                if self.key.GetValue() == '':
                    wx.MessageBox('IP Key required!', 'Error')
                    return
                else:
                    key_IP = self.key.GetValue().replace('0x', '')
                if self.key_SRB.GetValue() == '':
                    wx.MessageBox('SRB Key required!', 'Error')
                    return
                else:
                    key_RSB = self.key_SRB.GetValue().replace('0x', '')
                self.output.SetValue(self.RSB_Cipher(key_IP, key_RSB, count, direct, bearer, data))
            elif task == 'SRB Decipher + IP':
                if self.key.GetValue() == '':
                    wx.MessageBox('IP Key required!', 'Error')
                    return
                else:
                    key_IP = self.key.GetValue().replace('0x', '')
                if self.key_SRB.GetValue() == '':
                    wx.MessageBox('SRB Key required!', 'Error')
                    return
                else:
                    key_RSB = self.key_SRB.GetValue().replace('0x', '')
                self.output.SetValue(self.RSB_Decipher(key_IP, key_RSB, count, direct, bearer, data))
            else:
                wx.MessageBox('Task invalid!', 'Error')
                return
        except:
            wx.MessageBox("Invalid input!", "Error")
            return

    def RSB_Cipher(self, key_IP, key_RSB, count, direct, bearer, data):
        mac_i = self.cipher.IP(key_IP, count, direct, bearer, data)
        ciphered = self.cipher.encrypt(key_RSB, count, direct, bearer, data[2:]+mac_i)
        return data[:2] + " " + ciphered[:-8] + " " + ciphered[-8:]

    def RSB_Decipher(self, key_IP, key_RSB, count, direct, bearer, data):
        deciphered = self.cipher.decrypt(key_RSB, count, direct, bearer, data[2:])
        ip = self.cipher.IP(key_IP, count, direct, bearer, data[:2]+deciphered[:-8])
        if ip == deciphered[-8:]:
            ip_check = 'pass'
        else:
            ip_check = 'fail'
        return data[:2] + "  " + deciphered[:-8] + " " + deciphered[-8:] + " " + ip_check

    def onClear(self, event):
        for ctrlText in [self.key, self.cnt, self.bearer, self.data, self.output]:
            ctrlText.SetValue('')

    def onClearData(self, event):
        self.data.SetValue('')

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
