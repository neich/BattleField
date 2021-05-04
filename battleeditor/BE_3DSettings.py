import wx
import BE_Dialogs.BE_3DSettingsDlg
import xml.etree.cElementTree as ET
import xml.dom.minidom


class BE_3DSettings:

    """ 3D settings management class
        See usage document for more information
    """

    def __init__(self):

        self.__exportFilePath = "."
        self.__walls = True
        self.__towers = True
        self.__starFortress = {'Ravelins': True, 'HalfMoons': True, 'CovertWay': True }
        self.__houses = {'Export': True, 'ExportToExtraFile': True, 'ExportExtraFileSufix': "_houses"}

        self.__dialog = None    # Temporal reference to give acces to dialog control to OnSelectExportFolder

    def OpenDialog(self, parent):

        self.__dialog = BE_Dialogs.BE_3DSettingsDlg.BE_3DSettingsDlg(parent)

        self.__dialog.butFolder.Bind(wx.EVT_BUTTON, self.OnSelectExportFolder)

        self.__dialog.textFolder.SetValue(self.__exportFilePath)
        self.__dialog.checkWalls.SetValue(self.__walls)
        self.__dialog.checkTowers.SetValue(self.__towers)
        self.__dialog.checkRavelins.SetValue(self.__starFortress['Ravelins'])
        self.__dialog.checkHalfMoons.SetValue(self.__starFortress['HalfMoons'])
        self.__dialog.checkCovertWay.SetValue(self.__starFortress['CovertWay'])
        self.__dialog.checkHouses.SetValue(self.__houses['Export'])
        self.__dialog.checkHousesSeparatedFile.SetValue(self.__houses['ExportToExtraFile'])
        self.__dialog.textHousesSuffix.SetValue(self.__houses['ExportExtraFileSufix'])

        if (self.__dialog.ShowModal() == wx.ID_OK):

            self.__exportFilePath = self.__dialog.textFolder.GetValue()
            self.__walls = self.__dialog.checkWalls.GetValue()
            self.__towers = self.__dialog.checkTowers.GetValue()
            self.__starFortress['Ravelins'] = self.__dialog.checkRavelins.GetValue()
            self.__starFortress['HalfMoons'] = self.__dialog.checkHalfMoons.GetValue()
            self.__starFortress['CovertWay'] = self.__dialog.checkCovertWay.GetValue()
            self.__houses['Export'] = self.__dialog.checkHouses.GetValue()
            self.__houses['ExportToExtraFile'] = self.__dialog.checkHousesSeparatedFile.GetValue()
            self.__houses['ExportExtraFileSufix'] = self.__dialog.textHousesSuffix.GetValue()

        else:



         self.__dialog.Destroy()


    def OnSelectExportFolder(self, event):

        if (not self.__dialog):
            return

        dlg = wx.DirDialog(None, style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)

        if (dlg.ShowModal() == wx.ID_OK):
            self.__dialog.textFolder.SetValue(dlg.GetPath())

        dlg.Destroy()



    def ExportXML(self, filename):

        root = ET.Element("Export")

        ET.SubElement(root, "ExportFilePath").text = self.__exportFilePath + "/"

        # Yes, I know that parser already accepts True and False, but I didnt knew when I developed the "other-side" parser and I dont want to change it now (TODO),
        # , so next conversion is required (what a shame for me ... :__( )
        if (self.__walls):
            walls = '1'
        else:
            walls = '0'
        ET.SubElement(root, "Walls").text = walls

        if (self.__towers):
            towers = '1'
        else:
            towers = '0'
        ET.SubElement(root, "Towers").text = towers


        starfort = ET.SubElement(root, "StarFortress")

        if (self.__starFortress['Ravelins']):
            ravelins = '1'
        else:
            ravelins = '0'
        ET.SubElement(starfort, "Ravelins").text = ravelins

        if (self.__starFortress['HalfMoons']):
            halfmoons = '1'
        else:
            halfmoons = '0'
        ET.SubElement(starfort, "HalfMoons").text = halfmoons

        if (self.__starFortress['CovertWay']):
            covertway = '1'
        else:
            covertway = '0'
        ET.SubElement(starfort, "CovertWay").text = covertway



        houses = ET.SubElement(root, "Houses")

        if (self.__houses['Export']):
            housesact = '1'
        else:
            housesact = '0'
        ET.SubElement(houses, "Activate").text = housesact

        if (self.__houses['ExportToExtraFile']):
            export = '1'
        else:
            export = '0'
        ET.SubElement(houses, "ExportToExtraFile").text = export

        ET.SubElement(houses, "ExportExtraFileSufix").text = self.__houses['ExportExtraFileSufix']


        xmlstring = ET.tostring(root, 'utf-8', method='xml')
        parsed = xml.dom.minidom.parseString(xmlstring)
        pretty = parsed.toprettyxml(indent = "    ")

        filexml = open(filename, 'w')
        filexml.write(pretty)
        filexml.close()




    def ImportXML(self, filename):

        tree = xml.etree.cElementTree.parse(filename)
        main = tree.getroot()
        if (not main):
            print "ERROR: Wrong 3D settings file"
            return

        # Remember the 'True/False' fact (see ExportXML)

        try:
            self.__exportFilePath = main.find("ExportFilePath").text
        except:
            print "WARNING: ExportFilePath tag not found in " + filename

        try:
            w = main.find("Walls").text
            if (w == "1"):
                self.__walls = True
            else:
                self.__walls = False
        except:
            print "WARNING: Walls tag not found in " + filename

        try:
            t = main.find("Towers").text
            if (t == "1"):
                self.__towers = True
            else:
                self.__towers = False
        except:
            print "WARNING: Towers tag not found in " + filename


        star = main.find("StarFortress")
        if (not star):
            print "WARNING: StarFortress tag not found in " + filename
        else:

            try:
                r = star.find("Ravelins").text
                if (r == "1"):
                    self.__starFortress['Ravelins'] = True
                else:
                    self.__starFortress['Ravelins'] = False
            except:
                print "WARNING: Ravelins tag not found in " + filename

            try:
                h = star.find("HalfMoons").text
                if (h == "1"):
                    self.__starFortress['HalfMoons'] = True
                else:
                    self.__starFortress['HalfMoons'] = False
            except:
                print "WARNING: HalfMoons tag not found in " + filename

            try:
                c = star.find("CovertWay").text
                if (c == "1"):
                    self.__starFortress['CovertWay'] = True
                else:
                    self.__starFortress['CovertWay'] = False
            except:
                print "WARNING: CovertWay tag not found in " + filename




        houses = main.find("Houses")
        if (not houses):
            print "WARNING: Houses tag not found in " + filename
        else:
            try:
                a = houses.find("Activate").text
                if (a == "1"):
                    self.__houses['Export'] = True
                else:
                    self.__houses['Export'] = False
            except:
                print "WARNING: Activate tag not found in " + filename

            try:
                e = houses.find("ExportToExtraFile").text
                if (e == "1"):
                    self.__houses['ExportToExtraFile'] = True
                else:
                    self.__houses['ExportToExtraFile'] = False
            except:
                print "WARNING: ExportToExtraFile tag not found in " + filename

            try:
                self.__houses['ExportExtraFileSufix'] = houses.find("ExportExtraFileSufix").text
            except:
                print "WARNING: ExportExtraFileSufix tag not found in " + filename



