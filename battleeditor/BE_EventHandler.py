import wx
import BE_HandlerCanvas
import BE_Objects



class BE_EventHandler:

    """ Event handler class. Controls the toolbar/menu handlers, executing the related actions, and the canvas handlers, controlling the mouse events
        This class is the interface to be used externally to bind the events and controls

        NOTE: Since wxPython seems to have many problems binding the keyboard, and the Esc key is problematic, the right button click is choosen as the cancel event

        Attributes:
            action: Current action object, if any (if there arent any one, use the default one)
            mainWindow: Reference to the main window to get access to the canvas and document classes
    """



    def __init__(self, mainwindow):

        self.__action = BE_HandlerCanvas.BE_HandlerCanvas(mainwindow)
        self.__mainWindow = mainwindow


    def ResetAction(self):
        self.__action = BE_HandlerCanvas.BE_HandlerCanvas(self.__mainWindow)



    def OnCancel(self, event):
        # Cancel any action
        if (self.__action):
            self.__action.Cancel()
            self.ResetAction()


    def OnMouseMove(self, event):
        # Mouse move event on actions
        if (self.__action):
            self.__action.Move(event.GetX(), event.GetY(), self.__mainWindow.GetCanvasDC())


    def OnMouseClick(self, event):
       # Mouse left click event on actions
       if (self.__action):
            self.__action.Click(event.GetX(), event.GetY() )


    def OnMouseDoubleClick(self, event):
        # Mouse left double click event on actions
        if (self.__action):
            self.__action.DoubleClick(event.GetX(), event.GetY())




    def DrawAction(self, dc):
        # Draw current action objects. Receives the DC where to draw
        if (self.__action):
            self.__action.Draw(dc)



    def OnAddRiver(self, event):
        # Starts adding a river action

        self.__mainWindow.GetDocument().ResetSelect()

        # Ask for the river width
        dlg = wx.TextEntryDialog(None,'Enter the river width','Add River', '50')
        ret = dlg.ShowModal()
        if ret != wx.ID_OK:
            return
        dlg.Destroy()

        # Create the polyline
        self.__action = BE_HandlerCanvas.BE_HandlerPolyline(self.__mainWindow, int(dlg.GetValue()))
        self.__action.SetObjectReceiver(BE_Objects.BE_River())





    def OnAddCastle(self, event):
        # Starts creating the castle shape (walls and towers)

        # Check if there are a previous castle
        castles = self.__mainWindow.GetDocument().GetCanvasObjectsByType(BE_Objects.BE_Object.CANVASOBJECT_CASTLE)
        if (castles):
            dlg = wx.MessageDialog(self.__mainWindow, 'There is already a caste', 'Error', wx.ID_OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        self.__action = BE_HandlerCanvas.BE_HandlerCastle(self.__mainWindow)

        castle = BE_Objects.BE_Castle()
        self.__action.SetObjectReceiver(castle)

        self.__mainWindow.GetDocument().ResetSelect()




    def OnAddOldcity(self, event):
        # Adds new houses to the oldcity

        self.__action = BE_HandlerCanvas.BE_HandlerHouse(self.__mainWindow)
        self.__action.SetObjectReceiver(None)

        self.__mainWindow.GetDocument().ResetSelect()


    def OnAddCityEvolution(self, event):
        # Adds a new city evolution (segment + arrow

        self.__action = BE_HandlerCanvas.BE_HandlerCityEvolution(self.__mainWindow)
        self.__action.SetObjectReceiver(None)

        self.__mainWindow.GetDocument().ResetSelect()


    def OnAddFlank(self, event):
        # Check if there are any battle where to link the flank
        lst = self.__mainWindow.GetDocument().GetGameData().battles.GetBattlesYears()
        if (len(lst) == 0):
            dlg = wx.MessageDialog(self.__mainWindow, 'You must create any battle before creating flanks', 'Error', wx.ID_OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return


        # Adds a new flank (using an arrow). Then, a dialog asks about the flank battalions

        self.__action = BE_HandlerCanvas.BE_HandlerFlank(self.__mainWindow)
        self.__action.SetObjectReceiver(None)

        self.__mainWindow.GetDocument().ResetSelect()





    def OnEditSelected(self, event):
        # Edits current selected object

        if (not self.__mainWindow.GetDocument().IsSelected()):
            dlg = wx.MessageDialog(self.__mainWindow, 'You must select any oject to edit it', 'Error', wx.ID_OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        self.__mainWindow.GetDocument().EditSelected(self.__mainWindow)
        self.__mainWindow.Refresh()


    def OnDeleteSelected(self, event):
        # Deletes the selected object (if any)

        if (not self.__mainWindow.GetDocument().IsSelected()):
            dlg = wx.MessageDialog(self.__mainWindow, 'You must select any oject to delete it', 'Error', wx.ID_OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        self.__mainWindow.GetDocument().DeleteSelected()
        self.__mainWindow.Refresh()


    def OnSetBackgroundHelper(self, event):

        canvas = self.__mainWindow.GetCanvas()
        canvas.SetBackgroundHelper(self.__mainWindow)
        self.__mainWindow.Refresh()


    def OnDefaultSettingsCastle(self, event):

        defset = self.__mainWindow.GetDocument().GetDefaultSettings()
        defset.castle.OpenDialog(self.__mainWindow)
        self.__mainWindow.Refresh()

    def OnDefaultSettingsBattlefield(self, event):

        defset = self.__mainWindow.GetDocument().GetDefaultSettings()
        defset.battlefield.OpenDialog(self.__mainWindow)
        self.__mainWindow.Refresh()

    def OnDefaultSettingsArmy(self, event):

        defset = self.__mainWindow.GetDocument().GetDefaultSettings()
        defset.army.OpenDialog(self.__mainWindow)
        self.__mainWindow.Refresh()

    def OnDefaultSettingsCity(self, event):

        defset = self.__mainWindow.GetDocument().GetDefaultSettings()
        defset.city.OpenDialog(self.__mainWindow)
        self.__mainWindow.Refresh()

    def OnDefaultSettingsGame(self, event):

        defset = self.__mainWindow.GetDocument().GetDefaultSettings()
        defset.game.OpenDialog(self.__mainWindow)
        self.__mainWindow.Refresh()





    def OnSaveDefaultSettings(self, event):

        saveFileDialog = wx.FileDialog(self.__mainWindow, "Export default settings", "", "", "XML files (*.xml)|*.xml", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if (saveFileDialog.ShowModal() == wx.ID_OK):
            defset = self.__mainWindow.GetDocument()
            defset.SaveDefaultSettings(saveFileDialog.GetPath())

        saveFileDialog.Destroy()

    def OnLoadDefaultSettings(self, event):

        loadFileDialog = wx.FileDialog(self.__mainWindow, "Load default settings", "", "", "XML files (*.xml)|*.xml", wx.FD_OPEN)
        if (loadFileDialog.ShowModal() == wx.ID_OK):
            defset = self.__mainWindow.GetDocument()
            defset.LoadDefaultSettings(loadFileDialog.GetPath(), self.__mainWindow)
            self.__mainWindow.Refresh()

        loadFileDialog.Destroy()



    def OnGameDataType(self, event):

        data = self.__mainWindow.GetDocument().GetGameData()
        data.OpenTypeDialog(self.__mainWindow)
        self.__mainWindow.Refresh()

    def OnGameDataTimeRange(self, event):

        data = self.__mainWindow.GetDocument().GetGameData()
        data.OpenTimeRangeDialog(self.__mainWindow)
        self.__mainWindow.Refresh()

    def OnGameDataBattlefield(self, event):

        data = self.__mainWindow.GetDocument().GetGameData()
        data.battlefield.OpenDialog(self.__mainWindow)
        self.__mainWindow.Refresh()

    def OnGameDataCityExpansions(self, event):

        data = self.__mainWindow.GetDocument().GetGameData()
        data.cityEvolutions.OpenDialog(self.__mainWindow)
        self.__mainWindow.Refresh()

    def OnGameDataBattles(self, event):

        data = self.__mainWindow.GetDocument().GetGameData()
        data.battles.OpenDialog(self.__mainWindow)
        self.__mainWindow.Refresh()

    def OnGameDataStarFortress(self, event):

        data = self.__mainWindow.GetDocument().GetGameData()
        data.starfortress.OpenDialog(self.__mainWindow)
        self.__mainWindow.Refresh()

    def OnGameDataExpansionCheckings(self, event):

        data = self.__mainWindow.GetDocument().GetGameData()
        data.expansioncheckings.OpenDialog(self.__mainWindow)
        self.__mainWindow.Refresh()




    def OnSaveGameData(self, event):

        saveFileDialog = wx.FileDialog(self.__mainWindow, "Export game data", "", "", "XML files (*.xml)|*.xml", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if (saveFileDialog.ShowModal() == wx.ID_OK):
            data = self.__mainWindow.GetDocument()
            data.SaveGameData(saveFileDialog.GetPath())

        saveFileDialog.Destroy()


    def OnLoadGameData(self, event):

        loadFileDialog = wx.FileDialog(self.__mainWindow, "Load game data", "", "", "XML files (*.xml)|*.xml", wx.FD_OPEN)
        if (loadFileDialog.ShowModal() == wx.ID_OK):
            data = self.__mainWindow.GetDocument()
            data.LoadGameData(loadFileDialog.GetPath())
            self.__mainWindow.Refresh()

        loadFileDialog.Destroy()



    def On3DSettings(self, event):

        data = self.__mainWindow.GetDocument().Get3DSettings()
        data.OpenDialog(self.__mainWindow)


    def OnSave3DSettings(self, event):

        saveFileDialog = wx.FileDialog(self.__mainWindow, "Export 3D settings", "", "", "XML files (*.xml)|*.xml", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if (saveFileDialog.ShowModal() == wx.ID_OK):
            data = self.__mainWindow.GetDocument()
            data.Save3DSettings(saveFileDialog.GetPath())

        saveFileDialog.Destroy()


    def OnLoad3DSettings(self, event):
        loadFileDialog = wx.FileDialog(self.__mainWindow, "Load 3D settings", "", "", "XML files (*.xml)|*.xml", wx.FD_OPEN)
        if (loadFileDialog.ShowModal() == wx.ID_OK):
            data = self.__mainWindow.GetDocument()
            data.Load3DSettings(loadFileDialog.GetPath())
            self.__mainWindow.Refresh()

        loadFileDialog.Destroy()



    def OnPlay(self, event):

        self.__mainWindow.GetDocument().Play()


