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
## Class BE_GameStartFortressDlg
###########################################################################

class BE_GameStarFortressDlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Star Fortress", pos = wx.DefaultPosition, size = wx.Size( 202,113 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer44 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer44.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.checkActivate = wx.CheckBox( self, wx.ID_ANY, u"Activate", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer44.Add( self.checkActivate, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer44.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		m_sdbSizer15 = wx.StdDialogButtonSizer()
		self.m_sdbSizer15OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer15.AddButton( self.m_sdbSizer15OK )
		self.m_sdbSizer15Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer15.AddButton( self.m_sdbSizer15Cancel )
		m_sdbSizer15.Realize();
		
		bSizer44.Add( m_sdbSizer15, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.SetSizer( bSizer44 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

