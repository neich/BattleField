import wx
import BE_Canvas
import BE_EventHandler
import BE_DataManager

# Main Battle editor window class and related menus and toolbars



class BE_MainWindow(wx.Frame):

    """ Main Window class. It creates the main layout and connects the binding events. Also contains the document data. That is, this class is some kind of Controller
        in a pseudo MVC pattern, where Model is the document, and View is controlled by canvas and event handler classes

        Attributes:
            document: Document class, the data manager
            eventHandler: Event handler class for managing the button/menu events and canvas events
            menu: Application menu
            toolbar: Window toolbar
            statusbar: Window statusbar
            canvas: Central widget where canvas objects are drawn
    """

    def __init__(self, parent, title = 'Battles Editor'):
        wx.Frame.__init__(self, parent, title = title, size = (1047, 1052), style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)

        # Document class
        self.__document = BE_DataManager.BE_DataManager()


        # Event Handler. Pass to menu and toolbar objects to configure the bindings
        self.__eventHandler = BE_EventHandler.BE_EventHandler(self)

        # Menu
        self.__menu = BE_Menu(self, self.__eventHandler)
        self.SetMenuBar(self.__menu)

        # Toolbar
        self.__toolbar = self.CreateToolBar(style = wx.TB_RIGHT)
        self.__toolbar.AddLabelTool(BE_Menu.ID_MENUDRAW_CASTLE, "Add River", wx.Bitmap('img/castle.png'))
        self.__toolbar.AddLabelTool(BE_Menu.ID_MENUDRAW_RIVER, "Define castle", wx.Bitmap('img/river.png'))
        self.__toolbar.AddLabelTool(BE_Menu.ID_MENUDRAW_OLDCITY, "Define oldtown", wx.Bitmap('img/house.png'))
        self.__toolbar.AddLabelTool(BE_Menu.ID_MENUDRAW_CITYEVOLUTION, "Add City Evolution", wx.Bitmap('img/cityevolution.png'))
        self.__toolbar.AddLabelTool(BE_Menu.ID_MENUDRAW_FLANK, "Add Flank", wx.Bitmap('img/flank.png'))
        self.__toolbar.AddSeparator()
        self.__toolbar.AddLabelTool(BE_Menu.ID_MENUDRAW_EDIT, "Edit selected", wx.Bitmap('img/edit.png'))
        self.__toolbar.AddLabelTool(BE_Menu.ID_MENUDRAW_DELETE, "Delete selected", wx.Bitmap('img/delete.png'))
        self.__toolbar.AddSeparator()
        self.__toolbar.AddLabelTool(BE_Menu.ID_MENUFILE_PLAY, "Play", wx.Bitmap('img/play.png'))
        self.__toolbar.Realize()


        # Status bar
        self.__statusbar = self.CreateStatusBar()

        # Canvas
        self.__canvas = BE_Canvas.BE_Canvas(self, pos = (200, 0), size = (100,  100), style = wx.BORDER_SIMPLE, eventhandler = self.__eventHandler , document = self.__document)


        # Bindings
        self.__canvas.Bind(wx.EVT_LEFT_DOWN, self.__eventHandler.OnMouseClick)
        self.__canvas.Bind(wx.EVT_LEFT_DCLICK, self.__eventHandler.OnMouseDoubleClick)
        self.__canvas.Bind(wx.EVT_RIGHT_DOWN, self.__eventHandler.OnCancel)               # There are many problems gathering the keyboard events. The right mouse
                                                                                            # button click will be the action cancel event
        self.__canvas.Bind(wx.EVT_MOTION, self.__eventHandler.OnMouseMove)




    def OnClose(self, event):
        self.Close()



    # Return the canvas DC
    def GetCanvasDC(self):
        return wx.ClientDC(self.__canvas)

    # Return the canvas
    def GetCanvas(self):
        return self.__canvas


    # Return the document
    def GetDocument(self):
        return self.__document


    # Returns the event handler manager
    def GetEventHandler(self):
        return self.__eventHandler


    # Sets the cursor type on canvas
    def SetCanvasCursor(self, cursor):
        self.__canvas.SetCursor(cursor)




