import wx
import BE_Dialogs.BE_DefaultGameSettingsDlg
import BE_Dialogs.BE_DefaultCitySettingsDlg
import BE_Dialogs.BE_DefaultArmySettingsDlg
import BE_Dialogs.BE_DefaultBattlefieldSettingsDlg
import BE_Dialogs.BE_DefaultCastleSettingsDlg
import xml.etree.cElementTree as ET
import xml.dom.minidom
import ast




class BE_DefaultSettings:
    """ Class to manage the default game settings

        Attributes:
            (see usage documentation to get more information about all settings parameters)
    """

    def __init__(self):

        self.castle = BE_DefaultCastleSettings()
        self.battlefield = BE_DefaultBattlefieldSettings()
        self.army = BE_DefaultArmySettings()
        self.city = BE_DefaultCitySettings()
        self.game = BE_DefaultGameSettings()


    def ExportXML(self, filename):

        root = ET.Element("Battles")

        self.castle.ExportXML(root)
        self.battlefield.ExportXML(root)
        self.army.ExportXML(root)
        self.city.ExportXML(root)
        self.game.ExportXML(root)


        xmlstring = ET.tostring(root, 'utf-8', method='xml')
        parsed = xml.dom.minidom.parseString(xmlstring)
        pretty = parsed.toprettyxml(indent = "    ")

        filexml = open(filename, 'w')
        filexml.write(pretty)
        filexml.close()


    def ImportXML(self, filename, mainwindow):

        tree = xml.etree.cElementTree.parse(filename)
        main = tree.getroot()
        if (not main):
            print "ERROR: Wrong default settings file"
            return

        self.castle.ImportXML(main)
        self.battlefield.ImportXML(main)
        self.army.ImportXML(main)
        self.city.ImportXML(main)
        self.game.ImportXML(main, mainwindow)






class BE_DefaultCastleSettings:

    def __init__(self):

        self.orientationVector = {'X': 0.0, 'Y': -1.0}
        self.defendingLines = {'Width': 4.0, 'CellSize': 2.0, 'Height': 0.0}
        self.curtainWallOldCityMargin = 30.0
        self.showLabels = False

        self.walls = BE_DefaultCastleWallSettings()
        self.towers = BE_DefaultCastleTowerSettings()
        self.moat = BE_DefaultCastleMoatSettings()
        self.bastions = BE_DefaultCastleBastionSettings()
        self.starfortress = BE_DefaultCastleStarFortressSettings()


    def ExportXML(self, root):

        main = ET.SubElement(root, "Castle")


        ET.SubElement(main, "Orientation").text = "[" + str(self.orientationVector['X']) + "," + str(self.orientationVector['Y']) + "]"
        ET.SubElement(main, "ShowLabels").text = str(self.showLabels)
        ET.SubElement(main, "CurtainWallOldCityMargin").text = str(self.curtainWallOldCityMargin)

        defendingline = ET.SubElement(main, "DefendingLine")
        ET.SubElement(defendingline, "Width").text = str(self.defendingLines['Width'])
        ET.SubElement(defendingline, "CellSize").text = str(self.defendingLines['CellSize'])
        ET.SubElement(defendingline, "Height").text = str(self.defendingLines['Height'])

        self.walls.ExportXML(main)
        self.towers.ExportXML(main)
        self.moat.ExportXML(main)
        self.bastions.ExportXML(main)
        self.starfortress.ExportXML(main)



    def ImportXML(self, root):

        main = root.find("Castle")
        if (not main):
            print "ERROR: Castle settings not found"
            return

        try:
            arr = ast.literal_eval(main.find("Orientation").text)
            self.orientationVector = {'X': arr[0], 'Y': arr[1]}
        except:
            print "WARNING: Orientation tag not found in Castle category"

        try:
            self.showLabels = (main.find("ShowLabels").text in ['True', 'true', 'yes', 'YES', '1', 'Yes', 'TRUE'])
        except:
            print "WARNING: ShowLabels tag not found in Castle category"

        try:
            self.curtainWallOldCityMargin = float(main.find("CurtainWallOldCityMargin").text)
        except:
            print "WARNING: CurtainWallOldCityMargin tag not found in Castle category"

        dlxml = main.find("DefendingLine")
        if (dlxml != None):
            try:
                self.defendingLines['Width'] = float(dlxml.find("Width").text)
                self.defendingLines['CellSize'] = float(dlxml.find("CellSize").text)
                self.defendingLines['Height'] = float(dlxml.find("Height").text)
            except:
                print "WARNING: Wrong DefendingLine data in Castle category"
        else:
            print "WARNING: DefendingLine tag not found in Castle category"

        self.walls.ImportXML(main)
        self.towers.ImportXML(main)
        self.moat.ImportXML(main)
        self.bastions.ImportXML(main)
        self.starfortress.ImportXML(main)





    def OpenDialog(self, parent):

        dlg = BE_Dialogs.BE_DefaultCastleSettingsDlg.BE_DefaultCastleSettingsDlg(parent)

        dlg.textOrientationX.SetValue(str(self.orientationVector['X']))
        dlg.textOrientationY.SetValue(str(self.orientationVector['Y']))
        dlg.textDefendingLineWidth.SetValue(str(self.defendingLines['Width']))
        dlg.textDefendingLineCellsize.SetValue(str(self.defendingLines['CellSize']))
        dlg.textDefendingLineHeight.SetValue(str(self.defendingLines['Height']))
        dlg.textOldCityMargin.SetValue(str(self.curtainWallOldCityMargin))
        dlg.checkLabels.SetValue(self.showLabels)

        self.walls.PopulateDialog(dlg)
        self.towers.PopulateDialog(dlg)
        self.moat.PopulateDialog(dlg)
        self.bastions.PopulateDialog(dlg)
        self.starfortress.PopulateDialog(dlg)

        if (dlg.ShowModal() == wx.ID_OK):
            try:
                self.orientationVector['X'] = float(dlg.textOrientationX.GetValue())
            except:
                pass
            try:
                self.orientationVector['Y'] = float(dlg.textOrientationY.GetValue())
            except:
                pass
            try:
                self.defendingLines['Width'] = float(dlg.textDefendingLineWidth.GetValue())
            except:
                pass
            try:
                self.defendingLines['CellSize'] = float(dlg.textDefendingLineCellsize.GetValue())
            except:
                pass
            try:
                self.defendingLines['Height'] = float(dlg.textDefendingLineHeight.GetValue())
            except:
                pass
            try:
                self.curtainWallOldCityMargin = float(dlg.textOldCityMargin.GetValue())
            except:
                pass
            try:
                self.showLabels = dlg.checkLabels.GetValue()
            except:
                pass

            self.walls.GetDialogData(dlg)
            self.towers.GetDialogData(dlg)
            self.moat.GetDialogData(dlg)
            self.bastions.GetDialogData(dlg)
            self.starfortress.GetDialogData(dlg)


        dlg.Destroy()






class BE_DefaultCastleWallSettings:

    def __init__(self):

        self.height = 14.0
        self.thickness = 5.0
        self.merlonHeight = 2.0
        self.walkwayWidth = 4.0
        self.defenseIncrease = 700
        self.battalionGridCellSize = 2.0
        self.defenseAngle = {'Horizontal': 90.0, 'Vertical': [45.0, 90.0]}
        self.tiles = {'Width': 3.5, 'Height': 2.5, 'Resistance': 100000, 'RubbleConversionFactor': [0.25, 0.5, 0.25]}



    def ExportXML(self, root):

        main = ET.SubElement(root, "Wall")

        ET.SubElement(main, "InnerHeight").text = str(self.height)
        ET.SubElement(main, "Thickness").text = str(self.thickness)
        ET.SubElement(main, "MerlonHeight").text = str(self.merlonHeight)
        ET.SubElement(main, "WalkwayWidth").text = str(self.walkwayWidth)
        ET.SubElement(main, "DefenseIncrease").text = str(self.defenseIncrease)
        ET.SubElement(main, "BattalionGridCellSize").text = str(self.battalionGridCellSize)

        defenseangle = ET.SubElement(main, "DefenseAngle")
        ET.SubElement(defenseangle, "H").text = str(self.defenseAngle['Horizontal'])
        ET.SubElement(defenseangle, "V").text = "[" + str(self.defenseAngle['Vertical'][0]) + "," + str(self.defenseAngle['Vertical'][1]) + "]"

        tile = ET.SubElement(main, "Tile")
        ET.SubElement(tile, "Width").text = str(self.tiles['Width'])
        ET.SubElement(tile, "Height").text = str(self.tiles['Height'])
        ET.SubElement(tile, "Resistance").text = str(self.tiles['Resistance'])
        ET.SubElement(tile, "RubbleConversionFactor").text = "[" + str(self.tiles['RubbleConversionFactor'][0]) + "," + str(self.tiles['RubbleConversionFactor'][1]) + "," + str(self.tiles['RubbleConversionFactor'][2]) + "]"


    def ImportXML(self, root):

        main = root.find("Wall")
        if (not main):
            print "ERROR: Castle/Wall settings not found"
            return

        try:
            self.height = float(main.find("InnerHeight").text)
        except:
            print "WARNING: InnerHeight tag not found in Castle/Wall category"

        try:
            self.thickness = float(main.find("Thickness").text)
        except:
            print "WARNING: Thickness tag not found in Castle/Wall category"

        try:
            self.merlonHeight = float(main.find("MerlonHeight").text)
        except:
            print "WARNING: MerlonHeight tag not found in Castle/Wall category"

        try:
            self.walkwayWidth = float(main.find("WalkwayWidth").text)
        except:
            print "WARNING: WalkwayWidth tag not found in Castle/Wall category"

        try:
            self.defenseIncrease = float(main.find("DefenseIncrease").text)
        except:
            print "WARNING: DefenseIncrease tag not found in Castle/Wall category"

        try:
            self.battalionGridCellSize = float(main.find("BattalionGridCellSize").text)
        except:
            print "WARNING: BattalionGridCellSize tag not found in Castle/Wall category"


        defangxml = main.find("DefenseAngle")
        if (defangxml != None):
            try:
                self.defenseAngle['Horizontal'] = float(defangxml.find("H").text)
                arr = ast.literal_eval(defangxml.find("V").text)
                self.defenseAngle['Vertical'] = [float(arr[0]), float(arr[1])]

            except:
                print "WARNING: Wrong DefenseAngle data in Castle/Wall category"
        else:
            print "WARNING: DefenseAngle tag not found in Castle/Wall category"

        tilexml = main.find("Tile")
        if (tilexml != None):
            try:
                self.tiles['Width'] = float(tilexml.find("Width").text)
                self.tiles['Height'] = float(tilexml.find("Height").text)
                self.tiles['Resistance'] = float(tilexml.find("Resistance").text)
                arr = ast.literal_eval(tilexml.find("RubbleConversionFactor").text)
                self.tiles['RubbleConversionFactor'] = [float(arr[0]), float(arr[1]), float(arr[2])]
            except:
                print "WARNING: Wrong Tile data in Castle/Wall category"
        else:
            print "WARNING: Tile tag not found in Castle/Wall category"





    def PopulateDialog(self, dlg):

        dlg.textWallHeight.SetValue(str(self.height))
        dlg.textWallThickness.SetValue(str(self.thickness))
        dlg.textMerlonHeight.SetValue(str(self.merlonHeight))
        dlg.textWallWalkwayWidth.SetValue(str(self.walkwayWidth))
        dlg.textWallDefenseIncrease.SetValue(str(self.defenseIncrease))
        dlg.textWallBattalionCellSize.SetValue(str(self.battalionGridCellSize))
        dlg.textWallDefenseAngleHorizontal.SetValue(str(self.defenseAngle['Horizontal']))
        dlg.textWallDefenseAngleVertical1.SetValue(str(self.defenseAngle['Vertical'][0]))
        dlg.textWallDefenseAngleVertical2.SetValue(str(self.defenseAngle['Vertical'][1]))
        dlg.textWallTilesWidth.SetValue(str(self.tiles['Width']))
        dlg.textWallTilesHeight.SetValue(str(self.tiles['Height']))
        dlg.textWallTilesResistance.SetValue(str(self.tiles['Resistance']))
        dlg.textWallTilesRubble1.SetValue(str(self.tiles['RubbleConversionFactor'][0]))
        dlg.textWallTilesRubble2.SetValue(str(self.tiles['RubbleConversionFactor'][1]))
        dlg.textWallTilesRubble3.SetValue(str(self.tiles['RubbleConversionFactor'][2]))


    def GetDialogData(self, dlg):

        try:
            self.height = float(dlg.textWallHeight.GetValue())
        except:
            pass
        try:
            self.thickness = float(dlg.textWallThickness.GetValue())
        except:
            pass
        try:
            self.merlonHeight = float(dlg.textMerlonHeight.GetValue())
        except:
            pass
        try:
            self.walkwayWidth = float(dlg.textWallWalkwayWidth.GetValue())
        except:
            pass
        try:
            self.defenseIncrease = float(dlg.textWallDefenseIncrease.GetValue())
        except:
            pass
        try:
            self.battalionGridCellSize = float(dlg.textWallBattalionCellSize.GetValue())
        except:
            pass
        try:
            self.defenseAngle['Horizontal'] = float(dlg.textWallDefenseAngleHorizontal.GetValue())
        except:
            pass
        try:
            self.defenseAngle['Vertical'][0] = float(dlg.textWallDefenseAngleVertical1.GetValue())
        except:
            pass
        try:
            self.defenseAngle['Vertical'][1] = float(dlg.textWallDefenseAngleVertical2.GetValue())
        except:
            pass
        try:
            self.tiles['Width'] = float(dlg.textWallTilesWidth.GetValue())
        except:
            pass
        try:
            self.tiles['Height'] = float(dlg.textWallTilesHeight.GetValue())
        except:
            pass
        try:
            self.tiles['Resistance'] = float(dlg.textWallTilesResistance.GetValue())
        except:
            pass
        try:
            self.tiles['RubbleConversionFactor'][0] = float(dlg.textWallTilesRubble1.GetValue())
        except:
            pass
        try:
            self.tiles['RubbleConversionFactor'][1] = float(dlg.textWallTilesRubble2.GetValue())
        except:
            pass
        try:
            self.tiles['RubbleConversionFactor'][2] = float(dlg.textWallTilesRubble3.GetValue())
        except:
            pass





