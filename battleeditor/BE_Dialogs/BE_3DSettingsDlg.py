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
## Class BE_3DSettingsDlg
###########################################################################

class BE_3DSettingsDlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"3D Settings", pos = wx.DefaultPosition, size = wx.Size( 284,508 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer48 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText191 = wx.StaticText( self, wx.ID_ANY, u"Output folder :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText191.Wrap( -1 )
		bSizer48.Add( self.m_staticText191, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL, 5 )
		
		bSizer56 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.textFolder = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer56.Add( self.textFolder, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.butFolder = wx.Button( self, wx.ID_ANY, u"...", wx.DefaultPosition, wx.Size( 30,-1 ), 0 )
		bSizer56.Add( self.butFolder, 0, wx.ALL, 5 )
		
		
		bSizer48.Add( bSizer56, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_panel53 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer38 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel53, wx.ID_ANY, u"Castle" ), wx.VERTICAL )
		
		self.m_panel54 = wx.Panel( self.m_panel53, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer51 = wx.BoxSizer( wx.VERTICAL )
		
		self.checkWalls = wx.CheckBox( self.m_panel54, wx.ID_ANY, u"Walls", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer51.Add( self.checkWalls, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.checkTowers = wx.CheckBox( self.m_panel54, wx.ID_ANY, u"Towers", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer51.Add( self.checkTowers, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.m_panel54.SetSizer( bSizer51 )
		self.m_panel54.Layout()
		bSizer51.Fit( self.m_panel54 )
		sbSizer38.Add( self.m_panel54, 0, wx.EXPAND |wx.ALL, 5 )
		
		
		self.m_panel53.SetSizer( sbSizer38 )
		self.m_panel53.Layout()
		sbSizer38.Fit( self.m_panel53 )
		bSizer48.Add( self.m_panel53, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_panel51 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer34 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel51, wx.ID_ANY, u"Star Fortress" ), wx.VERTICAL )
		
		self.m_panel49 = wx.Panel( self.m_panel51, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer49 = wx.BoxSizer( wx.VERTICAL )
		
		self.checkRavelins = wx.CheckBox( self.m_panel49, wx.ID_ANY, u"Ravelins", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer49.Add( self.checkRavelins, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.checkHalfMoons = wx.CheckBox( self.m_panel49, wx.ID_ANY, u"HalfMoons", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer49.Add( self.checkHalfMoons, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.checkCovertWay = wx.CheckBox( self.m_panel49, wx.ID_ANY, u"Covert Way", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer49.Add( self.checkCovertWay, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.m_panel49.SetSizer( bSizer49 )
		self.m_panel49.Layout()
		bSizer49.Fit( self.m_panel49 )
		sbSizer34.Add( self.m_panel49, 0, wx.EXPAND |wx.ALL, 5 )
		
		
		self.m_panel51.SetSizer( sbSizer34 )
		self.m_panel51.Layout()
		sbSizer34.Fit( self.m_panel51 )
		bSizer48.Add( self.m_panel51, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_panel52 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer35 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel52, wx.ID_ANY, u"Houses" ), wx.VERTICAL )
		
		self.m_panel50 = wx.Panel( self.m_panel52, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer50 = wx.BoxSizer( wx.VERTICAL )
		
		self.checkHouses = wx.CheckBox( self.m_panel50, wx.ID_ANY, u"Houses", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer50.Add( self.checkHouses, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.checkHousesSeparatedFile = wx.CheckBox( self.m_panel50, wx.ID_ANY, u"Use extra file", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer50.Add( self.checkHousesSeparatedFile, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		gSizer55 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText190 = wx.StaticText( self.m_panel50, wx.ID_ANY, u"Extra file suffix :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText190.Wrap( -1 )
		gSizer55.Add( self.m_staticText190, 0, wx.ALL, 5 )
		
		self.textHousesSuffix = wx.TextCtrl( self.m_panel50, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer55.Add( self.textHousesSuffix, 0, wx.ALL, 5 )
		
		
		bSizer50.Add( gSizer55, 1, wx.EXPAND|wx.ALL, 5 )
		
		
		self.m_panel50.SetSizer( bSizer50 )
		self.m_panel50.Layout()
		bSizer50.Fit( self.m_panel50 )
		sbSizer35.Add( self.m_panel50, 0, wx.EXPAND |wx.ALL, 5 )
		
		
		self.m_panel52.SetSizer( sbSizer35 )
		self.m_panel52.Layout()
		sbSizer35.Fit( self.m_panel52 )
		bSizer48.Add( self.m_panel52, 0, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer48.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		m_sdbSizer17 = wx.StdDialogButtonSizer()
		self.m_sdbSizer17OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer17.AddButton( self.m_sdbSizer17OK )
		self.m_sdbSizer17Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer17.AddButton( self.m_sdbSizer17Cancel )
		m_sdbSizer17.Realize();
		
		bSizer48.Add( m_sdbSizer17, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		
		self.SetSizer( bSizer48 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	
