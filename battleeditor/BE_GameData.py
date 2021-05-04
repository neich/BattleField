import wx
import wx.grid
import BE_Objects
import BE_Dialogs
import BE_Dialogs.BE_GameTypeDlg
import BE_Dialogs.BE_GameTimeRangeDlg
import BE_Dialogs.BE_GameBattlefieldDlg
import BE_Dialogs.BE_GameCityExpansionsDlg
import BE_Dialogs.BE_GameStarFortressDlg
import BE_Dialogs.BE_GameDataExpansionCheckingsDlg
import BE_GameDataBattles
import Battles.Utils.Geometry as Geometry
import xml.etree.cElementTree as ET
import xml.dom.minidom
import ast


class BE_GameData:
    """ Manage the current game data
        See Usage documentation to more information

        Attributes:
            gameType: Type of game ("CityExpansion", "Battles")
                      NOTE: Since "Battles" mode is for debug purposes, this option is not yet available
            timeRange: Simulation time range


    """

    GAMETYPE_CITYEXPANSION = "CityExpansion"
    GAMETYPE_BATTLES = "Battles"

    def __init__(self):

        self.gameType = self.GAMETYPE_CITYEXPANSION
        self.timeRange = [9, 17]

        self.battlefield = BE_GameDataBattlefield()
        self.castle = BE_GameDataCastle()
        self.cityEvolutions = BE_GameDataCityEvolutions()   # NOTE: Usage documentation separates the city evolutions from city expansions. Here are managed in the same
                                                            # place to help to manage the group IDs

        self.battles = BE_GameDataBattles.BE_GameDataBattles()
        self.starfortress = BE_GameDataStarFortress()
        self.expansioncheckings = BE_GameDataExpansionCheckings()



    def ExportXML(self, filename, document):

        root = ET.Element("Game")

        ET.SubElement(root, "Type").text = self.gameType
        ET.SubElement(root, "TimeRange").text = "[" + str(self.timeRange[0]) + "," + str(self.timeRange[1]) +"]"

        self.battlefield.ExportXML(root, document)
        self.castle.ExportXML(root, document)
        self.cityEvolutions.ExportXML(root, document)
        self.battles.ExportXML(root, document)
        self.starfortress.ExportXML(root, document)
        self.expansioncheckings.ExportXML(root, document)

        xmlstring = ET.tostring(root, 'utf-8', method='xml')
        parsed = xml.dom.minidom.parseString(xmlstring)
        pretty = parsed.toprettyxml(indent = "    ")

        filexml = open(filename, 'w')
        filexml.write(pretty)
        filexml.close()



    def ImportXML(self, filename, document):

        tree = xml.etree.cElementTree.parse(filename)
        main = tree.getroot()
        if (not main):
            print "ERROR: Wrong game settings file"
            return

        try:
            self.gameType = main.find("Type").text
        except:
            print "WARNING: Type tag not found in " + filename

        try:
            tr = main.find("TimeRange").text
            self.timeRange = ast.literal_eval(tr)
        except:
            print "WARNING: TimeRange tag not found in " + filename


        self.battlefield.ImportXML(main, document)
        self.castle.ImportXML(main, document)
        self.cityEvolutions.ImportXML(main, document)
        self.battles.ImportXML(main, document)
        self.starfortress.ImportXML(main, document)
        self.expansioncheckings.ImportXML(main, document)





    def OpenTypeDialog(self, parent):

        dlg = BE_Dialogs.BE_GameTypeDlg.BE_GameTypeDlg(parent)

        if (self.gameType == self.GAMETYPE_CITYEXPANSION):
            dlg.optCityEvolution.SetValue(True)
            dlg.optBattles.SetValue(False)
        if (self.gameType == self.GAMETYPE_BATTLES):
            dlg.optCityEvolution.SetValue(False)
            dlg.optBattles.SetValue(True)

        # Battles game type is not yet available -> TODO
        dlg.optBattles.Enable(False)


        if (dlg.ShowModal() == wx.ID_OK):

            if (dlg.optCityEvolution.GetValue()):
                self.gameType = self.GAMETYPE_CITYEXPANSION
            elif (dlg.optBattles.GetValue()):
                self.gameType = self.GAMETYPE_BATTLES


        dlg.Destroy()




    def OpenTimeRangeDialog(self, parent):

        dlg = BE_Dialogs.BE_GameTimeRangeDlg.BE_GameTimeRangeDlg(parent)

        dlg.textTime1.SetValue(str(self.timeRange[0]))
        dlg.textTime2.SetValue(str(self.timeRange[1]))

        if (dlg.ShowModal() == wx.ID_OK):

            try:
                self.timeRange[0] = int(dlg.textTime1.GetValue())
            except:
                pass
            try:
                self.timeRange[1] = int(dlg.textTime2.GetValue())
            except:
                pass


        dlg.Destroy()







