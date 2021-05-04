# Set of simulation objects (drawable objects). Do not confuse with Battle package objects. Current ones are only used to be defined and edited, and contain just
# the required data to define them

import wx
import Battles.Utils.Geometry as Geometry
import BE_Dialogs.BE_MoatDlg
import BE_Dialogs.BE_CityEvolutionDlg
import BE_Dialogs.BE_FlankDlg



OBJECT_COUNTER = 0


class BE_Object:
    """ Base class for data objects

        Attributes:
            type: free string with the type of object
            ID: Object identifier
    """


    # Canvas object label
    CANVASOBJECT_NONE = 0
    CANVASOBJECT_RIVER = 1
    CANVASOBJECT_CASTLE = 2
    CANVASOBJECT_TOWER = 3
    CANVASOBJECT_HOUSE = 4
    CANVASOBJECT_CITYEVOLUTION = 5
    CANVASOBJECT_FLANK = 6




    def __init__(self):

        self._type = self.CANVASOBJECT_NONE

        global OBJECT_COUNTER;
        OBJECT_COUNTER += 1
        self.__ID = OBJECT_COUNTER



    def GetID(self):
        return self.__ID

    def GetType(self):
        return self._type

    def SetShape(self):
        # Sets the shape data. Each derived class must implement its own
        pass

    def Draw(self, dc, document, canvas):
        pass

    def GetBoundingBox(self):
        # Returns a BoundingBox object for current object
        return Geometry.BoundingQuad()


    def Select(self, point):
        # Returns true if given point "selects" current object
        bbox = self.GetBoundingBox()
        return bbox.IsInside(point)


    def Edit(self, parentwindow):
        # Edits the object information specified when the object was created (not default or game data)
        pass




class BE_River(BE_Object):
    """ River object

        Attributes:
            polyline: array of Point2D that define the river shape
            width: river width
    """

    def __init__(self):

        BE_Object.__init__(self)

        self._type = self.CANVASOBJECT_RIVER
        self.__polyline = []
        self.__width = 0




    def SetShape(self, pointslist, width):
        # Creates a river from an array of points

        self.__polyline = []

        i = 0
        while ( i < len(pointslist) ):
            self.__polyline.append(pointslist[i].Copy())
            i += 1

        self.__width = width


    def GetWidth(self):
        return self.__width


    def GetShape(self):
        return self.__polyline




    def Draw(self, dc, document, canvas):

        width = canvas.UserToScreenValue(self.__width)    # NOTE: This sould be changed if window/viewport are not squared

        lastpen = dc.GetPen()
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 255, wx.ALPHA_OPAQUE), width))

        i = 1
        while (i < len(self.__polyline)):
            p1 = canvas.UserToScreenCoord(self.__polyline[i-1].x, self.__polyline[i-1].y)
            p2 = canvas.UserToScreenCoord(self.__polyline[i].x, self.__polyline[i].y)
            dc.DrawLine(p1.x, p1.y, p2.x, p2.y)
            i += 1

        dc.SetPen(lastpen)



    def GetBoundingBox(self):
        bbox = Geometry.BoundingQuad()

        for p in self.__polyline:
            bbox.InsertPoint(p)

        bbox.Expand(self.__width)

        return bbox


    def Select(self, point):
        # Since river is a nonclosed polyline, we need to check the selection over each polyline segment

        i = 1
        while (i < len(self.__polyline)):
            seg = Geometry.Segment2D(self.__polyline[i-1], self.__polyline[i])
            poly = seg.GetBounding(self.__width / 2.0)
            bbox = Geometry.BoundingQuad()
            for p in poly.shape:
                bbox.InsertPoint(p.p1)
            if (len(poly.shape) > 0):
                bbox.InsertPoint(poly.shape[-1].p2)
            if (bbox.IsInside(point)):
                return True

            i += 1

        return False



    def Edit(self, parentwindow):

        dlg = wx.TextEntryDialog(parentwindow,'Enter the river width','Add River', str(self.__width))
        ret = dlg.ShowModal()
        if ret == wx.ID_OK:
            try:
                self.__width = float(dlg.GetValue())
            except:
                pass

        dlg.Destroy()