class BE_Menu(wx.MenuBar):

    """ Menu class manager
    """

    # Menu own identifiers
    ID_MENUDRAW_CASTLE = 1000
    ID_MENUDRAW_RIVER = 1001
    ID_MENUDRAW_OLDCITY = 1002
    ID_MENUDRAW_CITYEVOLUTION = 1003
    ID_MENUDRAW_FLANK = 1004
    ID_MENUDRAW_EDIT = 1009
    ID_MENUDRAW_DELETE = 1010
    ID_MENUDRAW_BACKGROUND = 1020

    ID_MENUDEFAULTSETTINGS_GAME = 1100
    ID_MENUDEFAULTSETTINGS_CITY = 1101
    ID_MENUDEFAULTSETTINGS_ARMY = 1102
    ID_MENUDEFAULTSETTINGS_BATTLEFIELD = 1103
    ID_MENUDEFAULTSETTINGS_CASTLE = 1104

    ID_MENUFILE_SAVEDEFAULTS = 1200
    ID_MENUFILE_SAVEGAMEDATA = 1201
    ID_MENUFILE_SAVE3D = 1202
    ID_MENUFILE_PLAY = 1203
    ID_MENUFILE_LOADGAMEDATA = 1204
    ID_MENUFILE_LOADDEFAULTS = 1205
    ID_MENUFILE_LOAD3D = 1206


    ID_MENUGAMEDATA_TYPE = 1300
    ID_MENUGAMEDATA_TIMERANGE = 1301
    ID_MENUGAMEDATA_BATTLEFIELD = 1302
    ID_MENUGAMEDATA_CITYEXPANSIONS = 1303
    ID_MENUGAMEDATA_BATTLES = 1304
    ID_MENUGAMEDATA_STARFORTRESS = 1305
    ID_MENUGAMEDATA_EXPANSIONCHECKINGS = 1306

    ID_MENU3D_SETTINGS = 1400


    def __init__(self, mainwindow, eventhandler):
        wx.MenuBar.__init__(self)

        # File menu
        fileMenu = wx.Menu()
        loadgame = fileMenu.Append(self.ID_MENUFILE_LOADGAMEDATA, "Load game data")
        loaddefault = fileMenu.Append(self.ID_MENUFILE_LOADDEFAULTS, "Load default settings")
        load3d = fileMenu.Append(self.ID_MENUFILE_LOAD3D, "Load 3D settings")
        fileMenu.AppendSeparator()
        savegame = fileMenu.Append(self.ID_MENUFILE_SAVEGAMEDATA, "Save game data")
        savedefault = fileMenu.Append(self.ID_MENUFILE_SAVEDEFAULTS, "Save default settings")
        save3d = fileMenu.Append(self.ID_MENUFILE_SAVE3D, "Save 3D settings")
        fileMenu.AppendSeparator()
        play = fileMenu.Append(self.ID_MENUFILE_PLAY, "Play")
        fileMenu.AppendSeparator()
        fileexit = fileMenu.Append(wx.ID_EXIT, "Exit")

        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnLoadGameData, loadgame)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnLoadDefaultSettings, loaddefault)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnLoad3DSettings, load3d)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnSaveGameData, savegame)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnSaveDefaultSettings, savedefault)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnSave3DSettings, save3d)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnPlay, play)
        mainwindow.Bind(wx.EVT_MENU, mainwindow.OnClose, fileexit)

        # Draw menu
        drawMenu = wx.Menu()
        addcastle = drawMenu.Append(self.ID_MENUDRAW_CASTLE, "Define Castle")
        addriver = drawMenu.Append(self.ID_MENUDRAW_RIVER, "Add River")
        addoldcity = drawMenu.Append(self.ID_MENUDRAW_OLDCITY, "Define Oldtown")
        addcityevolution = drawMenu.Append(self.ID_MENUDRAW_CITYEVOLUTION, "Add City Evolution")
        addflank = drawMenu.Append(self.ID_MENUDRAW_FLANK, "Add Flank")
        drawMenu.AppendSeparator()
        editselected = drawMenu.Append(self.ID_MENUDRAW_EDIT, "Edit selected")
        deleteselected = drawMenu.Append(self.ID_MENUDRAW_DELETE, "Delete selected")
        drawMenu.AppendSeparator()
        setbackground = drawMenu.Append(self.ID_MENUDRAW_BACKGROUND, "Set background helper")


        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnAddCastle, addcastle)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnAddRiver, addriver)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnAddOldcity, addoldcity)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnAddCityEvolution, addcityevolution)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnAddFlank, addflank)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnEditSelected, editselected)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnDeleteSelected, deleteselected)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnSetBackgroundHelper, setbackground)

        # Default settings menu
        defaultsettings = wx.Menu()
        defaultcastle = defaultsettings.Append(self.ID_MENUDEFAULTSETTINGS_CASTLE, "Castle")
        defaultbattlefield = defaultsettings.Append(self.ID_MENUDEFAULTSETTINGS_BATTLEFIELD, "Battlefield")
        defaultarmy = defaultsettings.Append(self.ID_MENUDEFAULTSETTINGS_ARMY, "Army")
        defaultcity = defaultsettings.Append(self.ID_MENUDEFAULTSETTINGS_CITY, "City")
        defaultgame = defaultsettings.Append(self.ID_MENUDEFAULTSETTINGS_GAME, "Game")

        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnDefaultSettingsCastle, defaultcastle)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnDefaultSettingsBattlefield, defaultbattlefield)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnDefaultSettingsArmy, defaultarmy)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnDefaultSettingsCity, defaultcity)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnDefaultSettingsGame, defaultgame)


        # Game data menu
        gamedata = wx.Menu()
        gametype = gamedata.Append(self.ID_MENUGAMEDATA_TYPE, "Game type")
        gametimerange = gamedata.Append(self.ID_MENUGAMEDATA_TIMERANGE, "Time range")
        gamebattlefield = gamedata.Append(self.ID_MENUGAMEDATA_BATTLEFIELD, "Battlefield")
        gamecityexpansions = gamedata.Append(self.ID_MENUGAMEDATA_CITYEXPANSIONS, "City expansions")
        gamebattles = gamedata.Append(self.ID_MENUGAMEDATA_BATTLES, "Battles")
        gamestarfortress = gamedata.Append(self.ID_MENUGAMEDATA_STARFORTRESS, "Star Fortrees")
        gameexpcheck = gamedata.Append(self.ID_MENUGAMEDATA_EXPANSIONCHECKINGS, "Expansion checkings")

        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnGameDataType, gametype)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnGameDataTimeRange, gametimerange)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnGameDataBattlefield, gamebattlefield)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnGameDataCityExpansions, gamecityexpansions)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnGameDataBattles, gamebattles)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnGameDataStarFortress, gamestarfortress)
        mainwindow.Bind(wx.EVT_MENU, eventhandler.OnGameDataExpansionCheckings, gameexpcheck)


        # 3D menu
        menu3d = wx.Menu()
        menu3dsettings = menu3d.Append(self.ID_MENU3D_SETTINGS, "3D Settings")

        mainwindow.Bind(wx.EVT_MENU, eventhandler.On3DSettings, menu3dsettings)





        self.Append(fileMenu, "File")
        self.Append(gamedata, "Game data")
        self.Append(drawMenu, "Draw")
        self.Append(defaultsettings, "Defaul settings")
        self.Append(menu3d, "3D")
