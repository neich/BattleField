import wx
import BE_Dialogs.BE_TowersDialog
import BE_Dialogs.BE_MoatDlg
import BE_Dialogs.BE_CityEvolutionDlg
import BE_Dialogs.BE_FlankDlg
import Battles.Utils.Geometry as Geometry
import BE_Objects



class BE_HandlerCanvas:

    """ Handler base class to manage the creation and edition of 2D shapes
        When the shape is created, the given object receiver is populate with its data and sent to the data manager
        By default, it shows the current coordinates on the status bar
        Also, it controls the object selection

        Attributes:
            status: Current handler status (see types below)
            mainWindow: Reference to the main window to get access to the canvas and document
            currMousePos: Current mouse position
            prevMousePos: Previous mouse position (to the current one)
            receiver: Canvas object that will receive the data created in the action and stored into the document
    """

    # Status types
    STATUS_NOTSTARTED = 0
    STATUS_STARTED = 1
    STATUS_FINISHED = 2

    def __init__(self, mainwindow):
        self._status = self.STATUS_NOTSTARTED
        self._mainWindow = mainwindow
        self._curMousePos = Geometry.Point2D()
        self._prevMousePos = Geometry.Point2D()
        self._receiver = None

    def GetCanvas(self):
        return self._mainWindow.GetCanvas()

    def Move(self, x, y, dc):
        # Mouse move handler. Receives screen coordinates and canvas DC
        p = self.GetCanvas().ScreenToUserCoord(x,y)

        self._prevMousePos = self._curMousePos.Copy()
        self._curMousePos = p.Copy()
        self._mainWindow.SetStatusText(str(p.x) + ', ' + str(p.y))

    def Click(self, x, y):

        p = self.GetCanvas().ScreenToUserCoord(x,y)
        self._mainWindow.GetDocument().Select(p)
        self._mainWindow.Refresh()


    def DoubleClick(self, x, y):
        pass

    def Finish(self):
        self._status = self.STATUS_FINISHED
        if (self._receiver):
            self._mainWindow.GetDocument().AddCanvasObject(self._receiver)
        self._mainWindow.GetEventHandler().ResetAction()
        self._mainWindow.Refresh()


    def Cancel(self):
        self._status = self.STATUS_NOTSTARTED
        self._mainWindow.GetEventHandler().ResetAction()
        self._mainWindow.Refresh()

    def Draw(self, dc):
        pass

    def SetObjectReceiver(self, canvasobject):
        self._receiver = canvasobject





# Handler for line creation
class BE_HandlerLine(BE_HandlerCanvas):

    """ Action to create a line

        Attributes:
            startPos: Line first vertex (Point2D)
            endPos: Line last vertex (Point2D)
    """

    def __init__(self, mainwindow):

        BE_HandlerCanvas.__init__(self, mainwindow)
        self.__startPos = None
        self.__endPos = None

    def Move(self, x, y, dc):
        BE_HandlerCanvas.Move(self, x, y, dc)
        if (self._status == self.STATUS_NOTSTARTED):
            self._mainWindow.SetStatusText(self._mainWindow.GetStatusBar().GetStatusText() + '       Left button click to start line drawing, or right click to cancel')
        if (self._status == self.STATUS_STARTED):
            self._mainWindow.SetStatusText(self._mainWindow.GetStatusBar().GetStatusText() + '       Left button click to end line drawing, or right click to cancel')

        self.Draw(dc)
        self._mainWindow.SetCanvasCursor(wx.StockCursor(wx.CURSOR_CROSS))



    def Click(self, x, y):

        p = self.GetCanvas().ScreenToUserCoord(x,y)

        if (self._status == self.STATUS_NOTSTARTED):
            self.__startPos = p.Copy()
            self._status = self.STATUS_STARTED
        else:
            if (self._status == self.STATUS_STARTED):
                self.__endPos = p.Copy()
                self.Finish()




    def Draw(self, dc):


        lastpen = dc.GetPen()
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0, wx.ALPHA_OPAQUE), 2))

        dc.SetLogicalFunction(wx.INVERT)

        # TODO: Improve

        if (self._status == self.STATUS_STARTED):
            dc.DrawLine(self.__startPos.x, self.__startPos.y, self._prevMousePos.x, self._prevMousePos.y)
        if (self._status == self.STATUS_FINISHED):
            dc.DrawLine(self.__startPos.x, self.__startPos.y, self.__endPos.x, self.__endPos.y)


        if (self._status == self.STATUS_STARTED):
            dc.DrawLine(self.__startPos.x, self.__startPos.y, self._curMousePos.x, self._curMousePos.y)
        if (self._status == self.STATUS_FINISHED):
            dc.DrawLine(self.__startPos.x, self.__startPos.y, self.__endPos.x, self.__endPos.y)


        dc.SetPen(lastpen)








