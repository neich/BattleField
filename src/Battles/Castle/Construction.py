"""
Created on Apr 17, 2013

@author: Albert Mas
"""

from Battles.Utils.Geometry import Point3D, BoundingQuad

from Battles.Factory import ConstructionFactory
from Battles.Utils.Message import *
from Battles.Army.Action import Command

import Battles.Army.Battalion as Battalion


class Construction:
    """ Base castle construction class
    
    Attributes:
        height: construction height (in meters)
        thickness: construction thickness (linearly) (in meters)
        battalions: helper list of assigned battalions (it contains the same than battalionGrid, but without the grid gaps)
        defenseIncrease: defense increase value for troops deployed in constructions
        battalionGrid: grid where battalions are deployed. 
        battalionGridCellSize: cell size of battalion grid
        label: label string only for display purposes
        shape2D: polyline (list of points) that define the 2D shape
        axis2D: list of segments that define the object axis used to construct it
        battleFieldCells: list of battlefield cells that intersect with construction

        canvasObjs: Canvas objects used to refresh the view
        
        adjacentConstructions: List of adjacent constructions to current construction. Used to get fast the adjacent construction parts (also accessible from castle joins)
        
        reachable: Internal flag to know if a construction is reachable when it is deployed into the battlefield. By default, true for all construction objects

        visitFlag: Internal flag used to mark the object as visited. Used usually in castle union algorithm

        forcedColor: Internal color value. By default, the color is taken from GetLevelColor. But if this value is not None, the color will be ever the same

    """

    def __init__(self):
        self._height = 0
        self._thickness = 0
        self._defenseIncrease = 0
        self._defendingLines = None  # Must be instanced on child classes

        self._label = ''

        self._canvasObjs = []

        self._shape2D = []
        self._axis2D = []

        self._battleFieldCells = []

        self._adjacentConstructions = [None, None]

        self._reachable = True

        self.visitedFlag = False

        self.forcedColor = None

    def Reset(self):
        # Remove battalions
        self._defendingLines.Reset()

        self._reachable = True

        self._shape2D = []
        self._axis2D = []

        self._battleFieldCells = []

        self._adjacentConstructions = [None, None]

    def ClearDraw(self, canvas):
        for c in self._canvasObjs:
            canvas.delete(c)

    def ResetCounter(self):
        pass

    def GetLabel(self):
        return self._label

    def SetLabel(self, s):
        self._label = s

    def SetThickness(self, t):
        self._thickness = t

    def GetThickness(self):
        return self._thickness

    def SetHeight(self, h):
        self._height = h

    def GetHeight(self):
        return self._height

    def Draw(self, level, canvas, viewport):

        # Clear stored canvas objects
        if (len(self._canvasObjs) > 0):
            for c in self._canvasObjs:
                canvas.delete(c)
        """        
        # Axis
        for seg in self._axis2D:
            p1 = viewport.W2V(seg.p1)
            p2 = viewport.W2V(seg.p2)
            self._canvasObjs.append(canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill="pink"))
        """

        # Debug: Show battlefield cells
        """
        for b in self._battleFieldCells:
            bq = b.GetBoundingQuad()
            vp1 = viewport.W2V(bq.minPoint)
            vp2 = viewport.W2V(bq.maxPoint)
            canvas.create_oval(vp1.x, vp1.y, vp2.x, vp2.y, fill="pink")
        """

    def GetLevelColor(self, level):

        if (self.forcedColor != None):
            return self.forcedColor
        else:
            if (level == 0):
                return "brown"
            elif (level == 1):
                return "SandyBrown"
            elif (level == 2):
                return "Goldenrod"
            elif (level == 3):
                return "BurlyWood"
            elif (level == 4):
                return "Maroon"
            elif (level == 5):
                return "Purple"
            elif (level == 6):
                return "Tan"
            else:
                return "Chocolate"

    def DistanceFromPoint(self, posfrom, squared=False):
        pass

    def GetNormalVector(self, index=0):
        pass

    def GetBounding(self):

        bound = BoundingQuad()
        for s in self._shape2D:
            bound.InsertPoint(s)

        return bound

    def GetMinDistance(self, constr):
        pass

    def DeployInBattleField(self, battlefield):
        # Clear the links from old battlefield cells to current construction
        for c in self._battleFieldCells:
            c.RemoveConstruction(self)

    def Project(self, position=Point3D):
        pass

    def JoinShape(self, obj, invert=False):
        pass

    def GetAdjacentConstructions(self):
        return self._adjacentConstructions

    def GetBattlefieldCells(self):
        return self._battleFieldCells

    def IsReachable(self):
        return self._reachable

    def Intersects(self, construction, margin=0, onlycheck=False):
        # Checks if current construction object intersects with the given one
        # The margin value is the used bounding margin used to check the intersection
        # In onlycheck is True the method returns if there is any intersection, not the intersection point (faster)

        plist1 = self.GetIntersectableSegments()
        plist2 = construction.GetIntersectableSegments()

        for p1 in plist1:
            for p2 in plist2:
                ret = p1.Intersect(segment=p2, margin=margin, onlycheck=onlycheck)
                if (ret):
                    return ret

        return None

    def GetIntersectableSegments(self):
        pass

    ###########################################################################33
    # HEIGHT VIEW RELATED METHODS
    ###########################################################################33
    def GetBoundingHeightView(self):
        pass

    def DrawHeightView(self, enemyarmy, canvas, vieport):
        pass

    ###########################################################################33
    # BATTALION RELATED METHODS
    ###########################################################################33
    def SetBattalionConstructionData(self, battalion, defendingline):
        # Updates given battalion with construction data

        # Increase the defense factor
        battalion.SetExtraDefense(self._defenseIncrease)

        # Set the attack vector from construction placement
        battalion.SetAttackVector(self.GetNormalVector(defendingline), self.GetDefenseAngle())

    def GetBattalionAltitude(self, defendingline):
        return self._defendingLines.GetAltitude(defendingline)

    def GetRandomBattalion(self):
        return self._defendingLines.GetRandomBattalion()

    def GetBattalionCellPosition(self, defendingline, battalion):
        # Returns the position of given indexed battalion cell 
        return self._defendingLines.GetCellPosition(defendingline, battalion)

    def GetRandomBattalionCellPosition(self, defendingline, battalion):
        # Returns a random position inside battalion cell (given by index)
        return self._defendingLines.GetRandomCellPosition(defendingline, battalion)

    def RemoveBattalion(self, defendingline, battalion):
        self._defendingLines.RemoveBattalion(defendingline, battalion)

    def HasBattalions(self):
        if (self._defendingLines == None):
            return False
        else:
            return self._defendingLines.HasBattalions()

    def DeployBattalions(self, army, battalions, placementtype, linespercell=-1, maxpercell=-1,
                         command=Command.DEFEND_CASTLE):
        # Deploys given battalion list on construction using placementtype method
        # linespercell limits the maximum number of troops lines per cell. -1 means no limit
        # maxpercell limits the maximum number of troops per cell. -1 means no limit
        # Given battalions (from given army) are stored into a dictionary, where each key is a battalion type, and related value is the number of assigned troops
        # If troops number is -1, all avaiable troops of battalion type will be placed
        # The battalions will be deployed following the avaiable regular space. The biggest elements will be placed first
        # The battalions types must match with armycomponent class names

        # Sort the battalions list by bigger size. 
        # Because we receive a dictionary with army types, we have to create a list with objects of each given type to get his size
        def takeSecond(elem):
            return elem[1]

        d = []
        # factory = ArmyFactory()
        for kind in battalions.keys():
            d.append((kind, Battalion.getBattalionDimensions(kind)))
            # if not army.finishedBattalions(kind):
            # d.append(kind)
            # nb = factory.newBattalion(army, kind, 0)
            # if (nb != None):
            #    d.append(nb)
            # else:
            #    print "WHOOOPS, this should not have happened ###################################"
        if (len(d) == 0):
            Log('Not enough troops to deploy in ' + self.GetLabel(), VERBOSE_WARNING)
            # print 'Not enough troops to deploy in ' + self.GetLabel()
            return

            # d.sort(key=GetArmyComponentSize, reverse=True)
        d.sort(key=takeSecond, reverse=True)

        # Deploys each battalion    
        for (aBattalion, aSize) in d:
            # Recover battalion class name to get the troops number
            # classname = aBattalion.__class__.__name__
            # print "deploying ", aBattalion, "(",battalions[aBattalion],")"
            self._DeployBattalion(army=army, kind=aBattalion, number=battalions[aBattalion], placetype=placementtype,
                                  linespercell=linespercell, maxpercell=maxpercell, command=command)

    def _DeployBattalion(self, army, kind, number, placetype, linespercell=-1, maxpercell=-1,
                         command=Command.DEFEND_CASTLE):
        pass

    def UnDeployBattalions(self):
        self._defendingLines.Reset()

    def GetAllBattalions(self):
        return self._defendingLines.GetAllBattalions(discardThrowers=False, discardArchers=False)

    def DrawBattalion(self, defendingline, battalion, canvas, viewport, canvasobjs):
        return self._defendingLines.DrawBattalion(defendingline, battalion, canvas, viewport, canvasobjs)

    ###########################################################################
    # TILES RELATED METHODS
    ###########################################################################

    def HasTiles(self):
        # Returns true if current object has, by definition, tiles
        return False

    def GetTileManager(self):
        return None

    ###########################################################################33
    # ACTION RELATED METHODS
    ###########################################################################33

    def GetDefenseAngle(self):
        pass

    def RecieveImpact(self, ray):
        pass

    def IsDefeated(self):
        pass

    def Respawn(self):
        pass

    def GetDefeatReason(self):
        pass

    def RedrawAttacked(self, canvas, viewport):
        pass

        pass

    def RayHitTest(self, ray):
        # Checks if given ray intersects with object
        # This method is used to check the shoot avaiability, not to do it
        pass


