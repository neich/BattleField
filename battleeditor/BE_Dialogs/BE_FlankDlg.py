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
## Class BE_FlankDlg
###########################################################################

class BE_FlankDlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Flank", pos = wx.DefaultPosition, size = wx.Size( 565,507 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer43 = wx.BoxSizer( wx.VERTICAL )
		
		gSizer49 = wx.GridSizer( 0, 5, 0, 0 )
		
		self.m_staticText177 = wx.StaticText( self, wx.ID_ANY, u"Battle year :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText177.Wrap( -1 )
		gSizer49.Add( self.m_staticText177, 0, wx.ALL, 5 )
		
		comboYearChoices = []
		self.comboYear = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, comboYearChoices, wx.CB_DROPDOWN|wx.CB_READONLY|wx.CB_SIMPLE|wx.CB_SORT )
		gSizer49.Add( self.comboYear, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		gSizer49.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.lblstand = wx.StaticText( self, wx.ID_ANY, u"Stand distance :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblstand.Wrap( -1 )
		gSizer49.Add( self.lblstand, 0, wx.ALL, 5 )
		
		self.textStandDistance = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer49.Add( self.textStandDistance, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer43.Add( gSizer49, 0, wx.EXPAND|wx.ALL, 5 )
		
		self.panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		staticBox = wx.StaticBoxSizer( wx.StaticBox( self.panel, wx.ID_ANY, u"Battalions units" ), wx.VERTICAL )
		
		gSizer54 = wx.GridSizer( 0, 2, 0, 0 )
		
		frameInfantry = wx.StaticBoxSizer( wx.StaticBox( self.panel, wx.ID_ANY, u"Infantry" ), wx.VERTICAL )
		
		self.panelInfantry = wx.Panel( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gridInfantry = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText178 = wx.StaticText( self.panelInfantry, wx.ID_ANY, u"Number :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText178.Wrap( -1 )
		gridInfantry.Add( self.m_staticText178, 0, wx.ALL, 5 )
		
		self.textInfantryNumber = wx.TextCtrl( self.panelInfantry, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gridInfantry.Add( self.textInfantryNumber, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText179 = wx.StaticText( self.panelInfantry, wx.ID_ANY, u"Battalion size :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText179.Wrap( -1 )
		gridInfantry.Add( self.m_staticText179, 0, wx.ALL, 5 )
		
		self.textInfantryBattalionSize = wx.TextCtrl( self.panelInfantry, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gridInfantry.Add( self.textInfantryBattalionSize, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText180 = wx.StaticText( self.panelInfantry, wx.ID_ANY, u"Group size :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText180.Wrap( -1 )
		gridInfantry.Add( self.m_staticText180, 0, wx.ALL, 5 )
		
		self.textInfantryGroupSize = wx.TextCtrl( self.panelInfantry, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gridInfantry.Add( self.textInfantryGroupSize, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText181 = wx.StaticText( self.panelInfantry, wx.ID_ANY, u"Group distance :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText181.Wrap( -1 )
		gridInfantry.Add( self.m_staticText181, 0, wx.ALL, 5 )
		
		self.textInfantryGroupDistance = wx.TextCtrl( self.panelInfantry, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gridInfantry.Add( self.textInfantryGroupDistance, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panelInfantry.SetSizer( gridInfantry )
		self.panelInfantry.Layout()
		gridInfantry.Fit( self.panelInfantry )
		frameInfantry.Add( self.panelInfantry, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		gSizer54.Add( frameInfantry, 0, wx.EXPAND|wx.ALL, 5 )
		
		frameArchers = wx.StaticBoxSizer( wx.StaticBox( self.panel, wx.ID_ANY, u"Archers" ), wx.VERTICAL )
		
		self.panelArchers = wx.Panel( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gridArchers = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText1781 = wx.StaticText( self.panelArchers, wx.ID_ANY, u"Number :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1781.Wrap( -1 )
		gridArchers.Add( self.m_staticText1781, 0, wx.ALL, 5 )
		
		self.textArchersNumber = wx.TextCtrl( self.panelArchers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gridArchers.Add( self.textArchersNumber, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText1791 = wx.StaticText( self.panelArchers, wx.ID_ANY, u"Battalion size :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1791.Wrap( -1 )
		gridArchers.Add( self.m_staticText1791, 0, wx.ALL, 5 )
		
		self.textArchersBattalionSize = wx.TextCtrl( self.panelArchers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gridArchers.Add( self.textArchersBattalionSize, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText1801 = wx.StaticText( self.panelArchers, wx.ID_ANY, u"Group size :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1801.Wrap( -1 )
		gridArchers.Add( self.m_staticText1801, 0, wx.ALL, 5 )
		
		self.textArchersGroupSize = wx.TextCtrl( self.panelArchers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gridArchers.Add( self.textArchersGroupSize, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText1811 = wx.StaticText( self.panelArchers, wx.ID_ANY, u"Group distance :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1811.Wrap( -1 )
		gridArchers.Add( self.m_staticText1811, 0, wx.ALL, 5 )
		
		self.textArchersGroupDistance = wx.TextCtrl( self.panelArchers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gridArchers.Add( self.textArchersGroupDistance, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panelArchers.SetSizer( gridArchers )
		self.panelArchers.Layout()
		gridArchers.Fit( self.panelArchers )
		frameArchers.Add( self.panelArchers, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		gSizer54.Add( frameArchers, 0, wx.EXPAND|wx.ALL, 5 )
		
		frameCannons = wx.StaticBoxSizer( wx.StaticBox( self.panel, wx.ID_ANY, u"Cannons" ), wx.VERTICAL )
		
		self.panelCannons = wx.Panel( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gridCannons = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText17811 = wx.StaticText( self.panelCannons, wx.ID_ANY, u"Number :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17811.Wrap( -1 )
		gridCannons.Add( self.m_staticText17811, 0, wx.ALL, 5 )
		
		self.textCannonsNumber = wx.TextCtrl( self.panelCannons, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gridCannons.Add( self.textCannonsNumber, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText17911 = wx.StaticText( self.panelCannons, wx.ID_ANY, u"Battalion size :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17911.Wrap( -1 )
		gridCannons.Add( self.m_staticText17911, 0, wx.ALL, 5 )
		
		self.textCannonsBattalionSize = wx.TextCtrl( self.panelCannons, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gridCannons.Add( self.textCannonsBattalionSize, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText18011 = wx.StaticText( self.panelCannons, wx.ID_ANY, u"Group size :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18011.Wrap( -1 )
		gridCannons.Add( self.m_staticText18011, 0, wx.ALL, 5 )
		
		self.textCannonsGroupSize = wx.TextCtrl( self.panelCannons, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gridCannons.Add( self.textCannonsGroupSize, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText18111 = wx.StaticText( self.panelCannons, wx.ID_ANY, u"Group distance :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18111.Wrap( -1 )
		gridCannons.Add( self.m_staticText18111, 0, wx.ALL, 5 )
		
		self.textCannonsGroupDistance = wx.TextCtrl( self.panelCannons, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gridCannons.Add( self.textCannonsGroupDistance, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panelCannons.SetSizer( gridCannons )
		self.panelCannons.Layout()
		gridCannons.Fit( self.panelCannons )
		frameCannons.Add( self.panelCannons, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		gSizer54.Add( frameCannons, 0, wx.EXPAND|wx.ALL, 5 )
		
		frameSiegeTowers = wx.StaticBoxSizer( wx.StaticBox( self.panel, wx.ID_ANY, u"Siege Towers" ), wx.VERTICAL )
		
		self.panelSiegeTowers = wx.Panel( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gridSiegeTowers = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText178111 = wx.StaticText( self.panelSiegeTowers, wx.ID_ANY, u"Number :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText178111.Wrap( -1 )
		gridSiegeTowers.Add( self.m_staticText178111, 0, wx.ALL, 5 )
		
		self.textSiegeTowersNumber = wx.TextCtrl( self.panelSiegeTowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gridSiegeTowers.Add( self.textSiegeTowersNumber, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText179111 = wx.StaticText( self.panelSiegeTowers, wx.ID_ANY, u"Battalion size :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText179111.Wrap( -1 )
		gridSiegeTowers.Add( self.m_staticText179111, 0, wx.ALL, 5 )
		
		self.textSiegeTowersBattalionSize = wx.TextCtrl( self.panelSiegeTowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gridSiegeTowers.Add( self.textSiegeTowersBattalionSize, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText180111 = wx.StaticText( self.panelSiegeTowers, wx.ID_ANY, u"Group size :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText180111.Wrap( -1 )
		gridSiegeTowers.Add( self.m_staticText180111, 0, wx.ALL, 5 )
		
		self.textSiegeTowersGroupSize = wx.TextCtrl( self.panelSiegeTowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gridSiegeTowers.Add( self.textSiegeTowersGroupSize, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText181111 = wx.StaticText( self.panelSiegeTowers, wx.ID_ANY, u"Group distance :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText181111.Wrap( -1 )
		gridSiegeTowers.Add( self.m_staticText181111, 0, wx.ALL, 5 )
		
		self.textSiegeTowersGroupDistance = wx.TextCtrl( self.panelSiegeTowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gridSiegeTowers.Add( self.textSiegeTowersGroupDistance, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panelSiegeTowers.SetSizer( gridSiegeTowers )
		self.panelSiegeTowers.Layout()
		gridSiegeTowers.Fit( self.panelSiegeTowers )
		frameSiegeTowers.Add( self.panelSiegeTowers, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		gSizer54.Add( frameSiegeTowers, 0, wx.EXPAND|wx.ALL, 5 )
		
		
		staticBox.Add( gSizer54, 0, wx.EXPAND|wx.ALL, 5 )
		
		
		self.panel.SetSizer( staticBox )
		self.panel.Layout()
		staticBox.Fit( self.panel )
		bSizer43.Add( self.panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		m_sdbSizer14 = wx.StdDialogButtonSizer()
		self.m_sdbSizer14OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer14.AddButton( self.m_sdbSizer14OK )
		self.m_sdbSizer14Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer14.AddButton( self.m_sdbSizer14Cancel )
		m_sdbSizer14.Realize();
		
		bSizer43.Add( m_sdbSizer14, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.SetSizer( bSizer43 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