class BE_HandlerPolyline(BE_HandlerCanvas):

    """ Action class for creating a polyline

        Attributes:
            points: array of polyline vertices (Point2D)
            thickness: polyline thickness/width
    """

    def __init__(self, mainwindow, thickness):

        BE_HandlerCanvas.__init__(self, mainwindow)
        self.__points = []
        self.__thickness = thickness


    def Move(self, x, y, dc):
        BE_HandlerCanvas.Move(self, x, y, dc)
        if (self._status == self.STATUS_NOTSTARTED):
            self._mainWindow.SetStatusText(self._mainWindow.GetStatusBar().GetStatusText() + '       Left button click to start line drawing, or right click to cancel')
        if (self._status == self.STATUS_STARTED):
            self._mainWindow.SetStatusText(self._mainWindow.GetStatusBar().GetStatusText() + '       Left button click to next point, double click to finish, or right click to cancel')

        self.Draw(dc)
        self._mainWindow.SetCanvasCursor(wx.StockCursor(wx.CURSOR_CROSS))



    def Click(self, x, y):

        p = self.GetCanvas().ScreenToUserCoord(x,y)

        if (self._status == self.STATUS_STARTED):
            self.__points.append(p.Copy())

        if (self._status == self.STATUS_NOTSTARTED):
            self.__points.append(p.Copy())
            self._status = self.STATUS_STARTED


    def DoubleClick(self, x, y):

        """
        if (self._status == self.STATUS_STARTED):
            self.__points.append(Geometry.Point2D(x, y))
        """
        # It is not require to add the new point, since Click function has been already added before DoubleClick

        self.Finish()


    def Draw(self, dc):

        if (self._status == self.STATUS_FINISHED):
            return

        canvas = self.GetCanvas()

        lastpen = dc.GetPen()
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0, wx.ALPHA_OPAQUE), 2))

        if ((self._status == self.STATUS_STARTED) or (self._status == self.STATUS_FINISHED)):
            i = 1
            while (i < len(self.__points)):
                p1 = canvas.UserToScreenCoord(self.__points[i-1].x, self.__points[i-1].y)
                p2 = canvas.UserToScreenCoord(self.__points[i].x, self.__points[i].y)
                dc.DrawLine(p1.x, p1.y, p2.x, p2.y)
                i += 1


        dc.SetLogicalFunction(wx.INVERT)

        if (self._status == self.STATUS_STARTED):
            p1 = canvas.UserToScreenCoord(self.__points[i-1].x, self.__points[i-1].y)
            prev = canvas.UserToScreenCoord(self._prevMousePos.x, self._prevMousePos.y)
            curr = canvas.UserToScreenCoord(self._curMousePos.x, self._curMousePos.y)
            dc.DrawLine(p1.x, p1.y, prev.x, prev.y)
            dc.DrawLine(p1.x, p1.y, curr.x, curr.y)



        dc.SetPen(lastpen)





    def Finish(self):

        self._receiver.SetShape(self.__points, self.__thickness)

        BE_HandlerCanvas.Finish(self)










