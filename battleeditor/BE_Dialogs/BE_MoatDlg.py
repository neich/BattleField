# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class BE_MoatDlg
###########################################################################

class BE_MoatDlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Moat", pos = wx.DefaultPosition, size = wx.Size( 211,143 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		sizer = wx.BoxSizer( wx.VERTICAL )
		
		self.panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerData = wx.BoxSizer( wx.VERTICAL )
		
		self.checkActive = wx.CheckBox( self.panel, wx.ID_ANY, u"Enable", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerData.Add( self.checkActive, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.checkHasWater = wx.CheckBox( self.panel, wx.ID_ANY, u"Has Water", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerData.Add( self.checkHasWater, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.panel.SetSizer( sizerData )
		self.panel.Layout()
		sizerData.Fit( self.panel )
		sizer.Add( self.panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		sizerOkCancel = wx.StdDialogButtonSizer()
		self.sizerOkCancelOK = wx.Button( self, wx.ID_OK )
		sizerOkCancel.AddButton( self.sizerOkCancelOK )
		self.sizerOkCancelCancel = wx.Button( self, wx.ID_CANCEL )
		sizerOkCancel.AddButton( self.sizerOkCancelCancel )
		sizerOkCancel.Realize();
		
		sizer.Add( sizerOkCancel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.SetSizer( sizer )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

