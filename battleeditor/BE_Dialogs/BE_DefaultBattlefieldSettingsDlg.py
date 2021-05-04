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
## Class BE_DefaultBattlefieldSettings
###########################################################################


# WARNING!! wxFormBuilderBug -> StaticBoxes must have only one children, a Panel. This can be done in the UI builder, but the other child controls, under the panel,
#                                set their parents as the staticbox, not the panel. If this is not solved, the program finishes without showing any warning or error message
#                               So, manual edition must be performed to change this. BE AWARE updating this file



class BE_DefaultBattlefieldSettingsDlg ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Default battlefield settings", pos = wx.DefaultPosition, size = wx.Size( 385,619 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

		sizer = wx.BoxSizer( wx.VERTICAL )

		sizerSize = wx.GridSizer( 0, 2, 0, 0 )

		self.labelSize = wx.StaticText( self, wx.ID_ANY, u"Size (square side) :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelSize.Wrap( -1 )
		sizerSize.Add( self.labelSize, 0, wx.ALL, 5 )

		self.textSize = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerSize.Add( self.textSize, 0, wx.ALL|wx.EXPAND, 5 )


		sizer.Add( sizerSize, 0, wx.EXPAND|wx.ALL, 5 )

		frameGroundcell = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Ground cells" ), wx.VERTICAL )

		self.m_panel29 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerGroundcell = wx.GridSizer( 0, 2, 0, 0 )

		self.labelGroundSize = wx.StaticText( self.m_panel29, wx.ID_ANY, u"Size :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelGroundSize.Wrap( -1 )
		sizerGroundcell.Add( self.labelGroundSize, 0, wx.ALL, 5 )

		self.textGroundcellSize = wx.TextCtrl( self.m_panel29, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerGroundcell.Add( self.textGroundcellSize, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelGroundHeight = wx.StaticText( self.m_panel29, wx.ID_ANY, u"Height :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelGroundHeight.Wrap( -1 )
		sizerGroundcell.Add( self.labelGroundHeight, 0, wx.ALL, 5 )

		self.textGroundcellHeight = wx.TextCtrl( self.m_panel29, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerGroundcell.Add( self.textGroundcellHeight, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelGroundDefenseInc = wx.StaticText( self.m_panel29, wx.ID_ANY, u"Defense increase :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelGroundDefenseInc.Wrap( -1 )
		sizerGroundcell.Add( self.labelGroundDefenseInc, 0, wx.ALL, 5 )

		self.textGroundcellDefenseIncrease = wx.TextCtrl( self.m_panel29, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerGroundcell.Add( self.textGroundcellDefenseIncrease, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelGroundPenalty = wx.StaticText( self.m_panel29, wx.ID_ANY, u"Penalty movement :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelGroundPenalty.Wrap( -1 )
		sizerGroundcell.Add( self.labelGroundPenalty, 0, wx.ALL, 5 )

		self.textGroundcellPenaltyMovement = wx.TextCtrl( self.m_panel29, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerGroundcell.Add( self.textGroundcellPenaltyMovement, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panel29.SetSizer( sizerGroundcell )
		self.m_panel29.Layout()
		sizerGroundcell.Fit( self.m_panel29 )
		frameGroundcell.Add( self.m_panel29, 1, wx.EXPAND |wx.ALL, 5 )


		sizer.Add( frameGroundcell, 0, wx.EXPAND|wx.ALL, 5 )

		frameTrench = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Trenches" ), wx.VERTICAL )

		self.m_panel30 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer33 = wx.BoxSizer( wx.VERTICAL )

		sizerTrench = wx.GridSizer( 0, 2, 0, 0 )

		self.labelTrenchDefenseInc = wx.StaticText( self.m_panel30, wx.ID_ANY, u"Defense increase :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTrenchDefenseInc.Wrap( -1 )
		sizerTrench.Add( self.labelTrenchDefenseInc, 0, wx.ALL, 5 )

		self.textTrenchDefenseIncrease = wx.TextCtrl( self.m_panel30, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTrench.Add( self.textTrenchDefenseIncrease, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelTrenchPenalty = wx.StaticText( self.m_panel30, wx.ID_ANY, u"Movement penalty :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTrenchPenalty.Wrap( -1 )
		sizerTrench.Add( self.labelTrenchPenalty, 0, wx.ALL, 5 )

		self.textTrenchPenaltyMovement = wx.TextCtrl( self.m_panel30, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTrench.Add( self.textTrenchPenaltyMovement, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer33.Add( sizerTrench, 1, wx.EXPAND, 5 )

		self.checkTrenchShowoutline = wx.CheckBox( self.m_panel30, wx.ID_ANY, u"Show outline", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer33.Add( self.checkTrenchShowoutline, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		frameTrenchRandomDeployment = wx.StaticBoxSizer( wx.StaticBox( self.m_panel30, wx.ID_ANY, u"Random deployment" ), wx.VERTICAL )

		self.m_panel31 = wx.Panel( self.m_panel30, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizerTrenchRandom = wx.GridSizer( 0, 2, 0, 0 )

		self.labelTrenchRandomValue = wx.StaticText( self.m_panel31, wx.ID_ANY, u"Factor :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTrenchRandomValue.Wrap( -1 )
		sizerTrenchRandom.Add( self.labelTrenchRandomValue, 0, wx.ALL, 5 )

		self.textTrenchRandomDeployment = wx.TextCtrl( self.m_panel31, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTrenchRandom.Add( self.textTrenchRandomDeployment, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelTrenchRandomConsecutive = wx.StaticText( self.m_panel31, wx.ID_ANY, u"Consecutive factor :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTrenchRandomConsecutive.Wrap( -1 )
		sizerTrenchRandom.Add( self.labelTrenchRandomConsecutive, 0, wx.ALL, 5 )

		self.textTrenchRandomDeploymentConsecutive = wx.TextCtrl( self.m_panel31, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTrenchRandom.Add( self.textTrenchRandomDeploymentConsecutive, 0, wx.ALL|wx.EXPAND, 5 )

		self.labelTrenchRandomMaxtries = wx.StaticText( self.m_panel31, wx.ID_ANY, u"Max tries :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelTrenchRandomMaxtries.Wrap( -1 )
		sizerTrenchRandom.Add( self.labelTrenchRandomMaxtries, 0, wx.ALL, 5 )

		self.textTrenchRandomDeploymentMaxTries = wx.TextCtrl( self.m_panel31, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTrenchRandom.Add( self.textTrenchRandomDeploymentMaxTries, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panel31.SetSizer( sizerTrenchRandom )
		self.m_panel31.Layout()
		sizerTrenchRandom.Fit( self.m_panel31 )
		frameTrenchRandomDeployment.Add( self.m_panel31, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer33.Add( frameTrenchRandomDeployment, 0, wx.EXPAND|wx.ALL, 5 )


		self.m_panel30.SetSizer( bSizer33 )
		self.m_panel30.Layout()
		bSizer33.Fit( self.m_panel30 )
		frameTrench.Add( self.m_panel30, 1, wx.EXPAND |wx.ALL, 5 )


		sizer.Add( frameTrench, 0, wx.EXPAND|wx.ALL, 5 )

		sizerRiver = wx.GridSizer( 0, 2, 0, 0 )

		self.labelRiverPenalty = wx.StaticText( self, wx.ID_ANY, u"Penalty movement :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.labelRiverPenalty.Wrap( -1 )
		sizerRiver.Add( self.labelRiverPenalty, 0, wx.ALL, 5 )

		self.textRiverPenalty = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerRiver.Add( self.textRiverPenalty, 0, wx.ALL|wx.EXPAND, 5 )


		sizer.Add( sizerRiver, 0, wx.EXPAND|wx.ALL, 5 )

		m_sdbSizer4 = wx.StdDialogButtonSizer()
		self.m_sdbSizer4OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer4.AddButton( self.m_sdbSizer4OK )
		self.m_sdbSizer4Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer4.AddButton( self.m_sdbSizer4Cancel )
		m_sdbSizer4.Realize();

		sizer.Add( m_sdbSizer4, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


		self.SetSizer( sizer )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