class BE_DefaultCastleTowerSettings:

    def __init__(self):

        self.timeRange = {'Squared': [-5, 14], 'Rounded': [12, 17], 'Bastion': [16, 19]}
        self.height = 25.0
        self.thickness = 4.0
        self.squareSide = 25.0
        self.circleRadius = 20.0
        self.defenseIncrease = 800
        self.battalionGridCellSize = {'Large': 10.0, 'Small': 2.0}
        self.defenseAngle = {'Horizontal': 90.0, 'Vertical': [45.0, 90.0]}
        self.requiredDistanceNeighborFactor = 3.0


    def ExportXML(self, root):

        main = ET.SubElement(root, "Tower")


        ET.SubElement(main, "InnerHeight").text = str(self.height)
        ET.SubElement(main, "Thickness").text = str(self.thickness)
        ET.SubElement(main, "DefenseIncrease").text = str(self.defenseIncrease)
        ET.SubElement(main, "SquareSide").text = str(self.squareSide)
        ET.SubElement(main, "CircleRadius").text = str(self.circleRadius)
        ET.SubElement(main, "RequiredDistanceNeighborFactor").text = str(self.requiredDistanceNeighborFactor)

        defenseangle = ET.SubElement(main, "DefenseAngle")
        ET.SubElement(defenseangle, "H").text = str(self.defenseAngle['Horizontal'])
        ET.SubElement(defenseangle, "V").text = "[" + str(self.defenseAngle['Vertical'][0]) + "," + str(self.defenseAngle['Vertical'][1]) + "]"

        battalion = ET.SubElement(main, "BattalionGridCellSize")
        ET.SubElement(battalion, "Large").text = str(self.battalionGridCellSize['Large'])
        ET.SubElement(battalion, "Small").text = str(self.battalionGridCellSize['Small'])

        timerange = ET.SubElement(main, "TimeRange")
        ET.SubElement(timerange, "Squared").text = "[" + str(self.timeRange['Squared'][0]) + "," + str(self.timeRange['Squared'][1]) + "]"
        ET.SubElement(timerange, "Rounded").text = "[" + str(self.timeRange['Rounded'][0]) + "," + str(self.timeRange['Rounded'][1]) + "]"
        ET.SubElement(timerange, "Bastion").text = "[" + str(self.timeRange['Bastion'][0]) + "," + str(self.timeRange['Bastion'][1]) + "]"




    def ImportXML(self, root):

        main = root.find("Tower")
        if (not main):
            print "ERROR: Castle/Tower settings not found"
            return


        try:
            self.height = float(main.find("InnerHeight").text)
        except:
            print "WARNING: InnerHeight tag not found in Castle/Tower category"

        try:
            self.thickness = float(main.find("Thickness").text)
        except:
            print "WARNING: Thickness tag not found in Castle/Tower category"

        try:
            self.defenseIncrease = float(main.find("DefenseIncrease").text)
        except:
            print "WARNING: DefenseIncrease tag not found in Castle/Tower category"

        try:
            self.circleRadius = float(main.find("CircleRadius").text)
        except:
            print "WARNING: CircleRadius tag not found in Castle/Tower category"

        try:
            self.squareSide = float(main.find("SquareSide").text)
        except:
            print "WARNING: SquareSide tag not found in Castle/Tower category"

        try:
            self.requiredDistanceNeighborFactor = float(main.find("RequiredDistanceNeighborFactor").text)
        except:
            print "WARNING: RequiredDistanceNeighborFactor tag not found in Castle/Tower category"


        defangxml = main.find("DefenseAngle")
        if (defangxml != None):
            try:
                self.defenseAngle['Horizontal'] = float(defangxml.find("H").text)
                arr = ast.literal_eval(defangxml.find("V").text)
                self.defenseAngle['Vertical'] = [float(arr[0]), float(arr[1])]

            except:
                print "WARNING: Wrong DefenseAngle data in Castle/Tower category"
        else:
            print "WARNING: DefenseAngle tag not found in Castle/Tower category"


        batxml = main.find("BattalionGridCellSize")
        if (batxml != None):
            try:
                self.battalionGridCellSize['Large'] = float(batxml.find("Large").text)
                self.battalionGridCellSize['Small'] = float(batxml.find("Small").text)
            except:
                print "WARNING: Wrong BattalionGridCellSize data in Castle/Tower category"
        else:
            print "WARNING: BattalionGridCellSize tag not found in Castle/Tower category"


        timexml = main.find("TimeRange")
        if (timexml != None):
            try:
                arr1 = ast.literal_eval(timexml.find("Squared").text)
                self.timeRange['Squared'] = [int(arr1[0]), int(arr1[1])]
                arr2 = ast.literal_eval(timexml.find("Rounded").text)
                self.timeRange['Rounded'] = [int(arr2[0]), int(arr2[1])]
                arr3 = ast.literal_eval(timexml.find("Bastion").text)
                self.timeRange['Bastion'] = [int(arr3[0]), int(arr3[1])]
            except:
                print "WARNING: Wrong TimeRange data in Castle/Tower category"
        else:
            print "WARNING: TimeRange tag not found in Castle/Tower category"





    def PopulateDialog(self, dlg):

        dlg.textTowerTimeRangeSquared1.SetValue(str(self.timeRange['Squared'][0]))
        dlg.textTowerTimeRangeSquared2.SetValue(str(self.timeRange['Squared'][1]))
        dlg.textTowerTimeRangeRounded1.SetValue(str(self.timeRange['Rounded'][0]))
        dlg.textTowerTimeRangeRounded2.SetValue(str(self.timeRange['Rounded'][1]))
        dlg.textTowerTimeRangeBastion1.SetValue(str(self.timeRange['Bastion'][0]))
        dlg.textTowerTimeRangeBastion2.SetValue(str(self.timeRange['Bastion'][1]))
        dlg.textTowerHeight.SetValue(str(self.height))
        dlg.textTowerThickness.SetValue(str(self.thickness))
        dlg.textTowerSide.SetValue(str(self.squareSide))
        dlg.textTowerRadius.SetValue(str(self.circleRadius))
        dlg.textTowerDefenseIncrease.SetValue(str(self.defenseIncrease))
        dlg.textTowerCellSizeLarge.SetValue(str(self.battalionGridCellSize['Large']))
        dlg.textTowerCellSizeSmall.SetValue(str(self.battalionGridCellSize['Small']))
        dlg.textTowerDefenseAngleHorizontal.SetValue(str(self.defenseAngle['Horizontal']))
        dlg.textTowerDefenseAngleVertical1.SetValue(str(self.defenseAngle['Vertical'][0]))
        dlg.textTowerDefenseAngleVertical2.SetValue(str(self.defenseAngle['Vertical'][1]))
        dlg.textTowerDistance.SetValue(str(self.requiredDistanceNeighborFactor))



    def GetDialogData(self, dlg):

        try:
            self.timeRange['Squared'][0] = int(dlg.textTowerTimeRangeSquared1.GetValue())
        except:
            pass
        try:
            self.timeRange['Squared'][1] = int(dlg.textTowerTimeRangeSquared2.GetValue())
        except:
            pass
        try:
            self.timeRange['Rounded'][0] = int(dlg.textTowerTimeRangeRounded1.GetValue())
        except:
            pass
        try:
            self.timeRange['Rounded'][1] = int(dlg.textTowerTimeRangeRounded2.GetValue())
        except:
            pass
        try:
            self.timeRange['Bastion'][0] = int(dlg.textTowerTimeRangeBastion1.GetValue())
        except:
            pass
        try:
            self.timeRange['Bastion'][1] = int(dlg.textTowerTimeRangeBastion2.GetValue())
        except:
            pass
        try:
            self.height = float(dlg.textTowerHeight.GetValue())
        except:
            pass
        try:
            self.thickness = float(dlg.textTowerThickness.GetValue())
        except:
            pass
        try:
            self.squareSide = float(dlg.textTowerSide.GetValue())
        except:
            pass
        try:
            self.circleRadius = float(dlg.textTowerRadius.GetValue())
        except:
            pass
        try:
            self.defenseIncrease = float(dlg.textTowerDefenseIncrease.GetValue())
        except:
            pass
        try:
            self.requiredDistanceNeighborFactor = float(dlg.textTowerDistance.GetValue())
        except:
            pass
        try:
            self.battalionGridCellSize['Large'] = float(dlg.textTowerCellSizeLarge.GetValue())
        except:
            pass
        try:
            self.battalionGridCellSize['Small'] = float(dlg.textTowerCellSizeSmall.GetValue())
        except:
            pass
        try:
            self.defenseAngle['Horizontal'] = float(dlg.textWallDefenseAngleHorizontal.GetValue())
        except:
            pass
        try:
            self.defenseAngle['Vertical'][0] = float(dlg.textWallDefenseAngleVertical1.GetValue())
        except:
            pass
        try:
            self.defenseAngle['Vertical'][1] = float(dlg.textWallDefenseAngleVertical2.GetValue())
        except:
            pass