class BE_GameDataBattlefield:

    def __init__(self):

        self.__bounding = 1000
        self.__cellsize = 10



    def ExportXML(self, root, document):

        main = ET.SubElement(root, "Battlefield")

        ET.SubElement(main, "Bounding").text = str(self.__bounding)
        ET.SubElement(main, "CellSize").text = str(self.__cellsize)

        # Export the rivers
        riverlst = document.GetCanvasObjectsByType(BE_Objects.BE_Object.CANVASOBJECT_RIVER)
        if (riverlst and (len(riverlst) > 0)):

            rivers = ET.SubElement(main, "Rivers")
            for river in riverlst:

                trace = ET.SubElement(rivers, "Trace")
                ET.SubElement(trace, "Width").text = str(river.GetWidth())

                polyline = river.GetShape()
                if (len(polyline) > 0):

                    pol = ET.SubElement(trace, "Polyline")
                    i = 0
                    while (i < len(polyline)):
                        ET.SubElement(pol, "Vertex").text = "[" + str(polyline[i].x) + "," + str(polyline[i].y) + "]"
                        i += 1




    def ImportXML(self, root, document):

        main = root.find("Battlefield")
        if (not main):
            return

        try:
            self.__bounding = int(main.find("Bounding").text)
        except:
            pass

        try:
            self.__cellsize = int(main.find("CellSize").text)
        except:
            pass

        rivers = main.find("Rivers")
        if (rivers):
            for trace in rivers:
                try:
                    if (trace.tag == "Trace"):
                        width = float(trace.find("Width").text)
                        pol = []
                        polyline = trace.find("Polyline")
                        if (polyline):
                            for v in polyline:
                                if (v.tag == "Vertex"):
                                    array = ast.literal_eval(v.text)
                                    pol.append(Geometry.Point2D(array[0], array[1]))

                        river = BE_Objects.BE_River()
                        river.SetShape(pol, width)
                        document.AddCanvasObject(river)
                except:
                    print "WARNING: Wrong river data"





    def OpenDialog(self, parent):

        dlg = BE_Dialogs.BE_GameBattlefieldDlg.BE_GameBattlefieldDlg(parent)

        dlg.textSize.SetValue(str(self.__bounding))
        dlg.textCellSize.SetValue(str(self.__cellsize))

        if (dlg.ShowModal() == wx.ID_OK):

            try:
                self.__bounding = int(dlg.textSize.GetValue())
            except:
                pass
            try:
                self.__cellsize = int(dlg.textCellSize.GetValue())
            except:
                pass


        dlg.Destroy()










