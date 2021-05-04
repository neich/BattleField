import math
import random
import operator

from Battles.Factory import ArmyFactory
from Battles.Utils.Message import *
from Battles.Utils.Geometry import Vector3D, Vector2D, Point3D, Segment2D, Point2D, PI
from Battles.Army.Action import Command
import Battles.Utils.Settings
import Battles.Army.Battalion as Battalion


# Battalions placement types
CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED = 1
CONSTRUCTION_BATTALION_DEPLOYMENT_CONSECUTIVE = 2


"""
###############################################################################
#  class DefendingBattalion
###############################################################################
"""
class DefendingBattalion:
    """ Defending battalion placed into a defending line

    Attributes:
        battalion: Battalion
        position: 3D point where battalion is placed
    """

    def __init__(self, battalion, position):
        self.battalion = battalion
        self.position = position


    def Equals(self, b):
        return (self.battalion.GetLabel() == b.GetLabel())






"""
###############################################################################
#  class DefendingLine
###############################################################################
"""
class DefendingLine:
    """ Construction battalion defending line

    Attributes:
        line: Segment that defines the defending line
        width: Width of defending line where troops can be deployed
        height: Defending line height
        battalions: List of deployed battalions. WARNING. This list is used only to get a sequential placement of troops. All accesses and queries must be performed on
                    battalionsMap structure. When a battalion is defeated, it is removed from map, but not from list, because the map has the indices to battalion objects
                    stored into this list
        battalionsMap: Dictionary that relates the battalion labels with indices on battalions list. Used to improve the performance searching
        gridCellSize: Size of grid where place the battalions. Its a 1D linear dimension
    """

    def __init__(self, segment, width = Battles.Utils.Settings.SETTINGS.Get_F(category = 'Castle', tag = 'DefendingLine', subtag='Width'),
                                height = Battles.Utils.Settings.SETTINGS.Get_F(category = 'Castle', tag = 'DefendingLine', subtag='Height'),
                                cellsize = Battles.Utils.Settings.SETTINGS.Get_F(category = 'Castle', tag = 'DefendingLine', subtag='CellSize')):
        self._line = segment
        self._width = width
        self._height = height
        self._battalions = []
        self._battalionsMap = {}
        self._gridCellSize = cellsize


    def Reset(self):
        self._battalions = []
        self._battalionsMap = {}



    def RemoveBattalion(self, battalion):
        # Do not remove the battalion from list because we should regenerate the full map
        #index = self._battalionsMap[battalion.GetLabel()]
        #del self._battalions[index]
        # Place a None at the battalion list position to let the garbage colector destroy the object
        index = self._battalionsMap[battalion.GetLabel()]
        self._battalions[index] = None

        del self._battalionsMap[battalion.GetLabel()]

    def HasBattalions(self):
        return (len(self._battalionsMap) > 0)

    def GetAltitude(self):
        return self._height

    def __GetLength(self):
        return self._line.p1.Distance(self._line.p2)

    def __GetStartLine3D(self):
            return Point3D(self._line.p1.x, self._line.p1.y, self._height)

    def __GetEndLine3D(self):
            return Point3D(self._line.p2.x, self._line.p2.y, self._height)

    def __GetVector2D(self):
            return Vector2D().CreateFrom2Points(self._line.p1, self._line.p2)

    def __GetVector3D(self):
            return Vector3D().CreateFrom2Points(self.__GetStartLine3D(), self.__GetEndLine3D())


    def canAppendBattalion(self, offset = 0):
        # verifies if a battalion that requires size space at next available position can be appended
        # Returns false if there isn't enough space to place the battalion
        # Returns true otherwise

        # Calculate next available placement
        if (len(self._battalions) == 0):
            pend = self._line.p1.Copy()
        else:
            pend = Point2D().SetFrom3D(self._battalions[len(self._battalions) - 1].position.Copy())

        dv = self.__GetVector2D()
        dv.Normalize()
        pend.Move(dv, (self._gridCellSize) + offset)

        # Check if new placement has reached the end of defending line
        dist1 = pend.Distance(self._line.p1)
        dist2 = pend.Distance(self._line.p2)
        endreached = (dist2 < self._gridCellSize) or (dist1 > self.__GetLength())
        if (endreached):
            if (len(self._battalions) > 0):
                return False
        return True


    def AppendBattalion(self, battalion, offset = 0):
        # Appends a battalion that requires size space at next avaiable position
        # Returns false if there isn't enough space to place the battalion
        # Parameter offset is used to place the next battalion at offset distance

        # Calculate next avaiable placement
        if (len(self._battalions) == 0):
            pend = self._line.p1.Copy()
        else:
            pend = Point2D().SetFrom3D(self._battalions[len(self._battalions) - 1].position.Copy())

        dv = self.__GetVector2D()
        dv.Normalize()
        pend.Move(dv, (self._gridCellSize) + offset)

        # Check if new placement has reached the end of defending line
        dist1 = pend.Distance(self._line.p1)
        dist2 = pend.Distance(self._line.p2)
        endreached = (dist2 < self._gridCellSize) or (dist1 > self.__GetLength())
        if (endreached):
            if (len(self._battalions) > 0):
                return False
            else:
                # If there are not enough space to deploy the battalion, but the defense line is empty, means that it is too short, but it is enough large to fit an unit
                # This can happens if offset is too big
                if (len(self._battalions) == 0):
                    pend = self._line.GetMidPoint()

        self._battalions.append(DefendingBattalion(battalion, Point3D(pend.x, pend.y, self._height)))
        self._battalionsMap[battalion.GetLabel()] = len(self._battalions) - 1
        return True




    def InsertBattalion(self, battalion, position):
        # Inserts a battalion into given 3D poisition
        # The free space is not considered
        self._battalions.append(DefendingBattalion(battalion, position))
        self._battalionsMap[battalion.GetLabel()] = len(self._battalions) - 1





    def GetRandomBattalion(self):

        if (len(self._battalionsMap) == 0):
            return None

        # The list object must be used for Python 3.X, because values() is an iterator. For previous Python versions, where values() are lists, this is only redundant
        index = random.choice(list(self._battalionsMap.values()))
        db = self._battalions[index]

        return db


    def GetDefendingBattalion(self, b):
        if (b.GetLabel() in self._battalionsMap):
            index = self._battalionsMap[b.GetLabel()]
            return self._battalions[index]
        else:
            return None
        """
        i = 0
        while (i < len(self._battalions)):
            db = self._battalions[i]
            if (db.Equals(b)):
                return db
            i += 1
        return None
        """

    def GetDefendingBattalionIndex(self, b):
        if (b.GetLabel() in self._battalionsMap):
            return self._battalionsMap[b.GetLabel()]
        else:
            return None
        """
        i = 0
        while (i < len(self._battalions)):
            db = self._battalions[i]
            if (db.Equals(b)):
                return i
            i += 1
        return -1
        """



    def GetAllBattalions(self, discardThrowers = False, discardArchers = False):
        ret = []
        factory = ArmyFactory()

        for index in self._battalionsMap.values():
            b = self._battalions[index].battalion
            if (((not discardThrowers) or (discardThrowers and not factory.IsThrower(b))) and ((not discardArchers) or (discardArchers and not factory.IsArcher(b)))):
                ret.append(b)

        return ret


    def GetCellPosition(self, battalion):
        # Returns the position of given  battalion

        index = self._battalionsMap[battalion.GetLabel()]
        return self._battalions[index].position

        """
        db = self.GetDefendingBattalion(battalion)
        if (db == None):
            print "ERROR: Battalion dont found for GetCellPosition"
            return None

        return db.position
        """


    def GetRandomCellPosition(self, battalion):
        # Returns a random position inside battalion cell

        db = self.GetDefendingBattalion(battalion)
        if (db == None):
            print "ERROR: Battalion dont found for GetRandomCellPosition"
            return None

        vector = self.__GetVector2D()
        tvector = vector.Copy()
        tvector.Rotate(-90)

        # Move to cell position
        pos = Point2D().SetFrom3D(db.position.Copy())

        # Calculate the random point
        #random.seed()
        r1 = random.uniform(0, self._gridCellSize)
        r2 = random.uniform(0, self._width / 2)
        pos.Move(vector, r1)
        pos.Move(tvector, -r2)

        return Point3D(pos.x, pos.y, self._height)


    def SetCellSize(self, cellsize):
        self._gridCellSize = cellsize

    def GetCellSize(self):
        return self._gridCellSize


    """
    def GetAvaiableCells(self):
        # Return the number of avaiable cells
        # Note that we use the battalions list, not the map. So, the defeated battalions are considered as a populated placement
        # This shouldn't be a problem since this method is usually called when the castle is populated
        if (len(self._battalions) == 0):
            length = self.__GetLength()
        else:
            db = self._battalions[len(self._battalions) - 1]
            length = db.position.Distance(self._line.p2)

        return length / self._gridCellSize
    """


    def CalculateDeploymentOffset(self, ncells):
        # Returns the offset (distance between battalions) that must be applied with sparsed deployment of given number of cells
        # Take the same consideration about defeated battalions than in GetAvaiableCells method
        t = ncells * self._gridCellSize

        if (len(self._battalions) == 0):
            length = self.__GetLength()
        else:
            db = self._battalions[len(self._battalions) - 1]
            length = db.position.Distance(self._line.p2)

        if (t > length):
            return 0		# This should never happens. Given ncells would be checked before call this method
        else:
            return (length - t) / ncells



    def ProjectPosition(self, pos):
        # Projects given position onto the defending line to get a centered good position

        pos2d = Point2D().SetFrom3D(pos)
        prj = self._line.ProjectPoint(pos2d)
        prj3d = Point3D().SetFrom2D(prj)
        prj3d.z = pos.z

        return prj3d



    def DrawBattalion(self, battalion, canvas, viewport, canvasobjs):
        # Draws battalion
        # NOTE: The canvas objects updating is delegated to Battalion class, so all drawn objects must be returned into canvasobjs list

        # Search the battalion
        db = self.GetDefendingBattalion(battalion)
        if (db == None):
            print "ERROR: Battalion dont found for DrawBattalion"
            return

        # Each kind of battalion is drawn in its own way
        # Note the difficulty about drawing the battalions on defending lines on themselves classes, so we need the wall direction, width, etc. The difficulty increases
        # when the defending line is rounded
        factory = ArmyFactory()
        if (factory.IsThrower(battalion)):

            # Draw a thrower battalion

            bound = battalion.GetBounding()

            # Get wall vectors to perform rotations
            vector = self.__GetVector2D()
            tvector = vector.Copy()
            tvector.Rotate(-90)

            # Draw a square for each occupied cell with the troops number
            pos = Point2D().SetFrom3D(db.position.Copy())
            pos.Move(tvector, -(self._width / 2))
            pos.Move(vector, -(bound.length / 2))
            pv1 = viewport.W2V(pos)

            pos2 = pos.Copy()
            pos2.Move(vector, bound.length)
            pv2 = viewport.W2V(pos2)

            pos2.Move(tvector, self._width)
            pv3 = viewport.W2V(pos2)

            pos.Move(tvector, self._width)
            pv4 = viewport.W2V(pos)

            canvasobjs.append(canvas.create_polygon((pv1.x, pv1.y, pv2.x, pv2.y, pv3.x, pv3.y, pv4.x, pv4.y), fill="DarkBlue", outline="cyan"))

            if (Battles.Utils.Settings.SETTINGS.Get_B(category = 'Castle', tag = 'ShowLabels')):
                # Deploy the avaiable troops number inside rectangle
                t = Point2D().SetFrom3D(db.position.Copy())
                tp = viewport.W2V(t)
                canvasobjs.append(canvas.create_text(tp.x, tp.y, text = int(db.battalion.GetNumber()), fill="cyan"))



        elif (factory.IsArcher(battalion) or factory.IsCannon(battalion)):

            # Draw an archer

            # Get wall vectors to perform rotations
            vector = self.__GetVector2D()
            tvector = vector.Copy()
            tvector.Rotate(-90)

            bound = battalion.GetBounding()

            # Draw a square for each occupied cell with the troops number
            pos = Point2D().SetFrom3D(db.position.Copy())
            pos.Move(tvector, -(bound.width / 2))
            pos.Move(vector, -(bound.length / 2))
            pv1 = viewport.W2V(pos)

            pos2 = pos.Copy()
            pos2.Move(vector, bound.length)
            pv2 = viewport.W2V(pos2)

            pos2.Move(tvector, bound.width)
            pv3 = viewport.W2V(pos2)

            pos.Move(tvector, bound.width)
            pv4 = viewport.W2V(pos)

            canvasobjs.append(canvas.create_polygon((pv1.x, pv1.y, pv2.x, pv2.y, pv3.x, pv3.y, pv4.x, pv4.y), fill="blue", outline = "cyan"))

            if (Battles.Utils.Settings.SETTINGS.Get_B(category = 'Castle', tag = 'ShowLabels')):
                # Deploy the avaiable troops number inside rectangle
                t = Point2D().SetFrom3D(db.position.Copy())
                tp = viewport.W2V(t)
                canvasobjs.append(canvas.create_text(tp.x, tp.y, text = int(db.battalion.GetNumber()), fill="cyan"))

            """
            # Draw the kind of battalion text
            t.Move(tvector, -(self.__width / 1))
            tpp = viewport.W2V(t)
            canvasobjs.append( canvas.create_text(tpp.x, tpp.y, text = db.battalion.GetLabel(), fill="gray"))
            """


        else:

            print("ERROR: DefendingLine.Draw -> Battalion not defined yet")




    def GetSubPositions(self, center, number, bounding):
        # Return a list of positions that should be the center of given bounding subdivided number times and centered at center
        # The subdivision is performed by length
        # This function is usefull for those battalions that want to be dissolved into smaller ones

        ret = []
        if (number <= 0):
            return ret

        parts = (bounding.length / float(number))

        vector = self.__GetVector2D()
        pos = Point2D().SetFrom3D(center)
        pos.Move(vector, (-bounding.length / 2.0) - (parts / 2.0))

        i = 0
        while (i < number):

            pos.Move(vector, parts)
            ret.append(Point3D(pos.x, pos.y, center.z))

            i += 1

        return ret