class BE_DefaultCastleMoatSettings:

    def __init__(self):

        self.depth = 5.0
        self.width = 5.0
        self.hasWater = True
        self.penaltyWater = 0.05
        self.penaltyNoWater = 0.2


    def ExportXML(self, root):

        main = ET.SubElement(root, "Moat")


        ET.SubElement(main, "Depth").text = str(self.depth)
        ET.SubElement(main, "Width").text = str(self.width)
        ET.SubElement(main, "HasWater").text = str(self.hasWater)
        ET.SubElement(main, "PenaltyWater").text = str(self.penaltyWater)
        ET.SubElement(main, "PenaltyNoWater").text = str(self.penaltyNoWater)


    def ImportXML(self, root):

        main = root.find("Moat")
        if (not main):
            print "ERROR: Castle/Moat settings not found"
            return

        try:
            self.depth = float(main.find("Depth").text)
        except:
            print "WARNING: Depth tag not found in Castle/Moat category"

        try:
            self.width = float(main.find("Width").text)
        except:
            print "WARNING: Width tag not found in Castle/Moat category"

        try:
            self.hasWater = (main.find("HasWater").text  in ['True', 'true', 'yes', 'YES', '1', 'Yes', 'TRUE'])
        except:
            print "WARNING: HasWater tag not found in Castle/Moat category"

        try:
            self.penaltyWater = float(main.find("PenaltyWater").text)
        except:
            print "WARNING: PenaltyWater tag not found in Castle/Moat category"

        try:
            self.penaltyNoWater = float(main.find("PenaltyNoWater").text)
        except:
            print "WARNING: PenaltyNoWater tag not found in Castle/Moat category"








    def PopulateDialog(self, dlg):

        dlg.textMoatDepth.SetValue(str(self.depth))
        dlg.textMoatWidth.SetValue(str(self.width))
        dlg.checkMoatHasWater.SetValue(self.hasWater)
        dlg.textMoatPenaltyWithWater.SetValue(str(self.penaltyWater))
        dlg.textMoatPenaltyWithoutWater.SetValue(str(self.penaltyNoWater))


    def GetDialogData(self, dlg):

        try:
            self.depth = float(dlg.textMoatDepth.GetValue())
        except:
            pass
        try:
            self.width = float(dlg.textMoatWidth.GetValue())
        except:
            pass
        try:
            self.hasWater = dlg.checkMoatHasWater.GetValue()
        except:
            pass
        try:
            self.penaltyWater = float(dlg.textMoatPenaltyWithWater.GetValue())
        except:
            pass
        try:
            self.penaltyNoWater = float(dlg.textMoatPenaltyWithoutWater.GetValue())
        except:
            pass



class BE_DefaultCastleBastionSettings:

    def __init__(self):

        self.virtualCircleRadius = 50.0
        self.thickness = 10.0
        self.height = 14.0
        self.battalionGridCellSize = {'Large': 10.0, 'Small': 2.0}
        self.minDistance = 10.0



    def ExportXML(self, root):

        main = ET.SubElement(root, "Bastion")


        ET.SubElement(main, "VirtualCircleRadius").text = str(self.virtualCircleRadius)
        ET.SubElement(main, "Thickness").text = str(self.thickness)
        ET.SubElement(main, "Height").text = str(self.height)
        ET.SubElement(main, "MinDistance").text = str(self.minDistance)

        battalion = ET.SubElement(main, "BattalionGridCellSize")
        ET.SubElement(battalion, "Large").text = str(self.battalionGridCellSize['Large'])
        ET.SubElement(battalion, "Small").text = str(self.battalionGridCellSize['Small'])


    def ImportXML(self, root):

        main = root.find("Bastion")
        if (not main):
            print "ERROR: Castle/Bastion settings not found"
            return

        try:
            self.virtualCircleRadius = float(main.find("VirtualCircleRadius").text)
        except:
            print "WARNING: VirtualCircleRadius tag not found in Castle/Bastion category"

        try:
            self.thickness = float(main.find("Thickness").text)
        except:
            print "WARNING: Thickness tag not found in Castle/Bastion category"

        try:
            self.height = float(main.find("Height").text)
        except:
            print "WARNING: Height tag not found in Castle/Bastion category"

        try:
            self.minDistance = float(main.find("MinDistance").text)
        except:
            print "WARNING: MinDistance tag not found in Castle/Bastion category"



        batxml = main.find("BattalionGridCellSize")
        if (batxml != None):
            try:
                self.battalionGridCellSize['Large'] = float(batxml.find("Large").text)
                self.battalionGridCellSize['Small'] = float(batxml.find("Small").text)
            except:
                print "WARNING: Wrong BattalionGridCellSize data in Castle/Bastion category"
        else:
            print "WARNING: BattalionGridCellSize tag not found in Castle/Bastion category"




    def PopulateDialog(self, dlg):

        dlg.textBastionVirtualCircleRadius.SetValue(str(self.virtualCircleRadius))
        dlg.textBastionThickness.SetValue(str(self.thickness))
        dlg.textBastionHeight.SetValue(str(self.height))
        dlg.textBastionCellSizeLarge.SetValue(str(self.battalionGridCellSize['Large']))
        dlg.textBastionCellSizeSmall.SetValue(str(self.battalionGridCellSize['Small']))
        dlg.textBastionMinDistance.SetValue(str(self.minDistance))


    def GetDialogData(self, dlg):

        try:
            self.virtualCircleRadius = float(dlg.textBastionVirtualCircleRadius.GetValue())
        except:
            pass
        try:
            self.thickness = float(dlg.textBastionThickness.GetValue())
        except:
            pass
        try:
            self.height = float(dlg.textBastionHeight.GetValue())
        except:
            pass
        try:
            self.battalionGridCellSize['Large'] = float(dlg.textBastionCellSizeLarge.GetValue())
        except:
            pass
        try:
            self.battalionGridCellSize['Small'] = float(dlg.textBastionCellSizeSmall.GetValue())
        except:
            pass
        try:
            self.minDistance = float(dlg.textBastionMinDistance.GetValue())
        except:
            pass




class BE_DefaultCastleStarFortressSettings:

    def __init__(self):

        self.ravelin = {'Method': 2, 'BastionAngle': 120.0, 'Radius': 50.0, 'MinimumWidth': 15.0, 'Height': 14.0}
        self.halfmoon = {'Active': True, 'CircleOffset': 5.0, 'Length': 30.0, 'Height': 14.0}
        self.covertway = {'Height': 14.0,'Thickness': 10.0, 'Offset': 5.0, 'PlaceOfArms': True, 'PlaceOfArmsLength': 10.0, 'MinimumSegmentLength': 20.0, 'GlacisHeight': 4.0, 'GlacisThickness': 10.0}



    def ExportXML(self, root):

        main = ET.SubElement(root, "StarFortress")

        ravelin = ET.SubElement(main, "Ravelin")
        ET.SubElement(ravelin, "Method").text = str(self.ravelin['Method'])
        ET.SubElement(ravelin, "BastionAngle").text = str(self.ravelin['BastionAngle'])
        ET.SubElement(ravelin, "Radius").text = str(self.ravelin['Radius'])
        ET.SubElement(ravelin, "MinimumWidth").text = str(self.ravelin['MinimumWidth'])
        ET.SubElement(ravelin, "Height").text = str(self.ravelin['Height'])

        halfmoon = ET.SubElement(main, "HalfMoon")
        ET.SubElement(halfmoon, "Active").text = str(self.halfmoon['Active'])
        ET.SubElement(halfmoon, "CircleOffset").text = str(self.halfmoon['CircleOffset'])
        ET.SubElement(halfmoon, "Length").text = str(self.halfmoon['Length'])
        ET.SubElement(halfmoon, "Height").text = str(self.halfmoon['Height'])

        covertway = ET.SubElement(main, "CovertWay")
        ET.SubElement(covertway, "Thickness").text = str(self.covertway['Thickness'])
        ET.SubElement(covertway, "Offset").text = str(self.covertway['Offset'])
        ET.SubElement(covertway, "PlaceOfArms").text = str(self.covertway['PlaceOfArms'])
        ET.SubElement(covertway, "PlaceOfArmsLength").text = str(self.covertway['PlaceOfArmsLength'])
        ET.SubElement(covertway, "MinimumSegmentLength").text = str(self.covertway['MinimumSegmentLength'])
        ET.SubElement(covertway, "GlacisThickness").text = str(self.covertway['GlacisThickness'])
        ET.SubElement(covertway, "Height").text = str(self.covertway['Height'])
        ET.SubElement(covertway, "GlacisHeight").text = str(self.covertway['GlacisHeight'])



    def ImportXML(self, root):

        main = root.find("StarFortress")
        if (not main):
            print "ERROR: Castle/StarFortress settings not found"
            return

        ravelinxml = main.find("Ravelin")
        if (ravelinxml != None):
            try:
                self.ravelin['Method'] = int(ravelinxml.find("Method").text)
                self.ravelin['BastionAngle'] = float(ravelinxml.find("BastionAngle").text)
                self.ravelin['Radius'] = float(ravelinxml.find("Radius").text)
                self.ravelin['MinimumWidth'] = float(ravelinxml.find("MinimumWidth").text)
            except:
                print "WARNING: Wrong Ravelin data in Castle/StarFortress category"

            try:
                self.ravelin['Height'] = float(ravelinxml.find("Height").text)
            except:
                pass        # Optional

        else:
            print "WARNING: Ravelin tag not found in Castle/StarFortress category"


        halfmoonxml = main.find("HalfMoon")
        if (halfmoonxml != None):
            try:
                self.halfmoon['Active'] = (halfmoonxml.find("Active").text in ['True', 'true', 'yes', 'YES', '1', 'Yes', 'TRUE'])
                self.halfmoon['CircleOffset'] = float(halfmoonxml.find("CircleOffset").text)
                self.halfmoon['Length'] = float(halfmoonxml.find("Length").text)
            except:
                print "WARNING: Wrong HalfMoon data in Castle/StarFortress category"

            try:
                self.halfmoon['Height'] = float(halfmoonxml.find("Height").text)
            except:
                pass        # Optional

        else:
            print "WARNING: HalfMoon tag not found in Castle/StarFortress category"



        covertxml = main.find("CovertWay")
        if (covertxml != None):
            try:
                self.covertway['Thickness'] = float(covertxml.find("Thickness").text)
                self.covertway['Offset'] = float(covertxml.find("Offset").text)
                self.covertway['PlaceOfArmsLength'] = float(covertxml.find("PlaceOfArmsLength").text)
                self.covertway['PlaceOfArms'] = (covertxml.find("PlaceOfArms").text in ['True', 'true', 'yes', 'YES', '1', 'Yes', 'TRUE'])
                self.covertway['MinimumSegmentLength'] = float(covertxml.find("MinimumSegmentLength").text)
                self.covertway['GlacisThickness'] = float(covertxml.find("GlacisThickness").text)
            except:
               print "WARNING: Wrong CovertWay data in Castle/StarFortress category"

            try:
                self.covertway['Height'] = float(covertxml.find("Height").text)
                self.covertway['GlacisHeight'] = float(covertxml.find("GlacisHeight").text)
            except:
                pass        # Optional

        else:
            print "WARNING: CovertWay tag not found in Castle/StarFortress category"







    def PopulateDialog(self, dlg):

        dlg.textFortressRavelinMethod.SetValue(str(self.ravelin['Method']))
        dlg.textFortressRavelinBastionAngle.SetValue(str(self.ravelin['BastionAngle']))
        dlg.textFortressRavelinRadius.SetValue(str(self.ravelin['Radius']))
        dlg.textFortressRavelinMinWidth.SetValue(str(self.ravelin['MinimumWidth']))
        dlg.textFortressRavelinHeight.SetValue(str(self.ravelin['Height']))
        dlg.checkFortressHalfmoon.SetValue(self.halfmoon['Active'])
        dlg.textFortressHalfmonnCircleRadius.SetValue(str(self.halfmoon['CircleOffset']))
        dlg.textFortressHalfmoonLength.SetValue(str(self.halfmoon['Length']))
        dlg.textFortressHalfmoonHeight.SetValue(str(self.halfmoon['Height']))
        dlg.textFortressCovertwayHeight.SetValue(str(self.covertway['Height']))
        dlg.textFortressCovertwayThickness.SetValue(str(self.covertway['Thickness']))
        dlg.textFortressCovertwayOffset.SetValue(str(self.covertway['Offset']))
        dlg.checkFortressPlaceofarms.SetValue(self.covertway['PlaceOfArms'])
        dlg.textFortressPlaceofarmsLength.SetValue(str(self.covertway['PlaceOfArmsLength']))
        dlg.textFortressCovertwayMinseglength.SetValue(str(self.covertway['MinimumSegmentLength']))
        dlg.textFortressGlacisHeight.SetValue(str(self.covertway['GlacisHeight']))
        dlg.textFortressGlacisThickness.SetValue(str(self.covertway['GlacisThickness']))


    def GetDialogData(self, dlg):

        try:
            self.ravelin['Method'] = int(dlg.textFortressRavelinMethod.GetValue())
        except:
            pass
        try:
            self.ravelin['BastionAngle'] = float(dlg.textFortressRavelinBastionAngle.GetValue())
        except:
            pass
        try:
            self.ravelin['Radius'] = float(dlg.textFortressRavelinRadius.GetValue())
        except:
            pass
        try:
            self.ravelin['MinimumWidth'] = float(dlg.textFortressRavelinMinWidth.GetValue())
        except:
            pass
        try:
            self.ravelin['Height'] = float(dlg.textFortressRavelinHeight.GetValue())
        except:
            pass
        try:
            self.halfmoon['Active'] = dlg.checkFortressHalfmoon.GetValue()
        except:
            pass
        try:
            self.halfmoon['CircleOffset'] = float(dlg.textFortressHalfmonnCircleRadius.GetValue())
        except:
            pass
        try:
            self.halfmoon['Length'] = float(dlg.textFortressHalfmoonLength.GetValue())
        except:
            pass
        try:
            self.halfmoon['Height'] = float(dlg.textFortressHalfmoonHeight.GetValue())
        except:
            pass
        try:
            self.covertway['Offset'] = float(dlg.textFortressCovertwayOffset.GetValue())
        except:
            pass
        try:
            self.covertway['PlaceOfArms'] = dlg.checkFortressPlaceofarms.GetValue()
        except:
            pass
        try:
            self.covertway['PlaceOfArmsLength'] = float(dlg.textFortressPlaceofarmsLength.GetValue())
        except:
            pass
        try:
            self.covertway['MinimumSegmentLength'] = float(dlg.textFortressCovertwayMinseglength.GetValue())
        except:
            pass
        try:
            self.covertway['GlacisHeight'] = float(dlg.textFortressGlacisHeight.GetValue())
        except:
            pass
        try:
            self.covertway['GlacisThickness'] = float(dlg.textFortressGlacisThickness.GetValue())
        except:
            pass
        try:
            self.covertway['Height'] = float(dlg.textFortressCovertwayHeight.GetValue())
        except:
            pass
        try:
            self.covertway['Thickness'] = float(dlg.textFortressCovertwayThickness.GetValue())
        except:
            pass
















class BE_DefaultBattlefieldSettings:

    def __init__(self):

        self.size = 100
        self.groundCell = {'Size': 10.0, 'Height': 0.0, 'DefenseIncrease': 0.0, 'MovimentPenalty': 1.0}
        self.trench = {'DefenseIncrease': 50000.0, 'MovementPenalty': 0.5, 'ShowOutline': False, 'RandomDeployment': 0.01, 'RandomDeploymentConsecutive': 0.7, 'RandomDeploymentMaxTries': 50}
        self.riverPenaltyMovement = 0.01



    def ExportXML(self, root):

        main = ET.SubElement(root, "Battlefield")

        ET.SubElement(main, "size").text = str(self.size)

        groundcell = ET.SubElement(main, "GroundCell")
        ET.SubElement(groundcell, "Size").text = str(self.groundCell['Size'])
        ET.SubElement(groundcell, "Height").text = str(self.groundCell['Height'])
        ET.SubElement(groundcell, "DefenseIncrease").text = str(self.groundCell['DefenseIncrease'])
        ET.SubElement(groundcell, "MovementPenalty").text = str(self.groundCell['MovimentPenalty'])

        trench = ET.SubElement(main, "Trench")
        ET.SubElement(trench, "DefenseIncrease").text = str(self.trench['DefenseIncrease'])
        ET.SubElement(trench, "MovementPenalty").text = str(self.trench['MovementPenalty'])
        ET.SubElement(trench, "ShowOutline").text = str(self.trench['ShowOutline'])
        ET.SubElement(trench, "RandomDeployment").text = str(self.trench['RandomDeployment'])
        ET.SubElement(trench, "RandomDeploymentConsecutive").text = str(self.trench['RandomDeploymentConsecutive'])
        ET.SubElement(trench, "RandomDeploymentMaxTries").text = str(self.trench['RandomDeploymentMaxTries'])

        river = ET.SubElement(main, "River")
        ET.SubElement(river, "PenaltyMovement").text = str(self.riverPenaltyMovement)



    def ImportXML(self, root):

        main = root.find("Battlefield")
        if (not main):
            print "ERROR: Battlefield settings not found"
            return

        try:
            self.size = float(main.find("size").text)
        except:
            print "WARNING: size tag not found in Battlefield settings"

        groundcellxml = main.find("GroundCell")
        if (groundcellxml != None):

            try:
                self.groundCell['Size'] = float(groundcellxml.find("Size").text)
            except:
                print "WARNING: Size tag not found in Battlefield/GroundCell settings"


            try:
                self.groundCell['Height'] = float(groundcellxml.find("Height").text)
            except:
                print "WARNING: Height tag not found in Battlefield/GroundCell settings"


            try:
                self.groundCell['DefenseIncrease'] = float(groundcellxml.find("DefenseIncrease").text)
            except:
                print "WARNING: DefenseIncrease tag not found in Battlefield/GroundCell settings"


            try:
                self.groundCell['MovimentPenalty'] = float(groundcellxml.find("MovementPenalty").text)
            except:
                print "WARNING: MovementPenalty tag not found in Battlefield/GroundCell settings"


        else:
            print "WARNING: GroundCell category not found in Battlefield settings"


        trenchxml = main.find("Trench")
        if (trenchxml != None):

            try:
                self.trench['DefenseIncrease'] = float(trenchxml.find("DefenseIncrease").text)
            except:
                print "WARNING: DefenseIncrease tag not found in Battlefield/GroundCell settings"

            try:
                self.trench['MovementPenalty'] = float(trenchxml.find("MovementPenalty").text)
            except:
                print "WARNING: MovementPenalty tag not found in Battlefield/GroundCell settings"

            try:
                self.trench['ShowOutline'] = (trenchxml.find("ShowOutline").text in ['True', 'true', 'yes', 'YES', '1', 'Yes', 'TRUE'])
            except:
                print "WARNING: ShowOutline tag not found in Battlefield/GroundCell settings"

            try:
                self.trench['RandomDeployment'] = float(trenchxml.find("RandomDeployment").text)
            except:
                print "WARNING: RandomDeployment tag not found in Battlefield/GroundCell settings"

            try:
                self.trench['RandomDeploymentConsecutive'] = float(trenchxml.find("RandomDeploymentConsecutive").text)
            except:
                print "WARNING: RandomDeploymentConsecutive tag not found in Battlefield/GroundCell settings"

            try:
                self.trench['RandomDeploymentMaxTries'] = float(trenchxml.find("RandomDeploymentMaxTries").text)
            except:
                print "WARNING: RandomDeploymentMaxTries tag not found in Battlefield/GroundCell settings"

        else:
            print "WARNING: Trench category not found in Battlefield settings"




        riverxml = main.find("River")
        if (riverxml != None):
            try:
                self.riverPenaltyMovement = float(riverxml.find("PenaltyMovement").text)
            except:
                print "WARNING: PenaltyMovement tag not foun in Battlefield/River settings"
        else:
            print "WARNING: River category not found in Battlefield settings"







    def OpenDialog(self, parent):

        dlg = BE_Dialogs.BE_DefaultBattlefieldSettingsDlg.BE_DefaultBattlefieldSettingsDlg(parent)

        dlg.textSize.SetValue(str(self.size))
        dlg.textGroundcellSize.SetValue(str(self.groundCell['Size']))
        dlg.textGroundcellHeight.SetValue(str(self.groundCell['Height']))
        dlg.textGroundcellDefenseIncrease.SetValue(str(self.groundCell['DefenseIncrease']))
        dlg.textGroundcellPenaltyMovement.SetValue(str(self.groundCell['MovimentPenalty']))
        dlg.textTrenchDefenseIncrease.SetValue(str(self.trench['DefenseIncrease']))
        dlg.textTrenchPenaltyMovement.SetValue(str(self.trench['MovementPenalty']))
        dlg.checkTrenchShowoutline.SetValue(self.trench['ShowOutline'])
        dlg.textTrenchRandomDeployment.SetValue(str(self.trench['RandomDeployment']))
        dlg.textTrenchRandomDeploymentConsecutive.SetValue(str(self.trench['RandomDeploymentConsecutive']))
        dlg.textTrenchRandomDeploymentMaxTries.SetValue(str(self.trench['RandomDeploymentMaxTries']))
        dlg.textRiverPenalty.SetValue(str(self.riverPenaltyMovement))

        if (dlg.ShowModal() == wx.ID_OK):

            try:
                self.size = float(dlg.textSize.GetValue())
            except:
                pass
            try:
                self.groundCell['Size'] = float(dlg.textGroundcellSize.GetValue())
            except:
                pass
            try:
                self.groundCell['Height'] = float(dlg.textGroundcellHeight.GetValue())
            except:
                pass
            try:
                self.groundCell['DefenseIncrease'] = float(dlg.textGroundcellDefenseIncrease.GetValue())
            except:
                pass
            try:
                self.groundCell['MovimentPenalty'] = float(dlg.textGroundcellPenaltyMovement.GetValue())
            except:
                pass
            try:
                self.trench['DefenseIncrease'] = float(dlg.textTrenchDefenseIncrease.GetValue())
            except:
                pass
            try:
                self.trench['MovementPenalty'] = float(dlg.textTrenchPenaltyMovement.GetValue())
            except:
                pass
            try:
                self.trench['ShowOutline'] = dlg.checkTrenchShowoutline.GetValue()
            except:
                pass
            try:
                self.trench['RandomDeployment'] = float(dlg.textTrenchRandomDeployment.GetValue())
            except:
                pass
            try:
                self.trench['RandomDeploymentConsecutive'] = float(dlg.textTrenchRandomDeploymentConsecutive.GetValue())
            except:
                pass
            try:
                self.trench['RandomDeploymentMaxTries'] = float(dlg.textTrenchRandomDeploymentMaxTries.GetValue())
            except:
                pass
            try:
                self.riverPenaltyMovement = float(dlg.textRiverPenalty.GetValue())
            except:
                pass



        dlg.Destroy()







class BE_DefaultArmySettings:

    def __init__(self):

        self.infantry = BE_DefaultArmyInfantrySettings()
        self.archers = BE_DefaultArmyArchersSettings()
        self.cannons = BE_DefaultArmyCannonsSettings()
        self.siegetowers = BE_DefaultArmySiegeTowersSettings()
        self.throwers = BE_DefaultArmyThrowersSettings()

        self.humanFOV = 120.0
        self.showOutline = False
        self.showLabels = False


    def ExportXML(self, root):

        main = ET.SubElement(root, "Army")

        self.infantry.ExportXML(main)
        self.archers.ExportXML(main)
        self.cannons.ExportXML(main)
        self.siegetowers.ExportXML(main)
        self.throwers.ExportXML(main)


        ET.SubElement(main, "HumanFieldOfView").text = str(self.humanFOV)
        ET.SubElement(main, "ShowLabels").text = str(self.showLabels)
        ET.SubElement(main, "ShowOutline").text = str(self.showOutline)



    def ImportXML(self, root):

        main = root.find("Army")
        if (not main):
            print "ERROR: Army settings not found"
            return

        try:
            self.humanFOV = float(main.find("HumanFieldOfView").text)
        except:
            print "WARNING: HumanFieldOfView tag not found in Army category"

        try:
            self.showLabels = (main.find("ShowLabels").text in ['True', 'true', 'yes', 'YES', '1', 'Yes', 'TRUE'])
        except:
            print "WARNING: HumanFieldOfView tag not found in Army category"

        try:
            self.showOutline = (main.find("ShowOutline").text in ['True', 'true', 'yes', 'YES', '1', 'Yes', 'TRUE'])
        except:
            print "WARNING: HumanFieldOfView tag not found in Army category"


        self.infantry.ImportXML(main)
        self.archers.ImportXML(main)
        self.cannons.ImportXML(main)
        self.siegetowers.ImportXML(main)
        self.throwers.ImportXML(main)








    def OpenDialog(self, parent):

        dlg = BE_Dialogs.BE_DefaultArmySettingsDlg.BE_DefaultArmySettingsDlg(parent)

        self.infantry.PopulateDialog(dlg)
        self.archers.PopulateDialog(dlg)
        self.cannons.PopulateDialog(dlg)
        self.siegetowers.PopulateDialog(dlg)
        self.throwers.PopulateDialog(dlg)

        dlg.textMiscHumanFOV.SetValue(str(self.humanFOV))
        dlg.checkMiscShowOutline.SetValue(self.showOutline)
        dlg.checkMiscLabels.SetValue(self.showLabels)


        if (dlg.ShowModal() == wx.ID_OK):

            self.infantry.GetDialogData(dlg)
            self.archers.GetDialogData(dlg)
            self.cannons.GetDialogData(dlg)
            self.siegetowers.GetDialogData(dlg)
            self.throwers.GetDialogData(dlg)

            try:
                self.humanFOV = float(dlg.textMiscHumanFOV.GetValue())
            except:
                pass
            try:
                self.showOutline = dlg.checkMiscShowOutline.GetValue()
            except:
                pass
            try:
                self.showLabels = dlg.checkMiscLabels.GetValue()
            except:
                pass



        dlg.Destroy()