class BE_Castle(BE_Object):
    """ Castle shape object

        Attributes:
            polyline: array of Point2D that define the river shape. Each point has a BE_CanvasTower associated data
            thickness: walls thickness
            isClosed: True if castle is closed. This must be ever true when polyline is ready. It is used to check at draw time if the castle is in create mode
            moat: Castle moat data. See Usage documentation to know more about it
    """

    def __init__(self):
        BE_Object.__init__(self)
        self._type = self.CANVASOBJECT_CASTLE
        self.__shape = []
        self.__isClosed = False
        self.__moat = {'Active': False, 'HasWater': False}

    def AddVertex(self, vertex = Geometry.Point2D()):
        self.__shape.append(vertex)

    def GetNVertices(self):
        return len(self.__shape)

    def SetMoat(self, active = False, width = 0, haswater = False):
        self.__moat['Active'] = active
        self.__moat['HasWater'] = haswater

    def GetMoat(self):
        return self.__moat

    def GetShape(self):
        return self.__shape


    def Close(self):
        self.__isClosed = True

    def Draw(self, dc, document, canvas):

        castledata = document.GetDefaultSettings().castle

        lastpen = dc.GetPen()

        # Draw the moat
        if (self.__moat['Active']):

            moatwidth = canvas.UserToScreenValue(castledata.moat.width)    # NOTE: This sould be changed if window/viewport are not squared

            if (self.__moat['HasWater']):
                dc.SetPen(wx.Pen(wx.Colour(162, 215, 245, wx.ALPHA_OPAQUE), moatwidth))
            else:
                dc.SetPen(wx.Pen(wx.Colour(128, 181, 72, wx.ALPHA_OPAQUE), moatwidth))

            # Expand the castle shape to cover it
            pol = Geometry.Polygon2D()
            pol.SetPointsList(self.__shape)

            gpc = Geometry.GPCWrapper()
            if (not gpc.IsCCW(self.__shape)):
                pol.SwitchOrientation()

            pol.Expand((castledata.walls.thickness / 2.0) + (castledata.moat.width / 2))
            plist = pol.GetPointsList()

            i = 1
            while (i < len(plist)):
                p1 = canvas.UserToScreenCoord(plist[i-1].x, plist[i-1].y)
                p2 = canvas.UserToScreenCoord(plist[i].x, plist[i].y)
                dc.DrawLine(p1.x, p1.y, p2.x, p2.y)
                i += 1
            if (len(plist) > 2):
                p1 = canvas.UserToScreenCoord(plist[-1].x, plist[-1].y)
                p2 = canvas.UserToScreenCoord( plist[0].x, plist[0].y)
                dc.DrawLine(p1.x, p1.y, p2.x, p2.y)


        thickness = canvas.UserToScreenValue(castledata.walls.thickness)    # NOTE: This sould be changed if window/viewport are not squared

        dc.SetPen(wx.Pen(wx.Colour(130, 130, 130, wx.ALPHA_OPAQUE), thickness))

        # Draw the walls
        i = 1
        while (i < len(self.__shape)):
            p1 = canvas.UserToScreenCoord(self.__shape[i-1].x, self.__shape[i-1].y)
            p2 = canvas.UserToScreenCoord(self.__shape[i].x, self.__shape[i].y)
            dc.DrawLine(p1.x, p1.y, p2.x, p2.y)
            i += 1
        if (self.__isClosed and (len(self.__shape) > 2)):
            p1 = canvas.UserToScreenCoord(self.__shape[-1].x, self.__shape[-1].y)
            p2 = canvas.UserToScreenCoord( self.__shape[0].x, self.__shape[0].y)
            dc.DrawLine(p1.x, p1.y, p2.x, p2.y)

        # Draw the towers
        i = 0
        while (i < len(self.__shape)):
            tower = self.__shape[i].data
            if (tower):
                tower.Draw(dc, document,canvas)
            i += 1

        dc.SetPen(lastpen)



    def GetBoundingBox(self):
        bbox = Geometry.BoundingQuad()

        for p in self.__shape:
            bbox.InsertPoint(p)

        for p in self.__shape:
            if (p.data):
                bbox.Expand(p.data.size)
                break

        return bbox




    def Edit(self, parentwindow):

        # Edit the moat castle data

        dlg = BE_Dialogs.BE_MoatDlg.BE_MoatDlg(parentwindow)

        dlg.checkActive.SetValue(self.__moat['Active'])
        dlg.checkHasWater.SetValue(self.__moat['HasWater'])

        ret = dlg.ShowModal()
        if (ret == wx.ID_OK):

            self.__moat['Active'] = dlg.checkActive.GetValue()
            self.__moat['HasWater'] = dlg.checkHasWater.GetValue()


        dlg.Destroy()