class BE_HandlerCastle(BE_HandlerCanvas):

    """ Action class to create the castle. The user must define a polyline, and for each new vertex, the tower data is required using a dialog
        Double click event closes the castle
    """

    def __init__(self, mainwindow):

        BE_HandlerCanvas.__init__(self, mainwindow)
        self.__lastPoint = Geometry.Point2D()

    def Move(self, x, y, dc):
        BE_HandlerCanvas.Move(self, x, y, dc)
        if (self._status == self.STATUS_NOTSTARTED):
            self._mainWindow.SetStatusText(self._mainWindow.GetStatusBar().GetStatusText() + '       Left button click to start line drawing, or right click to cancel')
        if (self._status == self.STATUS_STARTED):
            self._mainWindow.SetStatusText(self._mainWindow.GetStatusBar().GetStatusText() + '       Left button click to next point, or right click to cancel')

        self.Draw(dc)
        self._mainWindow.SetCanvasCursor(wx.StockCursor(wx.CURSOR_CROSS))



    def Click(self, x, y):

        if ((self._status == self.STATUS_STARTED) or (self._status == self.STATUS_NOTSTARTED)):

            point = self.GetCanvas().ScreenToUserCoord(x, y)

            # Ask about the tower data
            dlg = BE_Dialogs.BE_TowersDialog.BE_TowersDlg(self._mainWindow)

            # Disable the castle close option if the castle is too small
            if (self._receiver.GetNVertices() < 2):
                dlg.checkClose.Enable(False)
            else:
                dlg.checkClose.Enable(True)


            ret = dlg.ShowModal()
            if ret == wx.ID_OK:

                # Create the tower object

                if (dlg.radioSquared.GetValue()):
                    towertype = BE_Objects.BE_Tower.TOWERTYPE_SQUARED
                    center = point.Copy()
                    tower = BE_Objects.BE_Tower(towertype = towertype, center = center)
                    point.data = tower

                if (dlg.radioRounded.GetValue()):
                    towertype = BE_Objects.BE_Tower.TOWERTYPE_ROUNDED
                    center = point.Copy()
                    tower = BE_Objects.BE_Tower(towertype = towertype, center = center)
                    point.data = tower

                if (dlg.radioRandom.GetValue()):
                    towertype = BE_Objects.BE_Tower.TOWERTYPE_RANDOM
                    center = point.Copy()
                    tower = BE_Objects.BE_Tower(towertype = towertype, center = center)
                    point.data = tower


                self._receiver.AddVertex(point)
            else:
                self._receiver.AddVertex(point)



            # Check if action must finish
            if (dlg.checkClose.GetValue()):

                dlg.Destroy()

                dlgmoat = BE_Dialogs.BE_MoatDlg.BE_MoatDlg(self._mainWindow)

                # Populate dialog with default moat data
                moatdata = self._mainWindow.GetDocument().GetDefaultSettings().castle.moat
                dlgmoat.checkActive.SetValue(False)
                dlgmoat.checkHasWater.SetValue(moatdata.hasWater)

                retmoat = dlgmoat.ShowModal()
                if (retmoat == wx.ID_OK):

                    self._receiver.SetMoat(dlgmoat.checkActive.GetValue(), haswater = dlgmoat.checkHasWater.GetValue())

                else:
                    # Castle without moat
                    self._receiver.SetMoat(False)

                dlgmoat.Destroy()

                self._receiver.Close()
                self.Finish()
                return



            dlg.Destroy()



            self.__lastPoint = point.Copy()

            if (self._status == self.STATUS_NOTSTARTED):
                 self._status = self.STATUS_STARTED


    def DoubleClick(self, x, y):
        pass

    def Draw(self, dc):

        if (self._status == self.STATUS_FINISHED):
            return

        self._receiver.Draw(dc, self._mainWindow.GetDocument(), self._mainWindow.GetCanvas())

        canvas = self.GetCanvas()
        lastpen = dc.GetPen()
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0, wx.ALPHA_OPAQUE), 2))

        dc.SetLogicalFunction(wx.INVERT)

        if (self._status == self.STATUS_STARTED):
            last = canvas.UserToScreenCoord(self.__lastPoint.x, self.__lastPoint.y)
            prev = canvas.UserToScreenCoord(self._prevMousePos.x, self._prevMousePos.y)
            curr = canvas.UserToScreenCoord(self._curMousePos.x, self._curMousePos.y)
            dc.DrawLine(last.x, last.y, prev.x, prev.y)
            dc.DrawLine(last.x, last.y, curr.x, curr.y)



        dc.SetPen(lastpen)





    def Finish(self):

        BE_HandlerCanvas.Finish(self)