"""
###############################################################################
#  class DefendingLineRounded
###############################################################################
"""
class DefendingLineRounded(DefendingLine):

    """
    Special defending line defined as a circle. Usefull for rounded towers

    Attributes:

            center: circle center (2D)
            radius: circle radius
    """

    def __init__(self, center, radius, segment,
                 width=Battles.Utils.Settings.SETTINGS.Get_F(category='Castle', tag='DefendingLine', subtag='Width'),
                 height=Battles.Utils.Settings.SETTINGS.Get_F(category='Castle', tag='DefendingLine', subtag='Height'),
                 cellsize=Battles.Utils.Settings.SETTINGS.Get_F(category='Castle', tag='DefendingLine',
                                                                subtag='CellSize')):
        DefendingLine.__init__(self, segment)
        self._line = None
        self.__center = center
        self.__radius = radius
        self._width = width
        self._height = height
        self._battalions = []
        self._battalionsMap = {}
        self._gridCellSize = cellsize


    def GetStartCircle3D(self):
        p = Point3D()
        p.x = self.__center.x
        p.y = self.__center.y
        p.z = self._height


    def __GetMaxCellsNumber(self, margin = 0):
        # Return the maximum number of cells that can be deployed on the rounded shape (current deployed battalions are not considered)
        # We don't consider the intersection between cells due the circular shapes, only the arc chord
        # Margin is used as an extra space that must be added to the grid cell size (so, the units become more sparsed)

        perim = 2.0 * PI * self.__radius
        return math.floor(perim / (self._gridCellSize + margin))




    def GetAvaiableCells(self, margin = 0):
        # Return the number of avaiable cells

        n = self.__GetMaxCellsNumber(margin) - len(self._battalions)
        if (n < 0):
            n = 0
        return n




    def CalculateDeploymentOffset(self, ncells):
        # Returns the offset (distance between battalions) that must be applied with sparsed deployment of given number of cells
        # TODO
        return 0



    def AppendBattalion(self, battalion, offset = 0):
        # Appends a battalion
        # Returns false if there isn't enough space to place the battalion
        # Parameter offset is used to place the next battalion at offset distance - NOT IMPLEMENTED YET -> TODO

        if (self.GetAvaiableCells(margin = offset) == 0):
            return False

        # Calculate next avaiable placement
        nmax = self.__GetMaxCellsNumber(margin = offset)
        ang = 360.0 / nmax
        nextang = (ang * len(self._battalions)) + ang
        nextang = math.radians(nextang)

        p = Point2D()
        p.x = self.__center.x + (math.cos(nextang) * self.__radius)
        p.y = self.__center.y + (math.sin(nextang) * self.__radius)

        self._battalions.append(DefendingBattalion(battalion, Point3D(p.x, p.y, self._height)))
        self._battalionsMap[battalion.GetLabel()] = len(self._battalions) - 1

        return True


    def canAppendBattalion(self, offset = 0):
        # Checks whether we can append a battalion
        # Returns false if there isn't enough space to place the battalion
        # Parameter offset is used to place the next battalion at offset distance - NOT IMPLEMENTED YET -> TODO
        if (self.GetAvaiableCells(margin = offset) == 0):
            return False
        return True


    def GetRandomCellPosition(self, battalion):
        # TODO
        # Returns a random position inside battalion cell
        return self.GetCellPosition(battalion)



    def ProjectPosition(self, pos):
        # Projects given 3D point onto the rounded defending line

        print("ERROR: DefendingLineRounded.ProjectPosition -> Not implemented yet")
        return pos



    def DrawBattalion(self, battalion, canvas, viewport, canvasobjs):
        # Draws battalion
        # NOTE: The canvas objects updating is delegated to Battalion class, so all drawn objects must be returned into canvasobjs list

        # Search the battalion index
        index = self.GetDefendingBattalionIndex(battalion)
        if (index == -1):
            print "ERROR: Battalion dont found for DrawBattalion"
            return

        db = self._battalions[index]

        factory = ArmyFactory()
        if (factory.IsArcher(battalion)):

            # Draw an archer

            v = Vector2D().CreateFrom2Points(self.__center, db.position)
            v.Rotate(90)

            p1 = Point2D().SetFrom3D(db.position.Copy())
            p1.Move(v, -(self._gridCellSize / 2.0))
            p2 = p1.Copy()
            p2.Move(v, self._gridCellSize)
            p3 = p2.Copy()
            v2 = Vector2D().CreateFrom2Points(self.__center, p2)
            p3.Move(v2, -(self._width))
            p4 = p1.Copy()
            v3 = Vector2D().CreateFrom2Points(self.__center, p1)
            p4.Move(v3, -(self._width))

            pv1 = viewport.W2V(p1)
            pv2 = viewport.W2V(p2)
            pv3 = viewport.W2V(p3)
            pv4 = viewport.W2V(p4)


            canvasobjs.append(canvas.create_polygon((pv1.x, pv1.y, pv2.x, pv2.y, pv3.x, pv3.y, pv4.x, pv4.y), fill="blue", outline="cyan"))

            if (Battles.Utils.Settings.SETTINGS.Get_B(category = 'Castle', tag = 'ShowLabels')):
                # Deploy the avaiable troops number inside rectangle
                t = Segment2D(p1, p3).GetMidPoint()
                tp = viewport.W2V(t)
                canvasobjs.append(canvas.create_text(tp.x, tp.y, text = int(db.battalion.GetNumber()), fill="cyan"))


        elif (factory.IsCannon(battalion)):

            # Draw a cannon

            v = Vector2D().CreateFrom2Points(self.__center, db.position)
            v.Rotate(90)

            p1 = Point2D().SetFrom3D(db.position.Copy())
            p1.Move(v, -(self._gridCellSize / 2.0))
            p2 = p1.Copy()
            p2.Move(v, self._gridCellSize)
            p3 = p2.Copy()
            v2 = Vector2D().CreateFrom2Points(self.__center, p2)
            p3.Move(v2, -(self._width))
            p4 = p1.Copy()
            v3 = Vector2D().CreateFrom2Points(self.__center, p1)
            p4.Move(v3, -(self._width))

            pv1 = viewport.W2V(p1)
            pv2 = viewport.W2V(p2)
            pv3 = viewport.W2V(p3)
            pv4 = viewport.W2V(p4)


            canvasobjs.append(canvas.create_polygon((pv1.x, pv1.y, pv2.x, pv2.y, pv3.x, pv3.y, pv4.x, pv4.y), fill="DarkBlue", outline="cyan"))

            if (Battles.Utils.Settings.SETTINGS.Get_B(category = 'Castle', tag = 'ShowLabels')):
                # Deploy the avaiable troops number inside rectangle
                t = Segment2D(p1, p3).GetMidPoint()
                tp = viewport.W2V(t)
                canvasobjs.append(canvas.create_text(tp.x, tp.y, text = int(db.battalion.GetNumber()), fill="cyan"))
        else:

            print("ERROR: DefendingLineRounded.Draw -> Battalion not defined yet")


    def GetSubPositions(self, center, number, bounding):
        # TODO
        print "Error: GetSubPositions not implemented yet"
        return None






