from Battles.Castle import Construction, OldTown
from Battles.Factory import ConstructionFactory
from Battles.Utils.Geometry import Vector2D, Point2D, Segment2D, BoundingQuad
from Battles.Castle.StarFortress import *
from Battles.Army.Action import Command
import math
import Battles.Utils.Settings


class Castle:
    """ Castle class. It is a container for all castle constructions
    
    Attributes:
        joins: List of all castle joins. Note that we can get the construction objects from each join
        parts: Helper list of all castle parts (walls, towers, ...).
        moat: Moat object
        orientation: Castle orientation vector. Used as a reference, by example to place the squared towers
        city: List of [x,y] coordinates that define the city points
        convexhull: 2D convex hull of castle walls. Used as reference to deploy the moat and to get the interior castle region
        starfortress: Star Fortress object that defines all of exterior constructions that form a star fortress. The walls, towers and bastions are not considered
        innerCastle: Used in city evolution. When a castle has to be surrounded by a new curtain wall, it becomes a part of the new castle, and is referred in this field.
                     Dont be confused about the castle itself evolution. The castle evolution upgrades the castle towers. But the city evolution grows the city and creates a 
                     new curtain wall around it
        innerCastleJoined: Internal flag to know if the inner castle has been joined with the current one or if it is separated or covered by the current one
        hierarchyLevel: Internal counter for current castle level (greater for outer castles)
    """

    def __init__(self):
        self.__joins = []
        self.__parts = {"Walls": [], "Towers": []}
        self.__moat = None
        orientation = Battles.Utils.Settings.SETTINGS.Get_A(category='Castle', tag='Orientation')
        if (orientation is not None) and (len(orientation) == 2):
            self.__orientation = Vector2D(orientation[0], orientation[1])
        self.__oldTown = OldTown.OldTown(self)
        self.__starfortress = StarFortress(self)
        self.__wallsResistance = Battles.Utils.Settings.SETTINGS.Get_I('Castle', 'Wall', 'Tile/Resistance')
        self.__innerCastle = None
        self.__innerCastleJoined = False
        self.__hierarchyLevel = 0
        self.__reservedTroopsCanvas = []

    def GetHierarchyLevel(self):
        return self.__hierarchyLevel

    def SetInnerCastle(self, castle, joined=True):
        self.__innerCastle = castle
        self.__innerCastleJoined = joined
        self.__hierarchyLevel = castle.GetHierarchyLevel() + 1

        if joined:
            # Force the color for joined inner castle
            self.__innerCastle.SetGrayed()

    def SetGrayed(self):
        # Sets the gray color for the whole castle
        for j in self.__joins:
            j.ForcedColor("gray25")

    def isInside(self, point):
        castlehull = self.GetCastleHull()
        return castlehull.IsInside(point)

    # DEPRECATED
    """
    def CreateOuterCastle(self):
        # Creates and returns an empty castle that wraps the current one. 
        # Be aware. The new castle hasnt walls or towers. Its just the basic structure
        
        c = Castle()

        # Matches common data        
        c.SetCastleOrientation(self.__orientation)
        
        # Walls resistance cannot be specified since the walls are not yet created

        # Castle cannot be evolved yet due we dont have yet the curtain wall
        
        # Moat cannot be created unit the castle curtain wall is constructed
        # Star fortress configuration cannot be specified at this point
        
        c.__innerCastle = self
       
        return c    
    """

    def Draw(self, canvas, viewport, moat=True, city=True, starfortress=False):
        if moat:
            # Draw the moat
            if self.__moat is not None:
                self.__moat.Draw(1, canvas, viewport)

        if city:
            # Draw the city
            self.__oldTown.Draw(canvas, viewport)

        if self.__innerCastle:  # and not self.__innerCastleJoined):
            self.__innerCastle.Draw(canvas, viewport, moat=moat, city=city, starfortress=False)

        # Draw the castle
        i = 0
        while i < len(self.__joins):
            self.__joins[i].DrawStart(self.__hierarchyLevel, canvas, viewport)
            i += 1

        if starfortress:
            # Draw the star fortress
            self.__starfortress.Draw(canvas, viewport)

    def DrawReservedSoldiers(self, canvas, viewport, army):
        # Draw the reserved soldiers. Currently only archers are the only type of reserved battalions
        # TODO: Consider other kind of units

        for c in self.__reservedTroopsCanvas:
            canvas.delete(c)

        if army.AreAttackers():
            return

        archers = army.GetBattalionType("Archers")
        if archers and (archers.freenumber > 0) and (len(archers.battalions) > 0):
            # Draw the units at the castle center in a square shape        
            center = self.GetBounding().GetCenter()
            square = math.floor(math.sqrt(archers.freenumber))
            sizex = archers.battalions[0].GetBounding().length * square
            sizey = archers.battalions[0].GetBounding().width * square
            extrax = archers.freenumber - (square * square)

            pv1 = viewport.W2V(Point2D(center.x - (sizex / 2.0), center.y - (sizey / 2.0)))
            pv2 = viewport.W2V(Point2D(center.x + (sizex / 2.0), center.y + (sizey / 2.0)))
            self.__reservedTroopsCanvas.append(
                canvas.create_rectangle(pv1.x, pv1.y, pv2.x, pv2.y, fill="cyan", width=1, outline="cyan"))

            pv3 = viewport.W2V(Point2D(center.x - (sizex / 2.0), center.y + (sizey / 2.0)))
            pv4 = viewport.W2V(Point2D(center.x - (sizex / 2.0) + extrax,
                                       center.y + (sizey / 2.0) + archers.battalions[0].GetBounding().width))
            self.__reservedTroopsCanvas.append(
                canvas.create_rectangle(pv3.x, pv3.y, pv4.x, pv4.y, fill="cyan", width=1, outline="cyan"))

    def SetCastleOrientation(self, v):
        self.__orientation = v

    def GetCastleOrientation(self):
        return self.__orientation

    def WrapOldCity(self, city, margin, battlefieldcenter):
        # From a list of 2D points, constructs the curtain wall wrapping the old city with a polyline around it,  with specified margin
        # battlefieldcenter is a Point2D with the center of the battlefield. More info about it in City.Wrap method

        self.__oldTown.Wrap(city, margin, battlefieldcenter)
        self.ConstructCurtainWall(self.__oldTown.GetConvexHull().Get2DPointHull())

    def ConstructCurtainWall(self, polyline):
        # Constructs the curtain wall structure, only with walls. Given polyline is a list with points/vertices that define the shape

        factory = ConstructionFactory()

        # Convert each vertex into a join
        i = 0
        while i < len(polyline):

            if i == 0:

                currwall = factory.newConstruction("Wall")
                currwall.SetPosition(polyline[i], polyline[i + 1])

                j = Construction.Join(None, currwall)
                # j.SetPosition(polyline[i])
                currwall.SetFirstJoin(j)

                self.__joins.append(j)
                self.__parts["Walls"].append(currwall)

                lastwall = currwall

            elif (i + 1) == len(polyline):

                currwall = factory.newConstruction("Wall")
                currwall.SetPosition(polyline[i], polyline[0])

                j = Construction.Join(lastwall, currwall)
                # j.SetPosition(polyline[i])
                currwall.SetFirstJoin(j)
                currwall.SetSecondJoin(self.__joins[0])
                lastwall.SetSecondJoin(j)

                self.__joins.append(j)
                self.__parts["Walls"].append(currwall)

                # Closing join
                self.__joins[0].SetFirstConnected(currwall)

            else:

                currwall = factory.newConstruction("Wall")
                currwall.SetPosition(polyline[i], polyline[i + 1])

                j = Construction.Join(lastwall, currwall)
                # j.SetPosition(polyline[i])
                currwall.SetFirstJoin(j)
                lastwall.SetSecondJoin(j)

                self.__joins.append(j)
                self.__parts["Walls"].append(currwall)

                lastwall = currwall

            i += 1

        self.CreateCastleShape()

    def ConstructCornerTowers(self):
        # Deploys towers at each castle corner. By default, creates squared towers, except rounded is True
        # WARNING!: Use this method only if castle hasn't towers!!

        if len(self.__parts["Towers"]) > 0:
            return

        newjoins = []
        factory = ConstructionFactory()

        i = 0
        while i < len(self.__joins):
            # Insert a tower in each join

            join = self.__joins[i]

            # Check if current join has the forbidden tower flag (see Castle.ExpanCastle)
            if join.IsWallVertexForbiddenTower(removeFlag=True):
                newjoins.append(join)
                i += 1
                continue

            # Check if current join has walls with any vertex linked to a previous tower. This link is stored in Point2D object, and its a product of castle expansion method,
            # where the new castle shape vertices have been checked to know if they match any previous tower
            tower = join.GetWallVertexLinkedTower(removeLink=True)

            if tower is None:
                # Create a new tower
                tower = factory.newConstruction("Tower")

            j = join.InserCornerTower(tower, self.__orientation)

            # Stores the old and new joins to recreate the joins list at the end
            # NOTE that as is explained in InsertTower method, the old join is previous than new join 
            newjoins.append(join)
            if j is not None:
                newjoins.append(j)

            self.__parts["Towers"].append(tower)

            i += 1

        self.__joins = newjoins[0:len(newjoins)]

    def ConstructCurtainWallWithTowers(self, polylinetowers):
        # Constructs the curtain wall structure from a polyline
        # Each polyline item contains the 2D position and tower presence for each vertex. 
        # Each list item must has this format:  {"Point": [x, y], "HasTower": True/False, "TowerType": "SquaredTower/RoundedTower"}
        # TODO: Allow bastions 

        factory = ConstructionFactory()

        # Convert each vertex into a join
        i = 0
        while i < len(polylinetowers):

            if i == 0:

                currwall = factory.newConstruction("Wall")
                currwall.SetPosition(polylinetowers[i]["Point"], polylinetowers[i + 1]["Point"])

                tower = None
                if polylinetowers[i]["HasTower"]:

                    tower = factory.newConstruction(polylinetowers[i]["TowerType"])
                    if tower is not None:
                        j1 = Construction.Join(None, tower)
                        j2 = Construction.Join(tower, currwall)

                        currwall.SetFirstJoin(j2)

                        self.__joins.append(j1)
                        self.__joins.append(j2)

                        self.__parts["Walls"].append(currwall)
                        self.__parts["Towers"].append(tower)

                if tower is None:
                    j = Construction.Join(None, currwall)
                    # j.SetPosition(polyline[i])
                    currwall.SetFirstJoin(j)

                    self.__joins.append(j)
                    self.__parts["Walls"].append(currwall)

                lastwall = currwall

            elif (i + 1) == len(polylinetowers):
                currwall = factory.newConstruction("Wall")
                currwall.SetPosition(polylinetowers[i]["Point"], polylinetowers[0]["Point"])

                tower = None
                if polylinetowers[i]["HasTower"]:

                    tower = factory.newConstruction(polylinetowers[i]["TowerType"])
                    if tower is not None:
                        tower.SetPosition(polylinetowers[i]["Point"], lastwall, currwall, self.__orientation)

                        j1 = Construction.Join(lastwall, tower)
                        j2 = Construction.Join(tower, currwall)

                        lastwall.SetSecondJoin(j1)
                        currwall.SetFirstJoin(j2)
                        currwall.SetSecondJoin(self.__joins[0])

                        self.__joins.append(j1)
                        self.__joins.append(j2)

                        self.__parts["Walls"].append(currwall)
                        self.__parts["Towers"].append(tower)

                if tower is None:
                    j = Construction.Join(lastwall, currwall)
                    currwall.SetFirstJoin(j)
                    currwall.SetSecondJoin(self.__joins[0])
                    lastwall.SetSecondJoin(j)

                    self.__joins.append(j)
                    self.__parts["Walls"].append(currwall)

                # Closing the sequence
                self.__joins[0].SetFirstConnected(currwall)

                # Be aware about initial towers
                if factory.IsTower(self.__joins[0].GetSecondConnected()):
                    self.__joins[0].GetSecondConnected().SetPosition(polylinetowers[0]["Point"], currwall,
                                                                     self.__joins[1].GetSecondConnected(),
                                                                     self.__orientation)


            else:

                currwall = factory.newConstruction("Wall")
                currwall.SetPosition(polylinetowers[i]["Point"], polylinetowers[i + 1]["Point"])

                tower = None
                if polylinetowers[i]["HasTower"]:

                    tower = factory.newConstruction(polylinetowers[i]["TowerType"])
                    if tower is not None:
                        tower.SetPosition(polylinetowers[i]["Point"], lastwall, currwall, self.__orientation)

                        j1 = Construction.Join(lastwall, tower)
                        j2 = Construction.Join(tower, currwall)
                        lastwall.SetSecondJoin(j1)
                        currwall.SetFirstJoin(j2)

                        self.__joins.append(j1)
                        self.__joins.append(j2)

                        self.__parts["Walls"].append(currwall)
                        self.__parts["Towers"].append(tower)

                if tower is None:
                    j = Construction.Join(lastwall, currwall)
                    currwall.SetFirstJoin(j)
                    lastwall.SetSecondJoin(j)

                    self.__joins.append(j)
                    self.__parts["Walls"].append(currwall)

                lastwall = currwall

            i += 1

        self.CreateCastleShape()

    def CreateCastleShape(self):
        # Calculates the castle shape joining each castle construction with their adjacents

        for j in self.__joins:
            j.JoinShapes()

    def Evolve(self, climbings=None, attachedsiegetowers=None, battlefield=None):
        # Executes one castle evolution step
        # climbings is a list with all climbed parts. Each list element must be {'Construction': constructionLabel, 'WeakPoint': Point3D(...)}
        # First evolution step only places corner towers (ignoing the climbings or holes)
        # Returns false if castle cannot evolve

        # First evolution step: If castle doesn't have towers, place them at corners
        if len(self.__parts["Towers"]) == 0:

            self.ConstructCornerTowers()
            self.CreateCastleShape()

        else:

            factory = ConstructionFactory()

            if climbings is not None:
                for c in climbings:
                    if factory.IsWall(c["Construction"]):
                        self.EvolveWall(wall=c["Construction"], weakpoint=c["WeakPoint"])

            if attachedsiegetowers is not None:
                for c in climbings:
                    if factory.IsWall(c["Construction"]):
                        self.EvolveWall(wall=c["Construction"], weakpoint=c["WeakPoint"])

            if (climbings is not None) or (attachedsiegetowers is not None):
                self.CreateCastleShape()

        # Because the castle shape has changed, the castle placement on the battlefield grid has to be updated too
        if battlefield is not None:
            self.DeployInBattleField(battlefield)

        return True

    def EvolveWall(self, wall, weakpoint, canvas=None):
        # Evolves given wall splitting it by given weak point and inserting a tower, or upgrading any existent tower
        # WARNING: This method just evolves the related object, but not updates its related deployed battaions or the deployment in the battlefield

        factory = ConstructionFactory()

        # Search both joins to given object
        # Be aware about the connectivity. The castle should be closed, but this is not a requirement. Obviously, if the castle is opeened, it should be at the start and
        # end of wall sequence. In addittion, be aware also with towers
        i = 0
        found = False
        while (i < len(self.__joins)) and not found:
            c1 = self.__joins[i].GetFirstConnected()
            c2 = self.__joins[i].GetSecondConnected()

            if c1 == wall:
                if i == 0:
                    j = len(self.__joins) - 1
                else:
                    j = i - 1

                if self.__joins[j].GetSecondConnected() == wall:
                    jprev = self.__joins[j]
                else:
                    jprev = None

                jnext = self.__joins[i]
                insertjoinindex = i

                found = True

            elif c2 == wall:
                jprev = self.__joins[i]

                if (i + 1) >= len(self.__joins):
                    j = 0
                else:
                    j = i + 1

                if self.__joins[j].GetFirstConnected() == wall:
                    jnext = self.__joins[j]
                    insertjoinindex = j
                else:
                    jnext = None
                    insertjoinindex = len(self.__joins)

                found = True

            i += 1

        if not found:
            print 'ERROR: Given wall cannot evolve due it does not exist!!'
            return False

        # Get the splitting point projecting the weakpoint on the wall axis
        wp = Point2D().SetFrom3D(wall.Project(weakpoint, wallside=3))

        # Create the tower 
        tower = factory.newConstruction("Tower")

        """
        # Get the adjacent objects and distances
        tlst = []
        if (jprev != None):
            dist = wall.GetStartPosition().Distance(wp)
            t = jprev.GetFirstConnected()
            if (factory.IsTower(t)):
                tlst.append({'distance': dist, 'tower': t})
        if (jnext != None):
            dist = wall.GetEndPosition().Distance(wp)
            t = jnext.GetSecondConnected()
            if (factory.IsTower(t)):
                tlst.append({'distance': dist, 'tower': t})
        
        # Check the weakpoint for each adjacent object
        changedtomiddle = False
        for tl in tlst:
            
            # Increase the required distance by adjacent tower dimensions
            if (factory.IsRoundedTower(tl['tower'])):
                distrequired = required + tl['tower'].GetRadius()
            elif (factory.IsSquaredTower(tl['tower'])):
                distrequired= required + math.sqrt(2.0 * (tl['tower'].GetSideLength()**2))
            else:
                continue    
                
            # If the weakpoint has changed to the middle of the wall, we only need to check if this middle point is enough for the other tower
            if (changedtomiddle):
                if (distrequired > (wall.GetLength() / 2.0)):
                    Log(wall.GetLabel() + " cannot be evolved due none new tower can be placed!", VERBOSE_CASTLEEVOLUTION)
                    return
            
            # Change the weakpoint if it is too close to the tower
            if (distrequired > tl['distance']):
                wp = Segment2D(wall.GetStartPosition(), wall.GetEndPosition()).GetMidPoint()
                changedtomiddle = True
                # Check if the middle point is enough good
                if (distrequired > (wall.GetLength() / 2.0)):
                    Log(wall.GetLabel() + " cannot be evolved due none new tower can be placed!", VERBOSE_CASTLEEVOLUTION)
                    return
                else:
                    Log(wall.GetLabel() + " has changed the weakest point by its middle point due weakpoint its too close to a tower", VERBOSE_CASTLEEVOLUTION)
                    
        """

        # Check if the wall has towers at its vertices. If not, avoid to split the wall to insert a new tower. Just insert a tower between the two walls without one
        if (jprev is not None) and (factory.IsWall(jprev.GetFirstConnected())):

            self.__parts["Towers"].append(tower)
            jnew = jprev.InserCornerTower(tower, Vector2D().SetFrom3D(wall.GetNormalVector()))
            self.__joins.insert(insertjoinindex, jnew)

            Battles.Utils.Message.Log("Wall Evolution: Tower added)", Battles.Utils.Message.VERBOSE_RESULT)


        elif (jnext is not None) and (factory.IsWall(jnext.GetSecondConnected())):

            self.__parts["Towers"].append(tower)
            jnew = jnext.InserCornerTower(tower, Vector2D().SetFrom3D(wall.GetNormalVector()))
            self.__joins.insert(insertjoinindex + 1, jnew)

            Battles.Utils.Message.Log("Wall Evolution: Tower added)", Battles.Utils.Message.VERBOSE_RESULT)

        else:

            # Check if is closer to any tower. If it is, evolve the tower if current year allows the evolution. Otherwise, choose the middle wall point

            # The "closer" condition will be the double of the required space around the tower to place another tower
            requiredfactor = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Tower', 'RequiredDistanceNeighborFactor',
                                                                   default=3.0, required=False)
            required = tower.GetRequiredAroundSpace() * requiredfactor

            # Get the closer wall vertex to the weak point
            closertower = self.GetCloserWallTower(wall, wp)
            if closertower:
                dist = wp.Distance(closertower.GetPosition())

                if dist <= required:
                    # Evolve the related tower
                    if self.EvolveTower(closertower):
                        return True

            # At this point, or the closer tower cannot be evolved (due current year), or the weak point is not enough close to any tower, or the wall does not have towers
            # Therefore, split the wall

            # But before, check if there is enough space
            # Required is multiplied by 2 because when wall will be splitted the other tower required space has to be considered too
            if wall.GetLength() < (required * 2.0):
                Battles.Utils.Message.Log("Wall Evolution: Not enough space to place the tower)",
                                          Battles.Utils.Message.VERBOSE_RESULT)
                return False

            """
            # Checks the splitting position. If it is too close to any tower, discard it and get a central wall point

            # Get an initial required space
            required = tower.GetRequiredAroundSpace()

            dist1 = wall.GetStartPosition().Distance(wp)
            dist2 = wall.GetEndPosition().Distance(wp)
            if ((dist1 < required) or (dist2 < required)):
                if (required > (wall.GetLength() / 2.0)):
                    Log(wall.GetLabel() + " cannot be evolved due a new tower cannot be placed!", VERBOSE_CASTLEEVOLUTION)
                    return False
                else:
                    Log(wall.GetLabel() + " has changed the weakest point by its middle point due weakpoint its too close to a tower", VERBOSE_CASTLEEVOLUTION)
                    wp = Segment2D(wall.GetStartPosition(), wall.GetEndPosition()).GetMidPoint()
            """

            # Hacking the tower in cluster position -> Too many wrong cases in short walls or too angular cases
            # Just split by the mid point or evolve side towers
            wp = wall.GetMidPoint()

            # Split the wall and inserts a new tower
            newprevwall = factory.newConstruction("Wall")
            newnextwall = factory.newConstruction("Wall")
            newprevwall.SetPosition(wall.GetStartPosition(), wp)
            newnextwall.SetPosition(wp, wall.GetEndPosition())

            # Update the castle joins structure
            if jprev is not None:
                jprev.SetSecondConnected(newprevwall)
            if jnext is not None:
                jnext.SetFirstConnected(newnextwall)

            jnew = Construction.Join(newprevwall, newnextwall)
            self.__joins.insert(insertjoinindex, jnew)

            # Insert the new tower in the new join. This means a new join to place the tower between both
            self.__parts["Towers"].append(tower)
            jnew2 = jnew.InserCornerTower(tower, Vector2D().SetFrom3D(wall.GetNormalVector()))
            self.__joins.insert(insertjoinindex + 1, jnew2)

            # Remove the wall from lists and insert the new ones
            i = 0
            found = False
            while (i < len(self.__parts["Walls"])) and not found:
                if self.__parts["Walls"][i] == wall:
                    found = True
                    self.__parts["Walls"][i] = newnextwall
                    self.__parts["Walls"].insert(i, newprevwall)
                i += 1

            if not found:
                print 'ERROR: Wall not found in castle walls list when its evolving'
                return False

            if canvas:
                wall.ClearDraw(canvas)
            del wall

            Battles.Utils.Message.Log("Wall Evolution: New tower added)", Battles.Utils.Message.VERBOSE_RESULT)

        return True

    def GetCloserWallTower(self, wall, point):
        # Return the tower of given wall that is closer o the given point, or none if wall does not have towers

        factory = ConstructionFactory()

        # Get both towers (if any)
        index = self.GetIndexJoinFromConstruction(constr=wall, nextt=False)
        t2 = self.__joins[index].GetSecondConnected()
        if not factory.IsTower(t2):
            t2 = None
        t1 = self.__joins[index - 1].GetFirstConnected()
        if not factory.IsTower(t1):
            t1 = None
        if (t1 is None) and (t2 is None):
            return None

        # Get the closer tower
        if t1 is None:
            t = t1
        elif t2 is None:
            t = t2
        else:
            d1 = point.Distance(t1.GetPosition())
            d2 = point.Distance(t2.GetPosition())
            if d1 <= d2:
                t = t1
            else:
                t = t2

        # Check if the closer is upgradable
        if factory.IsSquaredTower(t) and factory.IsRoundedTowerTime():
            return t
        elif factory.IsRoundedTower(t) and factory.IsBastionTime():
            return t
        else:
            return None

    def EvolveTower(self, tower):
        # Evolves the tower to its next stage
        # WARNING: This method only upgrades the tower, but not updates related data, such are given tower battalions or battlefield deployment

        factory = ConstructionFactory()

        index = self.GetIndexJoinFromConstruction(constr=tower, nextt=False)

        # Get adjacent walls
        wall_next = self.__joins[index].GetSecondConnected()
        wall_prev = self.__joins[index - 1].GetFirstConnected()

        # Check required space to evolve tower
        wall_prev_length = wall_prev.GetLength()
        wall_next_length = wall_next.GetLength()

        # Get neighbor towers
        index_prev = self.GetIndexJoinFromConstruction(constr=wall_prev, nextt=True)
        tower_prev = self.__joins[index_prev].GetFirstConnected()
        required_prev = 0
        if (tower_prev is not None) and factory.IsTower(tower_prev):
            required_prev = tower_prev.GetRequiredAroundSpace()

        index_next = self.GetIndexJoinFromConstruction(constr=wall_next, nextt=False)
        tower_next = self.__joins[index_next].GetSecondConnected()
        required_next = 0
        if (tower_next is not None) and factory.IsTower(tower_next):
            required_next = tower_next.GetRequiredAroundSpace()

        # Create a new evolved tower to replace the given one
        if factory.IsSquaredTower(tower) and factory.IsRoundedTowerTime():
            # Evolve to rounded tower
            newtower = factory.newConstruction("RoundedTower")
            Battles.Utils.Message.Log("Wall Evolution: Tower evolved to rounded", Battles.Utils.Message.VERBOSE_RESULT)

        elif factory.IsRoundedTower(tower) and factory.IsBastionTime():
            # Evolve to bastion
            newtower = factory.newConstructionBastion()
            Battles.Utils.Message.Log("Wall Evolution: Tower evolved to bastion", Battles.Utils.Message.VERBOSE_RESULT)
        else:
            # No more evolutions are possible
            return None

        # Check required space with the new tower
        requiredspace = newtower.GetRequiredAroundSpace()
        if (((requiredspace + required_prev) >= wall_prev_length) or (
                (requiredspace + required_next) >= wall_next_length)):
            Battles.Utils.Message.Log("Wall Evolution: Not enough space to evolve the tower",
                                      Battles.Utils.Message.VERBOSE_RESULT)
            return None

        # Replace given tower by the new one on the joins list
        self.__joins[index].SetFirstConnected(newtower)
        self.__joins[index - 1].SetSecondConnected(newtower)

        # Regenerates its geometry
        newtower.SetPosition(tower.GetPosition(), self.__joins[index - 1].GetFirstConnected(),
                             self.__joins[index].GetSecondConnected(), self.__orientation)

        # WARNING: Now we should refresh two sets: army deployment, and tower deployment on the battlefield

        return newtower

    def SetMoat(self, thickness=Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Moat', 'Width'),
                depth=Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Moat', 'Depth'), haswater=True):
        # Sets the moat data. The moat shape cannot be defined until whole the castle is deployed on the battlefield 

        factory = ConstructionFactory()

        self.__moat = factory.newConstruction("Moat")
        self.__moat.SetThickness(thickness)
        self.__moat.SetDepth(depth)
        self.__moat.SetWater(haswater)

    def DeployMoat(self, battlefield):

        # Deploys the moat by the simplest way. Get all battlefield cells where the castle has been deployed, and expand them in all directions
        # This is a good solution since the goal is to define "walk-hard" battlefield cells

        if self.__moat is None:
            return

        cells = []
        for part in self.__parts.values():
            for c in part:
                cells += c.GetBattlefieldCells()

        self.__moat.ConstructFromCells(cells)

        # This is just a visual improvementt, so internal castle cells are never reached by enemies
        self.__moat.CropInside(self.GetCastleHull())

    def GetMoat(self):
        return self.__moat

    def GetWall(self, index):
        # Returns the wall by index
        if index > len(self.__parts["Walls"]):
            return None
        return self.__parts["Walls"][index]

    def GetWallsList(self):
        return self.__parts["Walls"]

    def GetTowersList(self):
        return self.__parts["Towers"]

    def GetTower(self, index):
        # Returns the tower by index
        if index > len(self.__parts["Towers"]):
            return None
        return self.__parts["Towers"][index]

    def GetCloserTower(self, point):
        # Returns the tower that is enough close to given 2D point. Otherwise, returns None
        for t in self.__parts["Towers"]:
            if t.IsCloser(point):
                return t
        return None

    def GetBastionsList(self):
        ret = []

        factory = ConstructionFactory()
        for t in self.__parts["Towers"]:
            if factory.IsBastion(t):
                ret.append(t)

        return ret

    def HasBastions(self):

        factory = ConstructionFactory()
        for t in self.__parts["Towers"]:
            if factory.IsBastion(t):
                return True

        return False

    def SetWallsResistance(self, r):

        self.__wallsResistance = r
        for w in self.__parts["Walls"]:
            w.GetTileManager().SetResistance(r)

    def GetWallsResistance(self):
        return self.__wallsResistance

    def GetClosestConstruction(self, populated, posfrom, tilesrequired, reachable):
        # Returns the closest construction element from given position
        # If populated is true, only returns the constructions populated with any battalion
        # If tilesrequired is true, only search on construction objects with tiles
        # If reachable is true, the construction must be reachable (any battalion can reach it on the battlefield)

        mindist = -1
        obj = None

        for parts in self.__parts.values():
            for constr in parts:
                if (((constr.HasBattalions() and populated) or not populated)
                        and ((constr.HasTiles() and tilesrequired) or not tilesrequired)
                        and ((reachable and constr.IsReachable()) or not reachable)
                ):

                    dist = constr.DistanceFromPoint(posfrom, True)
                    if (dist > 0) and ((obj is None) or (dist < mindist)):
                        mindist = dist
                        obj = constr

        return obj

    def GetClosestWall(self, populated, posfrom):
        # Like GetClosestConstruction, but only with walls (and reachable)
        mindist = -1
        obj = None

        for w in self.__parts["Walls"]:
            if ((w.HasBattalions() and populated == True) or (populated == False)) and w.IsReachable():

                dist = w.DistanceFromPoint(posfrom, True)
                if (dist > 0) and ((obj is None) or (dist < mindist)):
                    mindist = dist
                    obj = w

        return obj

    def GetConstructionByLabel(self, label):
        # Returns the construction object with the same label

        found = False
        for constr in self.__parts.values():
            i = 0
            while (i < len(constr)) and not found:
                if constr[i].GetLabel() == label:
                    found = True
                    return constr[i]
                i += 1

        return None

    def GetConstructionAdjacentConstructions(self, constr):
        # Return a list with joined construction parts with given construction object. Usually, it would be a list of two
        # This method follows the joins structure and don't use the ajdacenConstructions member data of each construction object

        ret = []

        i = 0
        while i < len(self.__joins):
            c1 = self.__joins[i].GetFirstConnected()
            c2 = self.__joins[i].GetSecondConnected()

            if c2 == constr:
                ret.append(c1)
                if i >= (len(self.__joins) - 1):
                    c3 = self.__joins[0].GetSecondConnected()
                else:
                    c3 = self.__joins[i + 1].GetSecondConnected()
                ret.append(c3)
                return ret
            elif c1 == constr:
                ret.append(c2)
                if i == 0:
                    c3 = self.__joins[-1].GetFirstConnected()
                else:
                    c3 = self.__joins[i - 1].GetFirstConnected()
                ret.append(c3)
                return ret

            i += 1

        return ret

    def GetIndexJoinFromConstruction(self, constr, nextt=True):
        # Returns the index of join that contains given construction object. If next is true returns the join that has the object at second link

        i = 0
        while i < len(self.__joins):

            if nextt:
                c = self.__joins[i].GetSecondConnected()
            else:
                c = self.__joins[i].GetFirstConnected()

            if c == constr:
                return i

            i += 1

        return None

    def GetWallAdjacentWall(self, wall, previous):
        # Return the previous or next wall of given one

        if previous:

            index = self.GetIndexJoinFromConstruction(constr=wall, nextt=True)
            if index is None:
                return None

            return self.__joins[index - 1].GetFirstConnected()

        else:

            index = self.GetIndexJoinFromConstruction(constr=wall, nextt=False)
            if index is None:
                return None

            if index == len(self.__joins):
                index = 0
            else:
                index += 1

            return self.__joins[index].GetSecondConnected()

    def InsertTowerBetweenWalls(self, wall1, wall2):
        # Creates a new tower and place it between given walls
        # Returns the new tower

        factory = ConstructionFactory()

        tower = factory.newConstruction("Tower")
        tower.SetPosition(wall1.GetEndPosition(), wall1, wall2, self.__orientation)

        j1 = Construction.Join(wall1, tower)
        j2 = Construction.Join(tower, wall2)

        self.__parts["Towers"].append(tower)

        # Search for the join between the two walls. It has to be deleted and the new ones have to be inserted in the same position
        i = 0
        j = self.__joins[0]
        while (j.GetFirstConnected() != wall1) and (j.GetSecondConnected() != wall2) and (i < len(self.__joins)):
            i += 1
            j = self.__joins[i]

        if i >= len(self.__joins):
            print "ERROR: Cannon insert a tower between two walls because both walls are not joined"
            return None

        self.__joins.insert(i, j1)
        self.__joins[i + 1] = j2

        self.__joins[i].JoinShapes()
        self.__joins[i + 1].JoinShapes()

        return tower

    def IsDefeated(self):
        """
        # The goal of cannons is to make a big hole in the wall to create a gateway for the soldiers. The hole is created on the top part of walls, from top to down. 
        # For each hole, more scratch fall on floor, creating  a gateway. So, the castle is never defeated until the troops enter on it
        return False
        """

        # Returns true if castle is defeated
        for part in self.__parts.values():
            for constr in part:
                if constr.IsDefeated():
                    return True

        return False

    def GetDefeatReason(self):
        # Returns a Result object if castle is defeated (None otherwise)
        for part in self.__parts.values():
            for constr in part:
                if constr.IsDefeated():
                    return constr.GetDefeatReason()
        return None

    def Respawn(self):
        # Respawn any defeated castle part        
        for part in self.__parts.values():
            for constr in part:
                constr.Respawn()

    def DeployInBattleField(self, battlefield):
        # Deploys current castle parts into given battlefield. Each battlefield cell will be linked with all  castle parts that interesect with it        
        for part in self.__parts.values():
            for constr in part:
                constr.DeployInBattleField(battlefield)

        # Deploy the moat around the castle
        self.DeployMoat(battlefield)

        # Mark the castle interior cells as city cells
        self.__oldTown.DeployInBattleField(battlefield)

        # Check those walls that are unreachable due there are towers too close or the wall is too short. Note that this depends on the battlefield grid size
        for w in self.__parts["Walls"]:
            w.CheckReachable()

    def Reset(self):
        # Reset all the castle data except the shape        
        for part in self.__parts.values():
            for constr in part:
                constr.Reset()

    def ClearDraw(self, canvas):
        for part in self.__parts.values():
            for constr in part:
                constr.ClearDraw(canvas)

    def RayHitTest(self, ray, exclude):
        # Checks if given ray intersects with any castle part, except for given exclude object        
        for part in self.__parts.values():
            for constr in part:
                if constr != exclude:
                    if constr.RayHitTest(ray):
                        return True
        return False

    def RayHitTest_Closest(self, ray, exclude, distance):
        # Checks if given ray intersects with any castle part, except for given exclude object, and the distance is less than given
        # Returns the intersected object, or None otherwise        
        for part in self.__parts.values():
            for constr in part:
                if constr != exclude:
                    if constr.RayHitTest(ray):
                        if ray.GetLength() < distance:
                            return constr
                        else:
                            ray.Reset()
        return None

    def DeployBattalions(self, army, battalions, placementtype, linespercell, command=Command.DEFEND_CASTLE):
        # Deploy battalions on all construction parts
        for part in self.__parts.values():
            for constr in part:
                constr.DeployBattalions(army=army, battalions=battalions, placementtype=placementtype,
                                        linespercell=linespercell, command=command)

    def UnDeployBattalions(self):
        # Reset castle defending lines (not kill them)
        for part in self.__parts.values():
            for constr in part:
                constr.UnDeployBattalions()

    def GetAllBattalions(self):
        # Return a list with all castle deployed battalions
        lst = []
        for part in self.__parts.values():
            for constr in part:
                lst.extend(constr.GetAllBattalions())

        return lst

    def ConvertAllTowersToBastions(self, bastioncircleradius, canvas=None):

        reshape = False
        factory = ConstructionFactory()
        it = 0
        while it < len(self.__parts['Towers']):

            t = self.__parts['Towers'][it]

            if ((not factory.IsBastion(t)) or (
                    factory.IsBastion(t) and (t.GetVirtualCircleRadius() != bastioncircleradius))):

                # Transform a tower to a bastion (or update a bastion to its new size

                reshape = True

                # Check the available space from the previous tower
                ijoin = self.GetIndexJoinFromConstruction(t, nextt=False)
                ijoin -= 2
                prevtower = self.__joins[ijoin].GetFirstConnected()
                tdist = t.GetPosition().Distance(prevtower.GetPosition())
                tspace = prevtower.GetRequiredAroundSpace()
                if ((tdist - (tspace + bastioncircleradius)) <= Battles.Utils.Settings.SETTINGS.Get_F('Castle',
                                                                                                      'Bastion',
                                                                                                      'MinDistance')):
                    currbastionsize = tdist - tspace - Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Bastion',
                                                                                             'MinDistance')
                    if currbastionsize <= 0:
                        print "ERROR ConvertAllTowersToBastions: There arent enough space to convert the tower to a bastion"
                        continue
                else:
                    currbastionsize = bastioncircleradius

                # Creates the bastion object
                b = factory.newConstructionBastion()
                b.SetVirtualCircleRadius(currbastionsize)

                # Search and update the current tower join with new bastion
                found = False
                i = 0
                while i < len(self.__joins) and not found:

                    currjoin = self.__joins[i]
                    if currjoin.GetFirstConnected() == t:

                        # Update the join links
                        currjoin.SetFirstConnected(b)
                        if i == 0:
                            self.__joins[len(self.__joins) - 1].SetSecondConnected(b)
                            wallA = self.__joins[len(self.__joins) - 1].GetFirstConnected()
                        else:
                            self.__joins[i - 1].SetSecondConnected(b)
                            wallA = self.__joins[i - 1].GetFirstConnected()

                        found = True

                        # Update tower position and force its reshape
                        wallB = currjoin.GetSecondConnected()
                        b.SetPosition(t.GetPosition(), wallA, wallB, self.__orientation)


                    elif currjoin.GetSecondConnected() == t:

                        # Update the join links
                        self.__joins[i].SetSecondConnected(b)
                        if i == (len(self.__joins) - 1):
                            self.__joins[0].SetFirstConnected(b)
                            wallB = self.__joins[0].GetSecondConnected()
                        else:
                            self.__joins[i + 1].SetFirstConnected(b)
                            wallB = self.__joins[i + 1].GetSecondConnected()

                        found = True

                        # Update tower position and force its reshape
                        wallA = currjoin.GetFirstConnected()
                        b.SetPosition(t.GetPosition(), wallA, wallB, self.__orientation)

                    i += 1

                if canvas:
                    t.ClearDraw(canvas)

                self.__parts['Towers'][it] = b

            it += 1

        if reshape:
            # Regenerates the walls and bastion shapes
            self.CreateCastleShape()

    def ConstructStarFortress(self, canvas=None):
        # Before the construction, we have to convert all towers to bastions. Otherwise, the star fortress algorithm will fail
        # Given canvas is used to refresh the display for the removed towers. It is optional

        data = StarFortressData()
        self.ConvertAllTowersToBastions(data.BastionRadius, canvas)

        # Creates the fortress    
        self.__starfortress.SetData(data)
        self.__starfortress.Create()

    # DEPRECATED
    # Old castle union method -> Too much bugs. Do not use with the castle set data structure
    def CastleUnion(self, castle):

        # Check if current and given castles intersect, and calculate the curtain wall union
        # A intersection between structures means that current castle wall will start to follow the given castle walls, following the shape until the other intersection is found
        # The given castle parts that match with new current castle parts will become hidden to avoid display overlapping
        # Both castles must be fully constructed (curtain wall, towers and bastions)
        # This method only should be called from castle evolution context, where the given castle is the older and current is the newer. So, the given castle has to be smaller
        # and inside (fully or not) the current one

        # Note that the union boolean operation with 2D shapes is not obvious due the high number of combinations. But in this case, and because this method is used from the 
        # city evolution context, we are sure that there arent holes. But since we are sure that current castle is convex, the given on not. By example, think about the union of 2
        # convex polygons. The result is ever a non-convex polygon.

        # So, the algorithm starts to follow the new castle shape. When an intersection is found, match the new shape with the old one. To do it use a simple rule:
        #    If the intersected object is a wall, get the attached towers and choose the closer one. Otherwise, use the intersected tower. Then, create a new join between
        #    the wall and selected tower
        # The algorithm continues until a new intersection is found, that means that we are "exiting" from old castle. The rule in this case is the same, but swapping it
        # See the __UnionConstructions method to know more about it

        # Some final considerations:
        #    The walls and towers use a visited flag to avoid infinite loops and intersections with already intersected objects. This can produce a side effect. Just imagine a wall
        #    intersected two times. Let this case as a future TODO
        #    The new castle starting wall must to be checked for the case when it intersects with castle. Remember that the curtain walls ever start from the bottom-left edge and
        #    follow the walls in clockwise sorting order
        #    If two towers intersect, one of them is removed/replaced by the other
        #    Bastions are too hard to consider due its geometry dependent from adjacent walls. For the moment, they are not allowed
        #    Im SURE that there will be any case that fails. So, this method will be in BETA mode for a long long time

        # More final considerations:
        #    Sometimes, the outcoming wall/tower falls inside the old castle. For that reason, a simple ray-casting is done for the tower position, or wall second position, to know
        #    if it falls inside or outside the oldcastle. In addition, the same method is used to solve those cases when a curtain wall intersects many times with the same wall. This
        #    case is checked only on the outcoming situation, by the nature of the incoming algorithm. When an interior outcoming point is detected, the algorithm dont get the next
        #    oldcastle object, but checks the other newcastle parts. When any part intersects, the algorithm takes the next wall/tower. Note that the visited flag is used to mark
        #    the discarded newcastle walls/towers.
        #    Finally, the function returns False if any error happens. Who calls this function must manage what to do in this case

        # A temporal joins list is used to store the progress of the new construction. Later, this join list will be transformed to the final castle structure
        tmpjoins = []

        # print "Castle Union"

        factory = ConstructionFactory()

        # We cannot allow the union with bastions. Althought the convex hull used to construct the current curtain wall contained the bastion vertices, the attempt to join
        # both castle curtain walls can produce several effects if the intersection is done near any bastion
        if self.HasBastions() or castle.HasBastions():
            return

        for part in self.__parts.values():
            for c in part:
                c.visitedFlag = False
        for part in castle.__parts.values():
            for c in part:
                c.visitedFlag = False

        # Get the old castle convex hull. This is used to check the new castle curtain wall doesnt go inside the old castle. This can happens in the exit intersection, when
        # a new castle part intersects the old castle after a previous one has already intersected. The new castle part could be placed inside the old castle. (yeah, I know, too much difficult to explain in words... sorry)
        castlehull = castle.GetCastleHull()

        # Precompute the intersections between all objects in both castles. Each object will be linked to a list of intersected objects
        # sorted by their basis distance. The goal of this algorithm is to avoid such cases when a wall, by example, intersects with two other
        # walls, and one intersection is the input point and the other one is the output point. Because each object updates the visited flag
        # when it is processed, the output point would be discarded, so the crossing wall would be marked as visited by the input point
        intlsts = self.GetAllIntersections(castle)
        newintersections = intlsts[0]
        oldintersections = intlsts[1]

        i = 0
        c = self.__joins[i].GetSecondConnected()

        # The algorithm starts the intersection search at the first stored castle part. If the first part is already intersecting
        # some part of the old castle, the algorithm becomes unstable due the too high cases number to control. The best option
        # , but not the most elegant, is to start the search at some point where there are not intersections
        start = False
        end = False

        while not start and not end:
            if factory.IsWall(c):

                intb = (len(newintersections[c]) > 0)
                # intc = castle.Intersects(constr = c, onlynonvisited = True)
                if not intb:
                    start = True

            if not start:
                i += 1
                if i >= len(self.__joins):
                    end = True
                    i = 0

                c = self.__joins[i].GetSecondConnected()

        finish = c.visitedFlag
        while not finish:

            # Input: Search any intersection with the old castle. If it is found, it is considered as an input intersection

            intc = None
            if len(newintersections[c]) > 0:
                ic = newintersections[c][0]
                newintersections[c].pop(0)

                # An object can intersect with many other objects. If an intersected object has already used/visited, get the 
                # next one in its castle sequence
                if ic.visitedFlag:
                    ici = castle.GetIndexJoinFromConstruction(ic, nextt=True)
                    icicounter = 0
                    while ic.visitedFlag and (icicounter < len(castle.__joins)):
                        if (ici + 1) >= len(self.__joins):
                            ici = 0
                        else:
                            ici += 1
                        ic = castle.__joins[ici].GetSecondConnected()
                        icicounter += 1
                    if ic.visitedFlag:
                        print "ERROR CastleUnion: Cannon find an intersection point due a loop sequence (1)"
                        return False

                intc = ic

            # intc = castle.Intersects(constr = c, onlynonvisited = True)
            c.visitedFlag = True
            if intc:

                # Unify the intersected parts
                if factory.IsWall(c) and (factory.IsWall(intc) or factory.IsTower(intc)):
                    jtower = self.__UnionConstructions(incomingwall=c, outcomingwall=None, stableobject=intc,
                                                       castle=castle, joinslist=tmpjoins)
                    if not jtower:
                        print "ERROR CastleUnion: Error on input wall union. Discarding objects"
                        i += 1
                        if i == len(self.__joins):
                            i = 0
                        c = self.__joins[i].GetSecondConnected()
                        finish = c.visitedFlag
                        # continue
                        return False

                elif factory.IsTower(c) and (factory.IsWall(intc) or factory.IsTower(intc)):
                    # Process the intersection at the last wall, not the intersected tower. With this, we avoid too many cases
                    # Be aware getting the last wall for the starting situations
                    if (len(tmpjoins) > 0) and (factory.IsWall(tmpjoins[-1].GetSecondConnected())):
                        lastwall = tmpjoins[-1].GetSecondConnected()
                    else:
                        lastwall = self.__joins[i - 1].GetSecondConnected()

                    jtower = self.__UnionConstructions(incomingwall=lastwall, outcomingwall=None, stableobject=intc,
                                                       castle=castle, joinslist=tmpjoins)
                    if not jtower:
                        print "ERROR CastleUnion: Error on input tower union. Discarding objects"
                        i += 1
                        if i == len(self.__joins):
                            i = 0
                        c = self.__joins[i].GetSecondConnected()
                        finish = c.visitedFlag
                        # continue
                        return False

                else:
                    print "ERROR CastleUnion: Unknown castle parts to unify on input intersection"
                    i += 1
                    # continue
                    return False

                # Output: From the intersection, follow the old castle path until a new intersection is found. Then, follow again the new castle path (scanline idea)

                # WARNING: Its possible to get an input intersection without any output one. This can happens if some part intersects a small part, and from the intersection point
                # and following the oldcastle path, there are not any other intersection. To solve it, store temporally the sequence. If it founds an output intersection, store
                # it to the joins list. Otherwise, go back to the intersection point and cancel it.
                badintersection = False
                tmptmpjoins = []

                # Get old castle join of tower that starts the old castle shape following
                index_oldjnext = castle.GetIndexJoinFromConstruction(jtower, nextt=True)
                j = index_oldjnext + 1
                found = False
                badcandidate = False

                while not found and (j != index_oldjnext) and not badintersection:

                    oldjnext = castle.__joins[j].GetSecondConnected()

                    # Check inner loops
                    if oldjnext.visitedFlag and not badcandidate:
                        badintersection = True
                        break

                    # Note that we check about the badcandidate flag (see bellow) before resetting to check the previous loop
                    badcandidate = False
                    outc = None

                    if (oldjnext != jtower) and (oldjnext != intc):
                        # outc = self.Intersects(constr = oldjnext, onlynonvisited = True)

                        # Check the intersection for the output sequence
                        if len(oldintersections[oldjnext]) > 0:
                            oc = oldintersections[oldjnext][0]
                            oldintersections[oldjnext].pop(0)

                            # An object can intersect with many other objects. If an intersected object has already used/visited, get the 
                            # next one in its castle sequence
                            if oc.visitedFlag:
                                oci = self.GetIndexJoinFromConstruction(oc, nextt=True)
                                occounter = 0
                                while oc.visitedFlag and (occounter < len(self.__joins)):
                                    oci += 1
                                    if oci >= len(self.__joins):
                                        oci = 0
                                    oc = self.__joins[oci].GetSecondConnected()
                                    occounter += 1

                                if oc.visitedFlag:
                                    print "ERROR CastleUnion: Cannon find an intersection point due a loop sequence (2)"
                                    return False

                            outc = oc

                    oldjnext.visitedFlag = True
                    if outc:

                        # Check possible inner paths. We are searching a new castle part to exit from old castle path. If the 
                        # ending point of this part is inside the old castle hull, it is a bad candidate. This can happens when
                        # the intersection is near to be tangent

                        if factory.IsTower(outc):
                            if castlehull.IsInside(outc.GetPosition()):
                                badcandidate = True
                            else:
                                tmpi = self.GetIndexJoinFromConstruction(outc, nextt=False)
                                nextwall = self.__joins[tmpi].GetSecondConnected()
                                if castlehull.IsInside(nextwall.GetEndPosition()):
                                    badcandidate = True
                                else:
                                    badcandidate = False
                        elif factory.IsWall(outc) and castlehull.IsInside(outc.GetEndPosition()):
                            badcandidate = True
                        else:
                            badcandidate = False

                        if not badcandidate:
                            found = True
                        else:
                            outc.visitedFlag = True
                            # If intersected object is a bad candidate, mark it as visited and check again for intersections
                            # If there are more than one input and output in the same wall, and the first intersection is a badcandidate
                            # we have to check for other candidates, until no more intersections are found
                        """else:
                            tj = Construction.Join(castle.__joins[j].GetFirstConnected(), castle.__joins[j].GetSecondConnected())    
                            tmptmpjoins.append(tj)
                        """

                    else:
                        tj = Construction.Join(castle.__joins[j].GetFirstConnected(),
                                               castle.__joins[j].GetSecondConnected())
                        tmptmpjoins.append(tj)

                    if not badcandidate:
                        j += 1
                        if j == len(castle.__joins):
                            j = 0

                if badintersection or not found:
                    print "ERROR CastleUnion: Wrong input intersection point"

                    # We do not return false here due the recovery algorithm works enough well to allow to continue

                    # There are not any clear solution to this case, so we have an initial and real intersection, but not the final intersection. This happens, sometimes, if
                    # the intersection point is close to a tangent point on both castles.
                    # One solution could be undo all created joins until the first intersection, but this doesnt solve the problem with the real intersection.
                    # The proposed solution keep the initial intersection treatment, but undo all followed path. Then, we get the next outer castle construction element and tries
                    # to join with the current last join in list (remember that the intersection treatment can generate different joins, 1, 2 or 3)
                    # Of course, this solution doesnt solve all cases, but is the less worst solution for now ...  TODO

                    lastobj = tmpjoins[-1].GetSecondConnected()
                    if i >= (len(self.__joins) - 1):
                        nextobj = self.__joins[0].GetSecondConnected()
                    else:
                        nextobj = self.__joins[i + 1].GetSecondConnected()

                    if factory.IsWall(lastobj) and factory.IsTower(nextobj):

                        lastobj.SetPosition(lastobj.GetStartPosition(), nextobj.GetPosition())
                        tj = Construction.Join(lastobj, nextobj)
                        tmpjoins.append(tj)
                        i += 2

                    elif factory.IsTower(lastobj) and factory.IsWall(nextobj):

                        nextobj.SetPosition(lastobj.GetPosition(), nextobj.GetEndPosition())
                        tj = Construction.Join(lastobj, nextobj)
                        tmpjoins.append(tj)
                        i += 2

                    elif factory.IsWall(lastobj) and factory.IsWall(nextobj):
                        if i == (len(self.__joins) - 1):  # ... avoiding branch simplification for debug purposes
                            inext = 1
                        elif i == (len(self.__joins) - 2):
                            inext = 0
                        else:
                            inext = i + 2

                        nexttower = self.__joins[inext].GetSecondConnected()
                        lastobj.SetPosition(lastobj.GetStartPosition(), nexttower.GetPosition())
                        tj = Construction.Join(lastobj, nexttower)
                        tmpjoins.append(tj)
                        i += 3

                    else:
                        if i == (len(self.__joins) - 1):  # ... avoiding branch simplification for debug purposes
                            inext = 1
                        elif i == (len(self.__joins) - 2):
                            inext = 0
                        else:
                            inext = i + 2

                        nextwall = self.__joins[inext].GetSecondConnected()
                        nextwall.SetPosition(lastobj.GetPosition(), nextwall.GetEndPosition())
                        tj = Construction.Join(lastobj, nextwall)
                        tmpjoins.append(tj)
                        i += 3





                elif found:

                    tmpjoins.extend(tmptmpjoins)

                    if factory.IsWall(outc) and (factory.IsTower(oldjnext) or (factory.IsWall(oldjnext))):
                        jtower = self.__UnionConstructions(incomingwall=None, outcomingwall=outc, stableobject=oldjnext,
                                                           castle=castle, joinslist=tmpjoins)
                        if not jtower:
                            print "ERROR CastleUnion: Error on output wall union. Discarding objects"
                            i += 1
                            if i == len(self.__joins):
                                i = 0
                            c = self.__joins[i].GetSecondConnected()
                            finish = c.visitedFlag
                            # continue
                            return False

                        # Update the new castle joins index
                        i = self.GetIndexJoinFromConstruction(outc, nextt=False)

                    elif factory.IsTower(outc) and (factory.IsTower(oldjnext) or (factory.IsWall(oldjnext))):
                        # Get the next wall to the intersected tower

                        i = self.GetIndexJoinFromConstruction(outc, nextt=False)
                        nextwall = self.__joins[i].GetSecondConnected()
                        jtower = self.__UnionConstructions(incomingwall=None, outcomingwall=nextwall,
                                                           stableobject=oldjnext, castle=castle, joinslist=tmpjoins)
                        if not jtower:
                            print "ERROR CastleUnion: Error on output wall union. Discarding objects"
                            i += 1
                            if i == len(self.__joins):
                                i = 0
                            c = self.__joins[i].GetSecondConnected()
                            finish = c.visitedFlag
                            # continue
                            return False

                        if tmpjoins[-1].GetSecondConnected() == self.__joins[i].GetSecondConnected():
                            i += 1

                    else:
                        print "ERROR CastleUnion: Unknown castle parts to unify on output intersection"
                        i += 1
                        # continue
                        return False

                    if factory.IsWall(tmpjoins[-1].GetSecondConnected()):
                        castlehull.IsInside(tmpjoins[-1].GetSecondConnected().GetEndPosition())




            else:

                if len(tmpjoins) == 0:
                    tj = Construction.Join(None, c)
                else:
                    tj = Construction.Join(tmpjoins[-1].GetSecondConnected(), c)

                tmpjoins.append(tj)

                i += 1

            # The algorithm stops when its found a really visited object, closing he path
            if i >= len(self.__joins):
                i = 0

            c = self.__joins[i].GetSecondConnected()
            finish = c.visitedFlag

        # Close the structure
        tmpjoins[0].SetFirstConnected(tmpjoins[-1].GetSecondConnected())

        # Check for the too short walls. Due we are sharing walls and towers between castles, we cannot remove any tower, only those that are from the new castle
        # tmpjoins2 = self.__UnionCasteFilterShort(tmpjoins, castle)
        tmpjoins2 = tmpjoins

        # From the temporal join list, construct the new castle structure
        if tmpjoins2:
            self.__joins = tmpjoins2

        # Update the castle shape with the new joins
        self.CreateCastleShape()
        self.UpdateCurtainWallFromJoins()

        # self.Evolve(climbings = None, attachedsiegetowers = None, battlefield = None)

        castle.__joins = []
        castle.__parts = {"Walls": [], "Towers": []}

        return True

    def __UnionConstructions(self, incomingwall, outcomingwall, stableobject, castle, joinslist):
        # Performs the union between two parts (walls or towers), that intersect, of two different castles (self castle, and given one, that is new castle and old castle respectively)
        # There are two modes: incoming intersection and outcoming intersection
        # For the incoming intersection a new castle part intersects with the old castle. incomingwall is the new castle wall that intersects with stableobject, the old castle part
        # If the new castle intersected part is a tower, incomingwall is the previous wall
        # For the outcoming intersection, the method is similar, but this time with outcomingwall object. outcomingwall is the new castle part, and stableobject the old castle part
        # joinslist is the list of joins to update. Note that the last element in list doesnt contain the intersected object (see main CastleUnion method)
        # Returns the selected tower

        # WARNING: Use this function only from CastleUnion context. It isnt ready to be used out of this context

        factory = ConstructionFactory()

        if incomingwall:

            if factory.IsWall(stableobject):

                # An old castle wall has been intersected by a new castle wall or tower
                # For the second case, the incoming wall is the previous wall to intersected tower (of the new castle)
                # Get the adjacent old castle towers to the intersected wall. Choose the closer tower to the incomingwall
                # If joinslist is empty we are sure that is the first case
                # Otherwise, if is the second case join the previous tower to incomingwall to the incomingwall (check main algorithm to see that they arent yet joined)
                # For both cases, join the incoming wall to the selected tower

                wp = incomingwall.GetStartPosition()
                towers = castle.GetConstructionAdjacentConstructions(stableobject)

                # WARNING!: There can be joined walls without towers!

                if towers[0].visitedFlag and towers[1].visitedFlag:
                    print "ERROR __UnionConstructions - Itself loop"
                    return None  # Looping itself. The algorithm has failed

                # New condition: Choose the closer only if angle after the modification is greater than 90 degrees

                if towers[0].visitedFlag:
                    jtower = towers[1]
                    if factory.IsTower(jtower):
                        closertpos = jtower.GetPosition()
                    else:
                        closertpos = stableobject.GetEndPosition()

                elif towers[1].visitedFlag:
                    jtower = towers[0]
                    if factory.IsTower(jtower):
                        closertpos = jtower.GetPosition()
                    else:
                        closertpos = stableobject.GetStartPosition()

                else:

                    # Check if adjacent constructions are walls or towers. At this point we only need the towers positions. If they are not towers, just use the wall vertex (first or second)
                    if factory.IsTower(towers[0]):
                        post0 = towers[0].GetPosition()
                    else:
                        post0 = stableobject.GetStartPosition()
                    if factory.IsTower(towers[1]):
                        post1 = towers[1].GetPosition()
                    else:
                        post1 = stableobject.GetEndPosition()

                    prevwall = self.GetWallAdjacentWall(incomingwall, previous=True)
                    seg1 = Segment2D(prevwall.GetStartPosition(), prevwall.GetEndPosition())
                    seg2 = Segment2D(seg1.p2, post0)
                    seg3 = Segment2D(seg1.p2, post1)
                    ang1 = seg1.AngleBetween(seg2)
                    ang2 = seg1.AngleBetween(seg3)
                    if (ang1 >= 100.0) and (ang1 <= 260.0):
                        badang1 = True
                    else:
                        badang1 = False
                    if (ang2 >= 100.0) and (ang2 <= 260.0):
                        badang2 = True
                    else:
                        badang2 = False

                    # Be aware here. We dont know if they are towers or walls
                    if badang1:
                        jtower = towers[1]
                        closertpos = post1
                    elif badang2:
                        jtower = towers[0]
                        closertpos = post0
                    else:

                        dist1 = wp.Distance(post0)
                        dist2 = wp.Distance(post1)

                        if dist1 <= dist2:
                            jtower = towers[0]
                            closertpos = post0
                        else:
                            jtower = towers[1]
                            closertpos = post1

                if not incomingwall.SetPosition(incomingwall.GetStartPosition(), closertpos):
                    return None

                if len(joinslist) == 0:
                    tj = Construction.Join(None, incomingwall)
                    joinslist.append(tj)
                else:
                    if not factory.IsWall(joinslist[-1].GetSecondConnected()):
                        tj = Construction.Join(joinslist[-1].GetSecondConnected(), incomingwall)
                        joinslist.append(tj)

                # Here is the point where we have to create the tower if there isnt. Note that we have to create and store the tower in the inner castle first.
                if not factory.IsTower(jtower):

                    if jtower == towers[0]:
                        jtower = castle.InsertTowerBetweenWalls(towers[0], stableobject)
                    else:
                        jtower = castle.InsertTowerBetweenWalls(stableobject, towers[1])

                tj = Construction.Join(incomingwall, jtower)
                joinslist.append(tj)




            elif factory.IsTower(stableobject):

                # A new castle wall or tower has intersected with an old castle tower
                # For the second case, the incomingwall is the previous wall to new castle intersected tower
                # For the first case we need to join the incomingwall previous tower with itself
                # For both cases, join the incoming wall with the old castle intersected tower

                jtower = stableobject
                if not incomingwall.SetPosition(incomingwall.GetStartPosition(), jtower.GetPosition()):
                    return None

                if (len(joinslist) > 0) and not factory.IsWall(joinslist[-1].GetSecondConnected()):
                    tj = Construction.Join(joinslist[-1].GetSecondConnected(), incomingwall)
                    joinslist.append(tj)

                tj = Construction.Join(incomingwall, jtower)
                joinslist.append(tj)



        elif outcomingwall:

            # The union is performed from the stableobject to an outer wall 

            if factory.IsWall(stableobject):

                # Old castle wall intersects with a new castle wall or tower
                # For the second case, given outcomingwall is the next wall to intersected tower
                # Get the two towers adjacent with old castle wall. Choose the closer to the outcomingwall
                # Current joinlist has at the last position the join with previous tower of old castle wall. If selected tower is this, just join the old tower with the new wall
                # Otherwise join the old castle tower with the old castle intersected wall. Then, join this wall with selected tower. Finally, join the selected tower with the outcoming wall
                # Note that we check if he last stored element in joinlist is a tower. This happens when the outcomingwall is the next wall to the intersected tower (second case, as stated before)

                wp = outcomingwall.GetEndPosition()
                towers = castle.GetConstructionAdjacentConstructions(stableobject)

                # WARNING!: There can be joined walls without towers!

                if towers[0].visitedFlag and towers[1].visitedFlag:
                    print "ERROR __UnionConstructions - Itself loop"
                    return None  # Looping itself. The algorithm has failed

                if towers[0].visitedFlag:
                    jtower = towers[1]
                    if factory.IsTower(jtower):
                        closertpos = jtower.GetPosition()
                    else:
                        closertpos = stableobject.GetEndPosition()

                elif towers[1].visitedFlag:
                    jtower = towers[0]
                    if factory.IsTower(jtower):
                        closertpos = jtower.GetPosition()
                    else:
                        closertpos = stableobject.GetStartPosition()

                else:

                    # Check if adjacent constructions are walls or towers. At this point we only need the towers positions. If they are not towers, just use the wall vertex (first or second)
                    if factory.IsTower(towers[0]):
                        post0 = towers[0].GetPosition()
                    else:
                        post0 = stableobject.GetStartPosition()
                    if factory.IsTower(towers[1]):
                        post1 = towers[1].GetPosition()
                    else:
                        post1 = stableobject.GetEndPosition()

                    nextwall = self.GetWallAdjacentWall(outcomingwall, previous=False)
                    seg1 = Segment2D(nextwall.GetStartPosition(), nextwall.GetEndPosition)
                    seg2 = Segment2D(seg1.p2, post0)
                    seg3 = Segment2D(seg1.p2, post1)
                    ang1 = seg1.AngleBetween(seg2)
                    ang2 = seg1.AngleBetween(seg3)
                    if (ang1 < 100.0) or (ang1 > 260.0):
                        badang1 = True
                    else:
                        badang1 = False
                    if (ang2 < 100.0) or (ang2 > 260.0):
                        badang2 = True
                    else:
                        badang2 = False

                    if badang1:
                        jtower = towers[1]
                        closertpos = post1
                    elif badang2:
                        jtower = towers[0]
                        closertpos = post0
                    else:

                        dist1 = wp.Distance(post0)
                        dist2 = wp.Distance(post1)

                        if dist1 <= dist2:
                            jtower = towers[0]
                            closertpos = post0
                        else:
                            jtower = towers[1]
                            closertpos = post1

                if not outcomingwall.SetPosition(closertpos, outcomingwall.GetEndPosition()):
                    return None

                # Here is the point where we have to create the tower if there isnt. Note that we have to create and
                # store the tower in the inner castle first.
                if not factory.IsTower(jtower):

                    if jtower == towers[0]:
                        jtower = castle.InsertTowerBetweenWalls(towers[0], stableobject)
                        tj = Construction.Join(joinslist[-1].GetSecondConnected(), jtower)
                        joinslist.append(tj)
                    else:
                        jtower = castle.InsertTowerBetweenWalls(stableobject, towers[1])
                        tj2 = Construction.Join(stableobject, jtower)
                        if joinslist[-1].GetSecondConnected() != stableobject:
                            tj1 = Construction.Join(joinslist[-1].GetSecondConnected(), stableobject)
                            joinslist.append(tj1)
                        joinslist.append(tj2)

                    joinslist.append(Construction.Join(jtower, outcomingwall))

                else:

                    if jtower == joinslist[-1].GetSecondConnected():
                        tj = Construction.Join(jtower, outcomingwall)
                        joinslist.append(tj)
                    else:
                        if factory.IsTower(joinslist[-1].GetSecondConnected()):
                            tj = Construction.Join(joinslist[-1].GetSecondConnected(), stableobject)
                            joinslist.append(tj)
                            tj = Construction.Join(stableobject, jtower)
                            joinslist.append(tj)

                        tj = Construction.Join(jtower, outcomingwall)
                        joinslist.append(tj)

            elif factory.IsTower(stableobject):

                # Old castle tower intersects with new castle tower or new castle wall
                # For the first case, given outcomingwall is the next wall to intersected tower
                # Join the last in joins list with the old castle tower
                # Join the old castle tower with the outcoming wall

                jtower = stableobject
                if not outcomingwall.SetPosition(jtower.GetPosition(), outcomingwall.GetEndPosition()):
                    return None

                tj = Construction.Join(joinslist[-1].GetSecondConnected(), jtower)
                joinslist.append(tj)
                tj = Construction.Join(jtower, outcomingwall)
                joinslist.append(tj)

        jtower.visitedFlag = True
        return jtower

    # DEPRECATED - TOO MUCH CASES TO SOLVE
    def __UnionCasteFilterShort(self, joinslist, castle):
        # Check for the too short walls. Due we are sharing walls and towers between castles, we cannot remove any tower, only those that are from the new castle

        factory = ConstructionFactory()

        ret = []
        lenjoins = len(joinslist)
        i = 0
        finish = False
        while (i < lenjoins) and not finish:
            w1 = joinslist[i].GetSecondConnected()
            if (factory.IsWall(w1) and (
                    w1.GetLength() < Battles.Utils.Settings.SETTINGS.Get_F('City', 'MinWallLength'))):
                # The modified walls in the union operation are ever the new castle walls. Because we need to remove one of the wall adjacent towers, we have to know what
                # tower is from new castle or from old. Only new castle towers can be removed
                tower1 = joinslist[i].GetFirstConnected()
                if i == (lenjoins - 1):
                    tower2 = ret[0].GetSecondConnected()
                else:
                    tower2 = joinslist[i + 1].GetSecondConnected()

                ht1 = castle.HasConstruction(tower1)
                ht2 = castle.HasConstruction(tower2)

                if ht1 and not ht2:

                    # Remove the second tower and its next wall. Current wall is modified, taking the current position to last position of removed wall

                    if i == (lenjoins - 1):
                        w2 = ret[1].GetSecondConnected()
                        towernext = ret[2].GetFirstConnected()
                        finish = True
                        i = 2
                    elif i == (lenjoins - 2):
                        w2 = ret[0].GetSecondConnected()
                        towernext = ret[1].GetFirstConnected()
                        finish = True
                        i = 1
                    else:
                        w2 = joinslist[i + 2].GetSecondConnected()
                        towernext = joinslist[i + 3].GetFirstConnected()
                        i += 4

                    w2.SetPosition(w1.GetStartPosition(), w2.GetEndPosition())
                    tj = Construction.Join(tower1, w2)
                    ret.append(tj)

                    # Update the next join with the new wall
                    tj = Construction.Join(w2, towernext)
                    ret.append(tj)

                elif not ht1 and ht2:

                    # Remove the first tower. We have to rewind until last tower and modify its wall, placing its
                    # second point to the second tower We have to remove current join and last join. Because the
                    # current join isnt stored yet, we have to remove only the previous one

                    if len(ret) == 0:
                        # Special case: First wall in list
                        joinslist.pop()
                        w2 = joinslist[-1].GetSecondConnected()
                    elif len(ret) == 1:
                        # Special case: Second wall in list
                        ret.pop()
                        w2 = joinslist[-1].GetSecondConnected()
                    else:
                        ret.pop()
                        w2 = ret[-1].GetSecondConnected()

                    w2.SetPosition(w2.GetStartPosition(), w1.GetEndPosition())

                    # Now just store the next join with the modified wall
                    tj = Construction.Join(w2, tower2)
                    ret.append(tj)

                    if (i + 2) >= lenjoins:
                        i = (i + 2) - lenjoins
                        finish = True
                    else:
                        i += 2



                else:
                    # This (not ht1 and not ht2) shouldnt never happens, so the castle wall generation already
                    # process the short walls. The "ht1 and ht2" case its to hard to solve (too much intersections in
                    # a small region) Avoid the tower removing

                    ret.append(joinslist[i])
                    i += 1


            else:
                ret.append(joinslist[i])

                i += 1

        return ret

    def Intersects(self, constr, onlynonvisited, margin=0):
        # Checks if given construction object intersects with any castle part and returns it
        # onlynonvisited parameter emans that only those constructions with visited flag are considered
        # margin parameter is the margin around the intersectable geometry applied to check the intersections

        for w in self.__parts["Walls"]:
            if (onlynonvisited and not w.visitedFlag) or not onlynonvisited:
                if w.Intersects(construction=constr, margin=margin, onlycheck=True):
                    return w

        for t in self.__parts["Towers"]:
            if (onlynonvisited and not t.visitedFlag) or not onlynonvisited:
                if t.Intersects(construction=constr, margin=margin, onlycheck=True):
                    return t

        return None

    def GetAllIntersections(self, castle):
        # Check all possible intersections between current castle and given one. Returns a list of 2 dictionaries
        # with all construction parts of each castle. For each part, a list of intersected objects is attached
        # Format: [ {"Wall_1": [Tower_25, Wall_24], "Tower_1": [], .....}, {"Wall_24: [Wall_1], .....} ] ,
        # where each element is a reference of an object, not its label The lists contain all objects,
        # with or without intersections The intersected objects are sorted by distance

        selfobjs = {}
        otherobjs = {}

        # Populate the lists
        for part in self.__parts.values():
            for c in part:
                selfobjs[c] = []
        for part in castle.__parts.values():
            for c in part:
                otherobjs[c] = []

        # Check the intersections and update the lists when anyone is found
        for selfpart in self.__parts.values():
            for selfc in selfpart:
                for otherpart in castle.__parts.values():
                    for otherc in otherpart:
                        if selfc.Intersects(otherc):
                            if otherc not in selfobjs[selfc]:
                                selfobjs[selfc].append(otherc)
                            if selfc not in otherobjs[otherc]:
                                otherobjs[otherc].append(selfc)

        ret = [selfobjs, otherobjs]

        # Sort by distance each set of intersected objects
        for lst in ret:
            for key, value in lst.items():
                if len(value) > 0:

                    tmplst = []
                    while len(value) > 0:

                        i = 0
                        mind = -1
                        minobj = None
                        while i < len(value):
                            d = key.GetMinDistance(value[i])
                            if (mind == -1) or (d < mind):
                                mind = d
                                minobj = value[i]
                            i += 1

                        tmplst.append(minobj)
                        value.remove(minobj)

                    lst[key] = tmplst

        return ret

    def HasConstruction(self, construction):

        for part in self.__parts.values():
            for c in part:
                if c == construction:
                    return True

        return False

    def UpdateCurtainWallFromJoins(self):
        # Removes current curtain wall objects list and recreate it from the joins list references

        factory = ConstructionFactory()

        self.__parts = {"Walls": [], "Towers": []}

        for j in self.__joins:
            obj = j.GetSecondConnected()
            if factory.IsWall(obj):
                self.__parts["Walls"].append(obj)
            elif factory.IsTower(obj):
                self.__parts["Towers"].append(obj)
            else:
                print "ERROR UpdateCurtainWallFromJoins: Unknown curtain wall object"

    def GetIntersectableSegments(self):

        ret = []
        for part in self.__parts.values():
            for c in part:
                ret.extend(c.GetIntersectableSegments())

        return ret

    def GetBounding(self):

        # Return the bounding castle into a bounding quad

        bound = BoundingQuad()
        for part in self.__parts.values():
            for c in part:
                b = c.GetBounding()
                bound.InsertPoint(b.minPoint)
                bound.InsertPoint(b.maxPoint)

        if self.__starfortress:
            b = self.__starfortress.GetBounding()
            if b:
                bound.InsertPoint(b.minPoint)
                bound.InsertPoint(b.maxPoint)

        return bound

    def GetJoinsPolygon(self):
        # Return a polygon where all vertices are joins centers
        plist = []
        for j in self.__joins:
            jp = j.GetCenterPoint()
            if jp is not None:
                plist.append(jp)

        poly = Polygon2D()
        poly.SetPointsList(plist)
        return poly

    def GetCastleHull(self):

        # Returns a polygon that envolopes the castle

        factory = ConstructionFactory()
        poly = Polygon2D()

        # Do not use only towers. There can be walls without towers

        for j in self.__joins:
            seg = Segment2D()

            obj1 = j.GetFirstConnected()
            obj2 = j.GetSecondConnected()

            if factory.IsWall(obj1):
                seg.p1 = obj1.GetEndPosition()
            elif factory.IsTower(obj1):
                seg.p1 = obj1.GetPosition()
            else:
                continue

            if factory.IsWall(obj2):
                seg.p2 = obj2.GetStartPosition()
            elif factory.IsTower(obj2):
                seg.p2 = obj2.GetPosition()
            else:
                continue
            # print "appending hull:", seg.p1.x, seg.p1.y, seg.p2.x, seg.p2.x
            poly.shape.append(seg)

        return poly

        # poly.SwitchOrientation()        # The curtain wall orientation is not left handed

        """
        lastp = None
        for t in self.__parts["Towers"]:
            if (lastp):
                poly.shape.append(Segment2D(lastp, t.GetPosition().Copy()))
            
            lastp = t.GetPosition()
            
        poly.shape.append(Segment2D(lastp, self.__parts["Towers"][0].GetPosition()))   
        
        return poly
        """
