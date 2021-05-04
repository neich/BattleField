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
## Class BE_GameDataExpansionCheckingsDlg
###########################################################################

class BE_GameDataExpansionCheckingsDlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Expanion checking years", pos = wx.DefaultPosition, size = wx.Size( 208,236 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer46 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer48 = wx.BoxSizer( wx.HORIZONTAL )
		
		listChoices = []
		self.list = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, listChoices, wx.LB_ALWAYS_SB|wx.LB_SINGLE|wx.LB_SORT )
		self.list.SetMinSize( wx.Size( 70,125 ) )
		
		bSizer48.Add( self.list, 0, wx.ALL, 5 )
		
		bSizer47 = wx.BoxSizer( wx.VERTICAL )
		
		self.buttonAdd = wx.Button( self, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer47.Add( self.buttonAdd, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.buttonDelete = wx.Button( self, wx.ID_ANY, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer47.Add( self.buttonDelete, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer48.Add( bSizer47, 1, wx.EXPAND, 5 )
		
		
		bSizer46.Add( bSizer48, 1, wx.EXPAND|wx.ALL, 5 )
		
		m_sdbSizer16 = wx.StdDialogButtonSizer()
		self.m_sdbSizer16OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer16.AddButton( self.m_sdbSizer16OK )
		self.m_sdbSizer16Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer16.AddButton( self.m_sdbSizer16Cancel )
		m_sdbSizer16.Realize();
		
		bSizer46.Add( m_sdbSizer16, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.SetSizer( bSizer46 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

