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
## Class BE_BattleDlg
###########################################################################

class BE_BattleDlg ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Battle", pos = wx.DefaultPosition, size = wx.Size( 257,285 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

		bSizer47 = wx.BoxSizer( wx.VERTICAL )

		gSizer48 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText174 = wx.StaticText( self, wx.ID_ANY, u"Year :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText174.Wrap( -1 )
		gSizer48.Add( self.m_staticText174, 0, wx.ALL, 5 )

		self.textYear = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer48.Add( self.textYear, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText175 = wx.StaticText( self, wx.ID_ANY, u"Simulations :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText175.Wrap( -1 )
		gSizer48.Add( self.m_staticText175, 0, wx.ALL, 5 )

		self.textNSimulations = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer48.Add( self.textNSimulations, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer47.Add( gSizer48, 0, wx.EXPAND|wx.ALL, 5 )

		self.checkRepeatuntil = wx.CheckBox( self, wx.ID_ANY, u"Repeat until defenders win", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer47.Add( self.checkRepeatuntil, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_panel49 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer31 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel49, wx.ID_ANY, u"Defenders" ), wx.VERTICAL )

		gSizer49 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText176 = wx.StaticText( self.m_panel49, wx.ID_ANY, u"Archers :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText176.Wrap( -1 )
		gSizer49.Add( self.m_staticText176, 0, wx.ALL, 5 )

		self.textArchers = wx.TextCtrl( self.m_panel49, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer49.Add( self.textArchers, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText177 = wx.StaticText( self.m_panel49, wx.ID_ANY, u"Cannons :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText177.Wrap( -1 )
		gSizer49.Add( self.m_staticText177, 0, wx.ALL, 5 )

		self.textCannons = wx.TextCtrl( self.m_panel49, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer49.Add( self.textCannons, 0, wx.ALL|wx.EXPAND, 5 )


		sbSizer31.Add( gSizer49, 0, wx.EXPAND|wx.ALL, 5 )


		self.m_panel49.SetSizer( sbSizer31 )
		self.m_panel49.Layout()
		sbSizer31.Fit( self.m_panel49 )
		bSizer47.Add( self.m_panel49, 1, wx.EXPAND |wx.ALL, 5 )



		m_sdbSizer14 = wx.StdDialogButtonSizer()
		self.m_sdbSizer14OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer14.AddButton( self.m_sdbSizer14OK )
		self.m_sdbSizer14Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer14.AddButton( self.m_sdbSizer14Cancel )
		m_sdbSizer14.Realize();

		bSizer47.Add( m_sdbSizer14, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.SetSizer( bSizer47 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


