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
## Class BE_GameBattlefieldDlg
###########################################################################

class BE_GameBattlefieldDlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Game battlefield", pos = wx.DefaultPosition, size = wx.Size( 257,147 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer37 = wx.BoxSizer( wx.VERTICAL )
		
		gSizer44 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.lableSize = wx.StaticText( self, wx.ID_ANY, u"Size :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lableSize.Wrap( -1 )
		gSizer44.Add( self.lableSize, 0, wx.ALL, 5 )
		
		self.textSize = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer44.Add( self.textSize, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.labelCellsize = wx.StaticText( self, wx.ID_ANY, u"Cell size :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelCellsize.Wrap( -1 )
		gSizer44.Add( self.labelCellsize, 0, wx.ALL, 5 )
		
		self.textCellSize = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer44.Add( self.textCellSize, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer37.Add( gSizer44, 0, wx.EXPAND|wx.ALL, 5 )
		
		m_sdbSizer10 = wx.StdDialogButtonSizer()
		self.m_sdbSizer10OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer10.AddButton( self.m_sdbSizer10OK )
		self.m_sdbSizer10Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer10.AddButton( self.m_sdbSizer10Cancel )
		m_sdbSizer10.Realize();
		
		bSizer37.Add( m_sdbSizer10, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.SetSizer( bSizer37 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

