#!/usr/bin/env python
import wx

from abipy.gui.eos import EosFrame

volumes = [13.72, 14.83, 16.0, 17.23, 18.52]
energies = [-56.29, -56.41, -56.46, -56.46, -56.42]

app = wx.App()
frame = EosFrame(None, volumes, energies)
frame.Show()
app.SetTopWindow(frame)
app.MainLoop()
