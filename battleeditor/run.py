import wx
import BE_MainWindow



app = wx.App(False)
frame = BE_MainWindow.BE_MainWindow(None)
frame.Show(True)
app.MainLoop()
