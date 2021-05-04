from Battles.Utils.Geometry import BoundingQuad
import Battles.Utils.Settings
import Battles.Army.Action as Action
import Battles.Castle.Castle as Castle
from Battles.Castle import Wall, Tower


class CastleSet:
    """ Class to manage a set of castles.
        When a new curtain wall is calculated, a new castle is created. Usually this new castle is the union of the old castle and the new extension. But sometimes
        the new curtain wall falls over from old castle, creating two curtain walls. This class manages the set of castles for each evolution level.
        In addition, each castle will have a reference to its previous castle set.
        
        When the top level of this structure has more than one castle, one of them is designed as commander center. The commander center is the battle goal.
        But the soldiers have to aim to the closest castle, commander center or not. If a non-commander center falls, it is converted to trenches (just for the battle)
    
        See GroupCastles method to know more about the structure

        Members:
        
            Castles: List of castles. Each castle must be disconnected from the other.
            Commander: Castle designed as the commander center. In addition, is also used to get a default castle for those methods than need to work with only one castle of the set
            Defeated: List of defeated castles. They remain inactive while the play runs. When it ends, the defeated castles become valid again and are respawned to the castles list
        
    """

    def __init__(self, empty=False):
        self.__castles = []
        self.__commander = None
        self.__defeated = []
        if not empty:
            c = Castle.Castle()
            self.__castles.append(c)
            self.__commander = c

    def AddCastle(self, c):
        self.__castles.append(c)

    def GetCommander(self):
        return self.__commander

    def GetCastlesList(self):
        return self.__castles

    def GetNCastles(self):
        return len(self.__castles)

    #######################################################################
    # SIMPLE WRAPPER FUNCTIONS (just iterate on the list)
    #######################################################################

    def Draw(self, canvas, viewport, moat=True, city=True, starfortress=False, year=None):
        for c in self.__castles:
            c.Draw(canvas, viewport, moat, city, starfortress)
        self.save(year)

    def save(self, year):
        if year is None:
            year = 'initial'
        f = open('castle_{}.xml'.format(year), 'w')
        f.write('<Castle>\n')
        for c in self.__castles:
            f.write('<Orientation>[{}, {}]</Orientation>\n'.format(c.GetCastleOrientation().val[0],
                                                                   c.GetCastleOrientation().val[1]))
            f.write('<Shape>\n')
            for j in c._Castle__joins:
                if isinstance(j.GetFirstConnected(), Wall.Wall):
                    if isinstance(j.GetSecondConnected(), Tower.Tower):
                        t = j.GetSecondConnected()
                        f.write('<Vertex>\n')
                        f.write('<Point>[{}, {}]</Point>\n'.format(t.GetPosition().x, t.GetPosition().y))
                        f.write('<TowerType>{}</TowerType>\n'.format(j.GetSecondConnected().__class__.__name__))
                        f.write('</Vertex>\n')
                    else:
                        w = j.GetFirstConnected()
                        f.write('<Vertex>\n')
                        f.write('<Point>[{}, {}]</Point>\n'.format(w.GetEndPosition().x, w.GetEndPosition().y))
                        f.write('</Vertex>\n')

            f.write('</Shape>\n')

        f.write('</Castle>')
        f.close()

    def DrawReservedSoldiers(self, canvas, viewport, army):

        for c in self.__castles:
            c.DrawReservedSoldiers(canvas, viewport, army)

    def SetCastleOrientation(self, v):

        for c in self.__castles:
            c.SetCastleOrientation(v)

    def GetCastleOrientation(self):

        # As is defined in SetCastleOrientation, all castles should have the same orientation
        if len(self.__castles) > 0:
            return self.__castles[0].GetCastleOrientation()
        else:
            return None

    def DeployInBattleField(self, battlefield):

        for c in self.__castles:
            c.DeployInBattleField(battlefield)

    def CreateCastleShape(self):

        for c in self.__castles:
            c.CreateCastleShape()

    def GetWallsList(self):

        lst = []
        for c in self.__castles:
            lst.extend(c.GetWallsList())

        return lst

    def GetTowersList(self):

        lst = []
        for c in self.__castles:
            lst.extend(c.GetTowersList())

        return lst

    def GetBastionsList(self):

        lst = []
        for c in self.__castles:
            lst.extend(c.GetBastionsList())

        return lst

    def HasBastions(self):

        for c in self.__castles:
            if c.HasBastions():
                return True

        return False

    def SetWallsResistance(self, r):

        for c in self.__castles:
            c.SetWallsResistance(r)

    def GetWallsResistance(self):
        # As is defined in SetWallsResistance, all walls have the same resistance (TODO: Allow different resistances for different walls)
        if len(self.__castles) > 0:
            return self.__castles[0].GetWallsResistance()
        else:
            return 0.0

    def GetClosestConstruction(self, populated, posfrom, tilesrequired, reachable):

        lst = []
        for c in self.__castles:
            constr = c.GetClosestConstruction(populated, posfrom, tilesrequired, reachable)
            if constr:
                lst.append(constr)

        mindist = -1
        obj = None

        for constr in lst:
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

        lst = []
        for c in self.__castles:
            cw = c.GetClosestWall(populated, posfrom)
            if cw is not None:
                lst.append(cw)

        mindist = -1
        obj = None

        for w in lst:
            if ((w.HasBattalions() and populated == True) or (populated == False)) and w.IsReachable():

                dist = w.DistanceFromPoint(posfrom, True)
                if (dist > 0) and ((obj is None) or (dist < mindist)):
                    mindist = dist
                    obj = w

        if (obj is None) and populated:
            # This should never happens. If is true means that there arent any defender deployed and populated is true (so, it cannot find any closest populated wall)
            # This should be controlled by who calls this function. By the other hand, and to avoid to much crashes, search again for the closest one without "populated" flag
            obj = self.GetClosestWall(False, posfrom)

        return obj

    def GetConstructionByLabel(self, label):

        for c in self.__castles:
            obj = c.GetConstructionByLabel(label)
            if obj:
                return obj

        return None

    def GetConstructionAdjacentConstructions(self, constr):

        lst = []
        for c in self.__castles:
            lst = c.GetConstructionAdjacentConstructions(constr)
            if len(lst) > 0:
                return lst

        return lst

    def GetIndexJoinFromConstruction(self, constr, nextt=True):

        for c in self.__castles:
            i = c.GetIndexJoinFromConstruction(constr, nextt)
            if i is not None:
                return i

        return None

    def GetWallAdjacentWall(self, wall, previous):

        for c in self.__castles:
            obj = c.GetWallAdjacentWall(wall, previous)
            if obj is not None:
                return obj

        return None

    def InsertTowerBetweenWalls(self, wall1, wall2):

        # Search which castle has given walls using one of the wall labels
        for c in self.__castles:

            obj = c.GetConstructionByLabel(wall1.GetLabel())
            if obj == wall1:
                tower = c.InsertTowerBetweenWalls(wall1, wall2)
                return tower

        return None

    def IsDefeated(self):

        # Temporaly functionality: Set defeated if any castle has fallen
        for c in self.__castles:
            if c.IsDefeated():
                return True
        return False
        """# Return true if all castles are defeated (or castles list is empty, that means that all castles have been defeated and stored into defeated castles list)
        for c in self.__castles:
            if (not c.IsDefeated()):
                return False
            
        return True
        """

    def GetActiveDefeatedCastle(self):
        # Return the first active defeated castle (the defeated castle that it is still in the list of active castles)
        for c in self.__castles:
            if c.IsDefeated():
                return c
        return None

    def SetDefeatedCastle(self, castle):
        # Set the given castle as defeated
        for c in self.__castles:
            if c == castle:
                self.__castles.remove(castle)
                self.__defeated.append(castle)

    def GetDefeatReason(self):

        for c in self.__castles:
            r = c.GetDefeatReason()
            if r is not None:
                return r

        return None

    def Respawn(self):

        for c in self.__defeated:
            self.__castles.append(c)
        self.__defeated = []

        for c in self.__castles:
            c.Respawn()

    def Reset(self):

        for c in self.__defeated:
            self.__castles.append(c)
        self.__defeated = []

        for c in self.__castles:
            c.Reset()

    def ClearDraw(self, canvas):

        for c in self.__castles:
            c.ClearDraw(canvas)

    def RayHitTest(self, ray, exclude):

        for c in self.__castles:
            if c.RayHitTest(ray, exclude):
                return True

        return False

    def RayHitTest_Closest(self, ray, exclude, distance):

        for c in self.__castles:
            obj = c.RayHitTest_Closest(ray, exclude, distance)
            if obj is not None:
                return obj

        return None

    def DeployBattalions(self, army, battalions, placementtype, linespercell, command=Action.Command.DEFEND_CASTLE):

        for c in self.__castles:
            c.DeployBattalions(army, battalions, placementtype, linespercell, command)

    def UnDeployBattalions(self):

        for c in self.__castles:
            c.UnDeployBattalions()

    def Intersects(self, constr, onlynonvisited, margin=0):

        for c in self.__castles:
            obj = c.Intersects(constr, onlynonvisited, margin)
            if obj is not None:
                return obj

        return None

    def HasConstruction(self, construction):

        for c in self.__castles:
            if c.HasConstruction(construction):
                return True

        return False

    def UpdateCurtainWallFromJoins(self):

        for c in self.__castles:
            c.UpdateCurtainWallFromJoins()

    def GetIntersectableSegments(self):

        lst = []
        for c in self.__castles:
            lst.extend(c.GetIntersectableSegments())

        return lst

    def GetCloserTower(self, point):
        # Returns the tower that is enough close to given 2D point. Otherwise, returns None
        # Note that this doesnt return the closest one, just the first closer tower

        for c in self.__castles:
            t = c.GetCloserTower(point)
            if t is not None:
                return t

        return None

    def GetHierarchyLevel(self):
        # Return the maximum castles hierarchy level

        maxH = 0
        for c in self.__castles:
            maxH = max(c.GetHierarchyLevel(), maxH)

        return maxH

    def SetGrayed(self):
        # Sets the gray color for all castles in the set
        for c in self.__castles:
            c.SetGrayed()

    def GetCastleHullList(self):
        # Return a list with the castles convex hulls

        lst = []
        if len(self.__castles) == 0:
            print "ERROR: CastleSet::GetCastleHullList -> None castle to get the hull"
        else:
            for c in self.__castles:
                lst.append(c.GetCastleHull())

        return lst

    def GetBounding(self):

        bbquad = BoundingQuad()
        for c in self.__castles:
            b = c.GetBounding()
            bbquad.InsertBounding(b)

        return bbquad

    #######################################################################
    # COMPLEX WRAPPER FUNCTIONS (action over an unknown castle in the list)
    #######################################################################

    def GroupCastles(self, castleset, joinedlist, coveredlist):
        # This is one of the most important methods of the class. It groups the castles, creating the references between castle sets and between the castles that they contain
        # castleset parameter is the previous castle set
        # joinedlist parameter contains the castles that have been joined with the current one
        # coveredlist parameter contains the castles that current castle set covers

        if len(self.__castles) > 1:
            print "WARNING: CastleSet::GroupCastles -> There are more than one castle to group the others. Choosing the commander"

        if len(self.__castles) == 0:
            print "ERROR: CastleSet::GroupCastles -> Castle set is empty"

        if self.__commander is None:
            print "ERROR: CastleSet::GroupCastlell-> No commander defined"
            return

        # Check if commander covers all previous castles
        if len(coveredlist) > 0:

            fullcover = True
            i = 0
            while (i < len(castleset.__castles)) and fullcover:
                if castleset.__castles[i] not in coveredlist:
                    fullcover = False
                i += 1

            if fullcover:
                self.__commander.SetInnerCastle(castleset, True)
                return
            if not fullcover:
                # Creates a new castle set to group all covered castles and set it as the inner castle of the commander. Then, append the other castles
                cs = CastleSet(empty=True)
                for c in coveredlist:
                    cs.AddCastle(c)
                cs.__commander = cs.__castles[0]
                self.__commander.SetInnerCastle(cs, True)

                if len(joinedlist) == 0:
                    return

        if len(joinedlist) > 0:

            if len(joinedlist) > 1:
                # If there are many joined parts, store them into a new castle set and assign it as the inner castle
                cs = CastleSet(empty=True)
                for j in joinedlist:
                    cs.__castles.append(j)
                cs.__commander = cs.__castles[0]  # Set the first castle as the commander one, just for convenience
                self.__commander.SetInnerCastle(cs, True)

                # Insert the other castles
                for j in castleset.__castles:
                    if j not in joinedlist:
                        self.__castles.append(j)

                return

            else:
                # If there are only one joined part, set it as the inner castle of the commander
                self.__commander.SetInnerCastle(joinedlist[0], True)

                # Insert the other castles
                for j in castleset.__castles:
                    if j != joinedlist[0]:
                        self.__castles.append(j)

                return
        else:
            # The new castle is disconnected from the old ones
            for c in castleset.__castles:
                self.__castles.append(c)

            return

        # NOTE: The commander is usefull not only to know the simulation goal, also to get a reference to the default
        # castle. This is important on those cases where we need just one castle (and there are more than one castle
        # in the list).

    def WrapOldCity(self, city, margin, battlefieldcenter):

        if len(self.__castles) == 0:
            print "ERROR: CastleSet::WrapCity -> None castle to wrap"
        else:
            if len(self.__castles) > 1:
                print "WARNING: CastleSet::WrapCity -> Castle set with more than one castle. Choosing the commander"

            if self.__commander is None:
                print "ERROR: CastleSet::WrapCity -> Castle set without commmander"
            else:
                self.__commander.WrapOldCity(city, margin, battlefieldcenter)

    def ConstructCurtainWall(self, polyline):

        if len(self.__castles) == 0:
            print "ERROR: CastleSet::ConstructCurtainWall -> None castle where to construct the curtain wall"
        else:
            if len(self.__castles) > 1:
                print "WARNING: CastleSet::ConstructCurtainWall -> Castle set with more than one castle. Choosing the commander"

            if self.__commander is None:
                print "ERROR: CastleSet::ConstructCurtainWall -> Castle set without commmander"
            else:
                self.__commander.ConstructCurtainWall(polyline)

    def ConstructCornerTowers(self):

        if len(self.__castles) == 0:
            print "ERROR: CastleSet::ConstructCornerTowers -> None castle where to construct towers"
        else:
            if len(self.__castles) > 1:
                print "WARNING: CastleSet::ConstructCornerTowers -> Castle set with more than one castle. Choosing " \
                      "the commander "

            if self.__commander is None:
                print "ERROR: CastleSet::ConstructCornerTowers -> Castle set without commmander"
            else:
                self.__commander.ConstructCornerTowers()

    def ConstructCurtainWallWithTowers(self, polylinetowers):

        if len(self.__castles) == 0:
            print "ERROR: CastleSet::ConstructCurtainWallWithTowers -> None castle where to construct towers"
        else:
            if len(self.__castles) > 1:
                print "WARNING: CastleSet::ConstructCurtainWallWithTowers -> Castle set with more than one castle. " \
                      "Choosing the commander "

            if self.__commander is None:
                print "ERROR: CastleSet::ConstructCurtainWallWithTowers -> Castle set without commmander"
            else:
                self.__commander.ConstructCurtainWallWithTowers(polylinetowers)

    def Evolve(self, climbings=None, attachedsiegetowers=None, battlefield=None):

        if len(self.__castles) == 0:
            print "ERROR: CastleSet::Evolve -> None castle to evolve"
        else:
            if len(self.__castles) > 1:
                print "WARNING: CastleSet::Evolve -> Castle set with more than one castle. Choosing the commander"

            if self.__commander is None:
                print "ERROR: CastleSet::Evolve -> Castle set without commmander"
            else:
                return self.__commander.Evolve(climbings, attachedsiegetowers, battlefield)

        return False

    def EvolveWall(self, wall, weakpoint, canvas=None):

        for c in self.__castles:
            constr = c.GetConstructionByLabel(wall.GetLabel())
            if constr is not None:
                return c.EvolveWall(wall, weakpoint, canvas)

        print "ERROR: CastleShape::EvolveWall -> Given wall is attached to a nonpresent castle"
        return False

    def EvolveTower(self, tower):

        for c in self.__castles:
            constr = c.GetConstructionByLabel(tower.GetLabel())
            if constr is not None:
                return c.EvolveTower(tower)

        print "ERROR: CastleShape::EvolveTower -> Given tower is attached to a nonpresent castle"
        return None

    def GetCloserWallTower(self, wall, point):

        for c in self.__castles:
            constr = c.GetConstructionByLabel(wall.GetLabel())
            if constr is not None:
                return c.GetCloserWallTower(wall, point)

        print "ERROR: CastleShape::EvolveWall -> Given wall is attached to a nonpresent castle"
        return None

    def SetMoat(self, thickness=Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Moat', 'Width'),
                depth=Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Moat', 'Depth'), haswater=True):

        if len(self.__castles) == 0:
            print "ERROR: CastleSet::SetMoat -> None castle to set the moat"
        else:
            if len(self.__castles) > 1:
                print "WARNING: CastleSet::SetMoat -> Castle set with more than one castle. Choosing the commander"

            if self.__commander is None:
                print "ERROR: CastleSet::SetMoat -> Castle set without commmander"
            else:
                self.__commander.SetMoat(thickness, depth, haswater)

    def DeployMoat(self, battlefield):
        if len(self.__castles) == 0:
            print "ERROR: CastleSet::DeployMoat -> None castle to deploy the moat"
        else:
            if len(self.__castles) > 1:
                print "WARNING: CastleSet::DeployMoat -> Castle set with more than one castle. Choosing the commander"

            if self.__commander is None:
                print "ERROR: CastleSet::DeployMoat -> Castle set without commmander"
            else:
                self.__commander.DeployMoat(battlefield)

    def GetMoat(self):
        if len(self.__castles) == 0:
            print "ERROR: CastleSet::GetMoat -> None castle to get the moat"
        else:
            if len(self.__castles) > 1:
                print "WARNING: CastleSet::GetMoat -> Castle set with more than one castle. Choosing the commander"

            if self.__commander is None:
                print "ERROR: CastleSet::GetMoat -> Castle set without commmander"
            else:
                return self.__commander.GetMoat()

        return None

    def GetWall(self, index):
        if len(self.__castles) == 0:
            print "ERROR: CastleSet::GetWall -> None castle to get the wall"
        else:
            if len(self.__castles) > 1:
                print "WARNING: CastleSet::GetWall -> Castle set with more than one castle. Choosing the commander"

            if self.__commander is None:
                print "ERROR: CastleSet::GetWall -> Castle set without commmander"
            else:
                return self.__commander.GetWall(index)

        return None

    def GetTower(self, index):
        if len(self.__castles) == 0:
            print "ERROR: CastleSet::GetTower -> None castle to get the tower"
        else:
            if len(self.__castles) > 1:
                print "WARNING: CastleSet::GetTower -> Castle set with more than one castle. Choosing the commander"

            if self.__commander is None:
                print "ERROR: CastleSet::GetTower -> Castle set without commmander"
            else:
                return self.__commander.GetTower(index)
        return None

    def ConvertAllTowersToBastions(self, bastioncircleradius, canvas=None):

        if len(self.__castles) == 0:
            print "ERROR: CastleSet::ConvertAllTowersToBastions -> None castle to convert towers"
        else:
            if len(self.__castles) > 1:
                print "WARNING: CastleSet::ConvertAllTowersToBastions -> Castle set with more than one castle. Choosing the commander"

            if self.__commander is None:
                print "ERROR: CastleSet::ConvertAllTowersToBastions -> Castle set without commmander"
            else:
                self.__commander.ConvertAllTowersToBastions(bastioncircleradius, canvas)

    def ConstructStarFortress(self, canvas=None):
        if len(self.__castles) == 0:
            print "ERROR: CastleSet::ConstructStarFortress -> None castle to create a star fortress"
        else:
            if len(self.__castles) > 1:
                print "WARNING: CastleSet::ConstructStarFortress -> Castle set with more than one castle. Choosing the commander"

            if self.__commander is None:
                print "ERROR: CastleSet::ConstructStarFortress -> Castle set without commmander"
            else:
                self.__commander.ConstructStarFortress(canvas)

    def CastleUnion(self, castle):
        if len(self.__castles) == 0:
            print "ERROR: CastleSet::CastleUnion -> None castle to union"
        else:
            if len(self.__castles) > 1:
                print "WARNING: CastleSet::CastleUnion -> Castle set with more than one castle. Choosing thecommander"

            if self.__commander is None:
                print "ERROR: CastleSet::CastleUnion -> Castle set without commmander"
            else:
                return self.__commander.CastleUnion(castle)

        return False

    def GetAllIntersections(self, castle):
        if len(self.__castles) == 0:
            print "ERROR: CastleSet::GetAllIntersections -> None castle to calculate the intersections"
        else:
            if len(self.__castles) > 1:
                print "WARNING: CastleSet::GetAllIntersections -> Castle set with more than one castle. Choosing the commander"

            if self.__commander is None:
                print "ERROR: CastleSet::GetAllIntersections -> Castle set without commmander"
            else:
                return self.__commander.GetAllIntersections(castle)

        return None

    def GetCastleHull(self):
        # Return the commander convex hull

        if self.__commander is None:
            print "ERROR: CastleSet::GetConvexHull -> None castle to get the convex hull"
        else:
            return self.__commander.GetCastleHull()

        return None