class BE_Tower(BE_Object):
    """ Tower shape object. It can be squared, rounded or bastion

        Attributes:
            center: Tower center
            towertype: Tower type. See definitions below
            side: Tower side (for squared ones)
            radius: Tower radius (for rounded ones)
            size: internal size value, related to the towers size, used only to get the bounding box
    """


    # Tower types
    TOWERTYPE_SQUARED = 0
    TOWERTYPE_ROUNDED = 1
    TOWERTYPE_RANDOM = 2

    def __init__(self, towertype, center = Geometry.Point2D()):
        BE_Object.__init__(self)
        self._type = self.CANVASOBJECT_TOWER
        self.__towertype = towertype
        self.__center = center
        self.size = 0.0


    def GetTowerType(self):
        return self.__towertype




    def Draw(self, dc, document, canvas):

        towerdata = document.GetDefaultSettings().castle.towers
        self.size = towerdata.squareSide / 2.0

        lastpen = dc.GetPen()
        dc.SetPen(wx.Pen(wx.Colour(100, 100, 100, wx.ALPHA_OPAQUE), 1))

        if (self.__towertype == self.TOWERTYPE_SQUARED):
            center = self.__center.Copy()
            center.Move(Geometry.Vector2D(-1,-1), towerdata.squareSide / 2.0)
            center = canvas.UserToScreenCoord(center.x, center.y)
            side = canvas.UserToScreenValue(towerdata.squareSide)    # NOTE: This sould be changed if window/viewport are not squared
            dc.DrawRectangle(center.x, center.y, side, side)

        if (self.__towertype == self.TOWERTYPE_ROUNDED):
            center = self.__center.Copy()
            center.Move(Geometry.Vector2D(-1,-1), towerdata.circleRadius / 2.0)
            center = canvas.UserToScreenCoord(center.x, center.y)
            radius = canvas.UserToScreenValue(towerdata.circleRadius)    # NOTE: This sould be changed if window/viewport are not squared
            dc.DrawEllipse(center.x, center.y, radius*2, radius*2)

        if (self.__towertype == self.TOWERTYPE_RANDOM):
            lastfont = dc.GetFont()
            currfont = wx.Font(pointSize = 25, family = wx.FONTFAMILY_DEFAULT, style = wx.FONTSTYLE_NORMAL, weight = wx.FONTWEIGHT_BOLD)
            dc.SetFont(currfont)
            center = canvas.UserToScreenCoord(self.__center.x, self.__center.y)
            dc.DrawText("?", center.x, center.y)
            dc.SetFont(lastfont)

        dc.SetPen(lastpen)


    def Select(self, point):
        # Towers are not selectable, only the whole castle
        return False



class BE_House(BE_Object):
    """ House shape object

        Attributes:
            center: House center Point2D object
            size: internal house size value, used only to get the bounding box (where city houses settings are not available)
    """

    def __init__(self, center):
        BE_Object.__init__(self)
        self._type = self.CANVASOBJECT_HOUSE
        self.center = center
        self.__size = 8.0


    def Draw(self, dc, document, canvas):

        citydata = document.GetDefaultSettings().city
        self.__size = citydata.housesSize

        lastpen = dc.GetPen()
        lastbrush = dc.GetBrush()
        dc.SetPen(wx.Pen(wx.Colour(141, 114, 71, wx.ALPHA_OPAQUE), 1))
        dc.SetBrush(wx.Brush(wx.Colour(234, 207, 160), wx.SOLID))

        p = self.center.Copy()
        p.Move(Geometry.Vector2D(-1,-1), citydata.housesSize / 2.0)

        p = canvas.UserToScreenCoord(p.x, p.y)
        size = canvas.UserToScreenValue(citydata.housesSize)    # NOTE: This sould be changed if window/viewport are not squared. A polygon should be calculated instead
        dc.DrawRectangle(p.x, p.y, size, size)

        dc.SetBrush(lastbrush)
        dc.SetPen(lastpen)


    def GetBoundingBox(self):
        bbox = Geometry.BoundingQuad()

        p = self.center.Copy()
        p.Move(Geometry.Vector2D(-1,-1), self.__size / 2.0)
        bbox.InsertPoint(p)
        p = self.center.Copy()
        p.Move(Geometry.Vector2D(-1,1), self.__size / 2.0)
        bbox.InsertPoint(p)
        p = self.center.Copy()
        p.Move(Geometry.Vector2D(1,-1), self.__size / 2.0)
        bbox.InsertPoint(p)
        p = self.center.Copy()
        p.Move(Geometry.Vector2D(1,1), self.__size / 2.0)
        bbox.InsertPoint(p)

        return bbox