class BE_GameDataCastle:

    def __init__(self):
        pass


    def ExportXML(self, root, document):

        main = ET.SubElement(root, "Castle")

        # Export castle orientation vector. Use the default settings one
        orientation = document.GetDefaultSettings().castle.orientationVector
        ET.SubElement(main, "Orientation").text = "[" + str(orientation['X']) + "," + str(orientation['Y']) + "]"

        # Export oldcity
        # If none castle is defined, there can be an oldcity defined. So, castle tag should be ever created
        houselist = document.GetCanvasObjectsByType(BE_Objects.BE_Object.CANVASOBJECT_HOUSE)
        if (houselist and (len(houselist) > 0)):
            housesxml = ET.SubElement(main, "OldCity")
            for house in houselist:
                ET.SubElement(housesxml, "House").text = "[" + str(house.center.x) + "," + str(house.center.y) + "]"



        # Get the castle. It should be a list with only one item. Otherwise, take only the first one
        castlelst = document.GetCanvasObjectsByType(BE_Objects.BE_Object.CANVASOBJECT_CASTLE)
        if (not castlelst):
            return
        if (len(castlelst) == 0):
            return
        castle = castlelst[0]




        # Export moat presence
        moat = castle.GetMoat()
        if (moat['Active']):
            moatxml = ET.SubElement(main, "Moat")
            ET.SubElement(moatxml, "HasWater").text = str(moat['HasWater'])


        # Export the castle shape
        shape = castle.GetShape()
        if (len(shape) > 0):

            shapexml = ET.SubElement(main, "Shape")
            for vert in shape:

                vertxml = ET.SubElement(shapexml, "Vertex")
                ET.SubElement(vertxml, "Point").text = "[" + str(vert.x) + "," + str(vert.y) + "]"

                # Tower data is stored in extra data attached to Point2D object
                if (vert.data):
                    tower = vert.data
                    towertype = tower.GetTowerType()

                    if (towertype == BE_Objects.BE_Tower.TOWERTYPE_SQUARED):
                        ET.SubElement(vertxml, "TowerType").text = "SquaredTower"
                    elif (towertype == BE_Objects.BE_Tower.TOWERTYPE_ROUNDED):
                        ET.SubElement(vertxml, "TowerType").text = "RoundedTower"
                    elif (towertype == BE_Objects.BE_Tower.TOWERTYPE_RANDOM):
                        ET.SubElement(vertxml, "TowerType").text = "Tower"





    def ImportXML(self, root, document):

        main = root.find("Castle")
        if (not main):
            return

        try:
            arr = ast.literal_eval(main.find("Orientation").text)
            document.GetDefaultSettings().castle.orientationVector = {'X': arr[0], 'Y': arr[1]}
        except:
            print "WARNING: Orientation tag not found in Castle category"

        # Old city / houses
        housesxml = main.find("OldCity")
        if (housesxml != None):
            for hxml in housesxml:
                try:
                    arr = ast.literal_eval(hxml.text)
                    house = BE_Objects.BE_House(Geometry.Point2D(arr[0], arr[1]))
                    document.AddCanvasObject(house)
                except:
                    print "WARNING: Wrong house data in Castle category"

        castle = BE_Objects.BE_Castle()

        # Moat
        moatxml = main.find("Moat")
        if (moatxml != None):
            try:
                if (moatxml.find("HasWater").text == "True"):
                    water = True
                else:
                    water = False

                castle.SetMoat(active = True, haswater = water)
            except:
                print "WARNING: Moat/HasWater tag not found in Castle category"
        else:
            castle.SetMoat(active = False)


        # Castle shape
        shapexml = main.find("Shape")
        if (shapexml != None):
            for vertxml in shapexml:
                try:
                    arr = ast.literal_eval(vertxml.find("Point").text)
                    p = Geometry.Point2D(arr[0], arr[1])
                    towerxml = vertxml.find("TowerType")
                    if (towerxml != None):
                        towertype = None
                        if (towerxml.text == "SquaredTower"):
                            towertype = BE_Objects.BE_Tower.TOWERTYPE_SQUARED
                        elif (towerxml.text == "RoundedTower"):
                            towertype = BE_Objects.BE_Tower.TOWERTYPE_ROUNDED
                        elif (towerxml.text == "Tower"):
                            towertype = BE_Objects.BE_Tower.TOWERTYPE_RANDOM

                        if (towertype != None):
                            tower = BE_Objects.BE_Tower(towertype = towertype, center = p.Copy())
                            p.data = tower
                    castle.AddVertex(p)

                except:
                    print "ERROR: Wrong castle shape in Castle category"

        castle.Close()
        document.AddCanvasObject(castle)