"""
###############################################################################
#  class BattalionConstruction
###############################################################################
"""
class BattalionConstruction:
    """ Defines the deployment and management of battalions on a construction

    Attributes:

        defendingLines: List of defending lines and their battalions
        battalionGridCellSize: Battalion deployment size for each unit (default)
        lineWidth: Defending line width (default)       -> Not used anymore
        lineHeight: Defending line height (default)

    """


    def __init__(self, #linewidth = Battles.Utils.Settings.SETTINGS.Get_F(category = 'Castle', tag = 'DefendingLine', subtag='Width'),
                                height = Battles.Utils.Settings.SETTINGS.Get_F(category = 'Castle', tag = 'DefendingLine', subtag='Height'),
                                cellsize = Battles.Utils.Settings.SETTINGS.Get_F(category = 'Castle', tag = 'DefendingLine', subtag='CellSize')):
        self._defendingLines = []
        self._battalionGridCellSize = cellsize
        #self._lineWidth = linewidth
        self._lineHeight = height


    def Reset(self):
        # Removes all battalions
        for d in self._defendingLines:
            d.Reset()


    def HasBattalions(self):
        for d in self._defendingLines:
            if (d.HasBattalions()):
                return True
        return False


    def GetAltitude(self, index):
        if ((index < 0) or (index > len(self._defendingLines))):
            return 0
        else:
            return self._defendingLines[index].GetAltitude()


    def SetCellSize(self, index, cellsize):
        # Sets the cellsize of a defending line
        # It must be specified before the battalions deployment, with this method or with SetDefendingLine

        if ((index >= 0) and (index <= len(self._defendingLines))):
            self._defendingLines[index].SetCellSize(cellsize)





    def SetDefendingLine(self, index, segment, cellsize = -1):
        # Defines a defending line
        # If cellsize is -1, uses the default cellsize to the new defending line created.

        if (cellsize == -1):
            gridcellsize = self._battalionGridCellSize
        else:
            gridcellsize = cellsize



        if (index > len(self._defendingLines)):
            print 'ERROR: Set defending lines by order'
            return
        elif (index == len(self._defendingLines)):
            self._defendingLines.append(DefendingLine(segment, gridcellsize, self._lineHeight, gridcellsize))
        else:
            self._defendingLines[index].Reset()
            self._defendingLines[index] = DefendingLine(segment,gridcellsize, self._lineHeight, gridcellsize)




    def SetDefendingRoundedLine(self, index, center, radius):
        # Defines a rounded defending line

        if (index > len(self._defendingLines)):
            print 'ERROR: Set defending rounded lines by order'
            return
        elif (index == len(self._defendingLines)):
            self._defendingLines.append(DefendingLineRounded(center, radius, self._battalionGridCellSize, self._lineHeight, self._battalionGridCellSize))
        else:
            self._defendingLines[index].Reset()
            self._defendingLines[index] = DefendingLineRounded(center, radius, self._battalionGridCellSize, self._lineHeight, self._battalionGridCellSize)





    def RemoveBattalion(self, defendingline, battalion):
        self._defendingLines[defendingline].RemoveBattalion(battalion)

        # WARNING: Do not delete the defending line here. Deleting the defending line changes the list indices. These indices are the links between defending lines and
        # battalions. So deleting the indices imply update the indices of all battalions. The other side of this situation is that we have to check every time the defending
        # lines are accessed, if they have battalions





    def DeployBattalion(self, defendingline, construction, army, kind, number, placetype, linespercell = -1, maxpercell = -1, command = Command.DEFEND_CASTLE):
        # Deploys given kind of battalion on given construction
        # Parameters:
        #	defendingline: Index of defending line
        #   construction: Construction object where battalion is deployed
        #   army: Army object where to get the battalion
        #   kind: Battalion class name
        #   number: Number of battalion soldiers. -1 means all possible soldiers
        #   placetype: Type of placement (see header)
        #	linespercell: For each grid cell, the maximum number of lines. -1 means all
        #   maxpercell: For each grid cell, the maximum number of soldiers per battalion. -1 means no limits

        if army.finishedBattalions(kind):
            Log('Not enough troops to cover all deployment', VERBOSE_WARNING)
            #print '=================> Not enough troops to cover all deployment <================='
            return False

        cellSize = self._defendingLines[defendingline].GetCellSize()
        if not Battalion.battalionFitsInCell(kind, cellSize, cellSize):
            Log('Too big battalion units (%s) to be deployed in this wall' % (kind), VERBOSE_WARNING)
            #print '======================= Too big battalion units (%s) to be deployed in this wall' % (kind)
            return False

        # Calculates the maximum battalion size that fits into a cell
        sizex = math.ceil(self._battalionGridCellSize / Battalion.getBattalionDimensions(kind).length)
        sizey = sizex
        if ((linespercell != -1) and (linespercell < sizey)):
            sizey = linespercell
        size = sizex * sizey
        if ((maxpercell != -1) and (maxpercell < size)):
            size = maxpercell

        # Place the battalion using selected method

        # Some placement methods cannot work well if there are already previous battalions placed
        if (self._defendingLines[defendingline].HasBattalions()):
            if (placetype == CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED):
                placetype = CONSTRUCTION_BATTALION_DEPLOYMENT_CONSECUTIVE

        factory = ArmyFactory()
        if (placetype == CONSTRUCTION_BATTALION_DEPLOYMENT_CONSECUTIVE):
            #avaiable = battalion.GetNumber()
            availableUnits = army.getBattalionFreeNumber(kind)
            end = False
            while ((availableUnits > 0) and not end):
 
                if (availableUnits > size):
                    n = size
                else:
                    n = availableUnits
 
                # Extra default deployment margin from settings
                if (kind == "Archers"): #if (factory.IsArcher(b)):
                    margin = Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Archers', 'DefendersMarginSpace')
                else:
                    margin = 0
 
                if (self._defendingLines[defendingline].canAppendBattalion(offset = margin)):
                    b = factory.newBattalion(army, kind, number = n)
                    self._defendingLines[defendingline].AppendBattalion(b, offset = margin)
                    b.SetCommand(command)
                    b.AssignToConstruction(construction, defendingline)
                    army.InsertBattalion(b)
                    availableUnits -= n
                else:
                    end = True
            Log( 'Placed wall battalions (%s troops: %d). Remain troops: %d' % (kind, army.getBattalionFreeNumber(kind) - availableUnits, availableUnits))

        elif (placetype == CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED):
            # Note that this method only runs (TODO) when battalion grid is empty. Otherwise, cells will be overwritten
            # Number of available cells
            availableUnits = army.getBattalionFreeNumber(kind)
            cells = availableUnits / size
 
            # Get the relation between battalion size and grid size to get the free cells between each battalion
            #factor = int(math.ceil(self._defendingLines[defendingline].GetAvaiableCells() / cells))
            factor = self._defendingLines[defendingline].CalculateDeploymentOffset(cells)
            # Populate the grid
            end = False
            init = True
            while ((availableUnits > 0) and not end):
                if (availableUnits > size):
                    n = size
                else:
                    n = availableUnits
                 
                # Extra default deployment margin from settings
                if (kind == "Archers"):
                    margin = Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Archers', 'DefendersMarginSpace')
                else:
                    margin = 0

                if (init):
                    successAppending = self._defendingLines[defendingline].canAppendBattalion(offset = margin)
                    offsetToUse = margin
                    init = False
                else:
                    successAppending = self._defendingLines[defendingline].canAppendBattalion(offset = factor + margin)
                    offsetToUse = factor + margin
 
                if (successAppending and not army.finishedBattalions(kind)):
                    b = factory.newBattalion(army, kind, number = n)
                    self._defendingLines[defendingline].AppendBattalion(b, offset = offsetToUse)
                    b.SetCommand(command)
                    b.AssignToConstruction(construction, defendingline)
                    army.InsertBattalion(b)
                    availableUnits -= n
                else:
                    end = True
            Log( 'Placed wall battalions (troops: %d). Remain troops: %d' % (army.getBattalionFreeNumber(kind) - availableUnits, availableUnits))
        return True


    def GetDefendingLinesWithBattalions(self):
        # Return a list with the defending lines that have battalions

        lst = []
        for d in self._defendingLines:
            if (d.HasBattalions()):
                lst.append(d)
        return lst


    def GetDefendingLine(self, index):
        # Return only the defending line object
        if ((index < 0) or (index >= len(self._defendingLines))):
            return None
        else:
            return self._defendingLines[index]


    def GetCellPosition(self, defendingline, battalion):
        # Returns the position of given indexed battalion cell
        if ((defendingline < 0) or (defendingline >= len(self._defendingLines))):
            print 'ERROR: Construction battalion index cell out of bounds'
            return None

        return self._defendingLines[defendingline].GetCellPosition(battalion)



    def GetRandomCellPosition(self, defendingline, battalion):
        # Returns a random position inside battalion cell
        if ((defendingline < 0) or (defendingline >= len(self._defendingLines))):
            print 'ERROR: Construction battalion index cell out of bounds'
            return None

        return self._defendingLines[defendingline].GetRandomCellPosition(battalion)



    def GetRandomBattalion(self):
        # Returns a random battalion on any defending line

        lst = self.GetDefendingLinesWithBattalions()
        if (not lst):
            print 'ERROR: Current construction doesnt have battalions!'
            return None



        #random.seed()

        """
        r = random.random()
        d = lst[int(math.floor(len(lst) * r))]
        """

        d = random.choice(lst)

        db = d.GetRandomBattalion()
        if (db == None):
            return None
        else:
            return db.battalion



    def GetAllBattalions(self, discardThrowers = False, discardArchers = False):
        # Returns a list with all battalions

        ret = []

        for d in self._defendingLines:
            ret.extend(d.GetAllBattalions(discardThrowers = discardThrowers, discardArchers = discardArchers))

        return ret



    def DrawBattalion(self,  defendingline, battalion, canvas, viewport, canvasobjs):
        # Draws battalion stored in place index
        # NOTE: The canvas objects updating is delegated to Battalion class, so all drawn objects must be returned into canvasobjs list


        if ((defendingline < 0) or (defendingline >= len(self._defendingLines))):
            print 'ERROR: Battalion not found'
            return

        dl = self._defendingLines[defendingline]


        dl.DrawBattalion(battalion, canvas, viewport, canvasobjs)






    def GetClosestBattalions(self, number, frompos, defendingLine, discardThrowers, discardArchers):
        # Return a list with the closest battalions to frompos 3D position
        # number parameter defines the maximum size of the list
        # If discardThrowers is true, the battalions that are throwing are not considered
        # Similar with discardArchers

        ret = []

        # Get all battalions
        lst = defendingLine.GetAllBattalions(discardThrowers, discardArchers)
        if (not lst):
            return ret
        if (len(lst) <= number):
            return lst


        # Sort all battalions by distance
        lst.sort(key = operator.methodcaller('DistanceSort', frompos))


        # Get the closest ones
        ret = lst[0:number]

        return ret




    def GetClosestDefendingLine(self, frompos):
        # Return the closest defending line to given point and its index in a dictionary format

        ret = {"Object": None, "Index": -1}

        l = len(self._defendingLines)

        if (l == 0):
            return ret
        elif (l == 1):
            ret["Object"] = self._defendingLines[0]
            ret["Index"] = 0
            return ret
        else:
            # TODO
            print("ERROR: GetClosestDefendingLine for more than one line isnt yet implemented!!!!!!!")
            return ret




    def CreateThrower(self, stair,defendersarmy, movedList):
        # Creates a thrower battalion from defenders army and setup it to attack given stair
        # Returns the defending line index
        # Store into movedList the changed units for display refreshing purposes

        #ret = {"Object": None, "Index": -1}

        stairpos = stair.GetTopPosition()

        # Get the closest defending line (to the stair)
        ret = self.GetClosestDefendingLine(stairpos)
        if (not ret["Object"]):
            print("ERROR: BattalionConstruction.CreateThrower -> None closest defending line")
            return -1

        # Project the stair position over the defending line to get a central point where to place the thrower battalion
        projectedpos = ret["Object"].ProjectPosition(stairpos)



        # Get from the defending lines the closest archers to the stair
        blist = self.GetClosestBattalions(number = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Throwers', 'BattalionMaxSize'), frompos = projectedpos, defendingLine = ret["Object"], discardThrowers = True, discardArchers = False)
        if (not blist):
            return ret["Index"]

        # Create the Thrower battalion
        factory = ArmyFactory()
        t = factory.newBattalionNoCrop(army = defendersarmy, kind = "Throwers")
        t.SetNumber(len(blist))



        # Check if there is enough space for the new one
        # Because we have searched the closest battalions, we consider that no one battalion, except throwers, can intersect with the new thrower
        # Search only the current throwers

        # To avoid calculate the intersection of rotated 2D bounding boxes, we calculate only the 1D intesection from distance to wall start
        start = stair.GetConstruction().GetStartPosition()
        dist = start.Distance(Point2D().SetFrom3D(stair.GetTopPosition()))
        bound = t.GetBounding().length / 2.0
        distmin = dist - bound
        distmax = dist + bound

        tlist = ret["Object"].GetAllBattalions(discardThrowers = False, discardArchers = True)
        for th in tlist:
            tbnd = th.GetBounding().length / 2.0
            dsth = start.Distance(Point2D().SetFrom3D(th.GetCenterPosition()))
            dsthmin = dsth - tbnd
            dsthmax = dsth + tbnd

            if ((dsthmax >= distmin) and (dsthmin <= distmax)):
                return ret["Index"]



        # Check if thrower battalion are in any hole
        # Get the list of 2D hole wall segments
        seglist = stair.GetConstruction().GetTileManager().GetHolesSegmentList()
        for seg in seglist:
            dist1 = start.Distance(seg.p1)
            dist2 = start.Distance(seg.p2)
            if (((dist1 > distmin) and (dist1 < distmax)) or ((dist2 > distmin) and (dist2 < distmax)) or ((distmin > dist1) and (distmin < dist2)) or ((distmax > dist1) and (distmax < dist2))):
                return-1

        """
        # Check also if the thrower is placed any broken wall tile
        # Because the thrower can be larger than the tile, check it for a sparsed set of points on the thrower bounding
        bt = stair.GetTopPosition().Copy()
        wdir = Vector3D().SetFrom2D(stair.GetConstruction().GetWallVector())		# WARNING: This is valid only considering that a stair is on a wall. TODO: Setup for next stair-able constructions
        bt.Move(wdir, -t.GetBounding().length / 2.0)
        offset = t.GetBounding().length / t.GetNumber()
        i = 0
        while (i < t.GetNumber()):
            if (stair.GetConstruction().IsInHole(bt)):
                return -1
            bt.Move(wdir, offset)
            i += 1
        """

        # Insert the new battalion into the army
        defendersarmy.InsertBattalion(battalion = t, updatecounters = False)

        # Update the battalion status and remove the battalions from the defending lines . Now, their positions and control will be done by the trhower battalion
        t.SetCommand(command = Command.THROW_STAIR, target = stair)
        for b in blist:
            #dl.RemoveBattalion(b)
            defendersarmy.RemoveBattalion(b)
            if (movedList):
                movedList.append(b)

        # Insert the new battalion into the defending line
        ret["Object"].InsertBattalion(t, projectedpos)

        t.AssignToConstruction(stair.GetConstruction(), ret["Index"])


        t.SetStair(stair)
        stair.SetThrowers(t)

        if (movedList):
            movedList.append(t)

        return ret["Index"]





    def HasCannons(self, index):
        # Returns true if given defending line has any deployed cannon
        if ((index >= 0) and (index < len(self._defendingLines))):
            lst = self._defendingLines[index].GetAllBattalions(discardThrowers = True, discardArchers = True)
            return (len(lst) > 0)
        return False