class BE_CityEvolution(BE_Object):

    """ City evolution object

        Attributes:
            timerange: range of time (in years) to execute the evolution
            basesegment: base segment used to start the evolution
            arrow: evolution direction vector, represented as a segment, from basesegment mid point to the arrow edge
            housesperyear: number of houses per year (it can be < 1)
            groupID: ID of evolution group
    """

    # Color array. Each city evolution is drawn using the same color than other city evolutions with the same groupID
    COLOR_GROUP = ["ORANGE", "MAGENTA" , "PINK", "AQUAMARINE", "VIOLET", "MAROON", "GREEN YELLOW", "STEEL BLUE", "DARK GREEN", "FIREBRICK", "SALMON", "TURQUOISE", "GOLD", "KHAKI"]



    def __init__(self):

        BE_Object.__init__(self)
        self._type = self.CANVASOBJECT_CITYEVOLUTION
        self.timeRange = [0,0]
        self.baseSegment = Geometry.Segment2D()
        self.arrow = Geometry.Segment2D()
        self.housesPerYear = 1
        self.groupID = 0
        self.__colorDB = wx.ColourDatabase()


    def Draw(self, dc, document, canvas):

        # Get the colour from the groupID. A better approach would be to take it randomly, but there are the risk of obtaining too close colors
        # The main drawback of this method is that the number of groups is limited, so it is the number of colors. But a huge number of available colors should
        # be enough

        groupcolor = self.__colorDB.Find(self.COLOR_GROUP[self.groupID % len(self.COLOR_GROUP)])

        lastpen = dc.GetPen()
        lastbrush = dc.GetBrush()
        dc.SetPen(wx.Pen(groupcolor, 2))
        dc.SetBrush(wx.Brush(groupcolor, wx.SOLID))

        base1 = canvas.UserToScreenCoord(self.baseSegment.p1.x, self.baseSegment.p1.y)
        base2 = canvas.UserToScreenCoord(self.baseSegment.p2.x, self.baseSegment.p2.y)
        arrow1 = canvas.UserToScreenCoord(self.arrow.p1.x, self.arrow.p1.y)
        arrow2 = canvas.UserToScreenCoord(self.arrow.p2.x, self.arrow.p2.y)
        dc.DrawLine(base1.x, base1.y, base2.x, base2.y)
        dc.DrawLine(arrow1.x, arrow1.y, arrow2.x, arrow2.y)

        arrowshape = self.arrow.GetArrow(atEnd = True, size = 30, arrowangle = 20)
        plist = []
        for p in arrowshape:
            parr = canvas.UserToScreenCoord(p.x, p.y)
            plist.append([parr.x, parr.y])
        dc.DrawPolygon(plist)


        dc.SetBrush(lastbrush)
        dc.SetPen(lastpen)



    def GetBoundingBox(self):

        bbox = Geometry.BoundingQuad()

        bbox.InsertPoint(self.baseSegment.p1)
        bbox.InsertPoint(self.baseSegment.p2)
        bbox.InsertPoint(self.arrow.p2)

        return bbox


    def Edit(self, parentwindow):

        # Edits the timerange, houses per year, and groupID

        dlg = BE_Dialogs.BE_CityEvolutionDlg.BE_CityEvolutionDlg(parentwindow)

        dlg.textGroupID.SetValue(str(self.groupID))
        dlg.textTimeRangeStart.SetValue(str(self.timeRange[0]))
        dlg.textTimeRangeEnd.SetValue(str(self.timeRange[1]))
        dlg.textHousesYear.SetValue(str(self.housesPerYear))

        if (dlg.ShowModal() == wx.ID_OK):

            try:
                self.timeRange[0] = int(dlg.textTimeRangeStart.GetValue())
                self.timeRange[1] = int(dlg.textTimeRangeEnd.GetValue())
            except:
                pass

            try:
                self.housesPerYear = float(dlg.textHousesYear.GetValue())
            except:
                pass

            try:
                self.groupID = int(dlg.textGroupID.GetValue())
            except:
                pass



        dlg.Destroy()




