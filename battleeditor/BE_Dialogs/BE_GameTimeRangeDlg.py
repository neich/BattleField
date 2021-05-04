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
## Class BE_GameTimeRangeDlg
###########################################################################

class BE_GameTimeRangeDlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Time range (centuries)", pos = wx.DefaultPosition, size = wx.Size( 231,145 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer36 = wx.BoxSizer( wx.VERTICAL )
		
		gSizer43 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText161 = wx.StaticText( self, wx.ID_ANY, u"Start :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText161.Wrap( -1 )
		gSizer43.Add( self.m_staticText161, 0, wx.ALL, 5 )
		
		self.textTime1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer43.Add( self.textTime1, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText162 = wx.StaticText( self, wx.ID_ANY, u"End :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText162.Wrap( -1 )
		gSizer43.Add( self.m_staticText162, 0, wx.ALL, 5 )
		
		self.textTime2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer43.Add( self.textTime2, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer36.Add( gSizer43, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer36.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		m_sdbSizer9 = wx.StdDialogButtonSizer()
		self.m_sdbSizer9OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer9.AddButton( self.m_sdbSizer9OK )
		self.m_sdbSizer9Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer9.AddButton( self.m_sdbSizer9Cancel )
		m_sdbSizer9.Realize();
		
		bSizer36.Add( m_sdbSizer9, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.SetSizer( bSizer36 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

