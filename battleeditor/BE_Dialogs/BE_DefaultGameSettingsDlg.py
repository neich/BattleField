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
## Class BE_DefaultGameSettings
###########################################################################

class BE_DefaultGameSettingsDlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Default game settings", pos = wx.DefaultPosition, size = wx.Size( 411,301 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer32 = wx.BoxSizer( wx.VERTICAL )
		
		gSizer56 = wx.GridSizer( 0, 2, 0, 150 )
		
		self.m_staticText202 = wx.StaticText( self, wx.ID_ANY, u"Speed :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText202.Wrap( -1 )
		gSizer56.Add( self.m_staticText202, 0, wx.ALL, 5 )
		
		self.textSpeed = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer56.Add( self.textSpeed, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText203 = wx.StaticText( self, wx.ID_ANY, u"Window size (squared) :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText203.Wrap( -1 )
		gSizer56.Add( self.m_staticText203, 0, wx.ALL, 5 )
		
		self.textWindowSize = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.textWindowSize.Enable( False )
		
		gSizer56.Add( self.textWindowSize, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText205 = wx.StaticText( self, wx.ID_ANY, u"Viewport size (squared) :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText205.Wrap( -1 )
		gSizer56.Add( self.m_staticText205, 0, wx.ALL, 5 )
		
		self.textViewportSize = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer56.Add( self.textViewportSize, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText207 = wx.StaticText( self, wx.ID_ANY, u"Height view height :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText207.Wrap( -1 )
		gSizer56.Add( self.m_staticText207, 0, wx.ALL, 5 )
		
		self.textHeightViewHeight = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer56.Add( self.textHeightViewHeight, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText208 = wx.StaticText( self, wx.ID_ANY, u"Height view width :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText208.Wrap( -1 )
		gSizer56.Add( self.m_staticText208, 0, wx.ALL, 5 )
		
		self.textHeightViewWidth = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer56.Add( self.textHeightViewWidth, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer32.Add( gSizer56, 0, wx.EXPAND|wx.ALL, 5 )
		
		self.checkShowGrid = wx.CheckBox( self, wx.ID_ANY, u"Show grid", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer32.Add( self.checkShowGrid, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer32.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		m_sdbSizer7 = wx.StdDialogButtonSizer()
		self.m_sdbSizer7OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer7.AddButton( self.m_sdbSizer7OK )
		self.m_sdbSizer7Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer7.AddButton( self.m_sdbSizer7Cancel )
		m_sdbSizer7.Realize();
		
		bSizer32.Add( m_sdbSizer7, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		
		self.SetSizer( bSizer32 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

