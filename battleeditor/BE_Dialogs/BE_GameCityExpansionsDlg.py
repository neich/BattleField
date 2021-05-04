# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class BE_GameCityExpansionsDlg
###########################################################################

class BE_GameCityExpansionsDlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"City Expansions", pos = wx.DefaultPosition, size = wx.Size( 465,406 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer40 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer41 = wx.BoxSizer( wx.VERTICAL )
		
		self.grid = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.grid.CreateGrid( 0, 4 )
		self.grid.EnableEditing( True )
		self.grid.EnableGridLines( True )
		self.grid.EnableDragGridSize( False )
		self.grid.SetMargins( 0, 0 )
		
		# Columns
		self.grid.SetColSize( 0, 110 )
		self.grid.SetColSize( 1, 110 )
		self.grid.SetColSize( 2, 110 )
		self.grid.SetColSize( 3, 110 )
		self.grid.EnableDragColMove( False )
		self.grid.EnableDragColSize( True )
		self.grid.SetColLabelSize( 30 )
		self.grid.SetColLabelValue( 0, u"Group ID" )
		self.grid.SetColLabelValue( 1, u"Year" )
		self.grid.SetColLabelValue( 2, u"Walls height" )
		self.grid.SetColLabelValue( 3, u"Towers height" )
		self.grid.SetColLabelValue( 4, wx.EmptyString )
		self.grid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.grid.EnableDragRowSize( True )
		self.grid.SetRowLabelSize( 0 )
		self.grid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer41.Add( self.grid, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer42 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panel52 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer39 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel52, wx.ID_ANY, u"Walls length" ), wx.VERTICAL )
		
		gSizer60 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText171 = wx.StaticText( self.m_panel52, wx.ID_ANY, u"Min wall length :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText171.Wrap( -1 )
		gSizer60.Add( self.m_staticText171, 1, wx.ALL, 5 )
		
		self.textWallDimMin = wx.TextCtrl( self.m_panel52, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer60.Add( self.textWallDimMin, 0, wx.ALL, 5 )
		
		self.m_staticText172 = wx.StaticText(self.m_panel52, wx.ID_ANY, u"Max wall length :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText172.Wrap( -1 )
		gSizer60.Add( self.m_staticText172, 0, wx.ALL, 5 )
		
		self.textWallDimMax = wx.TextCtrl( self.m_panel52, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer60.Add( self.textWallDimMax, 0, wx.ALL, 5 )
		
		
		sbSizer39.Add( gSizer60, 0, wx.ALL, 5 )
		
		
		self.m_panel52.SetSizer( sbSizer39 )
		self.m_panel52.Layout()
		sbSizer39.Fit( self.m_panel52 )
		bSizer42.Add( self.m_panel52, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer49 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText173 = wx.StaticText( self, wx.ID_ANY, u"Years between expansions :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText173.Wrap( -1 )
		bSizer49.Add( self.m_staticText173, 0, wx.ALL, 5 )

		self.textYearsBetween = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer49.Add( self.textYearsBetween, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )



		
		bSizer42.Add( bSizer49, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer41.Add( bSizer42, 0, wx.ALL, 5 )
		
		
		bSizer40.Add( bSizer41, 1, wx.ALL, 5 )
		
		m_sdbSizer12 = wx.StdDialogButtonSizer()
		self.m_sdbSizer12OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer12.AddButton( self.m_sdbSizer12OK )
		self.m_sdbSizer12Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer12.AddButton( self.m_sdbSizer12Cancel )
		m_sdbSizer12.Realize();
		
		bSizer40.Add( m_sdbSizer12, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.SetSizer( bSizer40 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

