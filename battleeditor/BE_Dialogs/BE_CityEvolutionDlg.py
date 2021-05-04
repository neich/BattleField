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
## Class BE_CityEvolutionDlg
###########################################################################

class BE_CityEvolutionDlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"City Evolution", pos = wx.DefaultPosition, size = wx.Size( 304,232 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer38 = wx.BoxSizer( wx.VERTICAL )
		
		gSizer46 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText167 = wx.StaticText( self, wx.ID_ANY, u"Start time (year) :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText167.Wrap( -1 )
		gSizer46.Add( self.m_staticText167, 0, wx.ALL, 5 )
		
		self.textTimeRangeStart = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer46.Add( self.textTimeRangeStart, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText168 = wx.StaticText( self, wx.ID_ANY, u"End time (year) :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText168.Wrap( -1 )
		gSizer46.Add( self.m_staticText168, 0, wx.ALL, 5 )
		
		self.textTimeRangeEnd = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer46.Add( self.textTimeRangeEnd, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText169 = wx.StaticText( self, wx.ID_ANY, u"Houses per year :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText169.Wrap( -1 )
		gSizer46.Add( self.m_staticText169, 0, wx.ALL, 5 )
		
		self.textHousesYear = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer46.Add( self.textHousesYear, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText170 = wx.StaticText( self, wx.ID_ANY, u"Group ID :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText170.Wrap( -1 )
		gSizer46.Add( self.m_staticText170, 0, wx.ALL, 5 )
		
		self.textGroupID = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer46.Add( self.textGroupID, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer38.Add( gSizer46, 0, wx.EXPAND|wx.ALL, 5 )
		
		
		bSizer38.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		m_sdbSizer11 = wx.StdDialogButtonSizer()
		self.m_sdbSizer11OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer11.AddButton( self.m_sdbSizer11OK )
		self.m_sdbSizer11Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer11.AddButton( self.m_sdbSizer11Cancel )
		m_sdbSizer11.Realize();
		
		bSizer38.Add( m_sdbSizer11, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.SetSizer( bSizer38 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