class BE_Flank(BE_Object):

    """ Flank object. It is related to a battle on a specific year. All same year flanks are drawn with the same color

        Attributes:
            year: related battle year
            standDistance: (see Usage documentation)
            origin: flank origin
            target: flank target
            battalions: dictonary with the kind of battalions for this flank. Each one is a dictionary -> {'Number', 'BattalionSize', 'GroupSize', 'GroupDistance'}
    """

    def __init__(self):

        BE_Object.__init__(self)
        self._type = self.CANVASOBJECT_FLANK

        self.year = 0
        self.standDistance = None
        self.origin = Geometry.Point2D()
        self.target = Geometry.Point2D()

        self.battalions = {}
        self.battalions['Infantry'] = {'Number': None, 'BattalionSize': None, 'GroupSize': None, 'GroupDistance': None}
        self.battalions['Archers'] = {'Number': None, 'BattalionSize': None, 'GroupSize': None, 'GroupDistance': None}
        self.battalions['Cannons'] = {'Number': None, 'BattalionSize': None, 'GroupSize': None, 'GroupDistance': None}
        self.battalions['SiegeTowers'] = {'Number': None, 'BattalionSize': None, 'GroupSize': None, 'GroupDistance': None}


    def Draw(self, dc, document, canvas):

        battle = document.GetGameData().battles.GetBattle(self.year)
        if (not battle):
            return
        if (not battle.color):
            return

        lastpen = dc.GetPen()
        lastbrush = dc.GetBrush()
        dc.SetPen(wx.Pen(battle.color, 1))
        dc.SetBrush(wx.Brush(battle.color, wx.BDIAGONAL_HATCH))

        plist = []
        axis = Geometry.Segment2D(self.origin, self.target)
        length = axis.GetLength()
        direction = axis.GetDirection()
        normal = axis.GetNormal()

        arrowwidth = 20
        arrowcapheight = 50
        arrowcapwidth = 50


        p = self.origin.Copy()
        p.Move(normal, arrowwidth / 2.0)
        plist.append([p.x, p.y])
        p.Move(direction, length - arrowcapheight)
        plist.append([p.x, p.y])
        p.Move(normal, (arrowcapwidth / 2.0) - (arrowwidth / 2.0))
        plist.append([p.x, p.y])
        plist.append([self.target.x, self.target.y])
        p.Move(normal, -arrowcapwidth)
        plist.append([p.x, p.y])
        p.Move(normal, (arrowcapwidth / 2.0) - (arrowwidth / 2.0))
        plist.append([p.x, p.y])
        p = self.origin.Copy()
        p.Move(normal, -arrowwidth / 2.0)
        plist.append([p.x, p.y])

        plistcanvas = []
        for pl in plist:
            pc = canvas.UserToScreenCoord(pl[0], pl[1])
            plistcanvas.append([pc.x, pc.y])

        dc.DrawPolygon(plistcanvas)

        dc.SetBrush(lastbrush)
        dc.SetPen(lastpen)


    def GetBoundingBox(self):

        # TODO: Improve bounding over arrow (not box)

        bbox = Geometry.BoundingQuad()

        bbox.InsertPoint(self.origin)
        bbox.InsertPoint(self.target)
        bbox.Expand(20)

        return bbox


    def Edit(self, parentwindow):

        dlg = BE_Dialogs.BE_FlankDlg.BE_FlankDlg(parentwindow)

        if (self.standDistance):
            dlg.textStandDistance.SetValue(str(self.standDistance))

        # Populate the battalions data

        if (self.battalions['Infantry']['Number']):
            dlg.textInfantryNumber.SetValue(str(self.battalions['Infantry']['Number']))
        if (self.battalions['Infantry']['BattalionSize']):
            dlg.textInfantryBattalionSize.SetValue(str(self.battalions['Infantry']['BattalionSize']))
        if (self.battalions['Infantry']['GroupSize']):
            dlg.textInfantryGroupSize.SetValue(str(self.battalions['Infantry']['GroupSize']))
        if (self.battalions['Infantry']['GroupDistance']):
            dlg.textInfantryGroupDistance.SetValue(str(self.battalions['Infantry']['GroupDistance']))

        if (self.battalions['Archers']['Number']):
            dlg.textArchersNumber.SetValue(str(self.battalions['Archers']['Number']))
        if (self.battalions['Archers']['BattalionSize']):
            dlg.textArchersBattalionSize.SetValue(str(self.battalions['Archers']['BattalionSize']))
        if (self.battalions['Archers']['GroupSize']):
            dlg.textArchersGroupSize.SetValue(str(self.battalions['Archers']['GroupSize']))
        if (self.battalions['Archers']['GroupDistance']):
            dlg.textArchersGroupDistance.SetValue(str(self.battalions['Archers']['GroupDistance']))

        if (self.battalions['Cannons']['Number']):
            dlg.textCannonsNumber.SetValue(str(self.battalions['Cannons']['Number']))
        if (self.battalions['Cannons']['BattalionSize']):
            dlg.textCannonsBattalionSize.SetValue(str(self.battalions['Cannons']['BattalionSize']))
        if (self.battalions['Cannons']['GroupSize']):
            dlg.textCannonsGroupSize.SetValue(str(self.battalions['Cannons']['GroupSize']))
        if (self.battalions['Cannons']['GroupDistance']):
            dlg.textCannonsGroupDistance.SetValue(str(self.battalions['Cannons']['GroupDistance']))

        if (self.battalions['SiegeTowers']['Number']):
            dlg.textSiegeTowersNumber.SetValue(str(self.battalions['SiegeTowers']['Number']))
        if (self.battalions['SiegeTowers']['BattalionSize']):
            dlg.textSiegeTowersBattalionSize.SetValue(str(self.battalions['SiegeTowers']['BattalionSize']))
        if (self.battalions['SiegeTowers']['GroupSize']):
            dlg.textSiegeTowersGroupSize.SetValue(str(self.battalions['SiegeTowers']['GroupSize']))
        if (self.battalions['SiegeTowers']['GroupDistance']):
            dlg.textSiegeTowersGroupDistance.SetValue(str(self.battalions['SiegeTowers']['GroupDistance']))


        # Populate the years dialog combolist
        battleslist = parentwindow.GetDocument().GetGameData().battles.GetBattlesYears()
        i = 0
        sel = 0
        for year in battleslist:
            dlg.comboYear.Append(str(year))
            if (year == self.year):
                sel = i
            i += 1
        dlg.comboYear.SetSelection(sel)

        if (dlg.ShowModal() == wx.ID_OK):

            try:
                self.year = int(dlg.comboYear.GetStringSelection())
            except:
                return

            try:
                self.standDistance = float(dlg.textStandDistance.GetValue())
            except:
                pass

            try:
                self.battalions['Infantry']['Number'] = int(dlg.textInfantryNumber.GetValue())
            except:
                pass
            try:
                self.battalions['Infantry']['BattalionSize'] = int(dlg.textInfantryBattalionSize.GetValue())
            except:
                pass
            try:
                self.battalions['Infantry']['GroupSize'] = int(dlg.textInfantryGroupSize.GetValue())
            except:
                pass
            try:
                self.battalions['Infantry']['GroupDistance'] = int(dlg.textInfantryGroupSize.GetValue())
            except:
                pass



            try:
                self.battalions['Archers']['Number'] = int(dlg.textArchersNumber.GetValue())
            except:
                pass
            try:
                self.battalions['Archers']['BattalionSize'] = int(dlg.textArchersBattalionSize.GetValue())
            except:
                pass
            try:
                self.battalions['Archers']['GroupSize'] = int(dlg.textArchersGroupSize.GetValue())
            except:
                pass
            try:
                self.battalions['Archers']['GroupDistance'] = int(dlg.textArchersGroupSize.GetValue())
            except:
                pass




            try:
                self.battalions['Cannons']['Number'] = int(dlg.textCannonsNumber.GetValue())
            except:
                pass
            try:
                self.battalions['Cannons']['BattalionSize'] = int(dlg.textCannonsBattalionSize.GetValue())
            except:
                pass
            try:
                self.battalions['Cannons']['GroupSize'] = int(dlg.textCannonsGroupSize.GetValue())
            except:
                pass
            try:
                self.battalions['Cannons']['GroupDistance'] = int(dlg.textCannonsGroupSize.GetValue())
            except:
                pass


            try:
                self.battalions['SiegeTowers']['Number'] = int(dlg.textSiegeTowersNumber.GetValue())
            except:
                pass
            try:
                self.battalions['SiegeTowers']['BattalionSize'] = int(dlg.textSiegeTowersBattalionSize.GetValue())
            except:
                pass
            try:
                self.battalions['SiegeTowers']['GroupSize'] = int(dlg.textSiegeTowersGroupSize.GetValue())
            except:
                pass
            try:
                self.battalions['SiegeTowers']['GroupDistance'] = int(dlg.textSiegeTowersGroupSize.GetValue())
            except:
                pass



        dlg.Destroy()


