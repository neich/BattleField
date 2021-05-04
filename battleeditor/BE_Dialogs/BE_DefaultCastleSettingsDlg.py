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
## Class BE_DefaultCastleSettings
###########################################################################


# WARNING!! wxFormBuilderBug -> StaticBoxes must have only one children, a Panel. This can be done in the UI builder, but the other child controls, under the panel,
#                                set their parents as the staticbox, not the panel. If this is not solved, the program finishes without showing any warning or error message
#                               So, manual edition must be performed to change this. BE AWARE updating this file




class BE_DefaultCastleSettingsDlg ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Default castle settings", pos = wx.DefaultPosition, size = wx.Size( 384,895 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

		sizer = wx.BoxSizer( wx.VERTICAL )

		self.tabctrl = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.tabCastle = wx.Panel( self.tabctrl, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerCastle = wx.BoxSizer( wx.VERTICAL )

		frameOrientation = wx.StaticBoxSizer( wx.StaticBox( self.tabCastle, wx.ID_ANY, u"Orientation vector" ), wx.HORIZONTAL )

		self.m_panel32 = wx.Panel( self.tabCastle, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer35 = wx.BoxSizer( wx.HORIZONTAL )

		self.labelOrientationX = wx.StaticText( self.m_panel32, wx.ID_ANY, u"X :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelOrientationX.Wrap( -1 )
		bSizer35.Add( self.labelOrientationX, 0, wx.ALL, 5 )

		self.textOrientationX = wx.TextCtrl( self.m_panel32, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer35.Add( self.textOrientationX, 1, wx.ALL|wx.EXPAND, 5 )

		self.labelOrientationY = wx.StaticText( self.m_panel32, wx.ID_ANY, u"Y :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelOrientationY.Wrap( -1 )
		bSizer35.Add( self.labelOrientationY, 0, wx.ALL, 5 )

		self.textOrientationY = wx.TextCtrl( self.m_panel32, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer35.Add( self.textOrientationY, 1, wx.ALL|wx.EXPAND, 5 )


		self.m_panel32.SetSizer( bSizer35 )
		self.m_panel32.Layout()
		bSizer35.Fit( self.m_panel32 )
		frameOrientation.Add( self.m_panel32, 1, wx.EXPAND |wx.ALL, 5 )


		sizerCastle.Add( frameOrientation, 0, wx.EXPAND|wx.ALL, 5 )

		frameDefendingLine = wx.StaticBoxSizer( wx.StaticBox( self.tabCastle, wx.ID_ANY, u"Defending lines" ), wx.HORIZONTAL )

		self.m_panel33 = wx.Panel( self.tabCastle, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerDefendingLine = wx.GridSizer( 3, 2, 0, 0 )

		self.labelDLWidth = wx.StaticText( self.m_panel33, wx.ID_ANY, u"Width :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelDLWidth.Wrap( -1 )
		sizerDefendingLine.Add( self.labelDLWidth, 0, wx.ALL, 5 )

		self.textDefendingLineWidth = wx.TextCtrl( self.m_panel33, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerDefendingLine.Add( self.textDefendingLineWidth, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelDFCS = wx.StaticText( self.m_panel33, wx.ID_ANY, u"Cell size :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelDFCS.Wrap( -1 )
		sizerDefendingLine.Add( self.labelDFCS, 0, wx.ALL|wx.EXPAND, 5 )

		self.textDefendingLineCellsize = wx.TextCtrl( self.m_panel33, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerDefendingLine.Add( self.textDefendingLineCellsize, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelDFHeight = wx.StaticText( self.m_panel33, wx.ID_ANY, u"Height :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelDFHeight.Wrap( -1 )
		sizerDefendingLine.Add( self.labelDFHeight, 0, wx.ALL, 5 )

		self.textDefendingLineHeight = wx.TextCtrl( self.m_panel33, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerDefendingLine.Add( self.textDefendingLineHeight, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panel33.SetSizer( sizerDefendingLine )
		self.m_panel33.Layout()
		sizerDefendingLine.Fit( self.m_panel33 )
		frameDefendingLine.Add( self.m_panel33, 1, wx.EXPAND |wx.ALL, 5 )


		sizerCastle.Add( frameDefendingLine, 0, wx.EXPAND|wx.ALL, 5 )

		sizerOldCityMargin = wx.BoxSizer( wx.HORIZONTAL )

		self.labelOldCityMargin = wx.StaticText( self.tabCastle, wx.ID_ANY, u"Old city margin to wall :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelOldCityMargin.Wrap( -1 )
		sizerOldCityMargin.Add( self.labelOldCityMargin, 1, wx.ALL, 5 )

		self.textOldCityMargin = wx.TextCtrl( self.tabCastle, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerOldCityMargin.Add( self.textOldCityMargin, 1, wx.ALL, 5 )


		sizerCastle.Add( sizerOldCityMargin, 0, wx.EXPAND|wx.ALL, 5 )

		self.checkLabels = wx.CheckBox( self.tabCastle, wx.ID_ANY, u"Show labels", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerCastle.Add( self.checkLabels, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.tabCastle.SetSizer( sizerCastle )
		self.tabCastle.Layout()
		sizerCastle.Fit( self.tabCastle )
		self.tabctrl.AddPage( self.tabCastle, u"Castle", True )
		self.tabWall = wx.Panel( self.tabctrl, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerWall = wx.BoxSizer( wx.VERTICAL )

		sizerWallData = wx.GridSizer( 0, 2, 0, 0 )

		self.labelWallHeight = wx.StaticText( self.tabWall, wx.ID_ANY, u"Height :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelWallHeight.Wrap( -1 )
		sizerWallData.Add( self.labelWallHeight, 0, wx.ALL, 5 )

		self.textWallHeight = wx.TextCtrl( self.tabWall, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerWallData.Add( self.textWallHeight, 1, wx.ALL|wx.EXPAND, 5 )

		self.labelWallThickness = wx.StaticText( self.tabWall, wx.ID_ANY, u"Thickness :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelWallThickness.Wrap( -1 )
		sizerWallData.Add( self.labelWallThickness, 0, wx.ALL, 5 )

		self.textWallThickness = wx.TextCtrl( self.tabWall, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerWallData.Add( self.textWallThickness, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelWallMerlonHeight = wx.StaticText( self.tabWall, wx.ID_ANY, u"Merlon height :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelWallMerlonHeight.Wrap( -1 )
		sizerWallData.Add( self.labelWallMerlonHeight, 0, wx.ALL, 5 )

		self.textMerlonHeight = wx.TextCtrl( self.tabWall, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerWallData.Add( self.textMerlonHeight, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelWallWalkaway = wx.StaticText( self.tabWall, wx.ID_ANY, u"Walkway width : ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelWallWalkaway.Wrap( -1 )
		sizerWallData.Add( self.labelWallWalkaway, 0, wx.ALL, 5 )

		self.textWallWalkwayWidth = wx.TextCtrl( self.tabWall, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerWallData.Add( self.textWallWalkwayWidth, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelWallBatCellSize = wx.StaticText( self.tabWall, wx.ID_ANY, u"Battalion cell size :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelWallBatCellSize.Wrap( -1 )
		sizerWallData.Add( self.labelWallBatCellSize, 0, wx.ALL, 5 )

		self.textWallBattalionCellSize = wx.TextCtrl( self.tabWall, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerWallData.Add( self.textWallBattalionCellSize, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelWallDefenseInc = wx.StaticText( self.tabWall, wx.ID_ANY, u"Defense increase :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelWallDefenseInc.Wrap( -1 )
		sizerWallData.Add( self.labelWallDefenseInc, 0, wx.ALL, 5 )

		self.textWallDefenseIncrease = wx.TextCtrl( self.tabWall, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerWallData.Add( self.textWallDefenseIncrease, 0, wx.ALL|wx.EXPAND, 5 )


		sizerWall.Add( sizerWallData, 0, wx.EXPAND|wx.ALL, 5 )

		frameWallDefenseAngle = wx.StaticBoxSizer( wx.StaticBox( self.tabWall, wx.ID_ANY, u"Defense angle" ), wx.VERTICAL )

		self.m_panel34 = wx.Panel( self.tabWall, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerWallDefenseAngle = wx.GridSizer( 0, 2, 0, 0 )

		self.labelWallDAH = wx.StaticText( self.m_panel34, wx.ID_ANY, u"Horizontal :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelWallDAH.Wrap( -1 )
		sizerWallDefenseAngle.Add( self.labelWallDAH, 0, wx.ALL, 5 )

		self.textWallDefenseAngleHorizontal = wx.TextCtrl( self.m_panel34, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerWallDefenseAngle.Add( self.textWallDefenseAngleHorizontal, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelWallDAV1 = wx.StaticText( self.m_panel34, wx.ID_ANY, u"Vertical (start) :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelWallDAV1.Wrap( -1 )
		sizerWallDefenseAngle.Add( self.labelWallDAV1, 0, wx.ALL, 5 )

		self.textWallDefenseAngleVertical1 = wx.TextCtrl( self.m_panel34, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerWallDefenseAngle.Add( self.textWallDefenseAngleVertical1, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelWallDAV2 = wx.StaticText( self.m_panel34, wx.ID_ANY, u"Vertical (end) :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelWallDAV2.Wrap( -1 )
		sizerWallDefenseAngle.Add( self.labelWallDAV2, 0, wx.ALL, 5 )

		self.textWallDefenseAngleVertical2 = wx.TextCtrl( self.m_panel34, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerWallDefenseAngle.Add( self.textWallDefenseAngleVertical2, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panel34.SetSizer( sizerWallDefenseAngle )
		self.m_panel34.Layout()
		sizerWallDefenseAngle.Fit( self.m_panel34 )
		frameWallDefenseAngle.Add( self.m_panel34, 1, wx.EXPAND |wx.ALL, 5 )


		sizerWall.Add( frameWallDefenseAngle, 0, wx.ALL|wx.EXPAND, 5 )

		frameWallTiles = wx.StaticBoxSizer( wx.StaticBox( self.tabWall, wx.ID_ANY, u"Tiles" ), wx.VERTICAL )

		self.m_panel35 = wx.Panel( self.tabWall, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer36 = wx.BoxSizer( wx.VERTICAL )

		sizerWallTiles = wx.GridSizer( 0, 2, 0, 0 )

		self.labelWallTilesWidth = wx.StaticText( self.m_panel35, wx.ID_ANY, u"Width :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelWallTilesWidth.Wrap( -1 )
		sizerWallTiles.Add( self.labelWallTilesWidth, 0, wx.ALL, 5 )

		self.textWallTilesWidth = wx.TextCtrl( self.m_panel35, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerWallTiles.Add( self.textWallTilesWidth, 1, wx.ALL|wx.EXPAND, 5 )

		self.labelWallTilesHeight = wx.StaticText( self.m_panel35, wx.ID_ANY, u"Height :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelWallTilesHeight.Wrap( -1 )
		sizerWallTiles.Add( self.labelWallTilesHeight, 0, wx.ALL, 5 )

		self.textWallTilesHeight = wx.TextCtrl( self.m_panel35, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerWallTiles.Add( self.textWallTilesHeight, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelWallTilesResistance = wx.StaticText( self.m_panel35, wx.ID_ANY, u"Resistance :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelWallTilesResistance.Wrap( -1 )
		sizerWallTiles.Add( self.labelWallTilesResistance, 0, wx.ALL, 5 )

		self.textWallTilesResistance = wx.TextCtrl( self.m_panel35, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerWallTiles.Add( self.textWallTilesResistance, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer36.Add( sizerWallTiles, 0, wx.EXPAND|wx.ALL, 5 )

		frameWallTilesRumble = wx.StaticBoxSizer( wx.StaticBox( self.m_panel35, wx.ID_ANY, u"Rubble conversion factors" ), wx.VERTICAL )

		self.m_panel36 = wx.Panel( self.m_panel35, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerWallTilesRumble = wx.BoxSizer( wx.HORIZONTAL )

		self.textWallTilesRubble1 = wx.TextCtrl( self.m_panel36, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerWallTilesRumble.Add( self.textWallTilesRubble1, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.textWallTilesRubble2 = wx.TextCtrl( self.m_panel36, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerWallTilesRumble.Add( self.textWallTilesRubble2, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.textWallTilesRubble3 = wx.TextCtrl( self.m_panel36, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerWallTilesRumble.Add( self.textWallTilesRubble3, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )


		self.m_panel36.SetSizer( sizerWallTilesRumble )
		self.m_panel36.Layout()
		sizerWallTilesRumble.Fit( self.m_panel36 )
		frameWallTilesRumble.Add( self.m_panel36, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer36.Add( frameWallTilesRumble, 0, wx.EXPAND|wx.ALL, 5 )


		self.m_panel35.SetSizer( bSizer36 )
		self.m_panel35.Layout()
		bSizer36.Fit( self.m_panel35 )
		frameWallTiles.Add( self.m_panel35, 1, wx.EXPAND |wx.ALL, 5 )


		sizerWall.Add( frameWallTiles, 0, wx.EXPAND|wx.ALL, 5 )


		self.tabWall.SetSizer( sizerWall )
		self.tabWall.Layout()
		sizerWall.Fit( self.tabWall )
		self.tabctrl.AddPage( self.tabWall, u"Walls", False )
		self.tabTower = wx.Panel( self.tabctrl, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerTower = wx.BoxSizer( wx.VERTICAL )

		frameTowerTimeRange = wx.StaticBoxSizer( wx.StaticBox( self.tabTower, wx.ID_ANY, u"Time Range (centuries)" ), wx.VERTICAL )

		self.m_panel37 = wx.Panel( self.tabTower, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerTowerTimeRange = wx.GridSizer( 0, 3, 3, 0 )

		self.labelTowerTimeRangeSquared = wx.StaticText( self.m_panel37, wx.ID_ANY, u"Squared : ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTowerTimeRangeSquared.Wrap( -1 )
		sizerTowerTimeRange.Add( self.labelTowerTimeRangeSquared, 0, wx.ALL, 5 )

		self.textTowerTimeRangeSquared1 = wx.TextCtrl( self.m_panel37, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTowerTimeRange.Add( self.textTowerTimeRangeSquared1, 0, wx.ALL, 5 )

		self.textTowerTimeRangeSquared2 = wx.TextCtrl( self.m_panel37, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTowerTimeRange.Add( self.textTowerTimeRangeSquared2, 0, wx.ALL, 5 )

		self.labelTowerTimeRangeRounded = wx.StaticText( self.m_panel37, wx.ID_ANY, u"Rounded :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTowerTimeRangeRounded.Wrap( -1 )
		sizerTowerTimeRange.Add( self.labelTowerTimeRangeRounded, 0, wx.ALL, 5 )

		self.textTowerTimeRangeRounded1 = wx.TextCtrl( self.m_panel37, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTowerTimeRange.Add( self.textTowerTimeRangeRounded1, 0, wx.ALL, 5 )

		self.textTowerTimeRangeRounded2 = wx.TextCtrl( self.m_panel37, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTowerTimeRange.Add( self.textTowerTimeRangeRounded2, 0, wx.ALL, 5 )

		self.labelTowerTimeRangeBastion = wx.StaticText( self.m_panel37, wx.ID_ANY, u"Bastion :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTowerTimeRangeBastion.Wrap( -1 )
		sizerTowerTimeRange.Add( self.labelTowerTimeRangeBastion, 0, wx.ALL, 5 )

		self.textTowerTimeRangeBastion1 = wx.TextCtrl( self.m_panel37, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTowerTimeRange.Add( self.textTowerTimeRangeBastion1, 0, wx.ALL, 5 )

		self.textTowerTimeRangeBastion2 = wx.TextCtrl( self.m_panel37, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTowerTimeRange.Add( self.textTowerTimeRangeBastion2, 0, wx.ALL, 5 )


		self.m_panel37.SetSizer( sizerTowerTimeRange )
		self.m_panel37.Layout()
		sizerTowerTimeRange.Fit( self.m_panel37 )
		frameTowerTimeRange.Add( self.m_panel37, 1, wx.EXPAND |wx.ALL, 5 )


		sizerTower.Add( frameTowerTimeRange, 0, wx.EXPAND|wx.ALL, 5 )

		sizerTowerData = wx.GridSizer( 5, 2, 0, 0 )

		self.labelTowerHeight = wx.StaticText( self.tabTower, wx.ID_ANY, u"Height :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTowerHeight.Wrap( -1 )
		sizerTowerData.Add( self.labelTowerHeight, 0, wx.ALL, 5 )

		self.textTowerHeight = wx.TextCtrl( self.tabTower, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTowerData.Add( self.textTowerHeight, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelTowerThickness = wx.StaticText( self.tabTower, wx.ID_ANY, u"Thickness :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTowerThickness.Wrap( -1 )
		sizerTowerData.Add( self.labelTowerThickness, 0, wx.ALL, 5 )

		self.textTowerThickness = wx.TextCtrl( self.tabTower, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTowerData.Add( self.textTowerThickness, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelTowerSide = wx.StaticText( self.tabTower, wx.ID_ANY, u"Side (squared) :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTowerSide.Wrap( -1 )
		sizerTowerData.Add( self.labelTowerSide, 0, wx.ALL, 5 )

		self.textTowerSide = wx.TextCtrl( self.tabTower, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTowerData.Add( self.textTowerSide, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelTowerRadius = wx.StaticText( self.tabTower, wx.ID_ANY, u"Radius (rounded) :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTowerRadius.Wrap( -1 )
		sizerTowerData.Add( self.labelTowerRadius, 0, wx.ALL, 5 )

		self.textTowerRadius = wx.TextCtrl( self.tabTower, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTowerData.Add( self.textTowerRadius, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelTowerDefenseInc = wx.StaticText( self.tabTower, wx.ID_ANY, u"Defense increase :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTowerDefenseInc.Wrap( -1 )
		sizerTowerData.Add( self.labelTowerDefenseInc, 0, wx.ALL, 5 )

		self.textTowerDefenseIncrease = wx.TextCtrl( self.tabTower, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTowerData.Add( self.textTowerDefenseIncrease, 0, wx.ALL|wx.EXPAND, 5 )


		sizerTower.Add( sizerTowerData, 0, wx.EXPAND|wx.ALL, 5 )

		frameTowerDefenseAngle = wx.StaticBoxSizer( wx.StaticBox( self.tabTower, wx.ID_ANY, u"Defense angle" ), wx.VERTICAL )

		self.m_panel38 = wx.Panel(self.tabTower, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerTowerDefenseAngle = wx.GridSizer( 0, 2, 0, 0 )

		self.labelTowerDAH = wx.StaticText( self.m_panel38, wx.ID_ANY, u"Horizontal :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTowerDAH.Wrap( -1 )
		sizerTowerDefenseAngle.Add( self.labelTowerDAH, 0, wx.ALL, 5 )

		self.textTowerDefenseAngleHorizontal = wx.TextCtrl( self.m_panel38, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTowerDefenseAngle.Add( self.textTowerDefenseAngleHorizontal, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelTowerDAV1 = wx.StaticText( self.m_panel38, wx.ID_ANY, u"Vertical (start) :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTowerDAV1.Wrap( -1 )
		sizerTowerDefenseAngle.Add( self.labelTowerDAV1, 0, wx.ALL, 5 )

		self.textTowerDefenseAngleVertical1 = wx.TextCtrl( self.m_panel38, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTowerDefenseAngle.Add( self.textTowerDefenseAngleVertical1, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelTowerDAV2 = wx.StaticText( self.m_panel38, wx.ID_ANY, u"Vertical (end) :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTowerDAV2.Wrap( -1 )
		sizerTowerDefenseAngle.Add( self.labelTowerDAV2, 0, wx.ALL, 5 )

		self.textTowerDefenseAngleVertical2 = wx.TextCtrl( self.m_panel38, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTowerDefenseAngle.Add( self.textTowerDefenseAngleVertical2, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panel38.SetSizer( sizerTowerDefenseAngle )
		self.m_panel38.Layout()
		sizerTowerDefenseAngle.Fit( self.m_panel38 )
		frameTowerDefenseAngle.Add( self.m_panel38, 1, wx.EXPAND |wx.ALL, 5 )


		sizerTower.Add( frameTowerDefenseAngle, 0, wx.EXPAND|wx.ALL, 5 )

		frameTowerCellSize = wx.StaticBoxSizer( wx.StaticBox( self.tabTower, wx.ID_ANY, u"Battalion cell sizes" ), wx.VERTICAL )

		self.m_panel39 = wx.Panel( self.tabTower, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerTowerCellSize = wx.GridSizer( 0, 2, 0, 0 )

		self.labelTowerCellSizeLarge = wx.StaticText( self.m_panel39, wx.ID_ANY, u"Large :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTowerCellSizeLarge.Wrap( -1 )
		sizerTowerCellSize.Add( self.labelTowerCellSizeLarge, 0, wx.ALL, 5 )

		self.textTowerCellSizeLarge = wx.TextCtrl( self.m_panel39, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTowerCellSize.Add( self.textTowerCellSizeLarge, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelTowerCellSizeSmall = wx.StaticText( self.m_panel39, wx.ID_ANY, u"Small :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTowerCellSizeSmall.Wrap( -1 )
		sizerTowerCellSize.Add( self.labelTowerCellSizeSmall, 0, wx.ALL, 5 )

		self.textTowerCellSizeSmall = wx.TextCtrl( self.m_panel39, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTowerCellSize.Add( self.textTowerCellSizeSmall, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panel39.SetSizer( sizerTowerCellSize )
		self.m_panel39.Layout()
		sizerTowerCellSize.Fit( self.m_panel39 )
		frameTowerCellSize.Add( self.m_panel39, 1, wx.EXPAND |wx.ALL, 5 )


		sizerTower.Add( frameTowerCellSize, 0, wx.EXPAND|wx.ALL, 5 )

		sizerTowerDistance = wx.BoxSizer( wx.HORIZONTAL )

		self.labelTowerDistance = wx.StaticText( self.tabTower, wx.ID_ANY, u"Required Distance Neighbor Factor :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTowerDistance.Wrap( -1 )
		sizerTowerDistance.Add( self.labelTowerDistance, 0, wx.ALL, 5 )

		self.textTowerDistance = wx.TextCtrl( self.tabTower, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTowerDistance.Add( self.textTowerDistance, 1, wx.ALL|wx.EXPAND, 5 )


		sizerTower.Add( sizerTowerDistance, 0, wx.EXPAND|wx.ALL, 5 )


		self.tabTower.SetSizer( sizerTower )
		self.tabTower.Layout()
		sizerTower.Fit( self.tabTower )
		self.tabctrl.AddPage( self.tabTower, u"Towers", False )
		self.tabMoat = wx.Panel( self.tabctrl, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerMoat = wx.BoxSizer( wx.VERTICAL )

		sizerMoatData = wx.GridSizer( 0, 2, 0, 0 )

		self.labelMoatDepth = wx.StaticText( self.tabMoat, wx.ID_ANY, u"Depth :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelMoatDepth.Wrap( -1 )
		sizerMoatData.Add( self.labelMoatDepth, 0, wx.ALL, 5 )

		self.textMoatDepth = wx.TextCtrl( self.tabMoat, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerMoatData.Add( self.textMoatDepth, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelMoatWidth = wx.StaticText( self.tabMoat, wx.ID_ANY, u"Width :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelMoatWidth.Wrap( -1 )
		sizerMoatData.Add( self.labelMoatWidth, 0, wx.ALL, 5 )

		self.textMoatWidth = wx.TextCtrl( self.tabMoat, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerMoatData.Add( self.textMoatWidth, 0, wx.ALL|wx.EXPAND, 5 )


		sizerMoat.Add( sizerMoatData, 0, wx.EXPAND|wx.ALL, 5 )

		self.checkMoatHasWater = wx.CheckBox( self.tabMoat, wx.ID_ANY, u"Has water", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerMoat.Add( self.checkMoatHasWater, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		frameMoatPenalty = wx.StaticBoxSizer( wx.StaticBox( self.tabMoat, wx.ID_ANY, u"Movement penalty" ), wx.VERTICAL )

		self.m_panel40 = wx.Panel( self.tabMoat, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerMoatPenalty = wx.GridSizer( 0, 2, 0, 0 )

		self.labelMoatPenaltyWith = wx.StaticText( self.m_panel40, wx.ID_ANY, u"With water :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelMoatPenaltyWith.Wrap( -1 )
		sizerMoatPenalty.Add( self.labelMoatPenaltyWith, 0, wx.ALL, 5 )

		self.textMoatPenaltyWithWater = wx.TextCtrl( self.m_panel40, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerMoatPenalty.Add( self.textMoatPenaltyWithWater, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelMoatPenaltyNoWater = wx.StaticText( self.m_panel40, wx.ID_ANY, u"Without water :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelMoatPenaltyNoWater.Wrap( -1 )
		sizerMoatPenalty.Add( self.labelMoatPenaltyNoWater, 0, wx.ALL, 5 )

		self.textMoatPenaltyWithoutWater = wx.TextCtrl( self.m_panel40, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerMoatPenalty.Add( self.textMoatPenaltyWithoutWater, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panel40.SetSizer( sizerMoatPenalty )
		self.m_panel40.Layout()
		sizerMoatPenalty.Fit( self.m_panel40 )
		frameMoatPenalty.Add( self.m_panel40, 1, wx.EXPAND |wx.ALL, 5 )


		sizerMoat.Add( frameMoatPenalty, 0, wx.EXPAND|wx.ALL, 5 )


		self.tabMoat.SetSizer( sizerMoat )
		self.tabMoat.Layout()
		sizerMoat.Fit( self.tabMoat )
		self.tabctrl.AddPage( self.tabMoat, u"Moat", False )
		self.tabBastion = wx.Panel( self.tabctrl, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerBastion = wx.BoxSizer( wx.VERTICAL )

		sizerBastionData = wx.GridSizer( 0, 2, 0, 0 )

		self.labelBastionHeight = wx.StaticText( self.tabBastion, wx.ID_ANY, u"Height :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelBastionHeight.Wrap( -1 )
		sizerBastionData.Add( self.labelBastionHeight, 0, wx.ALL, 5 )

		self.textBastionHeight = wx.TextCtrl( self.tabBastion, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerBastionData.Add( self.textBastionHeight, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelBastionThickness = wx.StaticText( self.tabBastion, wx.ID_ANY, u"Thickness :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelBastionThickness.Wrap( -1 )
		sizerBastionData.Add( self.labelBastionThickness, 0, wx.ALL, 5 )

		self.textBastionThickness = wx.TextCtrl( self.tabBastion, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerBastionData.Add( self.textBastionThickness, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelBastionVirtualCircleRadius = wx.StaticText( self.tabBastion, wx.ID_ANY, u"Virtual circle radius :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelBastionVirtualCircleRadius.Wrap( -1 )
		sizerBastionData.Add( self.labelBastionVirtualCircleRadius, 0, wx.ALL, 5 )

		self.textBastionVirtualCircleRadius = wx.TextCtrl( self.tabBastion, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerBastionData.Add( self.textBastionVirtualCircleRadius, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelBastionMinDistance = wx.StaticText( self.tabBastion, wx.ID_ANY, u"Min distance :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelBastionMinDistance.Wrap( -1 )
		sizerBastionData.Add( self.labelBastionMinDistance, 0, wx.ALL, 5 )

		self.textBastionMinDistance = wx.TextCtrl( self.tabBastion, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerBastionData.Add( self.textBastionMinDistance, 0, wx.ALL|wx.EXPAND, 5 )


		sizerBastion.Add( sizerBastionData, 0, wx.EXPAND|wx.ALL, 5 )

		frameBastionCellSize = wx.StaticBoxSizer( wx.StaticBox( self.tabBastion, wx.ID_ANY, u"Battalion cell sizes" ), wx.VERTICAL )

		self.m_panel41 = wx.Panel( self.tabBastion, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerBastionCellSize = wx.GridSizer( 0, 2, 0, 0 )

		self.labelBastionCellSizeLarge = wx.StaticText( self.m_panel41, wx.ID_ANY, u"Large :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelBastionCellSizeLarge.Wrap( -1 )
		sizerBastionCellSize.Add( self.labelBastionCellSizeLarge, 0, wx.ALL, 5 )

		self.textBastionCellSizeLarge = wx.TextCtrl( self.m_panel41, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerBastionCellSize.Add( self.textBastionCellSizeLarge, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelBastionCellSizeSmall = wx.StaticText( self.m_panel41, wx.ID_ANY, u"Small :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelBastionCellSizeSmall.Wrap( -1 )
		sizerBastionCellSize.Add( self.labelBastionCellSizeSmall, 0, wx.ALL, 5 )

		self.textBastionCellSizeSmall = wx.TextCtrl( self.m_panel41, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerBastionCellSize.Add( self.textBastionCellSizeSmall, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panel41.SetSizer( sizerBastionCellSize )
		self.m_panel41.Layout()
		sizerBastionCellSize.Fit( self.m_panel41 )
		frameBastionCellSize.Add( self.m_panel41, 1, wx.EXPAND |wx.ALL, 5 )


		sizerBastion.Add( frameBastionCellSize, 0, wx.EXPAND|wx.ALL, 5 )


		self.tabBastion.SetSizer( sizerBastion )
		self.tabBastion.Layout()
		sizerBastion.Fit( self.tabBastion )
		self.tabctrl.AddPage( self.tabBastion, u"Bastions", False )
		self.tabStarFortress = wx.Panel( self.tabctrl, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerStarFortress = wx.BoxSizer( wx.VERTICAL )

		frameFortressRavelin = wx.StaticBoxSizer( wx.StaticBox( self.tabStarFortress, wx.ID_ANY, u"Ravelin" ), wx.VERTICAL )

		self.m_panel42 = wx.Panel( self.tabStarFortress, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerFortressRavelin = wx.GridSizer( 0, 2, 0, 0 )

		self.labelFortressRavelinMethod = wx.StaticText( self.m_panel42, wx.ID_ANY, u"Method (do not change) :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelFortressRavelinMethod.Wrap( -1 )
		sizerFortressRavelin.Add( self.labelFortressRavelinMethod, 0, wx.ALL, 5 )

		self.textFortressRavelinMethod = wx.TextCtrl( self.m_panel42, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerFortressRavelin.Add( self.textFortressRavelinMethod, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelFortressBastionAngle = wx.StaticText( self.m_panel42, wx.ID_ANY, u"Bastion Angle :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelFortressBastionAngle.Wrap( -1 )
		sizerFortressRavelin.Add( self.labelFortressBastionAngle, 0, wx.ALL, 5 )

		self.textFortressRavelinBastionAngle = wx.TextCtrl( self.m_panel42, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerFortressRavelin.Add( self.textFortressRavelinBastionAngle, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelFortressRavelinRadius = wx.StaticText( self.m_panel42, wx.ID_ANY, u"Radius :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelFortressRavelinRadius.Wrap( -1 )
		sizerFortressRavelin.Add( self.labelFortressRavelinRadius, 0, wx.ALL, 5 )

		self.textFortressRavelinRadius = wx.TextCtrl( self.m_panel42, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerFortressRavelin.Add( self.textFortressRavelinRadius, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelFortressRavelinMinWidth = wx.StaticText( self.m_panel42, wx.ID_ANY, u"Min Width :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelFortressRavelinMinWidth.Wrap( -1 )
		sizerFortressRavelin.Add( self.labelFortressRavelinMinWidth, 0, wx.ALL, 5 )

		self.textFortressRavelinMinWidth = wx.TextCtrl( self.m_panel42, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerFortressRavelin.Add( self.textFortressRavelinMinWidth, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelFortressRavelinHeight = wx.StaticText( self.m_panel42, wx.ID_ANY, u"Height :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelFortressRavelinHeight.Wrap( -1 )
		sizerFortressRavelin.Add( self.labelFortressRavelinHeight, 0, wx.ALL, 5 )

		self.textFortressRavelinHeight = wx.TextCtrl( self.m_panel42, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerFortressRavelin.Add( self.textFortressRavelinHeight, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panel42.SetSizer( sizerFortressRavelin )
		self.m_panel42.Layout()
		sizerFortressRavelin.Fit( self.m_panel42 )
		frameFortressRavelin.Add( self.m_panel42, 1, wx.EXPAND |wx.ALL, 5 )


		sizerStarFortress.Add( frameFortressRavelin, 0, wx.EXPAND|wx.ALL, 5 )

		frameFortressHalfmoon = wx.StaticBoxSizer( wx.StaticBox( self.tabStarFortress, wx.ID_ANY, u"Half moon" ), wx.VERTICAL )

		self.m_panel43 = wx.Panel( self.tabStarFortress, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer38 = wx.BoxSizer( wx.VERTICAL )

		self.checkFortressHalfmoon = wx.CheckBox( self.m_panel43, wx.ID_ANY, u"Active", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer38.Add( self.checkFortressHalfmoon, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		sizerFortressHalfmoon = wx.GridSizer( 0, 2, 0, 0 )

		self.labelFortressHalfmoonCircle = wx.StaticText( self.m_panel43, wx.ID_ANY, u"Circle radius :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelFortressHalfmoonCircle.Wrap( -1 )
		sizerFortressHalfmoon.Add( self.labelFortressHalfmoonCircle, 0, wx.ALL, 5 )

		self.textFortressHalfmonnCircleRadius = wx.TextCtrl( self.m_panel43, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerFortressHalfmoon.Add( self.textFortressHalfmonnCircleRadius, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelFortressHalfmoonHeight = wx.StaticText( self.m_panel43, wx.ID_ANY, u"Height :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelFortressHalfmoonHeight.Wrap( -1 )
		sizerFortressHalfmoon.Add( self.labelFortressHalfmoonHeight, 0, wx.ALL, 5 )

		self.textFortressHalfmoonHeight = wx.TextCtrl( self.m_panel43, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerFortressHalfmoon.Add( self.textFortressHalfmoonHeight, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelFortressHalfmoonLength = wx.StaticText( self.m_panel43, wx.ID_ANY, u"Length :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelFortressHalfmoonLength.Wrap( -1 )
		sizerFortressHalfmoon.Add( self.labelFortressHalfmoonLength, 0, wx.ALL, 5 )

		self.textFortressHalfmoonLength = wx.TextCtrl( self.m_panel43, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerFortressHalfmoon.Add( self.textFortressHalfmoonLength, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer38.Add( sizerFortressHalfmoon, 1, wx.EXPAND, 5 )


		self.m_panel43.SetSizer( bSizer38 )
		self.m_panel43.Layout()
		bSizer38.Fit( self.m_panel43 )
		frameFortressHalfmoon.Add( self.m_panel43, 1, wx.EXPAND |wx.ALL, 5 )


		sizerStarFortress.Add( frameFortressHalfmoon, 0, wx.EXPAND|wx.ALL, 5 )

		frameFortressCovertWay = wx.StaticBoxSizer( wx.StaticBox( self.tabStarFortress, wx.ID_ANY, u"Covert way" ), wx.VERTICAL )

		self.m_panel44 = wx.Panel( self.tabStarFortress, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer39 = wx.BoxSizer( wx.VERTICAL )

		sizerFortressCoverWay = wx.GridSizer( 0, 2, 0, 0 )

		self.labelFortressCovertwayHeight = wx.StaticText( self.m_panel44, wx.ID_ANY, u"Height :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelFortressCovertwayHeight.Wrap( -1 )
		sizerFortressCoverWay.Add( self.labelFortressCovertwayHeight, 0, wx.ALL, 5 )

		self.textFortressCovertwayHeight = wx.TextCtrl( self.m_panel44, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerFortressCoverWay.Add( self.textFortressCovertwayHeight, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelFortressCovertwayThickness = wx.StaticText( self.m_panel44, wx.ID_ANY, u"Thickness :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelFortressCovertwayThickness.Wrap( -1 )
		sizerFortressCoverWay.Add( self.labelFortressCovertwayThickness, 0, wx.ALL, 5 )

		self.textFortressCovertwayThickness = wx.TextCtrl( self.m_panel44, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerFortressCoverWay.Add( self.textFortressCovertwayThickness, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelFortressCovertwayOffset = wx.StaticText( self.m_panel44, wx.ID_ANY, u"Offset :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelFortressCovertwayOffset.Wrap( -1 )
		sizerFortressCoverWay.Add( self.labelFortressCovertwayOffset, 0, wx.ALL, 5 )

		self.textFortressCovertwayOffset = wx.TextCtrl( self.m_panel44, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerFortressCoverWay.Add( self.textFortressCovertwayOffset, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelFortressCovertwayMinseglength = wx.StaticText( self.m_panel44, wx.ID_ANY, u"Min segment length :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelFortressCovertwayMinseglength.Wrap( -1 )
		sizerFortressCoverWay.Add( self.labelFortressCovertwayMinseglength, 0, wx.ALL, 5 )

		self.textFortressCovertwayMinseglength = wx.TextCtrl( self.m_panel44, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerFortressCoverWay.Add( self.textFortressCovertwayMinseglength, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer39.Add( sizerFortressCoverWay, 1, wx.EXPAND|wx.ALL, 5 )

		frameFortressPlaceofarms = wx.StaticBoxSizer( wx.StaticBox( self.m_panel44, wx.ID_ANY, u"Place of arms" ), wx.VERTICAL )

		self.m_panel45 = wx.Panel( self.m_panel44, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer40 = wx.BoxSizer( wx.VERTICAL )

		self.checkFortressPlaceofarms = wx.CheckBox( self.m_panel45, wx.ID_ANY, u"Active", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer40.Add( self.checkFortressPlaceofarms, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		sizerFortressPlaceofarms = wx.GridSizer( 0, 2, 0, 0 )

		self.labelFortresPlaceofarms = wx.StaticText( self.m_panel45, wx.ID_ANY, u"Length :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelFortresPlaceofarms.Wrap( -1 )
		sizerFortressPlaceofarms.Add( self.labelFortresPlaceofarms, 0, wx.ALL, 5 )

		self.textFortressPlaceofarmsLength = wx.TextCtrl( self.m_panel45, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerFortressPlaceofarms.Add( self.textFortressPlaceofarmsLength, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer40.Add( sizerFortressPlaceofarms, 1, wx.EXPAND, 5 )


		self.m_panel45.SetSizer( bSizer40 )
		self.m_panel45.Layout()
		bSizer40.Fit( self.m_panel45 )
		frameFortressPlaceofarms.Add( self.m_panel45, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer39.Add( frameFortressPlaceofarms, 0, wx.EXPAND|wx.ALL, 5 )

		frameFortressGlacis = wx.StaticBoxSizer( wx.StaticBox( self.m_panel44, wx.ID_ANY, u"Glacis" ), wx.VERTICAL )

		self.m_panel46 = wx.Panel( self.m_panel44, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerFortressGlacier = wx.GridSizer( 0, 2, 0, 0 )

		self.labelFortressGlacisHeight = wx.StaticText( self.m_panel46, wx.ID_ANY, u"Height :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelFortressGlacisHeight.Wrap( -1 )
		sizerFortressGlacier.Add( self.labelFortressGlacisHeight, 0, wx.ALL, 5 )

		self.textFortressGlacisHeight = wx.TextCtrl( self.m_panel46, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerFortressGlacier.Add( self.textFortressGlacisHeight, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelFortressGlacisThickness = wx.StaticText( self.m_panel46, wx.ID_ANY, u"Thickness :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelFortressGlacisThickness.Wrap( -1 )
		sizerFortressGlacier.Add( self.labelFortressGlacisThickness, 0, wx.ALL, 5 )

		self.textFortressGlacisThickness = wx.TextCtrl( self.m_panel46, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerFortressGlacier.Add( self.textFortressGlacisThickness, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panel46.SetSizer( sizerFortressGlacier )
		self.m_panel46.Layout()
		sizerFortressGlacier.Fit( self.m_panel46 )
		frameFortressGlacis.Add( self.m_panel46, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer39.Add( frameFortressGlacis, 0, wx.EXPAND|wx.ALL, 5 )


		self.m_panel44.SetSizer( bSizer39 )
		self.m_panel44.Layout()
		bSizer39.Fit( self.m_panel44 )
		frameFortressCovertWay.Add( self.m_panel44, 1, wx.EXPAND |wx.ALL, 5 )


		sizerStarFortress.Add( frameFortressCovertWay, 0, wx.EXPAND|wx.ALL, 5 )


		self.tabStarFortress.SetSizer( sizerStarFortress )
		self.tabStarFortress.Layout()
		sizerStarFortress.Fit( self.tabStarFortress )
		self.tabctrl.AddPage( self.tabStarFortress, u"StarFortress", False )

		sizer.Add( self.tabctrl, 1, wx.EXPAND |wx.ALL, 5 )

		m_sdbSizer3 = wx.StdDialogButtonSizer()
		self.m_sdbSizer3OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer3.AddButton( self.m_sdbSizer3OK )
		self.m_sdbSizer3Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer3.AddButton( self.m_sdbSizer3Cancel )
		m_sdbSizer3.Realize();

		sizer.Add( m_sdbSizer3, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


		self.SetSizer( sizer )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass
