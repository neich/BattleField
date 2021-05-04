import wx
import BE_Dialogs.BE_GameBattlesDlg
import BE_Dialogs.BE_BattleDlg
import BE_Objects
import xml.etree.cElementTree as ET
import Battles.Utils.Geometry as Geometry
import ast




class BE_GameDataBattles:

    """ Battles class management. It follows the same structure than BE_GameData* classes, but with many more features (placed in a new py file for convenience)

        The Battles list is edited by BE_GameBattlesDlg class. Each battle is identified by its year (unique), and has a set of attackers flanks (and other data).
        This dialog allows to create and edit Battles and their data, except their flanks. Flanks are created on the canvas, defining its position and the attackers
        battalions. To create a flank, its related battle must be created before. If a battle is removed, all of its flanks become removed too

        Attributes:
            Battles: dictionary of Battles -> {year, battle_data}, where battle_data is a BE_BattleData object
            dialogbattles: internal reference to the Battles dialog (uncouple UI from data management, highly recommended since the UI is created externally and updates
                                        could remove the game data management code)
    """

    def __init__(self):

        self.__battles = {}
        self.__dialogBattles = None
        self.__mainWindow = None


    def GetBattlesYears(self):

        ret = []
        for k, v in self.__battles.items():
            ret.append(k)
        return ret



    def OpenDialog(self, mainwindow):

        self.__mainWindow = mainwindow

        self.__dialogBattles = BE_Dialogs.BE_GameBattlesDlg.BE_GameBattlesDlg(mainwindow)

        # Control the bindings to uncouple UI from data management
        self.__dialogBattles.buttonAdd.Bind(wx.EVT_BUTTON, self.OnAddBattle)
        self.__dialogBattles.buttonEdit.Bind(wx.EVT_BUTTON, self.OnEditBattle)
        self.__dialogBattles.buttonDelete.Bind(wx.EVT_BUTTON, self.OnDeleteBattle)


        # Populate the list
        if (self.__battles):
            for k, v in self.__battles.items():
                self.__dialogBattles.list.Append(str(k))
            self.__dialogBattles.list.SetSelection(0)

        self.__dialogBattles.ShowModal()         # Dialog does not have ok/cancel buttons, only the close one

        self.__dialogBattles.Destroy()
        self.__dialogBattles = None




    def OnAddBattle(self, event):

        dlg = BE_Dialogs.BE_BattleDlg.BE_BattleDlg(self.__dialogBattles)

        battledef = BE_BattleData()
        dlg.textYear.SetValue(str(battledef.year))
        dlg.textNSimulations.SetValue(str(battledef.nSimulations))
        dlg.checkRepeatuntil.SetValue(battledef.repeatUntil)
        dlg.textArchers.SetValue(str(battledef.defenders['Archers']))
        dlg.textCannons.SetValue(str(battledef.defenders['Cannons']))

        if (dlg.ShowModal() == wx.ID_OK):

            try:
                year = int(dlg.textYear.GetValue())
            except:
                year = None


            # Check if the battle year already exists
            if (not year or (year and self.__battles.has_key(year))):
                dlgerr = wx.MessageDialog(self.__dialogBattles, 'Wrong battle year', 'Error', wx.ID_OK | wx.ICON_ERROR)
                dlgerr.ShowModal()
                dlgerr.Destroy()
            else:

                battle = BE_BattleData()
                battle.SetColor()
                battle.year = year
                battle.repeatUntil = dlg.checkRepeatuntil.GetValue()

                try:
                    battle.nSimulations = int(dlg.textNSimulations.GetValue())
                except:
                    pass
                try:
                    battle.defenders['Archers'] = int(dlg.textArchers.GetValue())
                except:
                    pass
                try:
                    battle.defenders['Cannons'] = int(dlg.textCannons.GetValue())
                except:
                    pass

                self.__battles[battle.year] = battle
                self.__dialogBattles.list.Append(str(battle.year))

        dlg.Destroy()


    def OnEditBattle(self, event):

        if (not self.__mainWindow):
            return

        # Check if there are any selected year
        sel = self.__dialogBattles.list.GetSelection()
        if (sel == wx.NOT_FOUND):
            return
        else:

            if (not self.__battles.has_key(int(self.__dialogBattles.list.GetString(sel)))):
                return
            battle = self.__battles[int(self.__dialogBattles.list.GetString(sel))]

            dlg = BE_Dialogs.BE_BattleDlg.BE_BattleDlg(self.__dialogBattles)

            dlg.textYear.SetValue(str(battle.year))
            dlg.textNSimulations.SetValue(str(battle.nSimulations))
            dlg.checkRepeatuntil.SetValue(battle.repeatUntil)
            dlg.textArchers.SetValue(str(battle.defenders['Archers']))
            dlg.textCannons.SetValue(str(battle.defenders['Cannons']))

            # Get the related flanks to update their years
            flanks = self.GetBattleFlanks(battle.year, self.__mainWindow.GetDocument())

            if (dlg.ShowModal() == wx.ID_OK):
                try:
                    year = int(dlg.textYear.GetValue())
                except:
                    year = None

                prevYear = int(self.__dialogBattles.list.GetString(sel))
                differentYear = (year != prevYear)

                # Check if the battle year already exists
                if (not year or (year and self.__battles.has_key(year) and differentYear)):
                    dlgerr = wx.MessageDialog(self.__dialogBattles, 'Wrong battle year', 'Error', wx.ID_OK | wx.ICON_ERROR)
                    dlgerr.ShowModal()
                    dlgerr.Destroy()
                else:

                    battle.year = year
                    battle.repeatUntil = dlg.checkRepeatuntil.GetValue()

                    try:
                        battle.nSimulations = int(dlg.textNSimulations.GetValue())
                    except:
                        pass
                    try:
                        battle.defenders['Archers'] = int(dlg.textArchers.GetValue())
                    except:
                        pass
                    try:
                        battle.defenders['Cannons'] = int(dlg.textCannons.GetValue())
                    except:
                        pass

                    self.__battles[battle.year] = battle

                    if (differentYear):
                        self.__dialogBattles.list.SetString(sel, str(battle.year))
                        for f in flanks:
                            f.year = battle.year


            dlg.Destroy()



    def OnDeleteBattle(self, event):

        if (not self.__mainWindow):
            return

        # Check if there are any selected year
        sel = self.__dialogBattles.list.GetSelection()
        if (sel == wx.NOT_FOUND):
            return
        else:
            year = self.__dialogBattles.list.GetString(sel)
            if (not self.__battles.has_key(int(year))):
                return

            dlg = wx.MessageDialog(self.__dialogBattles, 'Are you sure? All related flanks will be removed too', 'Error', wx.ID_OK | wx.ID_CANCEL | wx.ICON_ERROR)
            if (dlg.ShowModal() == wx.ID_OK):

                # Serch for all related flanks and remove them
                flanks = self.GetBattleFlanks(int(year), self.__mainWindow.GetDocument())
                for f in flanks:
                    self.__mainWindow.GetDocument().DeleteCanvasObject(f)



                del self.__battles[int(year)]
                self.__dialogBattles.GetParent().Refresh()
                self.__dialogBattles.list.Delete(sel)


            dlg.Destroy()







    def GetBattleFlanks(self, battleyear, document):
        # Return the flanks related to given battle year
        # Remember that flanks are stored as BE_Objects, so they are visual (GameData objects are for those only specified as data to export)

        ret = []
        flanks = document.GetCanvasObjectsByType(BE_Objects.BE_Object.CANVASOBJECT_FLANK)
        if (flanks):
            for f in flanks:
                if (f.year == battleyear):
                    ret.append(f)

        return ret


    def GetBattle(self, year):
        # Returns the battle for given year
        if (self.__battles.has_key(year)):
            return self.__battles[year]
        else:
            return None


    def ExportXML(self, root, document):

        main = ET.SubElement(root, "BattleEvents")

        for k,v in self.__battles.items():

            battlexml = ET.SubElement(main, "Battle")

            ET.SubElement(battlexml, "Year").text = str(v.year)
            ET.SubElement(battlexml, "Simulations").text = str(v.nSimulations)
            ET.SubElement(battlexml, "RepeatUntilDefendersWin").text = str(v.repeatUntil)

            defendersxml = ET.SubElement(battlexml, "Defenders")
            if (v.defenders['Archers'] > 0):
                ET.SubElement(defendersxml, "Archers").text = str(v.defenders['Archers'])
            if (v.defenders['Cannons'] > 0):
                ET.SubElement(defendersxml, "Cannons").text = str(v.defenders['Cannons'])

            flanks = self.GetBattleFlanks(v.year, document)
            if (len(flanks) > 0):
                attackersxml = ET.SubElement(battlexml, "Attackers")

                for f in flanks:
                    flankxml = ET.SubElement(attackersxml, "Flank")

                    if (f.standDistance):
                        ET.SubElement(flankxml, "StandDistance").text = str(f.standDistance)
                    ET.SubElement(flankxml, "Origin").text = "[" + str(f.origin.x) + "," + str(f.origin.y) + "]"

                    seg = Geometry.Segment2D(f.origin, f.target)
                    dir = seg.GetDirection()
                    ET.SubElement(flankxml, "Direction").text = "[" + str(dir.val[0]) + "," + str(dir.val[1]) + "]"

                    # This is an extra field that only will be used by the Editor. It justs stores the user arrow length defined to reconstruct it on ImportXML function
                    # It does not change anything in the simulation, and is used only for visual purposes
                    arrowlength = ET.SubElement(flankxml, "BE_Editor_ArrowLength")
                    arrowlength.text = str(seg.GetLength())

                    battalionsxml = ET.SubElement(flankxml, "Battalions")
                    for bk, bv in f.battalions.items():
                        if (bv['Number'] and (bv['Number'] > 0)):
                            bxml = ET.SubElement(battalionsxml, "Battalion")
                            ET.SubElement(bxml, "Type").text = str(bk)
                            ET.SubElement(bxml, "Number").text = str(bv['Number'])
                            if (bv['BattalionSize']):
                                ET.SubElement(bxml, "BattalionSize").text = str(bv['BattalionSize'])
                            if (bv['GroupSize']):
                                ET.SubElement(bxml, "GroupSize").text = str(bv['GroupSize'])
                            if (bv['GroupDistance']):
                                ET.SubElement(bxml, "GroupDistance").text = str(bv['GroupDistance'])






    def ImportXML(self, root, document):

        main = root.find("BattleEvents")
        if (not main):
            return



        for battlexml in main:
            if (battlexml.tag == "Battle"):
                battle = BE_BattleData()

                try:
                    battle.year = int(battlexml.find("Year").text)
                except:
                    print "ERROR: Battle year not specified in a battle of the  BattleEvents category"
                    continue

                try:
                    battle.nSimulations = int(battlexml.find("Simulations").text)
                except:
                    print "WARNING: Wrong battle simulations number in a battle of the  BattleEvents category"

                try:
                    battle.repeatUntil = (battlexml.find("RepeatUntilDefendersWin").text in ['True', 'true', 'yes', 'YES', '1', 'Yes', 'TRUE'])

                except:
                    print "WARNING: RepeatUntilDefendersWin tag not found in a battle of the  BattleEvents category"

                # Defenders
                defendersxml = battlexml.find("Defenders")
                if (defendersxml != None):
                    try:
                        archersxml = defendersxml.find("Archers")
                        if (archersxml != None):
                            battle.defenders['Archers'] = int(archersxml.text)
                        else:
                            battle.defenders['Archers'] = 0
                        cannonsxml = defendersxml.find("Cannons")
                        if (cannonsxml != None):
                            battle.defenders['Cannons'] = int(cannonsxml.text)
                        else:
                            battle.defenders['Cannons'] = 0

                    except:
                        print "WARNING: Wrong defenders data in a battle of the BattleEvents category"
                else:
                    print "WARNING: None defenders has been specified in a battle of the BattleEvents category"


                # Attackers
                attackersxml = battlexml.find("Attackers")
                if (attackersxml != None):
                    # Flanks
                    for flankxml in attackersxml:
                        if (flankxml.tag == "Flank"):

                            flank = BE_Objects.BE_Flank()
                            flank.year = battle.year

                            try:

                                dist = flankxml.find("StandDistance")
                                if (dist != None):
                                    flank.standDistance = float(dist.text)      # Optional

                                # TODO: Place the arrow flank considering the standdistance


                                dirxml = ast.literal_eval(flankxml.find("Direction").text)
                                direction = Geometry.Vector2D(float(dirxml[0]), float(dirxml[1]))
                                direction.Normalize()

                                originxml = flankxml.find("origin")
                                if (originxml != None):
                                    origin = ast.literal_eval(originxml.text)
                                    flank.origin = Geometry.Point2D(float(origin[0]), float(origin[1]))
                                else:
                                    # Directional flank (no origin)
                                    # Place the arrow at the viewport edges
                                    viewsize = document.GetDefaultSettings().game.viewportSize
                                    origin = Geometry.Point2D(viewsize / 2.0, viewsize / 2.0)
                                    origin.Move(direction.Copy().Invert(), viewsize / 2.0)
                                    flank.origin = origin.Copy()

                                    # TODO : Improve this to work with standdistance


                                # Since arrow length is not used in the simulation, it could not be found in the incoming xml (except it is created by the editor, see ExportXML)
                                # If it is not present, use a default value
                                arrowlengthxml = flankxml.find("BE_Editor_ArrowLength")
                                if (arrowlengthxml == None):
                                    arrowlength = 200.0
                                else:
                                    arrowlength = float(arrowlengthxml.text)

                                flank.target = flank.origin.Copy()
                                flank.target.Move(direction, arrowlength)

                            except:
                                print "WARNING: Wrong flank data of a battle in BattleEvents category"

                            # Flank battalions
                            battalionsxml = flankxml.find("Battalions")
                            if (battalionsxml != None):
                                for battalionxml in battalionsxml:

                                    try:
                                        type = battalionxml.find("Type").text
                                        number = int(battalionxml.find("Number").text)

                                        batsizexml = battalionxml.find("BattalionSize")
                                        if (batsizexml != None):
                                            battalionsize = int(batsizexml.text)
                                        else:
                                            battalionsize = None

                                        groupsizexml = battalionxml.find("GroupSize")
                                        if (groupsizexml != None):
                                            groupsize = int(groupsizexml.text)
                                        else:
                                            groupsize = None

                                        groupdistxml = battalionxml.find("GroupDistance")
                                        if (groupdistxml != None):
                                            groupdist = int(groupdistxml.text)
                                        else:
                                            groupdist = None

                                        flank.battalions[type] = {'Number': number, 'BattalionSize': battalionsize, 'GroupSize': groupsize, 'GroupDistance': groupdist}

                                    except:
                                        print "WARNING: Wrong battalion data in a flank of the BattleEvents category"

                            else:
                                print "WARNING: None battalion has found in a flank of the BattleEvents category"

                            battle.flanks.append(flank)
                            document.AddCanvasObject(flank)

                else:
                    print "WARNING: None attackers has been specified in a battla of the BattleEvents category"

                battle.SetColor()
                self.__battles[battle.year] = battle







# Color array. Each battle has a color used to draw its flanks
BATTLE_COLOR_FLANKS = ["RED", "SIENNA", "NAVY", "MEDIUM VIOLET RED", "PURPLE", "GOLDENROD", "ORANGE RED", "INDIAN RED"]
BATTLE_COLOR_COUNTER = 0




class BE_BattleData:

    """ Battle data class

        Attributes:
            year: battle year. must be unique
            nsimulations: number of simulations for current battle
            repeatuntil: true if simulation must end only if defenders win
            defenders: dictionary with number of defender units for each kind (archers and cannons)
            flanks: list of flanks (see BE_Flank object)
            color: wxColor used by flanks
    """

    def __init__(self):

        self.year = 0
        self.nSimulations = 10
        self.repeatUntil = False
        self.defenders = {'Archers': 0, 'Cannons': 0}
        self.flanks = []
        self.color = None


    def SetColor(self):
        global BATTLE_COLOR_FLANKS
        global BATTLE_COLOR_COUNTER

        db = wx.ColourDatabase()

        self.color = db.Find(BATTLE_COLOR_FLANKS[BATTLE_COLOR_COUNTER % len(BATTLE_COLOR_FLANKS)])
        BATTLE_COLOR_COUNTER += 1




