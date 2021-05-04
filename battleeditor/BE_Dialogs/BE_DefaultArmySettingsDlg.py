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
## Class BE_DefaultArmySettings
###########################################################################



# WARNING!! wxFormBuilderBug -> StaticBoxes must have only one children, a Panel. This can be done in the UI builder, but the other child controls, under the panel,
#                                set their parents as the staticbox, not the panel. If this is not solved, the program finishes without showing any warning or error message
#                               So, manual edition must be performed to change this. BE AWARE updating this file



class BE_DefaultArmySettingsDlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Default army settings", pos = wx.DefaultPosition, size = wx.Size( 433,806 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		sizer = wx.BoxSizer( wx.VERTICAL )
		
		self.tabctrl = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.tabInfantry = wx.Panel( self.tabctrl, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerInfantry = wx.BoxSizer( wx.VERTICAL )
		
		gSizer25 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText81 = wx.StaticText( self.tabInfantry, wx.ID_ANY, u"Defense :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText81.Wrap( -1 )
		gSizer25.Add( self.m_staticText81, 0, wx.ALL, 5 )
		
		self.textInfantryDefense = wx.TextCtrl( self.tabInfantry, wx.ID_ANY, u"stationary", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer25.Add( self.textInfantryDefense, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText82 = wx.StaticText( self.tabInfantry, wx.ID_ANY, u"Attack :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText82.Wrap( -1 )
		gSizer25.Add( self.m_staticText82, 0, wx.ALL, 5 )
		
		self.textInfantryAttack = wx.TextCtrl( self.tabInfantry, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer25.Add( self.textInfantryAttack, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText83 = wx.StaticText( self.tabInfantry, wx.ID_ANY, u"Speed :  ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText83.Wrap( -1 )
		gSizer25.Add( self.m_staticText83, 0, wx.ALL, 5 )
		
		self.textInfantrySpeed = wx.TextCtrl( self.tabInfantry, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer25.Add( self.textInfantrySpeed, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText84 = wx.StaticText( self.tabInfantry, wx.ID_ANY, u"Reload :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText84.Wrap( -1 )
		gSizer25.Add( self.m_staticText84, 0, wx.ALL, 5 )
		
		self.textInfantryReload = wx.TextCtrl( self.tabInfantry, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer25.Add( self.textInfantryReload, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText85 = wx.StaticText( self.tabInfantry, wx.ID_ANY, u"Accuracy :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText85.Wrap( -1 )
		gSizer25.Add( self.m_staticText85, 0, wx.ALL, 5 )
		
		self.textInfantryAccuracy = wx.TextCtrl( self.tabInfantry, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer25.Add( self.textInfantryAccuracy, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText86 = wx.StaticText( self.tabInfantry, wx.ID_ANY, u"Distance :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText86.Wrap( -1 )
		gSizer25.Add( self.m_staticText86, 0, wx.ALL, 5 )
		
		self.textInfantryDistance = wx.TextCtrl( self.tabInfantry, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer25.Add( self.textInfantryDistance, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText87 = wx.StaticText( self.tabInfantry, wx.ID_ANY, u"Movement priority :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText87.Wrap( -1 )
		gSizer25.Add( self.m_staticText87, 0, wx.ALL, 5 )
		
		self.textInfantryMovementPriority = wx.TextCtrl( self.tabInfantry, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer25.Add( self.textInfantryMovementPriority, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		sizerInfantry.Add( gSizer25, 0, wx.EXPAND|wx.ALL, 5 )
		
		self.checkInfantryStationary = wx.CheckBox( self.tabInfantry, wx.ID_ANY, u"Stationary", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerInfantry.Add( self.checkInfantryStationary, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		sbSizer27 = wx.StaticBoxSizer( wx.StaticBox( self.tabInfantry, wx.ID_ANY, u"Bounding size" ), wx.VERTICAL )
		
		self.m_panel22 = wx.Panel( self.tabInfantry, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer27 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText91 = wx.StaticText( self.m_panel22, wx.ID_ANY, u"Length :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText91.Wrap( -1 )
		gSizer27.Add( self.m_staticText91, 0, wx.ALL, 5 )
		
		self.textInfantryBoundingLength = wx.TextCtrl( self.m_panel22, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer27.Add( self.textInfantryBoundingLength, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText92 = wx.StaticText( self.m_panel22, wx.ID_ANY, u"Height :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText92.Wrap( -1 )
		gSizer27.Add( self.m_staticText92, 0, wx.ALL, 5 )
		
		self.textInfantryBoundingHeight = wx.TextCtrl( self.m_panel22, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer27.Add( self.textInfantryBoundingHeight, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText93 = wx.StaticText( self.m_panel22, wx.ID_ANY, u"Width :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText93.Wrap( -1 )
		gSizer27.Add( self.m_staticText93, 0, wx.ALL, 5 )
		
		self.textInfantryBoundingWidth = wx.TextCtrl( self.m_panel22, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer27.Add( self.textInfantryBoundingWidth, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel22.SetSizer( gSizer27 )
		self.m_panel22.Layout()
		gSizer27.Fit( self.m_panel22 )
		sbSizer27.Add( self.m_panel22, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		sizerInfantry.Add( sbSizer27, 0, wx.EXPAND|wx.ALL, 5 )
		
		sbSizer26 = wx.StaticBoxSizer( wx.StaticBox( self.tabInfantry, wx.ID_ANY, u"Climbing" ), wx.VERTICAL )
		
		self.m_panel23 = wx.Panel( self.tabInfantry, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer26 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.lblclimbspeed = wx.StaticText( self.m_panel23, wx.ID_ANY, u"Speed :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblclimbspeed.Wrap( -1 )
		gSizer26.Add( self.lblclimbspeed, 0, wx.ALL, 5 )
		
		self.textInfantryClimbingSpeed = wx.TextCtrl( self.m_panel23, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer26.Add( self.textInfantryClimbingSpeed, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText89 = wx.StaticText( self.m_panel23, wx.ID_ANY, u"Rubble climbing speed :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText89.Wrap( -1 )
		gSizer26.Add( self.m_staticText89, 0, wx.ALL, 5 )
		
		self.textInfantryRubbleClimbingSpeed = wx.TextCtrl( self.m_panel23, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer26.Add( self.textInfantryRubbleClimbingSpeed, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText90 = wx.StaticText( self.m_panel23, wx.ID_ANY, u"Search Radius  To Rubble :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText90.Wrap( -1 )
		gSizer26.Add( self.m_staticText90, 0, wx.ALL, 5 )
		
		self.textInfantrySearchRadiusRubble = wx.TextCtrl( self.m_panel23, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer26.Add( self.textInfantrySearchRadiusRubble, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText209 = wx.StaticText( self.m_panel23, wx.ID_ANY, u"Movement priority :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText209.Wrap( -1 )
		gSizer26.Add( self.m_staticText209, 0, wx.ALL, 5 )

		self.textInfantryMovementPriorityClimbing = wx.TextCtrl( self.m_panel23, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer26.Add( self.textInfantryMovementPriorityClimbing, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_panel23.SetSizer( gSizer26 )
		self.m_panel23.Layout()
		gSizer26.Fit( self.m_panel23 )
		sbSizer26.Add( self.m_panel23, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		sizerInfantry.Add( sbSizer26, 0, wx.EXPAND|wx.ALL, 5 )
		
		
		self.tabInfantry.SetSizer( sizerInfantry )
		self.tabInfantry.Layout()
		sizerInfantry.Fit( self.tabInfantry )
		self.tabctrl.AddPage( self.tabInfantry, u"Infantry", False )
		self.tabArchers = wx.Panel( self.tabctrl, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerArchers = wx.BoxSizer( wx.VERTICAL )
		
		gSizer251 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText811 = wx.StaticText( self.tabArchers, wx.ID_ANY, u"Defense :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText811.Wrap( -1 )
		gSizer251.Add( self.m_staticText811, 0, wx.ALL, 5 )
		
		self.textArchersDefense = wx.TextCtrl( self.tabArchers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer251.Add( self.textArchersDefense, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText821 = wx.StaticText( self.tabArchers, wx.ID_ANY, u"Attack :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText821.Wrap( -1 )
		gSizer251.Add( self.m_staticText821, 0, wx.ALL, 5 )
		
		self.textArchersAttack = wx.TextCtrl( self.tabArchers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer251.Add( self.textArchersAttack, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText831 = wx.StaticText( self.tabArchers, wx.ID_ANY, u"Speed :  ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText831.Wrap( -1 )
		gSizer251.Add( self.m_staticText831, 0, wx.ALL, 5 )
		
		self.textArchersSpeed = wx.TextCtrl( self.tabArchers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer251.Add( self.textArchersSpeed, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText841 = wx.StaticText( self.tabArchers, wx.ID_ANY, u"Reload :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText841.Wrap( -1 )
		gSizer251.Add( self.m_staticText841, 0, wx.ALL, 5 )
		
		self.textArchersReload = wx.TextCtrl( self.tabArchers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer251.Add( self.textArchersReload, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText851 = wx.StaticText( self.tabArchers, wx.ID_ANY, u"Accuracy :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText851.Wrap( -1 )
		gSizer251.Add( self.m_staticText851, 0, wx.ALL, 5 )
		
		self.textArchersAccuracy = wx.TextCtrl( self.tabArchers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer251.Add( self.textArchersAccuracy, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText861 = wx.StaticText( self.tabArchers, wx.ID_ANY, u"Distance :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText861.Wrap( -1 )
		gSizer251.Add( self.m_staticText861, 0, wx.ALL, 5 )
		
		self.textArchersDistance = wx.TextCtrl( self.tabArchers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer251.Add( self.textArchersDistance, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText871 = wx.StaticText( self.tabArchers, wx.ID_ANY, u"Movement priority :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText871.Wrap( -1 )
		gSizer251.Add( self.m_staticText871, 0, wx.ALL, 5 )
		
		self.textArchersMovementPriority = wx.TextCtrl( self.tabArchers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer251.Add( self.textArchersMovementPriority, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		sizerArchers.Add( gSizer251, 0, wx.EXPAND|wx.ALL, 5 )
		
		self.checkArchersStationary = wx.CheckBox( self.tabArchers, wx.ID_ANY, u"Stationary", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerArchers.Add( self.checkArchersStationary, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		sbSizer271 = wx.StaticBoxSizer( wx.StaticBox( self.tabArchers, wx.ID_ANY, u"Bounding size" ), wx.VERTICAL )
		
		self.m_panel24 = wx.Panel( self.tabArchers, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer271 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText911 = wx.StaticText( self.m_panel24, wx.ID_ANY, u"Length :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText911.Wrap( -1 )
		gSizer271.Add( self.m_staticText911, 0, wx.ALL, 5 )
		
		self.textArchersBoundingLength = wx.TextCtrl( self.m_panel24, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer271.Add( self.textArchersBoundingLength, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText921 = wx.StaticText( self.m_panel24, wx.ID_ANY, u"Height :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText921.Wrap( -1 )
		gSizer271.Add( self.m_staticText921, 0, wx.ALL, 5 )
		
		self.textArchersBoundingHeight = wx.TextCtrl( self.m_panel24, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer271.Add( self.textArchersBoundingHeight, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText931 = wx.StaticText( self.m_panel24, wx.ID_ANY, u"Width :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText931.Wrap( -1 )
		gSizer271.Add( self.m_staticText931, 0, wx.ALL, 5 )
		
		self.textArchersBoudingWidth = wx.TextCtrl( self.m_panel24, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer271.Add( self.textArchersBoudingWidth, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel24.SetSizer( gSizer271 )
		self.m_panel24.Layout()
		gSizer271.Fit( self.m_panel24 )
		sbSizer271.Add( self.m_panel24, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		sizerArchers.Add( sbSizer271, 0, wx.EXPAND|wx.ALL, 5 )
		
		self.checkArchersDoubleCheck = wx.CheckBox( self.tabArchers, wx.ID_ANY, u"Defense shoot double check", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerArchers.Add( self.checkArchersDoubleCheck, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		gSizer33 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText114 = wx.StaticText( self.tabArchers, wx.ID_ANY, u"Shoots to stay :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText114.Wrap( -1 )
		gSizer33.Add( self.m_staticText114, 0, wx.ALL, 5 )
		
		self.textArchersShootsToStay = wx.TextCtrl( self.tabArchers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer33.Add( self.textArchersShootsToStay, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText115 = wx.StaticText( self.tabArchers, wx.ID_ANY, u"Trench search radius :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText115.Wrap( -1 )
		gSizer33.Add( self.m_staticText115, 0, wx.ALL, 5 )
		
		self.textArchersTrenchSearchRadius = wx.TextCtrl( self.tabArchers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer33.Add( self.textArchersTrenchSearchRadius, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText116 = wx.StaticText( self.tabArchers, wx.ID_ANY, u"Margin space (defenders) :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText116.Wrap( -1 )
		gSizer33.Add( self.m_staticText116, 0, wx.ALL, 5 )
		
		self.textArchersMarginSpace = wx.TextCtrl( self.tabArchers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer33.Add( self.textArchersMarginSpace, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		sizerArchers.Add( gSizer33, 0, wx.EXPAND|wx.ALL, 5 )
		
		
		self.tabArchers.SetSizer( sizerArchers )
		self.tabArchers.Layout()
		sizerArchers.Fit( self.tabArchers )
		self.tabctrl.AddPage( self.tabArchers, u"Archers", False )
		self.tabCannons = wx.Panel( self.tabctrl, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerCannons = wx.BoxSizer( wx.VERTICAL )
		
		gSizer2511 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText8111 = wx.StaticText( self.tabCannons, wx.ID_ANY, u"Defense :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8111.Wrap( -1 )
		gSizer2511.Add( self.m_staticText8111, 0, wx.ALL, 5 )
		
		self.textCannonsDefense = wx.TextCtrl( self.tabCannons, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2511.Add( self.textCannonsDefense, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText8211 = wx.StaticText( self.tabCannons, wx.ID_ANY, u"Attack :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8211.Wrap( -1 )
		gSizer2511.Add( self.m_staticText8211, 0, wx.ALL, 5 )
		
		self.textCannonsAttack = wx.TextCtrl( self.tabCannons, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2511.Add( self.textCannonsAttack, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText8311 = wx.StaticText( self.tabCannons, wx.ID_ANY, u"Speed :  ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8311.Wrap( -1 )
		gSizer2511.Add( self.m_staticText8311, 0, wx.ALL, 5 )
		
		self.textCannonsSpeed = wx.TextCtrl( self.tabCannons, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2511.Add( self.textCannonsSpeed, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText8411 = wx.StaticText( self.tabCannons, wx.ID_ANY, u"Reload :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8411.Wrap( -1 )
		gSizer2511.Add( self.m_staticText8411, 0, wx.ALL, 5 )
		
		self.textCannonsReload = wx.TextCtrl( self.tabCannons, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2511.Add( self.textCannonsReload, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText8511 = wx.StaticText( self.tabCannons, wx.ID_ANY, u"Accuracy :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8511.Wrap( -1 )
		gSizer2511.Add( self.m_staticText8511, 0, wx.ALL, 5 )
		
		self.textCannonsAccuracy = wx.TextCtrl( self.tabCannons, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2511.Add( self.textCannonsAccuracy, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText8611 = wx.StaticText( self.tabCannons, wx.ID_ANY, u"Distance :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8611.Wrap( -1 )
		gSizer2511.Add( self.m_staticText8611, 0, wx.ALL, 5 )
		
		self.textCannonsDistance = wx.TextCtrl( self.tabCannons, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2511.Add( self.textCannonsDistance, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText8711 = wx.StaticText( self.tabCannons, wx.ID_ANY, u"Movement priority :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8711.Wrap( -1 )
		gSizer2511.Add( self.m_staticText8711, 0, wx.ALL, 5 )
		
		self.textCannonsMovementPriority = wx.TextCtrl( self.tabCannons, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2511.Add( self.textCannonsMovementPriority, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		sizerCannons.Add( gSizer2511, 0, wx.EXPAND|wx.ALL, 5 )
		
		self.checkCannonsStationary = wx.CheckBox( self.tabCannons, wx.ID_ANY, u"Stationary", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerCannons.Add( self.checkCannonsStationary, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		sbSizer2711 = wx.StaticBoxSizer( wx.StaticBox( self.tabCannons, wx.ID_ANY, u"Bounding size" ), wx.VERTICAL )
		
		self.m_panel25 = wx.Panel( self.tabCannons, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer2711 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText9111 = wx.StaticText( self.m_panel25, wx.ID_ANY, u"Length :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9111.Wrap( -1 )
		gSizer2711.Add( self.m_staticText9111, 0, wx.ALL, 5 )
		
		self.textCannonsBoundingLength = wx.TextCtrl( self.m_panel25, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2711.Add( self.textCannonsBoundingLength, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText9211 = wx.StaticText( self.m_panel25, wx.ID_ANY, u"Height :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9211.Wrap( -1 )
		gSizer2711.Add( self.m_staticText9211, 0, wx.ALL, 5 )
		
		self.textCannonsBoundingHeight = wx.TextCtrl( self.m_panel25, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2711.Add( self.textCannonsBoundingHeight, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText9311 = wx.StaticText( self.m_panel25, wx.ID_ANY, u"Width :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9311.Wrap( -1 )
		gSizer2711.Add( self.m_staticText9311, 0, wx.ALL, 5 )
		
		self.textCannonsBoundingWidth = wx.TextCtrl( self.m_panel25, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2711.Add( self.textCannonsBoundingWidth, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel25.SetSizer( gSizer2711 )
		self.m_panel25.Layout()
		gSizer2711.Fit( self.m_panel25 )
		sbSizer2711.Add( self.m_panel25, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		sizerCannons.Add( sbSizer2711, 0, wx.EXPAND|wx.ALL, 5 )
		
		self.checkCannonsDoubleCheck = wx.CheckBox( self.tabCannons, wx.ID_ANY, u"Defense shoot double check", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerCannons.Add( self.checkCannonsDoubleCheck, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		sbSizer34 = wx.StaticBoxSizer( wx.StaticBox( self.tabCannons, wx.ID_ANY, u"Shoot angles" ), wx.VERTICAL )
		
		self.m_panel26 = wx.Panel( self.tabCannons, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer39 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText137 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"Horizontal : ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText137.Wrap( -1 )
		gSizer39.Add( self.m_staticText137, 0, wx.ALL, 5 )
		
		self.textCannonsShootHorizontal = wx.TextCtrl( self.m_panel26, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer39.Add( self.textCannonsShootHorizontal, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText138 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"Vertical start :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText138.Wrap( -1 )
		gSizer39.Add( self.m_staticText138, 0, wx.ALL, 5 )
		
		self.textCannonsShootVertical1 = wx.TextCtrl( self.m_panel26, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer39.Add( self.textCannonsShootVertical1, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText139 = wx.StaticText( self.m_panel26, wx.ID_ANY, u"Vertical end :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText139.Wrap( -1 )
		gSizer39.Add( self.m_staticText139, 0, wx.ALL, 5 )
		
		self.textCannonsShootVertical2 = wx.TextCtrl( self.m_panel26, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer39.Add( self.textCannonsShootVertical2, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel26.SetSizer( gSizer39 )
		self.m_panel26.Layout()
		gSizer39.Fit( self.m_panel26 )
		sbSizer34.Add( self.m_panel26, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		sizerCannons.Add( sbSizer34, 0, wx.EXPAND|wx.ALL, 5 )
		
		gSizer40 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText140 = wx.StaticText( self.tabCannons, wx.ID_ANY, u"Ball radius :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText140.Wrap( -1 )
		gSizer40.Add( self.m_staticText140, 0, wx.ALL, 5 )
		
		self.textCannonsBall = wx.TextCtrl( self.tabCannons, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer40.Add( self.textCannonsBall, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText141 = wx.StaticText( self.tabCannons, wx.ID_ANY, u"Default placement distance :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText141.Wrap( -1 )
		gSizer40.Add( self.m_staticText141, 0, wx.ALL, 5 )
		
		self.textCannonsPlacementDistance = wx.TextCtrl( self.tabCannons, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer40.Add( self.textCannonsPlacementDistance, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		sizerCannons.Add( gSizer40, 0, wx.EXPAND|wx.ALL, 5 )
		
		
		self.tabCannons.SetSizer( sizerCannons )
		self.tabCannons.Layout()
		sizerCannons.Fit( self.tabCannons )
		self.tabctrl.AddPage( self.tabCannons, u"Cannons", False )
		self.tabSiegeTowers = wx.Panel( self.tabctrl, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerSiegetowers = wx.BoxSizer( wx.VERTICAL )
		
		gSizer25111 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText81111 = wx.StaticText( self.tabSiegeTowers, wx.ID_ANY, u"Defense :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText81111.Wrap( -1 )
		gSizer25111.Add( self.m_staticText81111, 0, wx.ALL, 5 )
		
		self.textSiegeDefense = wx.TextCtrl( self.tabSiegeTowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer25111.Add( self.textSiegeDefense, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText82111 = wx.StaticText( self.tabSiegeTowers, wx.ID_ANY, u"Attack :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText82111.Wrap( -1 )
		gSizer25111.Add( self.m_staticText82111, 0, wx.ALL, 5 )
		
		self.textSiegeAttack = wx.TextCtrl( self.tabSiegeTowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer25111.Add( self.textSiegeAttack, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText83111 = wx.StaticText( self.tabSiegeTowers, wx.ID_ANY, u"Speed :  ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText83111.Wrap( -1 )
		gSizer25111.Add( self.m_staticText83111, 0, wx.ALL, 5 )
		
		self.textSiegeSpeed = wx.TextCtrl( self.tabSiegeTowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer25111.Add( self.textSiegeSpeed, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText84111 = wx.StaticText( self.tabSiegeTowers, wx.ID_ANY, u"Reload :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText84111.Wrap( -1 )
		gSizer25111.Add( self.m_staticText84111, 0, wx.ALL, 5 )
		
		self.textSiegeReload = wx.TextCtrl( self.tabSiegeTowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer25111.Add( self.textSiegeReload, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText85111 = wx.StaticText( self.tabSiegeTowers, wx.ID_ANY, u"Accuracy :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText85111.Wrap( -1 )
		gSizer25111.Add( self.m_staticText85111, 0, wx.ALL, 5 )
		
		self.textSiegeAccuracy = wx.TextCtrl( self.tabSiegeTowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer25111.Add( self.textSiegeAccuracy, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText86111 = wx.StaticText( self.tabSiegeTowers, wx.ID_ANY, u"Distance :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText86111.Wrap( -1 )
		gSizer25111.Add( self.m_staticText86111, 0, wx.ALL, 5 )
		
		self.textSiegeDistance = wx.TextCtrl( self.tabSiegeTowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer25111.Add( self.textSiegeDistance, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText87111 = wx.StaticText( self.tabSiegeTowers, wx.ID_ANY, u"Movement priority :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText87111.Wrap( -1 )
		gSizer25111.Add( self.m_staticText87111, 0, wx.ALL, 5 )
		
		self.textSiegeMovementPriority = wx.TextCtrl( self.tabSiegeTowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer25111.Add( self.textSiegeMovementPriority, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		sizerSiegetowers.Add( gSizer25111, 0, wx.EXPAND|wx.ALL, 5 )
		
		self.checkSiegeStationary = wx.CheckBox( self.tabSiegeTowers, wx.ID_ANY, u"Stationary", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerSiegetowers.Add( self.checkSiegeStationary, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		sbSizer27111 = wx.StaticBoxSizer( wx.StaticBox( self.tabSiegeTowers, wx.ID_ANY, u"Bounding size" ), wx.VERTICAL )
		
		self.m_panel27 = wx.Panel( self.tabSiegeTowers, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer27111 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText91111 = wx.StaticText( self.m_panel27, wx.ID_ANY, u"Length :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText91111.Wrap( -1 )
		gSizer27111.Add( self.m_staticText91111, 0, wx.ALL, 5 )
		
		self.textSiegeBoundingLength = wx.TextCtrl( self.m_panel27, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer27111.Add( self.textSiegeBoundingLength, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText92111 = wx.StaticText( self.m_panel27, wx.ID_ANY, u"Height :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText92111.Wrap( -1 )
		gSizer27111.Add( self.m_staticText92111, 0, wx.ALL, 5 )
		
		self.textSiegeBoundingHeight = wx.TextCtrl( self.m_panel27, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer27111.Add( self.textSiegeBoundingHeight, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText93111 = wx.StaticText( self.m_panel27, wx.ID_ANY, u"Width :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText93111.Wrap( -1 )
		gSizer27111.Add( self.m_staticText93111, 0, wx.ALL, 5 )
		
		self.textSiegeBoundingWidth = wx.TextCtrl( self.m_panel27, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer27111.Add( self.textSiegeBoundingWidth, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel27.SetSizer( gSizer27111 )
		self.m_panel27.Layout()
		gSizer27111.Fit( self.m_panel27 )
		sbSizer27111.Add( self.m_panel27, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		sizerSiegetowers.Add( sbSizer27111, 0, wx.EXPAND|wx.ALL, 5 )
		

		gSizer46 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText162 = wx.StaticText( self.tabSiegeTowers, wx.ID_ANY, u"Level height :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText162.Wrap( -1 )
		gSizer46.Add( self.m_staticText162, 0, wx.ALL, 5 )
		
		self.textSiegeLevelheight = wx.TextCtrl( self.tabSiegeTowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer46.Add( self.textSiegeLevelheight, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText163 = wx.StaticText( self.tabSiegeTowers, wx.ID_ANY, u"Construction time per level :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText163.Wrap( -1 )
		gSizer46.Add( self.m_staticText163, 0, wx.ALL, 5 )
		
		self.textSiegeConstructiontime = wx.TextCtrl( self.tabSiegeTowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer46.Add( self.textSiegeConstructiontime, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText164 = wx.StaticText( self.tabSiegeTowers, wx.ID_ANY, u"Turtle defense :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText164.Wrap( -1 )
		gSizer46.Add( self.m_staticText164, 0, wx.ALL, 5 )
		
		self.textSiegeTurtledefense = wx.TextCtrl( self.tabSiegeTowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer46.Add( self.textSiegeTurtledefense, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText165 = wx.StaticText( self.tabSiegeTowers, wx.ID_ANY, u"Cover moat speed :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText165.Wrap( -1 )
		gSizer46.Add( self.m_staticText165, 0, wx.ALL, 5 )
		
		self.textSiegeCovermoatspeed = wx.TextCtrl( self.tabSiegeTowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer46.Add( self.textSiegeCovermoatspeed, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		sizerSiegetowers.Add( gSizer46, 0, wx.EXPAND|wx.ALL, 5 )
		
		
		self.tabSiegeTowers.SetSizer( sizerSiegetowers )
		self.tabSiegeTowers.Layout()
		sizerSiegetowers.Fit( self.tabSiegeTowers )
		self.tabctrl.AddPage( self.tabSiegeTowers, u"Siege towers", False )
		self.tabThrowers = wx.Panel( self.tabctrl, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerThrowers = wx.BoxSizer( wx.VERTICAL )
		
		gSizer251111 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText811111 = wx.StaticText( self.tabThrowers, wx.ID_ANY, u"Defense :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText811111.Wrap( -1 )
		gSizer251111.Add( self.m_staticText811111, 0, wx.ALL, 5 )
		
		self.textThrowerDefense = wx.TextCtrl( self.tabThrowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer251111.Add( self.textThrowerDefense, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText821111 = wx.StaticText( self.tabThrowers, wx.ID_ANY, u"Attack :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText821111.Wrap( -1 )
		gSizer251111.Add( self.m_staticText821111, 0, wx.ALL, 5 )
		
		self.textThrowerAttack = wx.TextCtrl( self.tabThrowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer251111.Add( self.textThrowerAttack, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText831111 = wx.StaticText( self.tabThrowers, wx.ID_ANY, u"Speed :  ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText831111.Wrap( -1 )
		gSizer251111.Add( self.m_staticText831111, 0, wx.ALL, 5 )
		
		self.textThrowerSpeed = wx.TextCtrl( self.tabThrowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer251111.Add( self.textThrowerSpeed, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText841111 = wx.StaticText( self.tabThrowers, wx.ID_ANY, u"Reload :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText841111.Wrap( -1 )
		gSizer251111.Add( self.m_staticText841111, 0, wx.ALL, 5 )
		
		self.textThrowerReload = wx.TextCtrl( self.tabThrowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer251111.Add( self.textThrowerReload, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText851111 = wx.StaticText( self.tabThrowers, wx.ID_ANY, u"Accuracy :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText851111.Wrap( -1 )
		gSizer251111.Add( self.m_staticText851111, 0, wx.ALL, 5 )
		
		self.textThrowerAccuracy = wx.TextCtrl( self.tabThrowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer251111.Add( self.textThrowerAccuracy, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText861111 = wx.StaticText( self.tabThrowers, wx.ID_ANY, u"Distance :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText861111.Wrap( -1 )
		gSizer251111.Add( self.m_staticText861111, 0, wx.ALL, 5 )
		
		self.textThrowerDistance = wx.TextCtrl( self.tabThrowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer251111.Add( self.textThrowerDistance, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText871111 = wx.StaticText( self.tabThrowers, wx.ID_ANY, u"Movement priority :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText871111.Wrap( -1 )
		gSizer251111.Add( self.m_staticText871111, 0, wx.ALL, 5 )
		
		self.textThrowerMovementPriority = wx.TextCtrl( self.tabThrowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer251111.Add( self.textThrowerMovementPriority, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		sizerThrowers.Add( gSizer251111, 0, wx.EXPAND|wx.ALL, 5 )
		
		self.checkThrowerStationary = wx.CheckBox( self.tabThrowers, wx.ID_ANY, u"Stationary", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerThrowers.Add( self.checkThrowerStationary, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		sbSizer271111 = wx.StaticBoxSizer( wx.StaticBox( self.tabThrowers, wx.ID_ANY, u"Bounding size" ), wx.VERTICAL )
		
		self.m_panel28 = wx.Panel( self.tabThrowers, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer271111 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText911111 = wx.StaticText( self.m_panel28, wx.ID_ANY, u"Length :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText911111.Wrap( -1 )
		gSizer271111.Add( self.m_staticText911111, 0, wx.ALL, 5 )
		
		self.textThrowerBoundingLength = wx.TextCtrl( self.m_panel28, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer271111.Add( self.textThrowerBoundingLength, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText921111 = wx.StaticText( self.m_panel28, wx.ID_ANY, u"Height :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText921111.Wrap( -1 )
		gSizer271111.Add( self.m_staticText921111, 0, wx.ALL, 5 )
		
		self.textThrowerBoundingHeight = wx.TextCtrl( self.m_panel28, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer271111.Add( self.textThrowerBoundingHeight, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText931111 = wx.StaticText( self.m_panel28, wx.ID_ANY, u"Width :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText931111.Wrap( -1 )
		gSizer271111.Add( self.m_staticText931111, 0, wx.ALL, 5 )
		
		self.textThrowerBoundingWidth = wx.TextCtrl( self.m_panel28, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer271111.Add( self.textThrowerBoundingWidth, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel28.SetSizer( gSizer271111 )
		self.m_panel28.Layout()
		gSizer271111.Fit( self.m_panel28 )
		sbSizer271111.Add( self.m_panel28, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		sizerThrowers.Add( sbSizer271111, 0, wx.EXPAND|wx.ALL, 5 )
		
		gSizer52 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText186 = wx.StaticText( self.tabThrowers, wx.ID_ANY, u"Battalion max size :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText186.Wrap( -1 )
		gSizer52.Add( self.m_staticText186, 0, wx.ALL, 5 )
		
		self.textThrowerBattalionSize = wx.TextCtrl( self.tabThrowers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer52.Add( self.textThrowerBattalionSize, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		sizerThrowers.Add( gSizer52, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.tabThrowers.SetSizer( sizerThrowers )
		self.tabThrowers.Layout()
		sizerThrowers.Fit( self.tabThrowers )
		self.tabctrl.AddPage( self.tabThrowers, u"Throwers", False )
		self.tabMisc = wx.Panel( self.tabctrl, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerMisc = wx.BoxSizer( wx.VERTICAL )
		
		gSizer53 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText187 = wx.StaticText( self.tabMisc, wx.ID_ANY, u"Human field of view :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText187.Wrap( -1 )
		gSizer53.Add( self.m_staticText187, 0, wx.ALL, 5 )
		
		self.textMiscHumanFOV = wx.TextCtrl( self.tabMisc, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer53.Add( self.textMiscHumanFOV, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		sizerMisc.Add( gSizer53, 0, wx.EXPAND|wx.ALL, 5 )
		
		self.checkMiscShowOutline = wx.CheckBox( self.tabMisc, wx.ID_ANY, u"Show outline", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerMisc.Add( self.checkMiscShowOutline, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.checkMiscLabels = wx.CheckBox( self.tabMisc, wx.ID_ANY, u"Show labels", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerMisc.Add( self.checkMiscLabels, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.tabMisc.SetSizer( sizerMisc )
		self.tabMisc.Layout()
		sizerMisc.Fit( self.tabMisc )
		self.tabctrl.AddPage( self.tabMisc, u"Misc", False )
		
		sizer.Add( self.tabctrl, 1, wx.EXPAND |wx.ALL, 5 )
		
		m_sdbSizer5 = wx.StdDialogButtonSizer()
		self.m_sdbSizer5OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer5.AddButton( self.m_sdbSizer5OK )
		self.m_sdbSizer5Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer5.AddButton( self.m_sdbSizer5Cancel )
		m_sdbSizer5.Realize();
		
		sizer.Add( m_sdbSizer5, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.SetSizer( sizer )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

