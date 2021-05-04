import math

from Battles.Utils.Geometry import Point2D, Vector2D, Point3D, Vector3D, BoundingBox, Ray, Bounding, Segment2D, Ray2D
from Battles.Factory import ConstructionFactory, ArmyFactory
from Battles.Game import Results
from Battles.Castle import Construction, BattalionConstruction, TilesManager
from Battles.Army.Action import Command
import Battles.Utils.Settings


class Wall(Construction.Construction):
    """ Basic wall object from the castle curtain wall
        Wall position is defined by 2 2D points stored into the axis list
        Front wall position is defined by the 2 first 2D points stored into the shape list
        
    Attributes
        slope: Wall exterior and bottom slope. See at Geometry.Slope. None if construction element doesn't have slope
        joins: Construction objects joined by first and second wall segment vertices respectively
        walkway: Placement and dimensions of wall gateway
        
        rectangle3D: Exterior wall 3D rectangle. Generated internally when wall is placed and used later to test ray-wall intersection (shoots from cannons, e.g.)
        boundingRectangle3D: Current rectangle3D bounds. Generated automatically when rectangle3D is generated
        normalVector: Exterior normal wall vector
        
        heightCanvasObjs: Internal canvas objects used to update the height views
        
        climberStairs: List of current climbing stairs (see class Stair)
        
        climbedAttacker: If the wall has defeated by battalion climbing (the battalion object or None) and soldier index
        attachedSiegeTower: If the wall has defeated by a siege tower
        
        tilesManager: Manager for tiles
    """

    # Static wall counter for labeling 
    wallCounter = 0

    def __init__(self):
        Construction.Construction.__init__(self)
        self._thickness = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Wall', 'Thickness')
        self._height = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Wall', 'InnerHeight')
        self._defenseIncrease = Battles.Utils.Settings.SETTINGS.Get_I('Castle', 'Wall', 'DefenseIncrease')
        self.__slope = None
        self.__joins = [None, None]
        self.__walkway = {
            "altitude": (self._height - Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Wall', 'MerlonHeight')),
            "width": Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Wall', 'WalkwayWidth')}

        self._defendingLines = BattalionConstruction.BattalionConstruction(height=self.__walkway["altitude"],
                                                                           cellsize=Battles.Utils.Settings.SETTINGS.Get_F(
                                                                               'Castle', 'Wall',
                                                                               'BattalionGridCellSize'))

        self.__tilesManager = TilesManager.TilesManager(self)

        self._label = 'Wall_' + str(Wall.wallCounter)
        Wall.wallCounter += 1

        self.__rectangle3D = [Point3D(), Point3D(), Point3D(), Point3D()]
        self.__boundingRectangle3D = BoundingBox()
        self.__normalVector = Vector3D()

        self.__heightCanvasObjs = []

        self.__climberStairs = []

        self.__climbedAttacker = {"Battalion": None, "SoldierPosition": Point3D()}
        self.__attachedSiegeTower = {"SiegeTower": None, "Position": Point3D()}

    @classmethod
    def ResetCounter(cls):
        cls.wallCounter = 0

    def Reset(self):
        Construction.Construction.Reset(self)

        # Remove climbers and siege towers
        self.__climbedAttacker["Battalion"] = None
        self.__climbedAttacker["SoldierPosition"] = Point3D()
        self.__attachedSiegeTower["SiegeTower"] = None
        self.__attachedSiegeTower["Position"] = Point3D()

        # Clear the list of climbers, but not delete them
        self.__climberStairs = []

        self.__tilesManager.Reset()

    def Draw(self, level, canvas, viewport):
        Construction.Construction.Draw(self, level, canvas, viewport)

        # Walkway
        p1 = viewport.W2V(self.GetStartPosition())
        p2 = viewport.W2V(self.GetEndPosition())
        # self._canvasObjs.append(canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill="#F8F8F8", width=viewport.W2V_1f(self.__walkway["width"])))

        # Shape
        l = len(self._shape2D)
        if l > 0:
            p1 = self._shape2D[0]
            i = 1
            while i < l:
                p2 = self._shape2D[i]
                vp1 = viewport.W2V(p1)
                vp2 = viewport.W2V(p2)
                self._canvasObjs.append(canvas.create_line(vp1.x, vp1.y, vp2.x, vp2.y, fill=self.GetLevelColor(level)))

                p1 = p2
                i += 1

            if l > 2:
                # Close shape
                p1 = self._shape2D[0]
                p2 = self._shape2D[l - 1]
                vp1 = viewport.W2V(p1)
                vp2 = viewport.W2V(p2)
                self._canvasObjs.append(canvas.create_line(vp1.x, vp1.y, vp2.x, vp2.y, fill=self.GetLevelColor(level)))

        """if (Battles.Utils.Settings.SETTINGS.Get_B('Castle', 'ShowLabels')):
            # Text the kind of battalion
            cv = viewport.W2V(self.GetExteriorSegment().GetMidPoint())
            self._canvasObjs.append(canvas.create_text(cv.x, cv.y, text=self.GetLabel(), fill="blue"))
        """

    def SetPosition(self, p1, p2, reshape=True):
        # Sets the wall position with 2 points. If reshape is true, the wall 2D shape is recalculated

        if p1.Distance(p2) < 5:
            print "WARNING: Too short wall creation"
            # return False

        del self._axis2D[:]
        self._axis2D.append(Segment2D(p1, p2))

        # Generate the wall shape
        if reshape:
            self.JoinShape(None)

        # Recalculates the battalion grid (creates an empty battalion grid)
        # Note that battalion grid is created over wall axis. The wall shape is not taken into account
        self._defendingLines.SetDefendingLine(0, self._axis2D[0])

        # Recalculates the tiles
        self.__tilesManager.RecalculateTiles()

        # Recalculates the 3D rectangle and bounds (used to check shoot hits on wall)
        # Calculate the exterior wall 3D rectangle
        self.__rectangle3D[0] = Point3D(self.GetStartPosition().x, self.GetStartPosition().y, 0.0)
        # self.__rectangle3D[1] = Point3D(self.GetStartPosition().x, self.GetStartPosition().y, self.__walkway["altitude"])
        # self.__rectangle3D[2] = Point3D(self.GetEndPosition().x, self.GetEndPosition().y, self.__walkway["altitude"])
        self.__rectangle3D[1] = Point3D(self.GetStartPosition().x, self.GetStartPosition().y, self._height)
        self.__rectangle3D[2] = Point3D(self.GetEndPosition().x, self.GetEndPosition().y, self._height)
        self.__rectangle3D[3] = Point3D(self.GetEndPosition().x, self.GetEndPosition().y, 0.0)

        # Calculate the rectangle bounding
        self.__boundingRectangle3D = BoundingBox()
        for p in self.__rectangle3D:
            self.__boundingRectangle3D.InsertPoint(p)

        # Calculate the exterior normal vector
        self.CalculateNormalVector()

        return True

    def JoinShape(self, obj, invert=False):
        # Creates and join current shape with given object's shape
        # Note the order of objects: "Current wall is going to be joined with given object". This means that only is calculated the ending wall join
        # The invert flag changes this behaviour (only for towers -> TODO: Also for walls)

        factory = ConstructionFactory()

        if obj == None:
            # None object to join. Constructs a simple rectangular wall shape

            del self._shape2D[0:len(self._shape2D)]

            l = self.GetLength()
            vector = Vector2D()
            vector.CreateFrom2Points(self.GetStartPosition(), self.GetEndPosition())
            tvector = vector.Copy()
            tvector.Rotate(-90)

            p = self.GetStartPosition().Copy()
            p.Move(tvector, self._thickness / 2)
            self._shape2D.append(p.Copy())
            p.Move(vector, l)
            self._shape2D.append(p.Copy())
            p.Move(tvector, -self._thickness)
            self._shape2D.append(p.Copy())
            p.Move(vector, -l)
            self._shape2D.append(p.Copy())

            return

        else:

            # Updates the adjacencies

            if invert:
                self._adjacentConstructions[0] = obj
                obj._adjacentConstructions[1] = self
            else:
                self._adjacentConstructions[1] = obj
                obj._adjacentConstructions[0] = self

        if factory.IsWall(obj):

            # Calculate the bisector between both walls
            bisecang = self.GetBisector(obj)

            # The join point will be along the bisector 
            d = (self._thickness / 2.0) / math.cos(
                math.radians(bisecang["angle"] / 2.0))  # WARNING: We consider all walls of same thickness
            p = self.GetEndPosition().Copy()
            p.Move(bisecang["bisector"], d)

            self._shape2D[1] = p.Copy()
            obj._shape2D[0] = p.Copy()

            p.Move(bisecang["bisector"], -(d * 2.0))
            self._shape2D[2] = p.Copy()
            obj._shape2D[3] = p.Copy()

            self._adjacentConstructions[1] = obj
            obj._adjacentConstructions[0] = self




        elif factory.IsSquaredTower(obj):

            # Calculate the intersection points of wall shape with tower   

            # We must consider the invert flag. If it is true, the joined part will be the starting wall. Otherwise, the ending wall
            if invert:
                v = Vector3D().SetFrom2D(self.GetWallVector())
                v.Invert()
                ray1 = Ray(origin=Point3D().SetFrom2D(self._shape2D[1]), direction=v)
                ray2 = Ray(origin=Point3D().SetFrom2D(self._shape2D[2]), direction=v)
            else:
                v = Vector3D().SetFrom2D(self.GetWallVector())
                ray1 = Ray(origin=Point3D().SetFrom2D(self._shape2D[0]), direction=v)
                ray2 = Ray(origin=Point3D().SetFrom2D(self._shape2D[3]), direction=v)

            int1 = obj.RecieveImpact(ray1)
            int2 = obj.RecieveImpact(ray2)

            if int1 != None:
                if invert:
                    self._shape2D[0] = Point2D().SetFrom3D(int1)
                else:
                    self._shape2D[1] = Point2D().SetFrom3D(int1)
            if int2 != None:
                if invert:
                    self._shape2D[3] = Point2D().SetFrom3D(int2)
                else:
                    self._shape2D[2] = Point2D().SetFrom3D(int2)

            # Reshape the wall axis (and all dependant data). Get the medium points of side shape segments
            mp1 = Segment2D(self._shape2D[0], self._shape2D[3]).GetMidPoint()
            mp2 = Segment2D(self._shape2D[1], self._shape2D[2]).GetMidPoint()
            self.SetPosition(mp1, mp2, reshape=False)


        elif factory.IsRoundedTower(obj):

            # Calculate the intersection points of wall shape with tower   

            # We must consider the invert flag. If it is true, the joined part will be the starting wall. Otherwise, the ending wall
            if invert:
                v = Vector3D().SetFrom2D(self.GetWallVector())
                v.Invert()
                ray1 = Ray(origin=Point3D().SetFrom2D(self._shape2D[1]), direction=v)
                ray2 = Ray(origin=Point3D().SetFrom2D(self._shape2D[2]), direction=v)
            else:
                v = Vector3D().SetFrom2D(self.GetWallVector())
                ray1 = Ray(origin=Point3D().SetFrom2D(self._shape2D[0]), direction=v)
                ray2 = Ray(origin=Point3D().SetFrom2D(self._shape2D[3]), direction=v)

            int1 = obj.RecieveImpact(ray1)
            int2 = obj.RecieveImpact(ray2)

            if int1 != None:
                if invert:
                    self._shape2D[0] = Point2D().SetFrom3D(int1)
                else:
                    self._shape2D[1] = Point2D().SetFrom3D(int1)
            if int2 != None:
                if invert:
                    self._shape2D[3] = Point2D().SetFrom3D(int2)
                else:
                    self._shape2D[2] = Point2D().SetFrom3D(int2)

            # Reshape the wall axis (and all dependant data). Get the medium points of side shape segments
            mp1 = Segment2D(self._shape2D[0], self._shape2D[3]).GetMidPoint()
            mp2 = Segment2D(self._shape2D[1], self._shape2D[2]).GetMidPoint()
            self.SetPosition(mp1, mp2, reshape=False)


        elif factory.IsBastion(obj):
            # Fit the wall to the bastion

            if invert:
                self._shape2D[3] = obj.GetEndPosition(exterior=False)
                self._shape2D[0] = obj.GetEndPosition(exterior=True)
            else:
                self._shape2D[1] = obj.GetStartPosition(exterior=True)
                self._shape2D[2] = obj.GetStartPosition(exterior=False)

            # Reshape the wall axis (and all dependant data). Get the medium points of side shape segments
            mp1 = Segment2D(self._shape2D[0], self._shape2D[3]).GetMidPoint()
            mp2 = Segment2D(self._shape2D[1], self._shape2D[2]).GetMidPoint()
            self.SetPosition(mp1, mp2, reshape=False)

    def GetStartPosition(self):
        if len(self._axis2D) == 0:
            return None
        else:
            return self._axis2D[0].p1

    def GetEndPosition(self):
        if len(self._axis2D) == 0:
            return None
        else:
            return self._axis2D[0].p2

    def SetFirstJoin(self, join):
        self.__joins[0] = join

    def SetSecondJoin(self, join):
        self.__joins[1] = join

    def GetFirstJoin(self):
        return self.__joins[0]

    def GetSecondJoin(self):
        return self.__joins[1]

    def GetLength(self):
        return self.GetStartPosition().Distance(self.GetEndPosition())

    def GetMidPoint(self):
        seg = Segment2D(self.GetStartPosition(), self.GetEndPosition())
        return seg.GetMidPoint()

    def GetHeight(self):
        return self._height
        # return self.__walkway["altitude"]

    def GetWallVector(self):
        # Returns the wall vector
        v = Vector2D()
        v.CreateFrom2Points(self.GetStartPosition(), self.GetEndPosition())
        return v

    def CalculateNormalVector(self, index=0):
        # Returns the wall exterior normal angle
        # Due walls are ever perpendicular to terrain, we can calculate it in 2D
        v = Vector2D()
        v.CreateFrom2Points(self.GetStartPosition(), self.GetEndPosition())

        normal = Vector2D(v.val[1], -v.val[0])
        normal.Normalize()  # Redundant

        self.__normalVector = Vector3D(normal.val[0], normal.val[1], 0.0)

    def GetNormalVector(self, index=0):
        # WARNING + TODO: There are some bug that set this value as inverted
        self.CalculateNormalVector()
        return self.__normalVector

    def GetExteriorSegment(self):
        return Segment2D(self._shape2D[0], self._shape2D[1])

    def GetBisector(self, adj):
        # Returns the 2D bisector vector from current and adjacent wall and angle in a dictionary structure:
        #         ["bisector": Vector2D, "angle": float]. 
        # WARNING: Current wall is considered as first one, and given the second one 

        vwall1 = Vector2D().CreateFrom2Points(self.GetStartPosition(), self.GetEndPosition())
        vside1 = vwall1.Copy()
        vside1.Rotate(-90)

        vwall2 = Vector2D().CreateFrom2Points(adj.GetStartPosition(), adj.GetEndPosition())
        vside2 = vwall2.Copy()
        vside2.Rotate(-90)

        bisector = vside1.Bisector(vside2)
        ang = vside1.AngleBetween(vside2)

        return {"bisector": bisector, "angle": ang}

    def Project(self, position=Point3D(), wallside=1):
        # Projects given position over the exterior wall
        # If wallside is 1, projects over exterior wall. If it is 2, projects over the back wall side. Finally, if it is 3, projects over the medial axis
        # This is usually used when an attacker needs to be attached to the wall to climb it

        p = Point2D().SetFrom3D(position)

        if wallside == 1:
            prj = self.GetExteriorSegment().ProjectPoint(p)
        elif wallside == 2:
            seg = Segment2D(self._shape2D[3], self._shape2D[2])
            prj = seg.ProjectPoint(p)
        elif wallside == 3:
            seg = Segment2D(self.GetStartPosition(), self.GetEndPosition())
            prj = seg.ProjectPoint(p)
        else:
            return None

        position.x = prj.x
        position.y = prj.y

        return position

    def DeployInBattleField(self, battlefield):
        # Deploys current wall into given battlefield. Each battlefield cell will be linked with all  castle parts that intersect with it
        # Intersect the wall exterior segment with battlefield cells

        # print 'Deploying ' + self.GetLabel() + ' in battlefield'
        Construction.Construction.DeployInBattleField(self, battlefield)

        ext = self.GetExteriorSegment()

        self._battleFieldCells = battlefield.RayTraversal(ext.p1, ext.p2)

        for c in self._battleFieldCells:
            c.AppendDeployedConstruction(self)

    def CheckReachable(self):
        # Checks if wall is reachable by any battalion

        # If all battlefield cells where wall is deployed has other walls or towers, the wall is not reachable (remember that a battalion cannot move on a cell with a construction, except walls)   
        # This also covers the case of too short walls

        self._reachable = False

        factory = ConstructionFactory()

        for b in self._battleFieldCells:

            i = 0
            found = False
            clist = b.GetConstructions()
            while (i < len(clist)) and not found:
                if (factory.IsWall(clist[i]) and (clist[i] != self)) or factory.IsTower(clist[i]):
                    found = True
                i += 1

            if not found:
                self._reachable = True
                return

    def DistanceFromPoint(self, posfrom, squared=False):
        # Calculate the distance from given point to wall
        # Work in 2D to simplify

        p = Point2D(posfrom.x, posfrom.y)
        seg = Segment2D(self.GetStartPosition(), self.GetEndPosition())
        return seg.DistanceToPoint(p, squared)

    def GetIntersectableSegments(self):
        ret = [Segment2D(self._shape2D[0], self._shape2D[1]), Segment2D(self._shape2D[2], self._shape2D[3])]
        return ret

    def GetMinDistance(self, constr):

        factory = ConstructionFactory()

        if factory.IsWall(constr):

            # WARNING: We avoid to check the minimum distance from the two wall vertices due this function is used by the castle union
            # algorithm. Due the nature of that algorithm, we are more interested into get the minimum distance from the first vertex
            # Be aware changing this code     

            d1 = self.GetStartPosition().Distance(constr.GetStartPosition())
            d2 = self.GetStartPosition().Distance(constr.GetEndPosition())

        elif factory.IsTower(constr):

            return self.GetStartPosition().Distance(constr.GetPosition())

        else:
            return 0.0

        if d1 <= d2:
            return d1
        else:
            return d2

    ###########################################################################33
    # HEIGHT VIEW RELATED METHODS
    ###########################################################################33

    def GetBoundingHeightView(self):

        # Returns the wall bounding for height view (width will be the height)
        l = self.GetLength()
        if l < self._height:
            d = self._height
        else:
            d = l

        # Apply offsets
        d += d * 0.1

        # Squared viewports avoid problems....
        return Bounding(length=d, width=d)

    def DrawHeightView(self, enemyarmy, canvas, viewport):
        # Display the wall in a height view

        if len(self.__heightCanvasObjs) > 0:
            for c in self.__heightCanvasObjs:
                canvas.delete(c)

        # Draw the tiles
        self.__heightCanvasObjs.extend(self.__tilesManager.DrawTiles(canvas, viewport))

        l = self.GetLength()
        # Draw the wall bounding
        p1 = Point2D(0, 0)
        p2 = Point2D(l, self._height)

        pp1 = viewport.W2V(p1)
        pp2 = viewport.W2V(p2)

        self.__heightCanvasObjs.append(canvas.create_rectangle(pp1.x, pp1.y, pp2.x, pp2.y, fill=None, outline="blue"))

        # Draw the rubble (the order here is important to avoid overlapping)
        self.__heightCanvasObjs.extend(self.__tilesManager.DrawRubble(canvas, viewport))

        # Draw the wall climbers
        for stair in self.__climberStairs:
            self.__heightCanvasObjs.extend(stair.Draw(canvas, viewport))

    ###########################################################################33
    # BATTALION RELATED METHODS
    ###########################################################################33

    def _DeployBattalion(self, army, kind, number, placetype, linespercell=-1, maxpercell=-1,
                         command=Command.DEFEND_CASTLE):
        self._defendingLines.DeployBattalion(0, self, army, kind, number, placetype, linespercell, maxpercell, command)

    def GetDefendingLines(self):
        return self._defendingLines

    def GetDefendingLine(self, index):
        return self._defendingLines.GetDefendingLine(index)

    def CreateClimbingStair(self, stairposition, defendersarmy, climber, movedList):
        # Creates a climbing stair at stairposition for the attackers
        # Climber parameter is the waiting battalion to start to climb

        factory = ArmyFactory()
        stair = factory.newBattalionNoCrop(army=defendersarmy, kind="Stair")

        stair.SetPosition(stairposition)
        stair.SetDefendersArmy(defendersarmy)
        stair.SetConstruction(self)
        stair.SetWaitingBattalion(climber)

        self.__climberStairs.append(stair)

        # Creates a thrower battalion that will defend the wall against this stair
        stair.CreateThrower(movedList)

        """
        dl = self._defendingLines.CreateThrower(stair, defendersarmy, movedList)
        stair.SetDefendingLine(dl)
        """

        # Note that we dont need to refresh the stair because it is not drawable

        return stair

    """
    def CreateThrower(self, stair, defendersArmy, movedList):
        # Creates a thrower for given stair at given defendingLine
        # This is a helper function called by Stair.CreateThrower method when a thrower battalion needs to be created and there is not access to defending line or defenders army
        dl = self._defendingLines.CreateThrower(stair = stair, defendersarmy = defendersArmy, movedList = movedList)
        stair.SetDefendingLine(dl)
    """

    def RemoveClimbingStair(self, stair):
        if stair in self.__climberStairs:
            self.__climberStairs.remove(stair)

    def GetClosestClimberInAttackRange(self, posfrom, castle, action):
        # Returns the closest climbing battalions to given posfrom parameter (3D point)

        ret = None
        minD = -1

        for stair in self.__climberStairs:
            c = stair.GetClosestClimberInAttackRange(posfrom, castle, action)
            if c['Climber'] and ((c['MinDist'] < minD) or (not ret)):
                ret = c['Climber']
                minD = c['MinDist']

        return ret

    def GetStairs(self):
        return self.__climberStairs

    def GetClimberStair(self, climber):
        # Return the climber stair. Debug purposes ...
        for stair in self.__climberStairs:
            if stair.ExistsClimber(climber):
                return stair
        return None

    ###########################################################################33
    # TILES RELATED METHODS
    ###########################################################################33

    def HasTiles(self):
        return True

    def GetTileManager(self):
        return self.__tilesManager

    def GetDefendersOverTile(self, tile):
        # Return a list with all defender battalions that are deployed over given tile. Tile must be a top tile
        ret = []

        if not self.__tilesManager.IsTopTile(tile):
            return ret

        # Calculate the segment over the wall. To make it easy, we are going to work in height view, that is in wall coordinates
        tiledim = self.__tilesManager.GetTileWallDistance(tile)

        # Get all wall battalions and check those of them that intersect with the tile segment
        startpos = self.GetStartPosition()
        battalions = self._defendingLines.GetAllBattalions(discardThrowers=False, discardArchers=False)
        for b in battalions:
            pos = b.GetCenterPosition()
            dist = startpos.Distance(pos)
            if (dist >= tiledim["distance1"]) and (dist <= tiledim["distance2"]):
                ret.append(b)

        return ret

        ###########################################################################33

    # ACTION RELATED METHODS
    ###########################################################################33

    # Return the defense angle data (see Action class definition to know more about it)       
    def GetDefenseAngle(self):
        # return  WALL_DEFENSE_ANGLE
        h = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Wall', 'DefenseAngle/H')
        v = Battles.Utils.Settings.SETTINGS.Get_A('Castle', 'Wall', 'DefenseAngle/V')
        return {'H': h, 'V': {'bottom': v[0], 'top': v[1]}}

    def SetClimbedBattalion(self, battalion, climberpos):
        self.__climbedAttacker["Battalion"] = battalion
        self.__climbedAttacker["SoldierPosition"] = climberpos

    def SetAttachedSiegeTower(self, siegetower, position):
        self.__attachedSiegeTower["SiegeTower"] = siegetower
        self.__attachedSiegeTower["Position"] = position

    def RecieveImpact(self, ray):
        # Recieve an impact from given ray
        # Returns the impact point or None if it fails

        if ray.HitRectangle(self.__rectangle3D, self.__boundingRectangle3D, self.GetNormalVector()):
            # Get the tile where ray hits

            tile = self.__tilesManager.RayHit(ray)
            if not tile:
                print "ERROR -> Wall:RecieveImpact -> None tile has intersected with already checked ray wall intersection"
                return ray.GetHitPoint()

            return ray.GetHitPoint()

        else:
            return None

    def IsDefeated(self):
        # Returns true if wall is defeated

        if self.__climbedAttacker["Battalion"] != None:
            return True

        if self.__attachedSiegeTower["SiegeTower"] != None:
            return True

        if self.__tilesManager.IsWallFallen():
            return True

        return False

    def Respawn(self):
        # Respawn a defeated wall (or restore an attacked wall)

        self.__climbedAttacker = {"Battalion": None, "SoldierPosition": Point3D()}
        self.__attachedSiegeTower = {"SiegeTower": None, "Position": Point3D()}

        self.__climberStairs = []

        self.__tilesManager.RecalculateTiles()

    def GetDefeatReason(self):
        # If wall is defeated, returns a result object (None otherwise)
        if self.IsDefeated():
            if self.__climbedAttacker["Battalion"] != None:

                result = Results.ResultDataAttClimb(self.GetLabel(), self.__climbedAttacker["SoldierPosition"])
                return result
                # return 'Climbed by ' + self.__climbedBattalion.GetLabel()
            elif self.__attachedSiegeTower["SiegeTower"] != None:

                result = Results.ResultDataSiegeTower(self.GetLabel(), self.__attachedSiegeTower["Position"])
                return result
            else:

                # Yeah! The whole wall is fallen? Amazing!
                if not self.__tilesManager.IsWallFallen():
                    print('ERROR: Seems that wall is fallen, but NOT!!')

                result = Results.ResultDataWallFallen(self.GetLabel())

                return result
                # return 'Hole in the ' + self.GetLabel()

        else:
            return None

    def RayHitTest(self, ray):

        # Do the check in 2D -> easy and cheap (TODO: Do it (well) in 3D)
        ray2d = Ray2D().SetFrom3D(ray)
        seglist = self.GetIntersectableSegments()
        for seg in seglist:
            if ray2d.HitSegment3(seg):
                ray.SetHitPoint(Point3D().SetFrom2D(ray2d.GetHitPoint()))
                return True
        return False

        """# Checks if given ray intersects with wall
        invnorm = self.__normalVector.Copy()
        invnorm.Invert()
        if (ray.HitRectangle(self.__rectangle3D, self.__boundingRectangle3D, self.__normalVector)):
            return True
        elif (ray.HitRectangle(self.__rectangle3D, self.__boundingRectangle3D, invnorm)):
            return True
        else:
            return False
        """


def GetWallLength_Sort(wall):
    """ Function used to sort walls by length
    """

    return wall.GetLength()