class BE_GameDataCityEvolutions:

    """ This class manages the city evolution data and city expansion data, so both are related by group IDs. Note that usage documentation separate both kind of data.
        Note that this could be a little bit confusing. At some point, the group ID must be defined: in city evolution creation or in any city expansion definition.
        Current code uses the former. So, cityexpansions groups should match with city evolution groups. For the second case, the user should create first the group IDs,
        and then allow him to select any one (using a dropdown list by example) when a city evolution is created. This second case is also worse if any group ID is removed


        Attributes:
            expansions: dictionary with expansions data -> {group_id: {expansion_year, walls_height, towers_height}}
            wallsdimensions: walls max and min lengths on expansions
            yearsbetweenexpansions: (see usage) (optional)
    """

    def __init__(self):

        self.__expansions = {}
        self.__wallsDimensions = [50.0, 150.0]
        self.__yearsBetweenExpansions = None



    def ExportXML(self, root, document):

        # Export the city evolutions
        main = ET.SubElement(root, "CityEvolutions")

        groups = self.GetGroups(document)
        for k, v in groups.items():

            groupxml = ET.SubElement(main, "Group")
            ET.SubElement(groupxml, "ID").text = str(k)

            evolutionsxml = ET.SubElement(groupxml, "Evolutions")
            for ev in v:
                evolxml = ET.SubElement(evolutionsxml, "Evolution")

                ET.SubElement(evolxml, "TimeRange").text = "[" + str(ev.timeRange[0]) + "," + str(ev.timeRange[1]) + "]"
                ET.SubElement(evolxml, "HousesPerYear").text = str(ev.housesPerYear)

                vec = ev.arrow.GetDirection()
                ET.SubElement(evolxml, "Direction").text = "[" + str(vec.val[0]) + "," + str(vec.val[1]) + "]"

                segxml = ET.SubElement(evolxml, "SegmentBase")
                ET.SubElement(segxml, "P1").text = "[" + str(ev.baseSegment.p1.x) + "," + str(ev.baseSegment.p1.y) + "]"
                ET.SubElement(segxml, "P2").text = "[" + str(ev.baseSegment.p2.x) + "," + str(ev.baseSegment.p2.y) + "]"

                # This is an extra field that only will be used by the Editor. It justs stores the user arrow length defined to reconstruct it on ImportXML function
                # It does not change anything in the simulation, and is used only for visual purposes
                arrowlength = ET.SubElement(evolxml, "BE_Editor_ArrowLength")
                arrowlength.text = str(ev.arrow.GetLength())


        # Export the city expansions
        cityexpandxml = ET.SubElement(root, "CityExpansion")

        ET.SubElement(cityexpandxml, "WallDimensions").text = "[" + str(self.__wallsDimensions[0]) + "," + str(self.__wallsDimensions[1]) + "]"
        if (self.__yearsBetweenExpansions):
            ET.SubElement(cityexpandxml, "YearsBetweenExpansions").text = str(self.__yearsBetweenExpansions)

        for k, v in self.__expansions.items():

            expansionxml = ET.SubElement(cityexpandxml, "Expansion")
            ET.SubElement(expansionxml, "Year").text = str(v['Year'])
            ET.SubElement(expansionxml, "GroupID").text = k
            if (v['WallsHeight']):
                ET.SubElement(expansionxml, "WallHeight").text = str(v['WallsHeight'])
            if (v['TowersHeight']):
                ET.SubElement(expansionxml, "TowerHeight").text = str(v['TowersHeight'])





    def ImportXML(self, root, document):

        main = root.find("CityEvolutions")
        if (not main):
            return

        for groupxml in main:
            if (groupxml.tag == "Group"):
                try:
                    groupid = int(groupxml.find("ID").text)

                    evolutionsxml = groupxml.find("Evolutions")
                    for evxml in evolutionsxml:

                        cityevolution = BE_Objects.BE_CityEvolution()
                        cityevolution.groupID = groupid

                        arr = ast.literal_eval(evxml.find("TimeRange").text)
                        cityevolution.timeRange = [int(arr[0]), int(arr[1])]
                        cityevolution.housesPerYear = float(evxml.find("HousesPerYear").text)

                        # Reconstruct the base segment and arrow
                        arrdir = ast.literal_eval(evxml.find("Direction").text)
                        direction = Geometry.Vector2D(float(arrdir[0]), float(arrdir[1]))
                        direction.Normalize()
                        basexml = evxml.find("SegmentBase")
                        arrp1 = ast.literal_eval(basexml.find("P1").text)
                        arrp2 = ast.literal_eval(basexml.find("P2").text)
                        cityevolution.baseSegment.p1 = Geometry.Point2D(float(arrp1[0]), float(arrp1[1]))
                        cityevolution.baseSegment.p2 = Geometry.Point2D(float(arrp2[0]), float(arrp2[1]))

                        # Since arrow length is not used in the simulation, it could not be found in the incoming xml (except it is created by the editor, see ExportXML)
                        # If it is not present, use the base segment length as the default one

                        arrowlengthxml = evxml.find("BE_Editor_ArrowLength")
                        if (arrowlengthxml == None):
                            arrowlength = cityevolution.baseSegment.GetLength()
                        else:
                            arrowlength = float(arrowlengthxml.text)


                        mid = cityevolution.baseSegment.GetMidPoint()
                        mid.Move(direction, arrowlength)
                        cityevolution.arrow.p1 = cityevolution.baseSegment.GetMidPoint()
                        cityevolution.arrow.p2 = mid

                        document.AddCanvasObject(cityevolution)

                except:
                    print "WARNING: Wrong city evolution data in CityEvolutions category"


        # Parse the city expansion checkings
        cityexpandxml = root.find("CityExpansion")

        try:
            walldims = ast.literal_eval(cityexpandxml.find("WallDimensions").text)
            self.__wallsDimensions[0] = float(walldims[0])
            self.__wallsDimensions[1] = float(walldims[1])
        except:
            pass            # Optional

        try:
            self.__yearsBetweenExpansions = int(cityexpandxml.find("YearsBetweenExpansions").text)
        except:
            pass            # Optional

        if (cityexpandxml != None):
            for expxml in cityexpandxml:
                if (expxml.tag == "Expansion"):
                    try:
                        year = int(expxml.find("Year").text)
                        groupid = int(expxml.find("GroupID").text)
                        wxml = expxml.find("WallHeight")
                        if (wxml != None):          # Optional
                            wheight = float(wxml.text)
                        else:
                            wheight = None
                        txml = expxml.find("TowerHeight")
                        if (txml != None):          # Optional
                            theight = float(txml.text)
                        else:
                            theight = None

                        self.__expansions[str(groupid)] = {'Year': year, 'WallsHeight': wheight, 'TowersHeight': theight}


                    except:
                        print "WARNING: Wrong city expansion data in CityExpansions category"








    def GetGroups(self, document):
        # Returns dictionary where each key is a group ID and its values are lists with related city evolutions data

        groups = {}
        evolutions = document.GetCanvasObjectsByType(BE_Objects.BE_Object.CANVASOBJECT_CITYEVOLUTION)
        if (evolutions and (len(evolutions) > 0)):
            for ev in evolutions:
                if (groups.has_key(str(ev.groupID))):
                    groups[str(ev.groupID)].append(ev)
                else:
                    groups[str(ev.groupID)] = [ev]

        return groups



    def OpenDialog(self, parent):
        # Since the city evolutions grous do not have any game data to edit, current dialog edits the city expansion data

        # Match current list of city evolutions groups with current cityexpansion groups
        groups = self.GetGroups(parent.GetDocument())
        for k, v in groups.items():
            if (not self.__expansions.has_key(k)):
                self.__expansions[k] = {'Year': 0, 'WallsHeight': None, 'TowersHeight': None}
        for k, v in self.__expansions.items():
            if (not groups.has_key(k)):
                del self.__expansions[k]

        dlg = BE_Dialogs.BE_GameCityExpansionsDlg.BE_GameCityExpansionsDlg(parent)

        # Lock the group ID column in dialog grid
        attr = wx.grid.GridCellAttr()
        attr.SetReadOnly(True)
        dlg.grid.SetColAttr(0, attr)


        # Populate the dialog grid
        if (len(self.__expansions) > 0):
            dlg.grid.InsertRows(numRows = len(self.__expansions))
        i = 0
        for k, v in self.__expansions.items():
            dlg.grid.SetCellValue(i, 0, str(k))
            dlg.grid.SetCellValue(i, 1, str(v['Year']))
            if (v['WallsHeight']):
                dlg.grid.SetCellValue(i, 2, str(v['WallsHeight']))
            if (v['TowersHeight']):
                dlg.grid.SetCellValue(i, 3, str(v['TowersHeight']))

            i += 1

        dlg.textWallDimMin.SetValue(str(self.__wallsDimensions[0]))
        dlg.textWallDimMax.SetValue(str(self.__wallsDimensions[1]))
        if (self.__yearsBetweenExpansions):
            dlg.textYearsBetween.SetValue(str(self.__yearsBetweenExpansions))


        if (dlg.ShowModal() == wx.ID_OK):

            try:
                self.__wallsDimensions[0] = float(dlg.textWallDimMin.GetValue())
            except:
                pass
            try:
                self.__wallsDimensions[1] = float(dlg.textWallDimMax.GetValue())
            except:
                pass
            try:
                self.__yearsBetweenExpansions = int(dlg.textYearsBetween.GetValue())
            except:
                pass

            i = 0
            while (i < len(self.__expansions)):
                try:
                    group = dlg.grid.GetCellValue(i, 0)
                    year = int(dlg.grid.GetCellValue(i, 1))
                    self.__expansions[group] = {'Year': 0, 'WallsHeight': None, 'TowersHeight': None}
                    self.__expansions[group]['Year'] = year
                except:
                    i += 1
                    continue
                try:
                    self.__expansions[group]['WallsHeight'] = float(dlg.grid.GetCellValue(i, 2))
                except:
                    pass
                try:
                    self.__expansions[group]['TowersHeight'] = float(dlg.grid.GetCellValue(i, 3))
                except:
                    pass

                i += 1




        dlg.Destroy()