class BE_HandlerHouse(BE_HandlerCanvas):

    """ Action class to create houses for the castle oldcity. The user must define a set of points, one for each house
        Right click event closes the castle
    """

    def __init__(self, mainwindow):

        BE_HandlerCanvas.__init__(self, mainwindow)

    def Move(self, x, y, dc):
        BE_HandlerCanvas.Move(self, x, y, dc)
        self._mainWindow.SetStatusText(self._mainWindow.GetStatusBar().GetStatusText() + '       Left button click to set a house, or right click to cancel')
        self._mainWindow.SetCanvasCursor(wx.StockCursor(wx.CURSOR_CROSS))


    def Click(self, x, y):

        if ((self._status == self.STATUS_STARTED) or (self._status == self.STATUS_NOTSTARTED)):

            house = BE_Objects.BE_House(self.GetCanvas().ScreenToUserCoord(x, y))
            self._mainWindow.GetDocument().AddCanvasObject(house)

            self._mainWindow.Refresh()
            self._mainWindow.SetCanvasCursor(wx.StockCursor(wx.CURSOR_CROSS))








class BE_HandlerCityEvolution(BE_HandlerCanvas):

    """ Action class to create the segment + arrow to define a city evolution. At the end of process, a dialog asks about other city evolution data
        Right click cancels the action
    """

    # Particular states
    STATUS_EXT_NONE = 0
    STATUS_EXT_BASESEGMENT = 1       # Creating the base segment (remains the last point)
    STATUS_EXT_ARROW = 2             # Creating the arrow (remains the last point)


    def __init__(self, mainwindow):

        BE_HandlerCanvas.__init__(self, mainwindow)

        self.__extraStatus = self.STATUS_EXT_NONE

        self.__baseSegment = Geometry.Segment2D()
        self.__arrowEndPoint = Geometry.Point2D()

        self.__XORflag = False      # internal flag to control the draw xor issues for the first arrow drawing time



    def Move(self, x, y, dc):
        BE_HandlerCanvas.Move(self, x, y, dc)

        statustxt = ''
        if (self._status == self.STATUS_NOTSTARTED):
            statustxt = '      Left button click to start the base segment, or right to cancel'
        elif ((self._status == self.STATUS_STARTED) and (self.__extraStatus == self.STATUS_EXT_BASESEGMENT)):
            statustxt = '      Left button click to finish the base segment, or right to cancel'
        elif ((self._status == self.STATUS_STARTED) and (self.__extraStatus == self.STATUS_EXT_ARROW)):
            statustxt = '      Left button click to finish the city evolution direction, or right to cancel'
        self._mainWindow.SetStatusText(self._mainWindow.GetStatusBar().GetStatusText() + statustxt)

        self.Draw(dc)
        self._mainWindow.SetCanvasCursor(wx.StockCursor(wx.CURSOR_CROSS))



    def Click(self, x, y):

        if (self._status == self.STATUS_NOTSTARTED):

            self.__baseSegment.p1 = self.GetCanvas().ScreenToUserCoord(x, y)

            self._status = self.STATUS_STARTED
            self.__extraStatus = self.STATUS_EXT_BASESEGMENT
            self._mainWindow.Refresh()
            self._mainWindow.SetCanvasCursor(wx.StockCursor(wx.CURSOR_CROSS))


        elif ((self._status == self.STATUS_STARTED) and (self.__extraStatus == self.STATUS_EXT_BASESEGMENT)):

            self.__baseSegment.p2 = self.GetCanvas().ScreenToUserCoord(x, y)

            self.__extraStatus = self.STATUS_EXT_ARROW
            self._mainWindow.Refresh()
            self._mainWindow.SetCanvasCursor(wx.StockCursor(wx.CURSOR_CROSS))


        elif ((self._status == self.STATUS_STARTED) and (self.__extraStatus == self.STATUS_EXT_ARROW)):

            self.__arrowEndPoint = self.GetCanvas().ScreenToUserCoord(x, y)

            dlg = BE_Dialogs.BE_CityEvolutionDlg.BE_CityEvolutionDlg(self._mainWindow)

            defdata = self._mainWindow.GetDocument().GetDefaultSettings()
            gamedata = self._mainWindow.GetDocument().GetGameData()
            dlg.textHousesYear.SetValue(str(defdata.city.housesCreationPerYear))
            dlg.textTimeRangeStart.SetValue(str((gamedata.timeRange[0] - 1) * 100))
            dlg.textTimeRangeEnd.SetValue(str((gamedata.timeRange[1] - 1) * 100))
            dlg.textGroupID.SetValue("0")


            if (dlg.ShowModal() == wx.ID_OK):

                self._receiver = BE_Objects.BE_CityEvolution()
                self._receiver.baseSegment = self.__baseSegment.Copy()
                self._receiver.arrow = Geometry.Segment2D(self.__baseSegment.GetMidPoint(), self.__arrowEndPoint)

                try:
                    self._receiver.timeRange[0] = int(dlg.textTimeRangeStart.GetValue())
                    self._receiver.timeRange[1] = int(dlg.textTimeRangeEnd.GetValue())
                except:
                    pass

                try:
                    self._receiver.housesPerYear = float(dlg.textHousesYear.GetValue())
                except:
                    pass

                try:
                    self._receiver.groupID = int(dlg.textGroupID.GetValue())
                except:
                    pass

                self.Finish()

            else:
                self.Cancel()

            dlg.Destroy()

            self.__extraStatus = self.STATUS_EXT_NONE



    def Draw(self, dc):

        if (self._status == self.STATUS_FINISHED):
            return
        if (self._status == self.STATUS_NOTSTARTED):
            return

        canvas = self.GetCanvas()
        lastpen = dc.GetPen()

        if ((self._status == self.STATUS_STARTED) and (self.__extraStatus == self.STATUS_EXT_BASESEGMENT)):

            dc.SetPen(wx.Pen(wx.Colour(0, 0, 0, wx.ALPHA_OPAQUE), 2))
            dc.SetLogicalFunction(wx.INVERT)

            base1 = canvas.UserToScreenCoord(self.__baseSegment.p1.x, self.__baseSegment.p1.y)
            prev = canvas.UserToScreenCoord(self._prevMousePos.x, self._prevMousePos.y)
            curr = canvas.UserToScreenCoord(self._curMousePos.x, self._curMousePos.y)
            dc.DrawLine(base1.x, base1.y, prev.x, prev.y)
            dc.DrawLine(base1.x, base1.y, curr.x, curr.y)

        elif ((self._status == self.STATUS_STARTED) and (self.__extraStatus == self.STATUS_EXT_ARROW)):

            if (self._prevMousePos and self._curMousePos):
                dc.SetPen(wx.Pen(wx.Colour(0, 0, 0, wx.ALPHA_OPAQUE), 2))

                base1 = canvas.UserToScreenCoord(self.__baseSegment.p1.x, self.__baseSegment.p1.y)
                base2 = canvas.UserToScreenCoord(self.__baseSegment.p2.x, self.__baseSegment.p2.y)
                dc.DrawLine(base1.x, base1.y, base2.x, base2.y)

                mid = self.__baseSegment.GetMidPoint()

                dc.SetPen(wx.Pen(wx.Colour(0, 0, 0, wx.ALPHA_OPAQUE), 2))
                dc.SetLogicalFunction(wx.INVERT)

                pmid = canvas.UserToScreenCoord(mid.x, mid.y)
                prev = canvas.UserToScreenCoord(self._prevMousePos.x, self._prevMousePos.y)
                dc.DrawLine(pmid.x, pmid.y, prev.x, prev.y)

                # Draw the arrow

                if (self.__XORflag):
                    seg = Geometry.Segment2D(mid, self._prevMousePos)
                    arrow = seg.GetArrow(atEnd = True, size = 30, arrowangle = 20)
                    plist = []
                    for p in arrow:
                        parrow = canvas.UserToScreenCoord(p.x, p.y)
                        plist.append([parrow.x, parrow.y])
                    dc.DrawPolygon(plist)

                self.__XORflag = True

                curr = canvas.UserToScreenCoord(self._curMousePos.x, self._curMousePos.y)
                dc.DrawLine(pmid.x, pmid.y, curr.x, curr.y)

                seg = Geometry.Segment2D(mid, self._curMousePos)
                arrow = seg.GetArrow(atEnd = True, size = 30, arrowangle = 20)
                plist = []
                for p in arrow:
                    parrow = canvas.UserToScreenCoord(p.x, p.y)
                    plist.append([parrow.x, parrow.y])
                dc.DrawPolygon(plist)


        dc.SetPen(lastpen)