class BE_DefaultArmyInfantrySettings:

    def __init__(self):

        self.defense = 40
        self.attack = 0
        self.speed = 10
        self.reload = 1
        self.accuracy = 0
        self.distance = 2.0
        self.boundingLength = 2.0
        self.boundingHeight = 2.0
        self.boundingWidth = 2.0
        self.climbSpeed = 1.0
        self.stationary = False
        self.movementPriority = 1
        self.movementPriorityClimbing = 50
        self.rubbleClimbSpeed = 1.5
        self.searchRadiusGoToRubble = 7.0


    def ExportXML(self, root):

        main = ET.SubElement(root, "Infantry")

        ET.SubElement(main, "Defense").text = str(self.defense)
        ET.SubElement(main, "Attack").text = str(self.attack)
        ET.SubElement(main, "Speed").text = str(self.speed)
        ET.SubElement(main, "Reload").text = str(self.reload)
        ET.SubElement(main, "Accuracy").text = str(self.accuracy)
        ET.SubElement(main, "Distance").text = str(self.distance)
        ET.SubElement(main, "ClimbSpeed").text = str(self.climbSpeed)
        ET.SubElement(main, "Stationary").text = str(self.stationary)
        ET.SubElement(main, "MovementPriority").text = str(self.movementPriority)
        ET.SubElement(main, "MovementPriorityWaitingClimbing").text = str(self.movementPriorityClimbing)
        ET.SubElement(main, "RubbleClimbSpeed").text = str(self.rubbleClimbSpeed)
        ET.SubElement(main, "SearchRadiusGoToRumble").text = str(self.searchRadiusGoToRubble)

        bounding = ET.SubElement(main, "Bounding")
        ET.SubElement(bounding, "Length").text = str(self.boundingLength)
        ET.SubElement(bounding, "Height").text = str(self.boundingHeight)
        ET.SubElement(bounding, "Width").text = str(self.boundingWidth)




    def ImportXML(self, root):

        main = root.find("Infantry")
        if (not main):
            print "ERROR: Army/Infantry settings not found"
            return

        try:
            self.defense = float(main.find("Defense").text)
        except:
            print "WARNING: Defense tag not found in Army/Infantry category"

        try:
            self.attack = float(main.find("Attack").text)
        except:
            print "WARNING: Attack tag not found in Army/Infantry category"

        try:
            self.speed = float(main.find("Speed").text)
        except:
            print "WARNING: Speed tag not found in Army/Infantry category"

        try:
            self.reload = float(main.find("Reload").text)
        except:
            print "WARNING: Reload tag not found in Army/Infantry category"

        try:
            self.accuracy = float(main.find("Accuracy").text)
        except:
            print "WARNING: Accuracy tag not found in Army/Infantry category"

        try:
            self.distance = float(main.find("Distance").text)
        except:
            print "WARNING: Distance tag not found in Army/Infantry category"

        try:
            self.climbSpeed = float(main.find("ClimbSpeed").text)
        except:
            print "WARNING: ClimbSpeed tag not found in Army/Infantry category"

        try:
            self.stationary = (main.find("Stationary").text in ['True', 'true', 'yes', 'YES', '1', 'Yes', 'TRUE'])
        except:
            print "WARNING: Stationary tag not found in Army/Infantry category"

        try:
            self.movementPriority = float(main.find("MovementPriority").text)
        except:
            print "WARNING: MovementPriority tag not found in Army/Infantry category"

        try:
            self.movementPriorityClimbing = float(main.find("MovementPriorityWaitingClimbing").text)
        except:
            print "WARNING: MovementPriorityWaitingClimbing tag not found in Army/Infantry category"

        try:
            self.rubbleClimbSpeed = float(main.find("RubbleClimbSpeed").text)
        except:
            print "WARNING: RubbleClimbSpeed tag not found in Army/Infantry category"

        try:
            self.searchRadiusGoToRubble = float(main.find("SearchRadiusGoToRumble").text)
        except:
            print "WARNING: SearchRadiusGoToRumble tag not found in Army/Infantry category"

        boundxml = main.find("Bounding")
        if (boundxml != None):
            try:
                self.boundingLength = float(boundxml.find("Length").text)
                self.boundingHeight = float(boundxml.find("Height").text)
                self.boundingWidth = float(boundxml.find("Width").text)
            except:
                print "WARNING: Wrong Bounding data in Army/Infantry category"
        else:
            print "WARNING: Bounding tag not found in Army/Infantry category"







    def PopulateDialog(self, dlg):

        dlg.textInfantryDefense.SetValue(str(self.defense))
        dlg.textInfantryAttack.SetValue(str(self.attack))
        dlg.textInfantrySpeed.SetValue(str(self.speed))
        dlg.textInfantryReload.SetValue(str(self.reload))
        dlg.textInfantryAccuracy.SetValue(str(self.accuracy))
        dlg.textInfantryDistance.SetValue(str(self.distance))
        dlg.textInfantryBoundingLength.SetValue(str(self.boundingLength))
        dlg.textInfantryBoundingHeight.SetValue(str(self.boundingHeight))
        dlg.textInfantryBoundingWidth.SetValue(str(self.boundingWidth))
        dlg.textInfantryClimbingSpeed.SetValue(str(self.climbSpeed))
        dlg.textInfantryMovementPriority.SetValue(str(self.movementPriority))
        dlg.textInfantryMovementPriorityClimbing.SetValue(str(self.movementPriorityClimbing))
        dlg.textInfantryRubbleClimbingSpeed.SetValue(str(self.rubbleClimbSpeed))
        dlg.textInfantrySearchRadiusRubble.SetValue(str(self.searchRadiusGoToRubble))
        dlg.checkInfantryStationary.SetValue(self.stationary)


    def GetDialogData(self, dlg):

        try:
            self.defense = float(dlg.textInfantryDefense.GetValue())
        except:
            pass
        try:
            self.attack = float(dlg.textInfantryAttack.GetValue())
        except:
            pass
        try:
            self.speed = float(dlg.textInfantrySpeed.GetValue())
        except:
            pass
        try:
            self.reload = float(dlg.textInfantryReload.GetValue())
        except:
            pass
        try:
            self.accuracy = float(dlg.textInfantryAccuracy.GetValue())
        except:
            pass
        try:
            self.distance = float(dlg.textInfantryDistance.GetValue())
        except:
            pass
        try:
            self.boundingLength = float(dlg.textInfantryBoundingLength.GetValue())
        except:
            pass
        try:
            self.boundingHeight = float(dlg.textInfantryBoundingHeight.GetValue())
        except:
            pass
        try:
            self.boundingWidth = float(dlg.textInfantryBoundingWidth.GetValue())
        except:
            pass
        try:
            self.climbSpeed = float(dlg.textInfantryClimbingSpeed.GetValue())
        except:
            pass
        try:
            self.movementPriority = float(dlg.textInfantryMovementPriority.GetValue())
        except:
            pass
        try:
            self.movementPriorityClimbing = float(dlg.textInfantryMovementPriorityClimbing.GetValue())
        except:
            pass
        try:
            self.rubbleClimbSpeed = float(dlg.textInfantryRubbleClimbingSpeed.GetValue())
        except:
            pass
        try:
            self.searchRadiusGoToRubble = float(dlg.textInfantrySearchRadiusRubble.GetValue())
        except:
            pass
        try:
            self.stationary = dlg.checkInfantryStationary.GetValue()
        except:
            pass



