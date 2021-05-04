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
## Class BE_GameBattlesDlg
###########################################################################

class BE_GameBattlesDlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Battles", pos = wx.DefaultPosition, size = wx.Size( 208,223 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer44 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel48 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer45 = wx.BoxSizer( wx.HORIZONTAL )
		
		listChoices = []
		self.list = wx.ListBox( self.m_panel48, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, listChoices, wx.LB_ALWAYS_SB|wx.LB_SINGLE|wx.LB_SORT )
		self.list.SetMinSize( wx.Size( 70,125 ) )


		bSizer45.Add( self.list, 0, wx.ALL, 5 )
		
		
		bSizer45.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		bSizer46 = wx.BoxSizer( wx.VERTICAL )
		
		self.buttonAdd = wx.Button( self.m_panel48, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer46.Add( self.buttonAdd, 0, wx.ALL, 5 )
		
		self.buttonEdit = wx.Button( self.m_panel48, wx.ID_ANY, u"Edit", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer46.Add( self.buttonEdit, 0, wx.ALL, 5 )
		
		self.buttonDelete = wx.Button( self.m_panel48, wx.ID_ANY, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer46.Add( self.buttonDelete, 0, wx.ALL, 5 )
		
		
		bSizer45.Add( bSizer46, 0, wx.EXPAND|wx.ALL, 5 )
		
		
		self.m_panel48.SetSizer( bSizer45 )
		self.m_panel48.Layout()
		bSizer45.Fit( self.m_panel48 )
		bSizer44.Add( self.m_panel48, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.buttonClose = wx.Button( self, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.buttonClose.SetDefault() 
		bSizer44.Add( self.buttonClose, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.SetSizer( bSizer44 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.buttonClose.Bind( wx.EVT_BUTTON, self.OnClose )

	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnClose( self, event ):

		self.Destroy()
        #event.Skip()

	