class BE_HandlerFlank(BE_HandlerCanvas):

    """ Flank creation on canvas class manager. The flank is defined as an arrow (just 2 mouse clicks). Right mouse cancels
        Then a dialog appears to ask about the flank data and linked attacker battalions
    """


    def __init__(self, mainwindow):

        BE_HandlerCanvas.__init__(self, mainwindow)

        self.__startPos = None
        self.__endPos = None

        self.__XORflag = False      # internal flag to control the draw xor issues for the first arrow drawing time



    def Move(self, x, y, dc):
        BE_HandlerCanvas.Move(self, x, y, dc)

        statustxt = ''
        if (self._status == self.STATUS_NOTSTARTED):
            statustxt = '      Left button click to set the flank origin, or right to cancel'
        elif (self._status == self.STATUS_STARTED):
            statustxt = '      Left button click to set the flank direction, or right to cancel'
        self._mainWindow.SetStatusText(self._mainWindow.GetStatusBar().GetStatusText() + statustxt)

        self.Draw(dc)
        self._mainWindow.SetCanvasCursor(wx.StockCursor(wx.CURSOR_CROSS))




    def Click(self, x, y):

        if (self._status == self.STATUS_NOTSTARTED):

            self.__startPos = self.GetCanvas().ScreenToUserCoord(x, y)

            self._status = self.STATUS_STARTED

            self._mainWindow.Refresh()
            self._mainWindow.SetCanvasCursor(wx.StockCursor(wx.CURSOR_CROSS))

        elif (self._status == self.STATUS_STARTED):

            self.__endPos = self.GetCanvas().ScreenToUserCoord(x, y)

            dlg = BE_Dialogs.BE_FlankDlg.BE_FlankDlg(self._mainWindow)

            # Populate the years dialog combolist
            battleslist = self._mainWindow.GetDocument().GetGameData().battles.GetBattlesYears()
            for year in battleslist:
                dlg.comboYear.Append(str(year))
            if (len(battleslist) > 0):
                dlg.comboYear.SetSelection(0)

            if (dlg.ShowModal() == wx.ID_OK):

                self._receiver = BE_Objects.BE_Flank()
                self._receiver.origin = self.__startPos.Copy()
                self._receiver.target = self.__endPos.Copy()

                try:
                    self._receiver.year = int(dlg.comboYear.GetStringSelection())
                except:
                    self.Cancel()
                    return

                try:
                    self._receiver.standDistance = float(dlg.textStandDistance.GetValue())
                except:
                    pass



                try:
                    self._receiver.battalions['Infantry']['Number'] = int(dlg.textInfantryNumber.GetValue())
                except:
                    pass
                try:
                    self._receiver.battalions['Infantry']['BattalionSize'] = int(dlg.textInfantryBattalionSize.GetValue())
                except:
                    pass
                try:
                    self._receiver.battalions['Infantry']['GroupSize'] = int(dlg.textInfantryGroupSize.GetValue())
                except:
                    pass
                try:
                    self._receiver.battalions['Infantry']['GroupDistance'] = int(dlg.textInfantryGroupSize.GetValue())
                except:
                    pass



                try:
                    self._receiver.battalions['Archers']['Number'] = int(dlg.textArchersNumber.GetValue())
                except:
                    pass
                try:
                    self._receiver.battalions['Archers']['BattalionSize'] = int(dlg.textArchersBattalionSize.GetValue())
                except:
                    pass
                try:
                    self._receiver.battalions['Archers']['GroupSize'] = int(dlg.textArchersGroupSize.GetValue())
                except:
                    pass
                try:
                    self._receiver.battalions['Archers']['GroupDistance'] = int(dlg.textArchersGroupSize.GetValue())
                except:
                    pass




                try:
                    self._receiver.battalions['Cannons']['Number'] = int(dlg.textCannonsNumber.GetValue())
                except:
                    pass
                try:
                    self._receiver.battalions['Cannons']['BattalionSize'] = int(dlg.textCannonsBattalionSize.GetValue())
                except:
                    pass
                try:
                    self._receiver.battalions['Cannons']['GroupSize'] = int(dlg.textCannonsGroupSize.GetValue())
                except:
                    pass
                try:
                    self._receiver.battalions['Cannons']['GroupDistance'] = int(dlg.textCannonsGroupSize.GetValue())
                except:
                    pass


                try:
                    self._receiver.battalions['SiegeTowers']['Number'] = int(dlg.textSiegeTowersNumber.GetValue())
                except:
                    pass
                try:
                    self._receiver.battalions['SiegeTowers']['BattalionSize'] = int(dlg.textSiegeTowersBattalionSize.GetValue())
                except:
                    pass
                try:
                    self._receiver.battalions['SiegeTowers']['GroupSize'] = int(dlg.textSiegeTowersGroupSize.GetValue())
                except:
                    pass
                try:
                    self._receiver.battalions['SiegeTowers']['GroupDistance'] = int(dlg.textSiegeTowersGroupSize.GetValue())
                except:
                    pass


                self.Finish()

            else:
                self.Cancel()


            dlg.Destroy()



            self._mainWindow.Refresh()
            self._mainWindow.SetCanvasCursor(wx.StockCursor(wx.CURSOR_CROSS))






    def Draw(self, dc):

        if (self._status == self.STATUS_FINISHED):
            return
        if (self._status == self.STATUS_NOTSTARTED):
            return

        canvas = self.GetCanvas()
        lastpen = dc.GetPen()

        if (self._status == self.STATUS_STARTED):

            if (self._prevMousePos and self._curMousePos):

                dc.SetPen(wx.Pen(wx.Colour(0, 0, 0, wx.ALPHA_OPAQUE), 2))

                dc.SetLogicalFunction(wx.INVERT)

                start = canvas.UserToScreenCoord(self.__startPos.x, self.__startPos.y)
                prev = canvas.UserToScreenCoord(self._prevMousePos.x, self._prevMousePos.y)
                curr = canvas.UserToScreenCoord(self._curMousePos.x, self._curMousePos.y)

                dc.DrawLine(start.x, start.y, prev.x, prev.y)


                if (self.__XORflag):
                    seg = Geometry.Segment2D(self.__startPos, self._prevMousePos)
                    arrow = seg.GetArrow(atEnd = True, size = 30, arrowangle = 20)
                    plist = []
                    for p in arrow:
                        parrow = canvas.UserToScreenCoord(p.x, p.y)
                        plist.append([parrow.x, parrow.y])
                    dc.DrawPolygon(plist)

                self.__XORflag = True

                dc.DrawLine(start.x, start.y, curr.x, curr.y)

                seg = Geometry.Segment2D(self.__startPos, self._curMousePos)
                arrow = seg.GetArrow(atEnd = True, size = 30, arrowangle = 20)
                plist = []
                for p in arrow:
                    parrow = canvas.UserToScreenCoord(p.x, p.y)
                    plist.append([parrow.x, parrow.y])
                dc.DrawPolygon(plist)


        dc.SetPen(lastpen)
