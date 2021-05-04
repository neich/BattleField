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
## Class BE_BackgroundHelperDlg
###########################################################################

class BE_BackgroundHelperDlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Background helper", pos = wx.DefaultPosition, size = wx.Size( 320,184 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer53 = wx.BoxSizer( wx.VERTICAL )
		
		self.checkActive = wx.CheckBox( self, wx.ID_ANY, u"Activate", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer53.Add( self.checkActive, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticText190 = wx.StaticText( self, wx.ID_ANY, u"Background file :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText190.Wrap( -1 )
		bSizer53.Add( self.m_staticText190, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer56 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.textFilename = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer56.Add( self.textFilename, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.butFileDlg = wx.Button( self, wx.ID_ANY, u"...", wx.DefaultPosition, wx.Size( 30,-1 ), 0 )
		bSizer56.Add( self.butFileDlg, 0, wx.ALL, 5 )
		
		
		bSizer53.Add( bSizer56, 0, wx.EXPAND, 5 )
		
		
		bSizer53.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		m_sdbSizer18 = wx.StdDialogButtonSizer()
		self.m_sdbSizer18OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer18.AddButton( self.m_sdbSizer18OK )
		self.m_sdbSizer18Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer18.AddButton( self.m_sdbSizer18Cancel )
		m_sdbSizer18.Realize();
		
		bSizer53.Add( m_sdbSizer18, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.SetSizer( bSizer53 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

