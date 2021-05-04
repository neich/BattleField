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
## Class BE_GameTypeDlg
###########################################################################

class BE_GameTypeDlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Game type", pos = wx.DefaultPosition, size = wx.Size( 217,159 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer35 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer35.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.optCityEvolution = wx.RadioButton( self, wx.ID_ANY, u"City Evolution", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer35.Add( self.optCityEvolution, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.optBattles = wx.RadioButton( self, wx.ID_ANY, u"Battles", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer35.Add( self.optBattles, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer35.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		m_sdbSizer8 = wx.StdDialogButtonSizer()
		self.m_sdbSizer8OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer8.AddButton( self.m_sdbSizer8OK )
		self.m_sdbSizer8Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer8.AddButton( self.m_sdbSizer8Cancel )
		m_sdbSizer8.Realize();
		
		bSizer35.Add( m_sdbSizer8, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.SetSizer( bSizer35 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

