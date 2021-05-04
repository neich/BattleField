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
## Class BE_DefaultCitySettings
###########################################################################


# WARNING!! wxFormBuilderBug -> StaticBoxes must have only one children, a Panel. This can be done in the UI builder, but the other child controls, under the panel,
#                                set their parents as the staticbox, not the panel. If this is not solved, the program finishes without showing any warning or error message
#                               So, manual edition must be performed to change this. BE AWARE updating this file




class BE_DefaultCitySettingsDlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Default city settings", pos = wx.DefaultPosition, size = wx.Size( 374,614 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer31 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer41 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Houses" ), wx.VERTICAL )
		
		self.m_panel21 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer54 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText188 = wx.StaticText( self.m_panel21, wx.ID_ANY, u"Size :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText188.Wrap( -1 )
		gSizer54.Add( self.m_staticText188, 0, wx.ALL, 5 )
		
		self.textHousesSize = wx.TextCtrl( self.m_panel21, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer54.Add( self.textHousesSize, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText189 = wx.StaticText( self.m_panel21, wx.ID_ANY, u"Distance to wall :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText189.Wrap( -1 )
		gSizer54.Add( self.m_staticText189, 0, wx.ALL, 5 )
		
		self.textHousesDistanceWall = wx.TextCtrl( self.m_panel21, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer54.Add( self.textHousesDistanceWall, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText190 = wx.StaticText( self.m_panel21, wx.ID_ANY, u"Min distance between :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText190.Wrap( -1 )
		gSizer54.Add( self.m_staticText190, 0, wx.ALL, 5 )
		
		self.textHousesMinDistanceBetween = wx.TextCtrl( self.m_panel21, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer54.Add( self.textHousesMinDistanceBetween, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText191 = wx.StaticText( self.m_panel21, wx.ID_ANY, u"Max distance between :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText191.Wrap( -1 )
		gSizer54.Add( self.m_staticText191, 0, wx.ALL, 5 )
		
		self.textHousesMaxDistanceBetween = wx.TextCtrl( self.m_panel21, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer54.Add( self.textHousesMaxDistanceBetween, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText192 = wx.StaticText( self.m_panel21, wx.ID_ANY, u"Placement fuzzy factor :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText192.Wrap( -1 )
		gSizer54.Add( self.m_staticText192, 0, wx.ALL, 5 )
		
		self.textHousesPlacementFuzzy = wx.TextCtrl( self.m_panel21, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer54.Add( self.textHousesPlacementFuzzy, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText193 = wx.StaticText( self.m_panel21, wx.ID_ANY, u"Houses per year :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText193.Wrap( -1 )
		gSizer54.Add( self.m_staticText193, 0, wx.ALL, 5 )
		
		self.textHousesPerYear = wx.TextCtrl( self.m_panel21, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer54.Add( self.textHousesPerYear, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText194 = wx.StaticText( self.m_panel21, wx.ID_ANY, u"Preference factor :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText194.Wrap( -1 )
		gSizer54.Add( self.m_staticText194, 0, wx.ALL, 5 )
		
		self.textHousesPreference = wx.TextCtrl( self.m_panel21, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer54.Add( self.textHousesPreference, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel21.SetSizer( gSizer54 )
		self.m_panel21.Layout()
		gSizer54.Fit( self.m_panel21 )
		sbSizer41.Add( self.m_panel21, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer31.Add( sbSizer41, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		gSizer55 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText196 = wx.StaticText( self, wx.ID_ANY, u"Evolution speed :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText196.Wrap( -1 )
		gSizer55.Add( self.m_staticText196, 0, wx.ALL, 5 )
		
		self.textEvolutionSpeed = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer55.Add( self.textEvolutionSpeed, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText197 = wx.StaticText( self, wx.ID_ANY, u"Years per step :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText197.Wrap( -1 )
		gSizer55.Add( self.m_staticText197, 0, wx.ALL, 5 )
		
		self.textYearsPerStep = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer55.Add( self.textYearsPerStep, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText198 = wx.StaticText( self, wx.ID_ANY, u"Min wall length :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText198.Wrap( -1 )
		gSizer55.Add( self.m_staticText198, 0, wx.ALL, 5 )
		
		self.textMinWallLength = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer55.Add( self.textMinWallLength, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText199 = wx.StaticText( self, wx.ID_ANY, u"Max wall length :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText199.Wrap( -1 )
		gSizer55.Add( self.m_staticText199, 0, wx.ALL, 5 )
		
		self.textMaxWallLength = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer55.Add( self.textMaxWallLength, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText200 = wx.StaticText( self, wx.ID_ANY, u"Match vertices distance :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText200.Wrap( -1 )
		gSizer55.Add( self.m_staticText200, 0, wx.ALL, 5 )
		
		self.textMatchVerticesDistance = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer55.Add( self.textMatchVerticesDistance, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText201 = wx.StaticText( self, wx.ID_ANY, u"Wait battle :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText201.Wrap( -1 )
		gSizer55.Add( self.m_staticText201, 0, wx.ALL, 5 )
		
		self.textWaitBattle = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer55.Add( self.textWaitBattle, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer31.Add( gSizer55, 0, wx.EXPAND|wx.ALL, 5 )
		
		self.checkOldTownGrid = wx.CheckBox( self, wx.ID_ANY, u"Display OldTown Grid", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer31.Add( self.checkOldTownGrid, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer31.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		m_sdbSizer6 = wx.StdDialogButtonSizer()
		self.m_sdbSizer6OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer6.AddButton( self.m_sdbSizer6OK )
		self.m_sdbSizer6Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer6.AddButton( self.m_sdbSizer6Cancel )
		m_sdbSizer6.Realize();
		
		bSizer31.Add( m_sdbSizer6, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		
		self.SetSizer( bSizer31 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