class BE_DefaultArmyArchersSettings:

    def __init__(self):

        self.defense = 0
        self.attack = 20
        self.speed = 10
        self.reload = 2
        self.accuracy = 75
        self.distance = 100.0
        self.boundingLength = 2.0
        self.boundingHeight = 2.0
        self.boundingWidth = 2.0
        self.stationary = True
        self.movementPriority = 0
        self.defenseShootDoubleCheck = False
        self.shootsToStay = 0.2
        self.searchRadiusTrench = 100.0
        self.defendersMarginSpace = 1.0


    def ExportXML(self, root):

        main = ET.SubElement(root, "Archers")

        ET.SubElement(main, "Defense").text = str(self.defense)
        ET.SubElement(main, "Attack").text = str(self.attack)
        ET.SubElement(main, "Speed").text = str(self.speed)
        ET.SubElement(main, "Reload").text = str(self.reload)
        ET.SubElement(main, "Accuracy").text = str(self.accuracy)
        ET.SubElement(main, "Distance").text = str(self.distance)
        ET.SubElement(main, "Stationary").text = str(self.stationary)
        ET.SubElement(main, "MovementPriority").text = str(self.movementPriority)
        ET.SubElement(main, "DefenseShootDoubleCheck").text = str(self.defenseShootDoubleCheck)
        ET.SubElement(main, "ShootsToStay").text = str(self.shootsToStay)
        ET.SubElement(main, "SearchRadiusTrench").text = str(self.searchRadiusTrench)
        ET.SubElement(main, "DefendersMarginSpace").text = str(self.defendersMarginSpace)

        bounding = ET.SubElement(main, "Bounding")
        ET.SubElement(bounding, "Length").text = str(self.boundingLength)
        ET.SubElement(bounding, "Height").text = str(self.boundingHeight)
        ET.SubElement(bounding, "Width").text = str(self.boundingWidth)




    def ImportXML(self, root):

        main = root.find("Archers")
        if (not main):
            print "ERROR: Army/Archers settings not found"
            return

        try:
            self.defense = float(main.find("Defense").text)
        except:
            print "WARNING: Defense tag not found in Army/Archers category"

        try:
            self.attack = float(main.find("Attack").text)
        except:
            print "WARNING: Attack tag not found in Army/Archers category"

        try:
            self.speed = float(main.find("Speed").text)
        except:
            print "WARNING: Speed tag not found in Army/Archers category"

        try:
            self.reload = float(main.find("Reload").text)
        except:
            print "WARNING: Reload tag not found in Army/Archers category"

        try:
            self.accuracy = float(main.find("Accuracy").text)
        except:
            print "WARNING: Accuracy tag not found in Army/Archers category"

        try:
            self.distance = float(main.find("Distance").text)
        except:
            print "WARNING: Distance tag not found in Army/Archers category"

        try:
            self.stationary = (main.find("Stationary").text in ['True', 'true', 'yes', 'YES', '1', 'Yes', 'TRUE'])
        except:
            print "WARNING: Stationary tag not found in Army/Archers category"

        try:
            self.movementPriority = float(main.find("MovementPriority").text)
        except:
            print "WARNING: MovementPriority tag not found in Army/Archers category"

        try:
            self.defenseShootDoubleCheck = (main.find("DefenseShootDoubleCheck").text in ['True', 'true', 'yes', 'YES', '1', 'Yes', 'TRUE'])
        except:
            print "WARNING: DefenseShootDoubleCheck tag not found in Army/Archers category"

        try:
            self.shootsToStay = float(main.find("ShootsToStay").text)
        except:
            print "WARNING: ShootsToStay tag not found in Army/Archers category"

        try:
            self.searchRadiusTrench = float(main.find("SearchRadiusTrench").text)
        except:
            print "WARNING: SearchRadiusTrench tag not found in Army/Archers category"

        try:
            self.defendersMarginSpace = float(main.find("DefendersMarginSpace").text)
        except:
            print "WARNING: DefendersMarginSpace tag not found in Army/Archers category"



        boundxml = main.find("Bounding")
        if (boundxml != None):
            try:
                self.boundingLength = float(boundxml.find("Length").text)
                self.boundingHeight = float(boundxml.find("Height").text)
                self.boundingWidth = float(boundxml.find("Width").text)
            except:
                print "WARNING: Wrong Bounding data in Army/Archers category"
        else:
            print "WARNING: Bounding tag not found in Army/Archers category"









    def PopulateDialog(self, dlg):

        dlg.textArchersDefense.SetValue(str(self.defense))
        dlg.textArchersAttack.SetValue(str(self.attack))
        dlg.textArchersSpeed.SetValue(str(self.speed))
        dlg.textArchersReload.SetValue(str(self.reload))
        dlg.textArchersAccuracy.SetValue(str(self.accuracy))
        dlg.textArchersDistance.SetValue(str(self.distance))
        dlg.textArchersBoundingLength.SetValue(str(self.boundingLength))
        dlg.textArchersBoundingHeight.SetValue(str(self.boundingHeight))
        dlg.textArchersBoudingWidth.SetValue(str(self.boundingWidth))
        dlg.textArchersMovementPriority.SetValue(str(self.movementPriority))
        dlg.checkArchersStationary.SetValue(self.stationary)
        dlg.checkArchersDoubleCheck.SetValue(self.defenseShootDoubleCheck)
        dlg.textArchersShootsToStay.SetValue(str(self.shootsToStay))
        dlg.textArchersTrenchSearchRadius.SetValue(str(self.searchRadiusTrench))
        dlg.textArchersMarginSpace.SetValue(str(self.defendersMarginSpace))

    def GetDialogData(self, dlg):

        try:
            self.defense = float(dlg.textArchersDefense.GetValue())
        except:
            pass
        try:
            self.attack = float(dlg.textArchersAttack.GetValue())
        except:
            pass
        try:
            self.speed = float(dlg.textArchersSpeed.GetValue())
        except:
            pass
        try:
            self.reload = float(dlg.textArchersReload.GetValue())
        except:
            pass
        try:
            self.accuracy = float(dlg.textArchersAccuracy.GetValue())
        except:
            pass
        try:
            self.distance = float(dlg.textArchersDistance.GetValue())
        except:
            pass
        try:
            self.boundingLength = float(dlg.textArchersBoundingLength.GetValue())
        except:
            pass
        try:
            self.boundingHeight = float(dlg.textArchersBoundingHeight.GetValue())
        except:
            pass
        try:
            self.boundingWidth = float(dlg.textArchersBoudingWidth.GetValue())
        except:
            pass
        try:
            self.movementPriority = float(dlg.textArchersMovementPriority.GetValue())
        except:
            pass
        try:
            self.stationary = dlg.checkArchersStationary.GetValue()
        except:
            pass
        try:
            self.defenseShootDoubleCheck = dlg.checkArchersDoubleCheck.GetValue()
        except:
            pass
        try:
            self.shootsToStay = float(dlg.textArchersShootsToStay.GetValue())
        except:
            pass
        try:
            self.searchRadiusTrench = float(dlg.textArchersTrenchSearchRadius.GetValue())
        except:
            pass
        try:
            self.defendersMarginSpace = float(dlg.textArchersShootsToStay.GetValue())
        except:
            pass




class BE_DefaultArmyCannonsSettings:

    def __init__(self):

        self.defense = 120000
        self.attack = 30000
        self.speed = 0
        self.reload = 5
        self.accuracy = 75
        self.distance = 600.0
        self.boundingLength = 7.0
        self.boundingHeight = 1.0
        self.boundingWidth = 7.0
        self.stationary = True
        self.movementPriority = 100
        self.defenseShootDoubleCheck = False
        self.shootAngleHorizontal = 60.0
        self.shootAngleVertical1 = 45.0
        self.shootAngleVertical2 = 90.0
        self.ballRadius = 3.0
        self.defaultPlacementDistance = 0.6



    def ExportXML(self, root):

        main = ET.SubElement(root, "Cannons")

        ET.SubElement(main, "Defense").text = str(self.defense)
        ET.SubElement(main, "Attack").text = str(self.attack)
        ET.SubElement(main, "Speed").text = str(self.speed)
        ET.SubElement(main, "Reload").text = str(self.reload)
        ET.SubElement(main, "Accuracy").text = str(self.accuracy)
        ET.SubElement(main, "Distance").text = str(self.distance)
        ET.SubElement(main, "Stationary").text = str(self.stationary)
        ET.SubElement(main, "MovementPriority").text = str(self.movementPriority)
        ET.SubElement(main, "DefenseShootDoubleCheck").text = str(self.defenseShootDoubleCheck)
        ET.SubElement(main, "BallRadius").text = str(self.ballRadius)
        ET.SubElement(main, "DefaultPlacementDistance").text = str(self.defaultPlacementDistance)

        shootangle = ET.SubElement(main, "ShootAngle")
        ET.SubElement(shootangle, "H").text = str(self.shootAngleHorizontal)
        ET.SubElement(shootangle, "V").text = "[" + str(self.shootAngleVertical1) + "," + str(self.shootAngleVertical2) + "]"

        bounding = ET.SubElement(main, "Bounding")
        ET.SubElement(bounding, "Length").text = str(self.boundingLength)
        ET.SubElement(bounding, "Height").text = str(self.boundingHeight)
        ET.SubElement(bounding, "Width").text = str(self.boundingWidth)




    def ImportXML(self, root):

        main = root.find("Cannons")
        if (not main):
            print "ERROR: Army/Cannons settings not found"
            return

        try:
            self.defense = float(main.find("Defense").text)
        except:
            print "WARNING: Defense tag not found in Army/Cannons category"

        try:
            self.attack = float(main.find("Attack").text)
        except:
            print "WARNING: Attack tag not found in Army/Cannons category"

        try:
            self.speed = float(main.find("Speed").text)
        except:
            print "WARNING: Speed tag not found in Army/Cannons category"

        try:
            self.reload = float(main.find("Reload").text)
        except:
            print "WARNING: Reload tag not found in Army/Cannons category"

        try:
            self.accuracy = float(main.find("Accuracy").text)
        except:
            print "WARNING: Accuracy tag not found in Army/Cannons category"

        try:
            self.distance = float(main.find("Distance").text)
        except:
            print "WARNING: Distance tag not found in Army/Cannons category"

        try:
            self.stationary = (main.find("Stationary").text in ['True', 'true', 'yes', 'YES', '1', 'Yes', 'TRUE'])
        except:
            print "WARNING: Stationary tag not found in Army/Cannons category"

        try:
            self.movementPriority = float(main.find("MovementPriority").text)
        except:
            print "WARNING: MovementPriority tag not found in Army/Cannons category"

        try:
            self.defenseShootDoubleCheck = (main.find("DefenseShootDoubleCheck").text in ['True', 'true', 'yes', 'YES', '1', 'Yes', 'TRUE'])
        except:
            print "WARNING: DefenseShootDoubleCheck tag not found in Army/Cannons category"

        try:
            self.ballRadius = float(main.find("BallRadius").text)
        except:
            print "WARNING: BallRadius tag not found in Army/Cannons category"

        try:
            self.defaultPlacementDistance = float(main.find("DefaultPlacementDistance").text)
        except:
            print "WARNING: DefaultPlacementDistance tag not found in Army/Cannons category"


        shootxml = main.find("ShootAngle")
        if (shootxml != None):
            try:
                self.shootAngleHorizontal = float(shootxml.find("H").text)
                arr = ast.literal_eval(shootxml.find("V").text)
                self.shootAngleVertical1 = float(arr[0])
                self.shootAngleVertical2 = float(arr[1])

            except:
                print "WARNING: Wrong ShootAngle data in Army/Cannons category"
        else:
            print "WARNING: ShootAngle tag not found in Army/Cannons category"


        boundxml = main.find("Bounding")
        if (boundxml != None):
            try:
                self.boundingLength = float(boundxml.find("Length").text)
                self.boundingHeight = float(boundxml.find("Height").text)
                self.boundingWidth = float(boundxml.find("Width").text)
            except:
                print "WARNING: Wrong Bounding data in Army/Cannons category"
        else:
            print "WARNING: Bounding tag not found in Army/Cannons category"










    def PopulateDialog(self, dlg):

        dlg.textCannonsDefense.SetValue(str(self.defense))
        dlg.textCannonsAttack.SetValue(str(self.attack))
        dlg.textCannonsSpeed.SetValue(str(self.speed))
        dlg.textCannonsReload.SetValue(str(self.reload))
        dlg.textCannonsAccuracy.SetValue(str(self.accuracy))
        dlg.textCannonsDistance.SetValue(str(self.distance))
        dlg.textCannonsBoundingLength.SetValue(str(self.boundingLength))
        dlg.textCannonsBoundingHeight.SetValue(str(self.boundingHeight))
        dlg.textCannonsBoundingWidth.SetValue(str(self.boundingWidth))
        dlg.textCannonsMovementPriority.SetValue(str(self.movementPriority))
        dlg.checkCannonsStationary.SetValue(self.stationary)
        dlg.checkCannonsDoubleCheck.SetValue(self.defenseShootDoubleCheck)
        dlg.textCannonsShootHorizontal.SetValue(str(self.shootAngleHorizontal))
        dlg.textCannonsShootVertical1.SetValue(str(self.shootAngleVertical1))
        dlg.textCannonsShootVertical2.SetValue(str(self.shootAngleVertical2))
        dlg.textCannonsBall.SetValue(str(self.ballRadius))
        dlg.textCannonsPlacementDistance.SetValue(str(self.defaultPlacementDistance))

    def GetDialogData(self, dlg):

        try:
            self.defense = float(dlg.textCannonsDefense.GetValue())
        except:
            pass
        try:
            self.attack = float(dlg.textCannonsAttack.GetValue())
        except:
            pass
        try:
            self.speed = float(dlg.textCannonsSpeed.GetValue())
        except:
            pass
        try:
            self.reload = float(dlg.textCannonsReload.GetValue())
        except:
            pass
        try:
            self.accuracy = float(dlg.textCannonsAccuracy.GetValue())
        except:
            pass
        try:
            self.distance = float(dlg.textCannonsDistance.GetValue())
        except:
            pass
        try:
            self.boundingLength = float(dlg.textCannonsBoundingLength.GetValue())
        except:
            pass
        try:
            self.boundingHeight = float(dlg.textCannonsBoundingHeight.GetValue())
        except:
            pass
        try:
            self.boundingWidth = float(dlg.textCannonsBoudingWidth.GetValue())
        except:
            pass
        try:
            self.movementPriority = float(dlg.textCannonsMovementPriority.GetValue())
        except:
            pass
        try:
            self.stationary = dlg.checkCannonsStationary.GetValue()
        except:
            pass
        try:
            self.defenseShootDoubleCheck = dlg.checkCannonsDoubleCheck.GetValue()
        except:
            pass
        try:
            self.shootAngleHorizontal = float(dlg.textCannonsShootHorizontal.GetValue())
        except:
            pass
        try:
            self.shootAngleVertical1 = float(dlg.textCannonsShootVertical1.GetValue())
        except:
            pass
        try:
            self.shootAngleVertical2 = float(dlg.textCannonsShootVertical2.GetValue())
        except:
            pass
        try:
            self.ballRadius = float(dlg.textCannonsBall.GetValue())
        except:
            pass
        try:
            self.defaultPlacementDistance = float(dlg.textCannonsPlacementDistance.GetValue())
        except:
            pass





