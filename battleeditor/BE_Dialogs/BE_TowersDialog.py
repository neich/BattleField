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
## Class BE_TowersDlg
###########################################################################

class BE_TowersDlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Add Tower", pos = wx.DefaultPosition, size = wx.Size( 225,214 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		sizer = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel41 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerData = wx.BoxSizer( wx.VERTICAL )
		
		self.radioSquared = wx.RadioButton( self.m_panel41, wx.ID_ANY, u"Squared", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerData.Add( self.radioSquared, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.radioRounded = wx.RadioButton( self.m_panel41, wx.ID_ANY, u"Rounded", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerData.Add( self.radioRounded, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.radioRandom = wx.RadioButton( self.m_panel41, wx.ID_ANY, u"Random", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerData.Add( self.radioRandom, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		sizerData.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.checkClose = wx.CheckBox( self.m_panel41, wx.ID_ANY, u"Close castle", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerData.Add( self.checkClose, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.m_panel41.SetSizer( sizerData )
		self.m_panel41.Layout()
		sizerData.Fit( self.m_panel41 )
		sizer.Add( self.m_panel41, 1, wx.EXPAND |wx.ALL, 5 )
		
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
	

