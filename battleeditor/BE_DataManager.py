import BE_Objects
import BE_GameData
import BE_DefaultSettings
import BE_3DSettings
import wx
import Battles.Run


class BE_DataManager:

    """ Data manager class

        Attributes:
            gamedata: Game data
            canvasObjects: Dictionary with all defined canvas objects (walls, rivers, ...) The dictionary key is the class type, and value is an array with the list
                            of objects of the same type
            defaultSettings: Default settings
            selection: Current selected object
            3DSettings: exportation 3D settings

    """

    def __init__(self):

        self.__gameData = BE_GameData.BE_GameData()
        self.__canvasObjects = {}
        self.__defaultSettings = BE_DefaultSettings.BE_DefaultSettings()
        self.__3DSettings = BE_3DSettings.BE_3DSettings()
        self.__selection = None




    def AddCanvasObject(self, canvasobject = BE_Objects.BE_Object()):
        # Adds a canvas object to the dictionary. Given object must be BE_CanvasObject type

        kind = canvasobject.GetType()

        if (not self.__canvasObjects.has_key(kind)):
            self.__canvasObjects[kind] = [canvasobject]
        else:
            self.__canvasObjects[kind].append(canvasobject)



    def Draw(self, dc, canvas):
        # Draws all canvas objects using given context

        for kind in self.__canvasObjects:
            for obj in self.__canvasObjects[kind]:
                obj.Draw(dc, self, canvas)

        # Draws a bounding rectangle around the selected object
        if (self.__selection):

            lastpen = dc.GetPen()
            dc.SetPen(wx.Pen(wx.Colour(100, 100, 100, wx.ALPHA_OPAQUE), 1, wx.SHORT_DASH))

            bbox = self.__selection.GetBoundingBox()
            bbox.Expand(10)
            seglist = bbox.GetSegments()
            for seg in seglist:
                p1 = canvas.UserToScreenCoord(seg.p1.x, seg.p1.y)
                p2 = canvas.UserToScreenCoord(seg.p2.x, seg.p2.y)
                dc.DrawLine(p1.x, p1.y, p2.x, p2.y)

            dc.SetPen(lastpen)



    def DeleteCanvasObject(self, obj):

        for objkey in self.__canvasObjects:
            for o in self.__canvasObjects[objkey]:
                if (o.GetID() == obj.GetID()):
                    self.__canvasObjects[objkey].remove(o)

                    if (self.__selection == obj):
                        self.__selection = None

                    return True

        return False




    def GetDefaultSettings(self):
        return self.__defaultSettings


    def GetGameData(self):
        return self.__gameData


    def Get3DSettings(self):
        return self.__3DSettings



    def GetCanvasObjectsByType(self, type):
        if (self.__canvasObjects.has_key(type)):
            return self.__canvasObjects[type]
        else:
            return None



    def Select(self, point):
        # Try to select an object

        self.__selection = None

        # Get the selectable objects in the seletion preference order (trying to helping on overlapping objects, such is the castle)

        # Houses
        houses = self.GetCanvasObjectsByType(BE_Objects.BE_Object.CANVASOBJECT_HOUSE)
        if (houses and (len(houses) > 0)):
            for h in houses:
                if (h.Select(point)):
                    self.__selection = h
                    return

        # Flanks
        flanks = self.GetCanvasObjectsByType(BE_Objects.BE_Object.CANVASOBJECT_FLANK)
        if (flanks and (len(flanks) > 0)):
            for f in flanks:
                if (f.Select(point)):
                    self.__selection = f
                    return

        # City evolutions
        cityevolutions = self.GetCanvasObjectsByType(BE_Objects.BE_Object.CANVASOBJECT_CITYEVOLUTION)
        if (cityevolutions and (len(cityevolutions) > 0)):
            for ev in cityevolutions:
                if (ev.Select(point)):
                    self.__selection = ev
                    return

        # Rivers
        rivers = self.GetCanvasObjectsByType(BE_Objects.BE_Object.CANVASOBJECT_RIVER)
        if (rivers and (len(rivers) > 0)):
            for r in rivers:
                if (r.Select(point)):
                    self.__selection = r
                    return

        # Castle
        castle = self.GetCanvasObjectsByType(BE_Objects.BE_Object.CANVASOBJECT_CASTLE)
        if (castle and (len(castle) > 0)):
            if (castle[0].Select(point)):
                self.__selection = castle[0]
                return


    def IsSelected(self):
        return self.__selection != None

    def ResetSelect(self):
        self.__selection = None


    def EditSelected(self, parentwindow):
        if (self.__selection):
            self.__selection.Edit(parentwindow)


    def DeleteSelected(self):
        if (self.__selection):
            if (self.DeleteCanvasObject(self.__selection)):
                self.__selection = None





    def Play(self):
        # Executes the simulation with current data

        self.__defaultSettings.ExportXML("./__tmp_default.xml")
        self.__gameData.ExportXML("./__tmp_game.xml", self)
        self.__3DSettings.ExportXML("./__tmp_3d.xml")

        game = Battles.Run.Run(playdataxml = "./__tmp_game.xml", settingsxml = "./__tmp_default.xml", export3dxml = "./__tmp_3d.xml")
        game.execute()



    def SaveDefaultSettings(self, filename):
        self.__defaultSettings.ExportXML(filename)

    def LoadDefaultSettings(self, filename, mainwindow):
        self.__defaultSettings.ImportXML(filename, mainwindow)


    def SaveGameData(self, filename):
        self.__gameData.ExportXML(filename, self)

    def LoadGameData(self, filename):
        del self.__gameData
        self.__gameData = BE_GameData.BE_GameData()
        self.__canvasObjects.clear()
        self.__gameData.ImportXML(filename, self)
        pass

    def Save3DSettings(self, filename):
        self.__3DSettings.ExportXML(filename)

    def Load3DSettings(self, filename):
        del self.__3DSettings
        self.__3DSettings = BE_3DSettings.BE_3DSettings()
        self.__3DSettings.ImportXML(filename)