class BE_DefaultArmySiegeTowersSettings:

    def __init__(self):

        self.defense = 5000
        self.attack = 20
        self.speed = 7
        self.reload = 1
        self.accuracy = 75
        self.distance = 100.0
        self.boundingLength = 5.0
        self.boundingHeight = 0.0
        self.boundingWidth = 10.0
        self.stationary = False
        self.movementPriority = 5
        self.levelHeight = 2.0
        self.constructionTimePerLevel = 1
        self.turtleDefense = 400
        self.covertMoatSpeed = 0.02


    def ExportXML(self, root):

        main = ET.SubElement(root, "SiegeTowers")

        ET.SubElement(main, "Defense").text = str(self.defense)
        ET.SubElement(main, "Attack").text = str(self.attack)
        ET.SubElement(main, "Speed").text = str(self.speed)
        ET.SubElement(main, "Reload").text = str(self.reload)
        ET.SubElement(main, "Accuracy").text = str(self.accuracy)
        ET.SubElement(main, "Distance").text = str(self.distance)
        ET.SubElement(main, "Stationary").text = str(self.stationary)
        ET.SubElement(main, "MovementPriority").text = str(self.movementPriority)
        ET.SubElement(main, "LevelHeight").text = str(self.levelHeight)
        ET.SubElement(main, "ConstructionTimePerLevel").text = str(self.constructionTimePerLevel)
        ET.SubElement(main, "TurtleDefense").text = str(self.turtleDefense)
        ET.SubElement(main, "CoverMoatSpeed").text = str(self.covertMoatSpeed)


        bounding = ET.SubElement(main, "Bounding")
        ET.SubElement(bounding, "Length").text = str(self.boundingLength)
        ET.SubElement(bounding, "Height").text = str(self.boundingHeight)
        ET.SubElement(bounding, "Width").text = str(self.boundingWidth)




    def ImportXML(self, root):

        main = root.find("SiegeTowers")
        if (not main):
            print "ERROR: Army/SiegeTowers settings not found"
            return

        try:
            self.defense = float(main.find("Defense").text)
        except:
            print "WARNING: Defense tag not found in Army/SiegeTowers category"

        try:
            self.attack = float(main.find("Attack").text)
        except:
            print "WARNING: Attack tag not found in Army/SiegeTowers category"

        try:
            self.speed = float(main.find("Speed").text)
        except:
            print "WARNING: Speed tag not found in Army/SiegeTowers category"

        try:
            self.reload = float(main.find("Reload").text)
        except:
            print "WARNING: Reload tag not found in Army/SiegeTowers category"

        try:
            self.accuracy = float(main.find("Accuracy").text)
        except:
            print "WARNING: Accuracy tag not found in Army/SiegeTowers category"

        try:
            self.distance = float(main.find("Distance").text)
        except:
            print "WARNING: Distance tag not found in Army/SiegeTowers category"

        try:
            self.stationary = (main.find("Stationary").text in ['True', 'true', 'yes', 'YES', '1', 'Yes', 'TRUE'])
        except:
            print "WARNING: Stationary tag not found in Army/SiegeTowers category"

        try:
            self.movementPriority = float(main.find("MovementPriority").text)
        except:
            print "WARNING: MovementPriority tag not found in Army/SiegeTowers category"

        try:
            self.levelHeight = float(main.find("LevelHeight").text)
        except:
            print "WARNING: LevelHeight tag not found in Army/SiegeTowers category"

        try:
            self.constructionTimePerLevel = float(main.find("ConstructionTimePerLevel").text)
        except:
            print "WARNING: ConstructionTimePerLevel tag not found in Army/SiegeTowers category"

        try:
            self.turtleDefense = float(main.find("TurtleDefense").text)
        except:
            print "WARNING: TurtleDefense tag not found in Army/SiegeTowers category"

        try:
            self.covertMoatSpeed = float(main.find("CoverMoatSpeed").text)
        except:
            print "WARNING: CoverMoatSpeed tag not found in Army/SiegeTowers category"



        boundxml = main.find("Bounding")
        if (boundxml != None):
            try:
                self.boundingLength = float(boundxml.find("Length").text)
                self.boundingHeight = float(boundxml.find("Height").text)
                self.boundingWidth = float(boundxml.find("Width").text)
            except:
                print "WARNING: Wrong Bounding data in Army/SiegeTowers category"
        else:
            print "WARNING: Bounding tag not found in Army/SiegeTowers category"





    def PopulateDialog(self, dlg):

        dlg.textSiegeDefense.SetValue(str(self.defense))
        dlg.textSiegeAttack.SetValue(str(self.attack))
        dlg.textSiegeSpeed.SetValue(str(self.speed))
        dlg.textSiegeReload.SetValue(str(self.reload))
        dlg.textSiegeAccuracy.SetValue(str(self.accuracy))
        dlg.textSiegeDistance.SetValue(str(self.distance))
        dlg.textSiegeBoundingLength.SetValue(str(self.boundingLength))
        dlg.textSiegeBoundingHeight.SetValue(str(self.boundingHeight))
        dlg.textSiegeBoundingWidth.SetValue(str(self.boundingWidth))
        dlg.textSiegeMovementPriority.SetValue(str(self.movementPriority))
        dlg.checkSiegeStationary.SetValue(self.stationary)
        dlg.textSiegeLevelheight.SetValue(str(self.levelHeight))
        dlg.textSiegeConstructiontime.SetValue(str(self.constructionTimePerLevel))
        dlg.textSiegeTurtledefense.SetValue(str(self.turtleDefense))
        dlg.textSiegeCovermoatspeed.SetValue(str(self.turtleDefense))


    def GetDialogData(self, dlg):

        try:
            self.defense = float(dlg.textSiegeDefense.GetValue())
        except:
            pass
        try:
            self.attack = float(dlg.textSiegeAttack.GetValue())
        except:
            pass
        try:
            self.speed = float(dlg.textSiegeSpeed.GetValue())
        except:
            pass
        try:
            self.reload = float(dlg.textSiegeReload.GetValue())
        except:
            pass
        try:
            self.accuracy = float(dlg.textSiegeAccuracy.GetValue())
        except:
            pass
        try:
            self.distance = float(dlg.textSiegeDistance.GetValue())
        except:
            pass
        try:
            self.boundingLength = float(dlg.textSiegeBoundingLength.GetValue())
        except:
            pass
        try:
            self.boundingHeight = float(dlg.textSiegeBoundingHeight.GetValue())
        except:
            pass
        try:
            self.boundingWidth = float(dlg.textSiegeBoudingWidth.GetValue())
        except:
            pass
        try:
            self.movementPriority = float(dlg.textSiegeMovementPriority.GetValue())
        except:
            pass
        try:
            self.stationary = dlg.checkSiegeStationary.GetValue()
        except:
            pass
        try:
            self.levelHeight = float(dlg.textSiegeLevelheight.GetValue())
        except:
            pass
        try:
            self.constructionTimePerLevel = float(dlg.textSiegeConstructiontime.GetValue())
        except:
            pass
        try:
            self.turtleDefense = float(dlg.textSiegeTurtledefense.GetValue())
        except:
            pass
        try:
            self.turtleDefense = float(dlg.textSiegeCovermoatspeed.GetValue())
        except:
            pass








class BE_DefaultArmyThrowersSettings:

    def __init__(self):

        self.defense = 0
        self.attack = 200
        self.speed = 0
        self.reload = 15
        self.accuracy = 95
        self.distance = 0.5
        self.boundingLength = 0
        self.boundingHeight = 2.0
        self.boundingWidth = 0.0
        self.stationary = True
        self.movementPriority = 0
        self.battalionMaxSize = 3


    def ExportXML(self, root):

        main = ET.SubElement(root, "Throwers")

        ET.SubElement(main, "Defense").text = str(self.defense)
        ET.SubElement(main, "Attack").text = str(self.attack)
        ET.SubElement(main, "Speed").text = str(self.speed)
        ET.SubElement(main, "Reload").text = str(self.reload)
        ET.SubElement(main, "Accuracy").text = str(self.accuracy)
        ET.SubElement(main, "Distance").text = str(self.distance)
        ET.SubElement(main, "Stationary").text = str(self.stationary)
        ET.SubElement(main, "MovementPriority").text = str(self.movementPriority)
        ET.SubElement(main, "BattalionMaxSize").text = str(self.battalionMaxSize)


        bounding = ET.SubElement(main, "Bounding")
        ET.SubElement(bounding, "Length").text = str(self.boundingLength)
        ET.SubElement(bounding, "Height").text = str(self.boundingHeight)
        ET.SubElement(bounding, "Width").text = str(self.boundingWidth)





    def ImportXML(self, root):

        main = root.find("Throwers")
        if (not main):
            print "ERROR: Army/Throwers settings not found"
            return

        try:
            self.defense = float(main.find("Defense").text)
        except:
            print "WARNING: Defense tag not found in Army/Throwers category"

        try:
            self.attack = float(main.find("Attack").text)
        except:
            print "WARNING: Attack tag not found in Army/Throwers category"

        try:
            self.speed = float(main.find("Speed").text)
        except:
            print "WARNING: Speed tag not found in Army/Throwers category"

        try:
            self.reload = float(main.find("Reload").text)
        except:
            print "WARNING: Reload tag not found in Army/Throwers category"

        try:
            self.accuracy = float(main.find("Accuracy").text)
        except:
            print "WARNING: Accuracy tag not found in Army/Throwers category"

        try:
            self.distance = float(main.find("Distance").text)
        except:
            print "WARNING: Distance tag not found in Army/Throwers category"

        try:
            self.stationary = (main.find("Stationary").text in ['True', 'true', 'yes', 'YES', '1', 'Yes', 'TRUE'])
        except:
            print "WARNING: Stationary tag not found in Army/Throwers category"

        try:
            self.movementPriority = float(main.find("MovementPriority").text)
        except:
            print "WARNING: MovementPriority tag not found in Army/Throwers category"

        try:
            self.battalionMaxSize = int(main.find("BattalionMaxSize").text)
        except:
            print "WARNING: BattalionMaxSize tag not found in Army/Throwers category"



        boundxml = main.find("Bounding")
        if (boundxml != None):
            try:
                self.boundingLength = float(boundxml.find("Length").text)
                self.boundingHeight = float(boundxml.find("Height").text)
                self.boundingWidth = float(boundxml.find("Width").text)
            except:
                print "WARNING: Wrong Bounding data in Army/Throwers category"
        else:
            print "WARNING: Bounding tag not found in Army/Throwers category"









    def PopulateDialog(self, dlg):

        dlg.textThrowerDefense.SetValue(str(self.defense))
        dlg.textThrowerAttack.SetValue(str(self.attack))
        dlg.textThrowerSpeed.SetValue(str(self.speed))
        dlg.textThrowerReload.SetValue(str(self.reload))
        dlg.textThrowerAccuracy.SetValue(str(self.accuracy))
        dlg.textThrowerDistance.SetValue(str(self.distance))
        dlg.textThrowerBoundingLength.SetValue(str(self.boundingLength))
        dlg.textThrowerBoundingHeight.SetValue(str(self.boundingHeight))
        dlg.textThrowerBoundingWidth.SetValue(str(self.boundingWidth))
        dlg.textThrowerMovementPriority.SetValue(str(self.movementPriority))
        dlg.checkThrowerStationary.SetValue(self.stationary)
        dlg.textThrowerBattalionSize.SetValue(str(self.battalionMaxSize))


    def GetDialogData(self, dlg):

        try:
            self.defense = float(dlg.textThrowerDefense.GetValue())
        except:
            pass
        try:
            self.attack = float(dlg.textThrowerAttack.GetValue())
        except:
            pass
        try:
            self.speed = float(dlg.textThrowerSpeed.GetValue())
        except:
            pass
        try:
            self.reload = float(dlg.textThrowerReload.GetValue())
        except:
            pass
        try:
            self.accuracy = float(dlg.textThrowerAccuracy.GetValue())
        except:
            pass
        try:
            self.distance = float(dlg.textThrowerDistance.GetValue())
        except:
            pass
        try:
            self.boundingLength = float(dlg.textThrowerBoundingLength.GetValue())
        except:
            pass
        try:
            self.boundingHeight = float(dlg.textThrowerBoundingHeight.GetValue())
        except:
            pass
        try:
            self.boundingWidth = float(dlg.textThrowerBoundingWidth.GetValue())
        except:
            pass
        try:
            self.movementPriority = float(dlg.textThrowerMovementPriority.GetValue())
        except:
            pass
        try:
            self.stationary = dlg.checkThrowerStationary.GetValue()
        except:
            pass
        try:
            self.battalionMaxSize = int(dlg.textThrowerBattalionSize.GetValue())
        except:
            pass