class BE_GameDataStarFortress:

    """ Star Fortress game data. Currently only manages its activation or not
    """

    def __init__(self):

        self.__activated = False


    def OpenDialog(self, parent):

        dlg = BE_Dialogs.BE_GameStarFortressDlg.BE_GameStarFortressDlg(parent)

        dlg.checkActivate.SetValue(self.__activated)

        if (dlg.ShowModal() == wx.ID_OK):

            self.__activated = dlg.checkActivate.GetValue()

        dlg.Destroy()


    def ExportXML(self, root, document):

        if (not self.__activated):
            return

        # Export the city evolutions
        main = ET.SubElement(root, "StarFortress")
        ET.SubElement(main, "Activate").text = str(self.__activated)

    def ImportXML(self, root, document):

        main = root.find("StarFortress")
        if (not main):
            return

        try:
            self.__activated = (main.find("Activate").text in ['True', 'true', 'yes', 'YES', '1', 'Yes', 'TRUE'])

        except:
            print "WARNING: Activate tag not found in Star Fortress category"




class BE_GameDataExpansionCheckings:

    """ Expansion checking dates class management

        Attributes:
            checkings: Years list

    """

    def __init__(self):

        self.__checkings = []
        self.__dialog = None


    def OpenDialog(self, parent):

        self.__dialog = BE_Dialogs.BE_GameDataExpansionCheckingsDlg.BE_GameDataExpansionCheckingsDlg(parent)

        # Control the bindings to uncouple UI from data management
        self.__dialog.buttonAdd.Bind(wx.EVT_BUTTON, self.OnAddYear)
        self.__dialog.buttonDelete.Bind(wx.EVT_BUTTON, self.OnDeleteYear)

        # Populate the list
        if (self.__checkings):
            for year in self.__checkings:
                self.__dialog.list.Append(str(year))
            self.__dialog.list.SetSelection(0)


        if (self.__dialog.ShowModal() == wx.ID_OK):

            self.__checkings = []
            i = 0
            while i < self.__dialog.list.GetCount() :
                try:
                    self.__checkings.append(int(self.__dialog.list.GetString(i)))
                except:
                    pass

                i += 1


        self.__dialog.Destroy()
        self.__dialog = None





    def OnAddYear(self, event):

        if (not self.__dialog):
            return

        dlg = wx.TextEntryDialog(self.__dialog, 'Add expansion checking ','Year')
        if dlg.ShowModal() == wx.ID_OK:
            self.__dialog.list.Append(str(dlg.GetValue()))

        dlg.Destroy()




    def OnDeleteYear(self, event):

        if (not self.__dialog):
            return

        sel = self.__dialog.list.GetSelection()
        if (sel == wx.NOT_FOUND):
            return
        else:
            self.__dialog.list.Delete(sel)





    def ExportXML(self, root, document):

        if (len(self.__checkings) > 0):
            main = ET.SubElement(root, "ExpansionCheckings")

            for year in self.__checkings:
                ET.SubElement(main, "Year").text = str(year)



    def ImportXML(self, root, document):

        main = root.find("ExpansionCheckings")
        if (not main):
            return

        for check in main:
            if (check.tag == "Year"):
                try:
                    self.__checkings.append(int(check.text))
                except:
                    print "WARNING: Wrong Year data in ExpansionCheckings category"