# Flag used in Castle.ExpandCastle to mark those wall vertices that cannot be used to construct a new tower
# It is stored into the Point2D extra data field, and it is usefull to avoid the creation of new towers on those curtain wall parts that mathc with inner castle walls that
# dont have towers
FORBIDDEN_TOWER_FLAG = "forbiddenTower"


class Join:
    """ Connection between two Construction objects, such as between a wall and another wall or a tower
    
    Attributes:
        connectedA, connectedB: Objects connection
        center: Join center position. It's not a physical position, just a reference to construct the curtainwall shape. DEPRECATED
    """

    def __init__(self, objA, objB):
        self.__connectedA = objA
        self.__connectedB = objB
        # self.__center = Point2D()

    def SetFirstConnected(self, obj):
        self.__connectedA = obj

    def SetSecondConnected(self, obj):
        self.__connectedB = obj

    def GetFirstConnected(self):
        return self.__connectedA

    def GetSecondConnected(self):
        return self.__connectedB

    """def SetPosition(self, position):
        self.__center.x = position.x
        self.__center.y = position.y
       
    def GetPosition(self):
        return self.__center
    """

    def DrawBoth(self, canvas, viewport):
        # Draws both adjacent objects
        if (self.__connectedA):
            self.__connectedA.Draw(canvas, viewport)
        if (self.__connectedB):
            self.__connectedB.Draw(canvas, viewport)

    def DrawStart(self, level, canvas, viewport):
        # Draws only starting adjacent object
        if (self.__connectedA):
            self.__connectedA.Draw(level, canvas, viewport)

    def DrawEnd(self, level, canvas, viewport):
        # Draws only ending adjacent object
        # Level parameter means the current castle level
        if (self.__connectedB):
            self.__connectedB.Draw(level, canvas, viewport)

    def ForcedColor(self, color):
        # Forces to draw color for both constructions
        if (self.__connectedA):
            self.__connectedA.forcedColor = color
        if (self.__connectedB):
            self.__connectedB.forcedColor = color

    def InserCornerTower(self, tower, castlevector):
        # Inserts given tower between two objects. 
        # Returns a new join object created to represent the new link (the current one updates their links).
        # WARNING: Current join update the link with object A. New join links with object B
        # castlevector allows to rotate the squared towers on the castle orientation

        factory = ConstructionFactory()

        if (factory.IsWall(self.__connectedA) and factory.IsWall(self.__connectedB)):

            tower.SetPosition(self.__connectedB.GetStartPosition(), self.__connectedA, self.__connectedB, castlevector)

            # Update links
            newjoin = Join(tower, self.__connectedB)
            self.__connectedB = tower

            return newjoin

        else:
            return None

    def GetCenterPoint(self):
        # Return the approximated join center point
        factory = ConstructionFactory()

        if (factory.IsTower(self.__connectedA)):
            return self.__connectedA.GetPosition()
        elif (factory.IsTower(self.__connectedB)):
            return self.__connectedB.GetPosition()
        elif (factory.IsWall(self.__connectedA)):
            return self.__connectedA.GetEndPosition()
        elif (factory.IsWall(self.__connectedB)):
            return self.__connectedB.GetStartPosition()
        else:
            return None

    def IsWallVertexForbiddenTower(self, removeFlag):
        # Check if current join has any wall with its join vertex containng extra data flag that forbids the tower creation
        # See Castle.ExpandCastle to know more about it

        factory = ConstructionFactory()

        if (factory.IsWall(self.__connectedA)):
            p = self.__connectedA.GetEndPosition()
            if (p.data == FORBIDDEN_TOWER_FLAG):
                if (removeFlag):
                    p.data = None
                return True

        if (factory.IsWall(self.__connectedB)):
            p = self.__connectedB.GetStartPosition()
            if (p.data == FORBIDDEN_TOWER_FLAG):
                if (removeFlag):
                    p.data = None
                return True

        return False

    def GetWallVertexLinkedTower(self, removeLink):
        # Check if current join has any wall with its join vertex linked with a previous tower. This link is stored into the Point2D object
        # See Caste.ExpandCastle to know more about it
        # If the tower is found, returns a copy of it
        # If removeLink is true, removes the point link

        factory = ConstructionFactory()

        if (factory.IsWall(self.__connectedA)):
            p = self.__connectedA.GetEndPosition()
            if (factory.IsTower(p.data)):
                tower = p.data.Copy()
                if (removeLink):
                    p.data = None
                return tower

        if (factory.IsWall(self.__connectedB)):
            p = self.__connectedB.GetStartPosition()
            if (factory.IsTower(p.data)):
                tower = p.data.Copy()
                if (removeLink):
                    p.data = None
                return tower

        return None

    def JoinShapes(self):
        if (self.__connectedA != None):
            self.__connectedA.JoinShape(self.__connectedB)