class BE_DefaultCitySettings:

    def __init__(self):

        self.housesSize = 8.0
        self.housesDistanceWall = 50.0
        self.housesMinDistanceBetween = 16.0
        self.housesMaxDistanceBetween = 35.0
        self.housesPlacementFuzzy = 1.5
        self.housesCreationPerYear = 1
        self.housesPreferenceFactor = 0.2
        self.evolutionSpeed = 20
        self.yearsPerStep = 1
        self.minWallsLengh = 30.0
        self.maxWallsLength = 6000.0
        self.matchVerticesDistance = 5.0
        self.waitBattle = 1
        self.displayOldTownGrid = False



    def ExportXML(self, root):

        main = ET.SubElement(root, "City")

        houses = ET.SubElement(main, "Houses")
        ET.SubElement(houses, "Size").text = str(self.housesSize)
        ET.SubElement(houses, "DistanceWall").text = str(self.housesDistanceWall)
        ET.SubElement(houses, "MinDistanceBetween").text = str(self.housesMinDistanceBetween)
        ET.SubElement(houses, "MaxDistanceBetween").text = str(self.housesMaxDistanceBetween)
        ET.SubElement(houses, "PlacementFuzzy").text = str(self.housesPlacementFuzzy)
        ET.SubElement(houses, "CreationPerYear").text = str(self.housesCreationPerYear)
        ET.SubElement(houses, "PreferenceFactor").text = str(self.housesPreferenceFactor)

        ET.SubElement(main, "EvolutionSpeed").text = str(self.evolutionSpeed)
        ET.SubElement(main, "YearsPerStep").text = str(self.yearsPerStep)
        ET.SubElement(main, "MinWallLength").text = str(self.minWallsLengh)
        ET.SubElement(main, "MaxWallLength").text = str(self.maxWallsLength)
        ET.SubElement(main, "MatchVerticesDistance").text = str(self.matchVerticesDistance)
        ET.SubElement(main, "WaitBattle").text = str(self.waitBattle)
        ET.SubElement(main, "DisplayOldTownGrid").text = str(self.displayOldTownGrid)



    def ImportXML(self, root):

        main = root.find("City")
        if (not main):
            print "ERROR: City settings not found"
            return

        try:
            self.evolutionSpeed = int(main.find("EvolutionSpeed").text)
        except:
            print "WARNING: EvolutionSpeed tag not found in City settings"

        try:
            self.yearsPerStep = int(main.find("YearsPerStep").text)
        except:
            print "WARNING: YearsPerStep tag not found in City settings"

        try:
            self.minWallsLengh = float(main.find("MinWallLength").text)
        except:
            print "WARNING: MinWallLength tag not found in City settings"

        try:
            self.maxWallsLength = float(main.find("MaxWallLength").text)
        except:
            print "WARNING: MaxWallLength tag not found in City settings"

        try:
            self.matchVerticesDistance = float(main.find("MatchVerticesDistance").text)
        except:
            print "WARNING: MatchVerticesDistance tag not found in City settings"

        try:
            self.waitBattle = int(main.find("WaitBattle").text)
        except:
            print "WARNING: WaitBattle tag not found in City settings"

        try:
            self.displayOldTownGrid = (main.find("DisplayOldTownGrid").text in ['True', 'true', 'yes', 'YES', '1', 'Yes', 'TRUE'])
        except:
            print "WARNING: DisplayOldTownGrid tag not found in City settings"


        housesxml = main.find("Houses")
        if (housesxml):

            try:
                self.housesSize = float(housesxml.find("Size").text)
            except:
                print "WARNING: Size tag not found in City settings"

            try:
                self.housesDistanceWall = float(housesxml.find("DistanceWall").text)
            except:
                print "WARNING: DistanceWall tag not found in City settings"

            try:
                self.housesMinDistanceBetween = float(housesxml.find("MinDistanceBetween").text)
            except:
                print "WARNING: MinDistanceBetween tag not found in City settings"

            try:
                self.housesMaxDistanceBetween = float(housesxml.find("MaxDistanceBetween").text)
            except:
                print "WARNING: MaxDistanceBetween tag not found in City settings"

            try:
                self.housesPlacementFuzzy = float(housesxml.find("PlacementFuzzy").text)
            except:
                print "WARNING: PlacementFuzzy tag not found in City settings"

            try:
                self.housesCreationPerYear = float(housesxml.find("CreationPerYear").text)
            except:
                print "WARNING: CreationPerYear tag not found in City settings"

            try:
                self.housesPreferenceFactor = float(housesxml.find("PreferenceFactor").text)
            except:
                print "WARNING: PreferenceFactor tag not found in City/Houses settings"

        else:
            print "WARNING: Houses category not found in City settings"



    def OpenDialog(self, parent):

        dlg = BE_Dialogs.BE_DefaultCitySettingsDlg.BE_DefaultCitySettingsDlg(parent)

        # Set the initial values
        dlg.textHousesSize.SetValue(str(self.housesSize))
        dlg.textHousesDistanceWall.SetValue(str(self.housesDistanceWall))
        dlg.textHousesMinDistanceBetween.SetValue(str(self.housesMinDistanceBetween))
        dlg.textHousesMaxDistanceBetween.SetValue(str(self.housesMaxDistanceBetween))
        dlg.textHousesPlacementFuzzy.SetValue(str(self.housesPlacementFuzzy))
        dlg.textHousesPerYear.SetValue(str(self.housesCreationPerYear))
        dlg.textHousesPreference.SetValue(str(self.housesPreferenceFactor))
        dlg.textEvolutionSpeed.SetValue(str(self.evolutionSpeed))
        dlg.textYearsPerStep.SetValue(str(self.yearsPerStep))
        dlg.textMinWallLength.SetValue(str(self.minWallsLengh))
        dlg.textMaxWallLength.SetValue(str(self.maxWallsLength))
        dlg.textMatchVerticesDistance.SetValue(str(self.matchVerticesDistance))
        dlg.textWaitBattle.SetValue(str(self.waitBattle))
        dlg.checkOldTownGrid.SetValue(self.displayOldTownGrid)


        if (dlg.ShowModal() == wx.ID_OK):

            # Update data
            try:
                self.housesSize = float(dlg.textHousesSize.GetValue())
            except:
                pass
            try:
                self.housesDistanceWall = float(dlg.textHousesDistanceWall.GetValue())
            except:
                pass
            try:
                self.housesMinDistanceBetween = float(dlg.textHousesMinDistanceBetween.GetValue())
            except:
                pass
            try:
                self.housesMaxDistanceBetween = float(dlg.textHousesMaxDistanceBetween.GetValue())
            except:
                pass
            try:
                self.housesPlacementFuzzy = float(dlg.textHousesPlacementFuzzy.GetValue())
            except:
                pass
            try:
                self.housesCreationPerYear = float(dlg.textHousesPerYear.GetValue())
            except:
                pass
            try:
                self.housesPreferenceFactor = float(dlg.textHousesPreference.GetValue())
            except:
                pass
            try:
                self.evolutionSpeed = int(dlg.textEvolutionSpeed.GetValue())
            except:
                pass
            try:
                self.yearsPerStep = int(dlg.textYearsPerStep.GetValue())
            except:
                pass
            try:
                self.minWallsLengh = float(dlg.textMinWallLength.GetValue())
            except:
                pass
            try:
                self.maxWallsLength = float(dlg.textMaxWallLength.GetValue())
            except:
                pass
            try:
                self.matchVerticesDistance = float(dlg.textMatchVerticesDistance.GetValue())
            except:
                pass
            try:
                self.waitBattle = int(dlg.textWaitBattle.GetValue())
            except:
                pass
            try:
                self.displayOldTownGrid = dlg.checkOldTownGrid.GetValue()
            except:
                pass


        dlg.Destroy()





class BE_DefaultGameSettings:

    """ Misc default settings. Note that window and viewport sizes are squared (see BE_Canvas for more information)
        In addittion, window size should not be changed
    """

    def __init__(self):

        self.speed = 1
        self.windowSize = 1000
        self.viewportSize = 1000
        self.heightViewHeight = 400
        self.heigthViewWidth = 400
        self.showGrid = False



    def ExportXML(self, root):

        main = ET.SubElement(root, "Game")

        ET.SubElement(main, "speed").text = str(self.speed)
        ET.SubElement(main, "WindowHeight").text = str(self.windowSize)
        ET.SubElement(main, "WindowWidth").text = str(self.windowSize)
        ET.SubElement(main, "ViewportHeight").text = str(self.viewportSize)
        ET.SubElement(main, "ViewportWidth").text = str(self.viewportSize)
        ET.SubElement(main, "HeightViewHeight").text = str(self.heightViewHeight)
        ET.SubElement(main, "HeightViewWidth").text = str(self.heigthViewWidth)
        ET.SubElement(main, "ShowGrid").text = str(self.showGrid)


    def ImportXML(self, root, mainwindow):

        main = root.find("Game")
        if (not main):
            print "ERROR: Game settings not found"
            return

        try:
            self.speed = int(main.find("speed").text)
        except:
            print "WARNING: speed tag not found in Games category"

        try:
            self.windowSize = int(main.find("WindowHeight").text)
        except:
            print "WARNING: WindowHeight tag not found in Games category"

        """try:
            self.speed = int(main.find("WindowWidth").text)
        except:
            print "WARNING: WindowWidth tag not found in Games category"
        """

        try:
            self.viewportSize = int(main.find("ViewportHeight").text)
            mainwindow.GetCanvas().SetUserViewSize(self.viewportSize, self.viewportSize)
        except:
            print "WARNING: ViewportHeight tag not found in Games category"

        """try:
            self.speed = int(main.find("ViewportWidth").text)
        except:
            print "WARNING: ViewportWidth tag not found in Games category"
        """

        try:
            self.heightViewHeight = int(main.find("HeightViewHeight").text)
        except:
            print "WARNING: HeightViewHeight tag not found in Games category"

        try:
            self.heigthViewWidth = int(main.find("HeightViewWidth").text)
        except:
            print "WARNING: HeightViewWidth tag not found in Games category"

        try:
            self.showGrid = (main.find("ShowGrid").text in ['True', 'true', 'yes', 'YES', '1', 'Yes', 'TRUE'])
        except:
            print "WARNING: ShowGrid tag not found in Games category"





    def OpenDialog(self, parent):

        dlg = BE_Dialogs.BE_DefaultGameSettingsDlg.BE_DefaultGameSettingsDlg(parent)

        # Set the initial values
        dlg.textSpeed.SetValue(str(self.speed))
        dlg.textWindowSize.SetValue(str(self.windowSize))
        dlg.textViewportSize.SetValue(str(self.viewportSize))
        dlg.textHeightViewHeight.SetValue(str(self.heightViewHeight))
        dlg.textHeightViewWidth.SetValue(str(self.heigthViewWidth))
        dlg.checkShowGrid.SetValue(self.showGrid)


        if (dlg.ShowModal() == wx.ID_OK):

            # Update data
            try:
                self.speed = int(dlg.textSpeed.GetValue())
            except:
                pass
            try:
                self.windowSize = int(dlg.textWindowSize.GetValue())
            except:
                pass
            try:
                self.viewportSize = int(dlg.textViewportSize.GetValue())
            except:
                pass
            try:
                self.heightViewHeight = int(dlg.textHeightViewHeight.GetValue())
            except:
                pass
            try:
                self.heigthViewWidth = int(dlg.textHeightViewWidth.GetValue())
            except:
                pass
            try:
                self.showGrid = dlg.checkShowGrid.GetValue()
            except:
                pass

            parent.GetCanvas().SetUserViewSize(self.viewportSize, self.viewportSize)
            parent.Refresh()        # Update view to refresh the new viewport size


        dlg.Destroy()