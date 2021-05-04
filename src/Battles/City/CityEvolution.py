from Tkinter import *

from Battles.Castle.Construction import FORBIDDEN_TOWER_FLAG
from Battles.City.BattleEvent import *
from Battles.Factory import *
import Battles.Utils.Message
import Battles.Utils.Settings
import Battles.Castle.CastleSet as CastleSet
from Battles.Utils.Geometry import *

import random

import pyscreenshot as ImageGrab
import ntpath
import os
import io
import PIL

import timingevent as te


class House:
    """ Defines a city house. In a simple way, a house is only a square. See Defaults file to get the house standard size
    """

    def __init__(self, center):
        self.center = center

    def GetQuad(self):
        return BoundingQuad().FromCenterSize(center=self.center,
                                             size=Battles.Utils.Settings.SETTINGS.Get_F('City', 'Houses', 'Size'))

    def IsInRiver(self, battlefield):
        # Return true if house is in river (or close to)

        # Use the curtain wall distance to check if house is too close, avoiding a possible curtain wall on the water
        margin = Battles.Utils.Settings.SETTINGS.Get_F(category='Castle', tag='CurtainWallOldCityMargin')
        bound = self.GetQuad()
        bound.Expand(margin)
        vertices = bound.GetVertices()

        for v in vertices:
            cell = battlefield.GetCellFromPoint(v)
            if cell and cell.HasRiver():
                return True

        return False


class CityEvolutionPattern:
    """ Defines a city evolution pattern. The evolution has a years range and a vector of evolution. All new houses will be placed in that direction and outside from inner castle
        There are 2 methods of evolution:
            - Using only an expansion direction vector. The city walls are used as segments to start placing houses
            - Using an expansion direction vector and a segment. Like the previous one, but using given segment as starting base
    
        Attributes:
        
        DateRange: List with start and ending years of evolution. The ending year can be None for a constant evolution
        Direction: Vector of direction
        Base: Origin 2D segment where starts the evolution. The segment orientation isnt important, so it is modified automatically to match the segment normal vector with the direction vector
        HousesPerYear: Number of constructed houses per year
        HousesPerYearSlowCounter: Internal counter to control the waiting time in years to create houses
        
        isEvolving: Internal flag to control when the evolution has started
        houses: list with all created houses
        edgehouses: list with houses at the edges of current evolution. They are also stored into houses list
    """

    def __init__(self, startyear, endyear=None, direction=Vector2D(), base=None,
                 housesperyear=Battles.Utils.Settings.SETTINGS.Get_I('City', 'Houses', 'CreationPerYear')):
        self.DateRange = [startyear, endyear]
        self.Direction = direction
        self.Base = base
        self.HousesPerYear = housesperyear
        self.HousesPerYearSlowCounter = 0.0
        self.isEvolving = False
        self.Houses = []
        self.EdgeHouses = []

        # Check the segment orientation. Change its orientation to match the direction vector
        if self.Base:
            normal = self.Base.GetNormal()
            if normal.DotProd(self.Direction) < 0:
                self.Base = Segment2D(self.Base.p2, self.Base.p1)


class CityEvolution:
    """ Manages the whole city evolution, with or without Battles. In fact, Battles are used only to modify the city inner castle structure. But the city grows anyway as time
        advances. The city creates a new castle structure around the whole city when it grows too much
        
        Attributes:
            PlayerData: Basic data for castle, battlefield and armies
            StartCentury: Century when evolution starts
            EndCentury: Century when evolution ends
            CurrentYear: Current year. It must be specified before start the evolution
            EvolutionPatterns: Group of lists of city evolution patterns (see CityEvolutionPattern class). If there are patterns in list that intersect the date ranges, the evolution will
                            be performed by list inserting preference. The groups are used when the curtain wall must to be constructed
            CastleExpansionYears: Dictionary with years when the castle must expand. The dictionary key is the year and the value is another dictionary with extra data, such is 
                                  the pattern group ID:
            StarFortressData: Parmaters for the final star fortress construction. None by default (no final star fortress)
            minWallLength: Minimum wall length when city is expanded
            maxWallLength: Maximum wall length when city is expanded
            battleEvents: List of battle events
            currentBattleEvents: Internal counter for current battle events
            castleExpansionCheckings: List of dates where the system checks the current castle expansion status
            castleExpansionHistory: Castle expansion history. It is a list where each element has the next composition:
                            { "Year": 1999, "FromBattle": True/False }
                            
                            FromBattle value means if the expansion has been done from a battle decision (defenders fall) or it is an user manual decision
            existNewHouses: Internal flag used to control if new houses have been added since the last castle expansion
            marginTimeBetweenExpansions: Minimum years between city expansions
                            
     """

    def __init__(self):

        self._playerData = None
        self._startCentury = 8
        self._endCentury = 19
        self.__evolutionPatterns = {}
        self.__lastAddedHouses = []
        self.__existNewHouses = False

        self._currentYear = (self._startCentury - 1) * 100

        self.__castleExpansionYears = {}

        self._minWallLength = Battles.Utils.Settings.SETTINGS.Get_F(category='City', tag='MinWallLength')
        self._maxWallLength = Battles.Utils.Settings.SETTINGS.Get_F(category='City', tag='MaxWallLength')
        if self._minWallLength > self._maxWallLength:
            self._minWallLength = self._maxWallLength

        self.__tkinter = Tk()
        self.__canvas = None
        self.__canvasTextObj = None
        self.__canvasHouses = []
        self.__viewport = None
        self.__starFortressData = None

        self.__battleEvents = []
        self.__currentBattleEvents = 0

        self.__castleExpansionCheckings = []
        self.__castleExpansionHistory = []  # [ {"Year": 1999, "FromBattle": True/False } ]
        self.__marginTimeBetweenExpansions = 0

    def SetPlayerData(self, data):
        self._playerData = data

    def SetCenturiesRange(self, start, end):
        self._startCentury = start
        self._endCentury = end

        self._currentYear = (self._startCentury - 1) * 100

    def SetWallLengths(self, minlength, maxlength):
        self._minWallLength = minlength
        self._maxWallLength = maxlength
        if self._minWallLength > self._maxWallLength:
            self._minWallLength = self._maxWallLength

    def AddEvolutionPattern(self, groupID, pattern):
        if groupID in self.__evolutionPatterns:
            self.__evolutionPatterns[groupID].append(pattern)
        else:
            self.__evolutionPatterns[groupID] = [pattern]

    def AddCastleExpansionDate(self, year, groupID=0):
        self.__castleExpansionYears[year] = {'GroupID': groupID}

    def AddCastleExpansionChecking(self, year):
        self.__castleExpansionCheckings.append(year)

    def SetFinalStarFortressData(self, data):
        self.__starFortressData = data

    def AddBattleEvent(self, data):
        self.__battleEvents.append(data)

    def Start(self):
        # Starts the evolution

        # Setup the initial player data
        # The initial castle and oldtown is already defined in the player data
        self._playerData.SetTimePeriod(self._startCentury)
        self._playerData.SetLoopsForEachTest(2)  # TODO
        self._playerData.SetMaxCastleEvolutions(5)  # TODO

        self.__canvas = Canvas(self.__tkinter, height=Battles.Utils.Settings.SETTINGS.Get_I('Game', 'WindowHeight'),
                               width=Battles.Utils.Settings.SETTINGS.Get_I('Game', 'WindowWidth'), bg="white")
        self.__canvas.pack()

        # Draw the initial cityshape
        self._playerData.DrawCastleShape(canvas=self.__canvas, city=True, starfortress=False, resetData=False)
        self.__viewport = Viewport(Bounding(Battles.Utils.Settings.SETTINGS.Get_I('Game', 'WindowWidth'),
                                            Battles.Utils.Settings.SETTINGS.Get_I('Game', 'WindowHeight')),
                                   self._playerData.GetBattlefield().GetBounding(), Point2D(x=0.0, y=0.0))
        # Creates here the viewport due it needs the battlefield, that is created in DrawCastleShape method

        # Draw the terrain WARNING/PROBLEM: The terrain elements shouldnt be drawn over the castle. But we need the
        # viewport, that is created with data that is available only after DrawCastleShape is called TODO: Solve it
        self._playerData.DrawTerrain(canvas=self.__canvas, viewport=self.__viewport)

        # Shows the current year
        self.__ShowCurrentYear()

        # Check the minimum wall length to allow bastions placement
        if self.__starFortressData and (self._minWallLength < (self.__starFortressData.BastionRadius * 2.0)):
            self._minWallLength = 2.0 * self.__starFortressData.BastionRadius

        self.__tkinter.after(Battles.Utils.Settings.SETTINGS.Get_I(category='City', tag='EvolutionSpeed'),
                             self.__EvolutionStep)
        print '############################################################'
        print '#    City Evolution Start !!!                              #'
        print '############################################################'
        mainloop()
        print '############################################################'
        print '#    City Evolution End  !!!                               #'
        print '############################################################'

    def __EvolutionStep(self):
        # print "#######################################################  CityEvolution.__EvolutionStep !!!"
        if self.__currentBattleEvents > 0:
            # There are a battle running. Wait until it finishes
            self.__tkinter.after(Battles.Utils.Settings.SETTINGS.Get_I(category='City', tag='WaitBattle'),
                                 self.__EvolutionStep)

        else:

            # Increases one year in the simulation and shows the changes

            # Updates the current year
            self._currentYear += Battles.Utils.Settings.SETTINGS.Get_I(category='City', tag='YearsPerStep')
            self._playerData.SetTimePeriod(math.ceil(self._currentYear / 100))
            self.__ShowCurrentYear()

            # Get the evolution patterns for current year and draw the evolved houses

            # for ch in self.__canvasHouses:
            #    self.__canvas.delete(ch)

            for evolve in self.__evolutionPatterns.values():
                for ep in evolve:
                    if ((self._currentYear >= ep.DateRange[0]) and (
                            (self._currentYear <= ep.DateRange[1]) or (not ep.DateRange[1]))):
                        if not ep.isEvolving:
                            self.__EvolveWithPattern(ep)
                            self.__DrawEvolvedHouses(ep)
                        else:
                            self.__EvolveWithPattern(ep)
                            self.__DrawLastEvolvedHouses(ep)
                    else:
                        ep.isEvolving = False

            # Check the castle expansion checkings
            if self.__castleExpansionCheckings:
                if self._currentYear >= self.__castleExpansionCheckings[0]:
                    self.__CheckCastleExpansions()
                    self.__castleExpansionCheckings.pop(0)

            # Check the castle evolution condition
            # Note that the list is sorted, and for each evolution, the first element is removed
            if self.__castleExpansionYears:
                if self._currentYear in self.__castleExpansionYears:

                    if self.AllowExpansionByHistory():
                        Battles.Utils.Message.Log("CASTLE EXPANSION EVENT (" + str(self._currentYear) + ")",
                                                  Battles.Utils.Message.VERBOSE_RESULT)

                        self.ClearDrawCastle()
                        self.ExpandCastle(groupID=self.__castleExpansionYears[self._currentYear]['GroupID'],
                                          frombattle=False, battlefield=self._playerData.GetBattlefield())
                        self.DrawCastle(starfortress=False)
                        # self.__AutoFitView()
                    else:
                        Battles.Utils.Message.Log(
                            "Scheduled expansion cancelled due a previous one. Year " + str(self._currentYear),
                            Battles.Utils.Message.VERBOSE_RESULT)

            # Check for any battle for this year
            for be in self.__battleEvents:
                if be.year == self._currentYear:
                    Battles.Utils.Message.Log("BATTLE EVENT (" + str(self._currentYear) + ")",
                                              Battles.Utils.Message.VERBOSE_RESULT)

                    head, tail = ntpath.split(self._playerData._Player__data._PlayerDataFromXML__xml._Settings__xmlfilename)
                    filename = os.path.splitext(tail)[0] + '.jpg'

                    te.timing_event_start('BattleEvent', os.path.splitext(tail)[0] + '.txt')
                    self.__currentBattleEvents += 1
                    self.__BattleEvent(be)
                    self.__currentBattleEvents -= 1
                    te.timing_event_stop('BattleEvent', 'Battle event finished (year {0})'.format(self._currentYear), os.path.splitext(tail)[0] + '.txt')

                    self._snapCanvas(filename)

                    # Avoid two Battles or more at the same time
                    self.__battleEvents.remove(be)

                    break

            if self.__currentBattleEvents > 0:
                self.__tkinter.after(Battles.Utils.Settings.SETTINGS.Get_I(category='City', tag='WaitBattle'),
                                     self.__EvolutionStep)

            # Check the ending condition
            if self._currentYear < (self._endCentury * 100):
                self.__tkinter.after(Battles.Utils.Settings.SETTINGS.Get_I(category='City', tag='EvolutionSpeed'),
                                     self.__EvolutionStep)
            else:

                if self.__starFortressData:
                    # self._playerData.GetCastle().ConstructStarFortress(starfortressdata = self.__starFortressData, canvas = self.__canvas)
                    self._playerData.GetCastle().ConstructStarFortress(canvas=self.__canvas)
                    self.DrawCastle(starfortress=True)

                # self.__AutoFitView()

                if self.__canvasTextObj:
                    self.__canvas.delete(self.__canvasTextObj)

                exit(0)

    def _snapCanvas(self, filename):
        canvas = self.__canvas # Get Window Coordinates of Canvas
        ps = canvas.postscript(colormode='color')
        im = PIL.Image.open(io.BytesIO(ps.encode('utf-8')))
        im.save(filename)

    def __ShowCurrentYear(self):
        # Displays the current year on the canvas
        if self.__canvasTextObj:
            self.__canvas.delete(self.__canvasTextObj)

        self.__canvasTextObj = (self.__canvas.create_text(20, 10, text=str(self._currentYear), fill="black"))

    def __AutoFitView(self):

        # Resize the viewport to fit the castle
        bound = self._playerData.GetCastle().GetBounding()
        offset = Point2D(-bound.minPoint.x, -bound.minPoint.y)
        voffset = self.__viewport.W2V(offset)
        # voffset.x += 5
        # voffset.y += 5

        vlength = self.__viewport.W2V_1f(bound.GetLength()) + voffset.x
        vheight = self.__viewport.W2V_1f(bound.GetWidth()) + voffset.y

        if vlength >= vheight:
            if vlength > Battles.Utils.Settings.SETTINGS.Get_I('Game', 'WindowWidth'):
                newfactor = Battles.Utils.Settings.SETTINGS.Get_I('Game', 'WindowWidth') / vlength
            else:
                newfactor = 1.0
        else:
            if vheight > Battles.Utils.Settings.SETTINGS.Get_I('Game', 'WindowHeight'):
                newfactor = Battles.Utils.Settings.SETTINGS.Get_I('Game', 'WindowHeight') / vheight
            else:
                newfactor = 1.0

        # self.__canvas.scale("all", 0, 0, newfactor, newfactor)
        # self.__canvas.move("all", voffset.x * newfactor, voffset.y * newfactor)

        print "bound -> "

        self.__viewport = Viewport(Bounding(Battles.Utils.Settings.SETTINGS.Get_I('Game', 'WindowWidth'),
                                            Battles.Utils.Settings.SETTINGS.Get_I('Game', 'WindowHeight')),
                                   Bounding(length=vlength * newfactor, width=vheight * newfactor), Point2D(x=0, y=0))
        # self._playerData.GetCastle().Draw(canvas =  self.__canvas, viewport = self.__viewport, moat = True, city = True, starfortress = False)
        self.DrawCastle(starfortress=False)

    def __EvolveWithPattern(self, pattern):
        # Evolves the city with given pattern    

        self.__existNewHouses = True

        # random.seed()

        housemindist = Battles.Utils.Settings.SETTINGS.Get_F('City', 'Houses', 'MinDistanceBetween')
        housemaxdist = Battles.Utils.Settings.SETTINGS.Get_F('City', 'Houses', 'MaxDistanceBetween')

        if not pattern.isEvolving:

            # NOTE: The initial evolution doesnt take into account the houseperyear speed factor

            # If evolution method is using only the expansion direction vector, the castle walls are considered as starting placements (see CityEvolutionPattern description)
            # Otherwise, use the given segment

            seglist = []
            fromsegment = False
            if pattern.Base:

                seglist.append(pattern.Base)
                fromsegment = True

            else:
                # Construct the convexhull around the castle and place house in front of those segments wich normal matches with pattern evolution direction
                # NOTE: This method doesnt consider the nonconvex castle walls. This could be a problem, but in fact, nonconvex walls ever are a possible source of problems, so ....

                # calculate the distance from curtain walls
                offset = Battles.Utils.Settings.SETTINGS.Get_F('City', 'Houses', 'DistanceWall')
                moat = self._playerData.GetCastle().GetMoat()
                if moat:
                    offset += moat.GetThickness()

                # Get the castle shape and construct the convex hull from it
                segments = self._playerData.GetCastle().GetIntersectableSegments()
                plist = []
                for s in segments:
                    plist.append(s.p1)
                    plist.append(s.p2)

                chull = ConvexHull(None)
                chull.SetPoint2DList(plist)
                chull.Calculate()
                chull.SetMargin(offset)
                seglist = chull.GetSegmentList()

            for seg in seglist:
                if pattern.Direction.DotProd(seg.GetNormal()) >= 0:
                    segdir = seg.GetDirection()
                    seglen = seg.GetLength()

                    # Populate the segment with houses. 
                    # Since we only need the house position, and the house size is sized by a constant value, we are going to create simply 2D points

                    h = House(seg.p1)
                    first = h.center.Copy()
                    pattern.Houses.append(h)
                    pattern.EdgeHouses.append(h)
                    end = False
                    while not end:
                        # To avoid using a brensenham algorithm style, we are going to use a little bit of brute force. We calculate the intersection of ray from previous point to
                        # the current house bounding box. Then, we move the intersected point along the segment a random distance between the minimum and maximum allowed houses distances
                        bquad = h.GetQuad()
                        ray = Ray2D(origin=h.center, direction=segdir)
                        if not ray.HitBoundingQuad(bquad):
                            end = True
                        else:
                            h = House(ray.GetHitPoint())
                            h.center.Move(segdir, ray.GetLength() + random.uniform(housemindist, housemaxdist))

                            # Check if initial houses are in the river, but only if them are placed around the castle wall.
                            # If the user specifies an initial base segment where to deploy them, its the user problem if the houses start in the river or too close to it
                            if ((not h.IsInRiver(
                                    self._playerData.GetBattlefield()) and not fromsegment) or fromsegment):
                                pattern.Houses.append(h)
                                pattern.EdgeHouses.append(h)

                                if h.center.Distance(first) > seglen:
                                    end = True
                            else:
                                end = True

            # Store the constructed houses to be used at next evolution step

            if pattern.Houses:  # Only allow evolution if there are the initial houses
                pattern.isEvolving = True
        else:

            # From the previously created houses, choose one randomly  and create a new one at the neighbor cell that is at the same (near) direction than the evolving pattern

            # Repeat the process as many times as number of houses per year and per number of year per evolution step
            # If the pattern number of houses per year is 1 or greater, repeat the process as many as houses per year number
            # Otherwise, increase the temporal pattern housesyear counter and exits. The counter will be reset when the number of years spent are enough

            if pattern.HousesPerYear < 1:

                pattern.HousesPerYearSlowCounter += pattern.HousesPerYear
                if pattern.HousesPerYearSlowCounter >= (1.0 / pattern.HousesPerYear):
                    pattern.HousesPerYearSlowCounter = 0.0
                else:
                    return

            hy = 0
            while (hy < pattern.HousesPerYear) and (len(pattern.EdgeHouses) > 0):

                # (TODO) Check for castle construction elements intersections
                # (TODO) Creates the house in a trench if there are any intersection
                # (TODO) DONT create the house over other previously created house

                index = int(math.floor(random.random() * (
                        len(pattern.EdgeHouses) * Battles.Utils.Settings.SETTINGS.Get_F('City', 'Houses',
                                                                                        'PreferenceFactor'))))
                if index >= len(pattern.EdgeHouses):
                    index = len(pattern.EdgeHouses) - 1
                    if index < 0:
                        continue

                house = pattern.EdgeHouses[index]

                bquad = house.GetQuad()
                ray = Ray2D(origin=house.center.Copy(), direction=pattern.Direction.Copy())
                if ray.HitBoundingQuad(bquad):
                    newhouse = House(ray.GetHitPoint().Copy())

                    # Apply a cosine distribution to add some fuzzy on the new house direction from old one
                    sph = Sphere(radius=Battles.Utils.Settings.SETTINGS.Get_F('City', 'Houses', 'PlacementFuzzy'),
                                 position=Point3D().SetFrom2D(newhouse.center.Copy()))
                    cosdir = Vector2D().SetFrom3D(sph.GetRayCosine(Vector3D().SetFrom2D(pattern.Direction.Copy())))
                    newhouse.center.Move(cosdir, ray.GetLength() + random.uniform(housemindist, housemaxdist))
                    # house.Move(cosdir, HOUSE_MINDISTANCE_BETWEEN)

                ray.Reset()

                # Remove the chosen house from the list and insert the new one
                pattern.EdgeHouses.pop(index)

                # Check if the newhouse has fallen on a river
                if not newhouse.IsInRiver(self._playerData.GetBattlefield()):
                    pattern.Houses.append(newhouse)
                    pattern.EdgeHouses.append(newhouse)

                    self.__lastAddedHouses.append(newhouse)

                hy += 1

    def __DrawEvolvedHouses(self, pattern):

        housesize = Battles.Utils.Settings.SETTINGS.Get_F('City', 'Houses', 'Size')
        for h in pattern.Houses:
            vp1 = self.__viewport.W2V(Point2D(h.center.x - housesize, h.center.y - housesize))
            vp2 = self.__viewport.W2V(Point2D(h.center.x + housesize, h.center.y + housesize))
            self.__canvasHouses.append(
                self.__canvas.create_rectangle(vp1.x, vp1.y, vp2.x, vp2.y, fill="gray93", outline="gray93"))

    def __DrawLastEvolvedHouses(self, pattern):

        housesize = Battles.Utils.Settings.SETTINGS.Get_F('City', 'Houses', 'Size')
        for h in self.__lastAddedHouses:
            vp1 = self.__viewport.W2V(Point2D(h.center.x - housesize, h.center.y - housesize))
            vp2 = self.__viewport.W2V(Point2D(h.center.x + housesize, h.center.y + housesize))
            self.__canvasHouses.append(
                self.__canvas.create_rectangle(vp1.x, vp1.y, vp2.x, vp2.y, fill="gray93", outline="gray93"))

        self.__lastAddedHouses = []

    def GetHouses(self):
        ret = []
        for ev in self.__evolutionPatterns.values():
            for p in ev:
                for h in p.Houses:
                    ret.append(h)

        return ret

    def ExpandCastle(self, frombattle, battlefield, groupID=None):

        # If none groupID has been specified, take the first one from the evolution patterns, if any (this function can be called from other non-city evolution context, by example, from an unique battle result)
        if (groupID == None) and (len(self.__evolutionPatterns) > 0):
            print "WARNING: Castle::ExpandCastle -> None groupID has been specified"
            lst = list(self.__evolutionPatterns.keys())
            groupID = lst[0]

        # Expands the castle creating a curtain wall around current city houses
        # If frombattle is true means that the expansion has been commanded from a battle result (defenders have fallen)
        # groupID is used to get the set of evolution patterns (that is the created houses) to construct the curtain wall
        print "Extending castle"

        factory = ConstructionFactory()

        # Current castle with current houses will be now stored as the inner castle of the new one (it only will be used for display purposes)
        oldcastle = self._playerData.GetCastle()

        # Defines a list with all current houses points. Then, compute the convex hull
        plist = []
        if len(self.__evolutionPatterns) > 0:
            for pat in self.__evolutionPatterns[groupID]:
                for h in pat.Houses:
                    plist.append(h.center.Copy())

        # Add to the houses points list the bastion vertices (if any). Because the final convex hull can intersect the old castle, we perform an union operation.
        # But the union algorithm cannot treat bastions due to its complexity (too many geometric cases). For that reason, we include the castle vertices to avoid any collision
        # Also we will add the old castle vertices if there are not any house in the evolution patterns. This can happens if two consecutive evolutions are performed or if
        # none city evolution has been defined between them
        if oldcastle.HasBastions() or factory.IsBastionTime() or not self.__existNewHouses:
            seglist = oldcastle.GetIntersectableSegments()
            for s in seglist:
                plist.append(s.p1)
                plist.append(
                    s.p2)  # One of both is usually not necessary but we cannot be sure for all objects. TODO: Improve this

        # Calculate the convex hull
        chull = ConvexHull(None)
        chull.SetPoint2DList(plist)
        chull.Calculate()
        chull.SetMargin(Battles.Utils.Settings.SETTINGS.Get_F(category='Castle', tag='CurtainWallOldCityMargin'))
        chull.SplitLongSegments(
            self._maxWallLength)  # First split the too long segments, so the method can generate small segments
        chull.PurgeSmallSegments(self._minWallLength)
        if chull.GetNPoints() < 3:
            print "ERROR: Cannot expand the castle due the minimum and maximum wall lengths (none wall pass the filter)"
            return

        # Check if the convex hull intersects with any river. If intersects, modify it. Note that we convert the convex hull to a 2D polygon, so the result could be a nonconvex polygon
        convexpoly = chull.GetPolygon2D()
        battlefield.CheckShapeOnRiver(convexpoly)

        gpc = GPCWrapper()

        # Check the initial polyong orientation
        newverts = convexpoly.GetPointsList()
        if not gpc.IsCCW(newverts):
            newverts.reverse()
            convexpoly.SetPointsList(newverts)
        newverts = convexpoly.GetPointsList()
        if not gpc.IsCCW(newverts):
            newverts.reverse()
            convexpoly.SetPointsList(newverts)

        # Check if new castle hull overlaps the old one. If not, none clipping operation has to be performed
        # Note that the oldcastle could has many convex hulls. Check the union for all hulls
        oldcastlelist = oldcastle.GetCastlesList()

        joinedlist = []
        coveredlist = []
        covererror = False

        for oldc in oldcastlelist:

            oldpoly = oldc.GetCastleHull()
            oldverts = oldpoly.GetPointsList()
            newverts = convexpoly.GetPointsList()

            if gpc.Covers(oldverts, newverts):
                print "ERROR: The new castle is fully covered by the old one. Choosing the old castle shape as the new one"
                covererror = True
            elif gpc.Covers(newverts, oldverts):
                coveredlist.append(oldc)
            elif gpc.Overlaps(oldverts, newverts):
                # Performs a union clipping operation between new shape and old castle one

                joinedlist.append(oldc)

                margincloser = Battles.Utils.Settings.SETTINGS.Get_F(category='City', tag='MatchVerticesDistance')

                newverts = gpc.Union(newverts, oldverts)

                # Because this operation is purely geometrical, there are some issues that we have to refine

                # New vertices are created in the union. But from  the castle construction point of view, its cheaper to join a wall to an existent tower/vertex than create a new one
                # To solve it, check for each new vertex, if falls over an old castle tower/vertex. If not (falls over a wall/segment), search the nearest vertex and move the segment to it

                i = 0
                while i < len(newverts):
                    p = oldpoly.IsCloserToVertex(point=newverts[i], margin=margincloser)
                    if p != None:
                        # Match the vertices
                        newverts[i] = p
                    else:

                        seg = oldpoly.GetCloserSegment(point=newverts[i], margin=margincloser)
                        if seg != None:
                            newverts[i] = seg.GetCloserVertex(newverts[i])
                    i += 1

                # Clean repeated vertices or too close
                # newverts = gpc.Clean(newverts)
                # DO NOT CLEAN WITH GPC -> ITS AN AMAZING PIECE OF BULLSHIT .... :(

                # Check if each vertex falls closer to any tower
                # This check cannot be done before, so the clean operation would remove all extra data linked in points
                # Next, check if vertex belongs to the oldcastle, using a dummy flag that indicates that this vertex cannot be transformed to a new tower. With this flag we
                # allow to create new towers only for the new walls

                i = 0
                while i < len(newverts):
                    tower = oldcastle.GetCloserTower(newverts[i])
                    if tower != None:
                        # Link the tower with the point. Next, when the curtain wall will be constructed, the tower will be replied and inserted into the curtain walls
                        # In addition, move the vertex to match with the tower center. This avoids precision problems and error accumulation throught consecutive expansions
                        newverts[i] = tower.GetPosition().Copy()
                        newverts[i].data = tower
                    else:
                        # Check if vertex is an old castle vertex. Note that we could we used the previous identical check to set the flag. But the gpc.Clean operation removes the
                        # Point2D extra data, so it has to be recalculated again
                        p = oldpoly.IsCloserToVertex(point=newverts[i], margin=margincloser)
                        if p != None:
                            newverts[i].data = FORBIDDEN_TOWER_FLAG

                    i += 1

                # Check the polygon orientation. It should be ccw to avoid wrong wall normal vectors
                # WARNING: Do not be confused by the geometry drawn on the screen. Remember that Y axis is shown inverted, so the polygons shown as cw are really in ccw
                if not gpc.IsCCW(newverts):
                    newverts.reverse()

                # Finally, convert the resulting vertices to a polygon
                convexpoly.shape = []
                i = 0
                while i < len(newverts):
                    if (newverts[i - 1].Distance(newverts[i]) > Battles.Utils.Settings.SETTINGS.Get_F('City',
                                                                                                      'MinWallLength')):
                        convexpoly.shape.append(Segment2D(newverts[i - 1], newverts[i]))
                    i += 1

        # If any part of the old castle covers the new shape, it becomes invalid or unuseful, and none new castle set has to be created
        if not covererror:
            # Creates the new CastleSet
            newcastle = CastleSet.CastleSet()

            # Define the references structure between the old and new one
            newcastle.GroupCastles(castleset=oldcastle, joinedlist=joinedlist, coveredlist=coveredlist)

            # Updates the current player CastleSet
            self._playerData.SetCastle(newcastle)

            # Set the orientation
            newcastle.SetCastleOrientation(oldcastle.GetCastleOrientation())

            # Construct the curtain wall
            # Note that preivously linked towers remain in convexpoly as extra data for each segment vertex. Also, the created walls will have intact these links
            # in self.__axis data member
            newcastle.ConstructCurtainWall(convexpoly.GetPointsList())

            # Set the walls resistance
            newcastle.SetWallsResistance(oldcastle.GetWallsResistance())

            # Evolve the new castle to upgrade the towers
            newcastle.Evolve(climbings=None, attachedsiegetowers=None, battlefield=None)

            # Update the moat from the original castle (TODO: Allow new moat configuration for each expansion)
            moat = oldcastle.GetMoat()
            if moat:
                newcastle.SetMoat(thickness=moat.GetThickness(), depth=moat.GetDepth(), haswater=moat.HasWater())

        # All current houses evolution patterns must stop
        # EDIT: Im not sure about this restriction. I believe that to avoid that houses will be deployed intersecting the new curtain wall, or to get right results
        # for those kind of expansions that start from the castle bounding. For our last examples (evolutions from a segment and direction) this is not required
        # In addition, it is not recommendable. The evolution patterns cannot be predicted if we dont know how the castle will be expanded
        """if (len(self.__evolutionPatterns) > 0):
            for pat in self.__evolutionPatterns[groupID]:
                if (pat.isEvolving):
                    pat.DateRange[1] = self._currentYear
        """

        self.__existNewHouses = False

        # Update the castle expansion history
        self.__castleExpansionHistory.append({"Year": self._currentYear, "FromBattle": frombattle})

    """
    def ExpandCastle_Old(self, frombattle, battlefield, groupID = None):
        
        # If none groupID has been specified, take the first one from the evolution patterns, if any (this function can be called from other non-city evolution context, by example, from an unique battle result)
        if ((groupID == None) and (len(self.__evolutionPatterns) > 0)):
            print "WARNING: Castle::ExpandCastle -> None groupID has been specified"
            lst = list(self.__evolutionPatterns.keys())
            groupID = lst[0]
            
        
        # Expands the castle creating a curtain wall around current city houses
        # If frombattle is true means that the expansion has been commanded from a battle result (defenders have fallen) 
        # groupID is used to get the set of evolution patterns (that is the created houses) to construct the curtain wall
        print "Extending castle"
        
        factory = ConstructionFactory()
        
        # Current castle with current houses will be now stored as the inner castle of the new one (it only will be used for display purposes)
        oldcastle = self._playerData.GetCastle()
        
        # Defines a list with all current houses points. Then, compute the convex hull
        plist = []
        if (len(self.__evolutionPatterns) > 0):
            for pat in self.__evolutionPatterns[groupID]:
                for h in pat.Houses:
                    plist.append(h.center.Copy())
             

        # Add to the houses points list the bastion vertices (if any). Because the final convex hull can intersect the old castle, we perform an union operation. 
        # But the union algorithm cannot treat bastions due to its complexity (too many geometric cases). For that reason, we include the castle vertices to avoid any collision
        # Also we will add the old castle vertices if there are not any house in the evolution patterns. This can happens if two consecutive evolutions are performed or if
        # none city evolution has been defined between them
        union = True
        if (oldcastle.HasBastions() or factory.IsBastionTime() or not self.__existNewHouses):
            union = False
            seglist = oldcastle.GetIntersectableSegments()
            for s in seglist:
                plist.append(s.p1)
                plist.append(s.p2)  # One of both is usually not necessary but we cannot be sure for all objects. TODO: Improve this

            
        end = False
        
        while (not end):   
            # Calculate the convex hull
            chull = ConvexHull(None)
            chull.SetPoint2DList(plist)
            chull.Calculate()
            chull.SetMargin(Battles.Utils.Settings.SETTINGS.Get_F(category = 'Castle', tag = 'CurtainWallOldCityMargin')) 
            chull.SplitLongSegments(self._maxWallLength)   # First split the too long segments, so the method can generate small segments
            chull.PurgeSmallSegments(self._minWallLength)
            if (chull.GetNPoints() < 3):
                print "ERROR: Cannot expand the castle due the minimum and maximum wall lengths (none wall pass the filter)"
                return
            

            # Check if the convex hull intersects with any river. If intersects, modify it. Note that we convert the convex hull to a 2D polygon, so the result could be a nonconvex polygon
            convexpoly = chull.GetPolygon2D()
            battlefield.CheckShapeOnRiver(convexpoly)



            newcastle = CastleSet.CastleSet()
            newcastle.SetInnerCastle(oldcastle)
            
            self._playerData.SetCastle(newcastle)
     
                    
            # Set the orientation
            newcastle.SetCastleOrientation(oldcastle.GetCastleOrientation())
            
            # Construct the curtain wall
            newcastle.ConstructCurtainWall(convexpoly.GetPointsList())
            
            # Set the walls resistance
            newcastle.SetWallsResistance(oldcastle.GetWallsResistance())
            
            # Evolve the new castle to upgrade the towers
            newcastle.Evolve(climbings = None, attachedsiegetowers = None, battlefield = None)
                    
            # Update the moat from the original castle (TODO: Allow new moat configuration for each expansion)
            moat = oldcastle.GetMoat()
            if (moat):
                newcastle.SetMoat(thickness = moat.GetThickness(), depth = moat.GetDepth(), haswater = moat.HasWater())
            
            
            
            # Check if previous castle intersects with current one, and calculates an union of both curtain walls
            if (union):
                if (newcastle.CastleUnion(oldcastle)):
                    end = True
                else:
                    end = False
                    
                    # Something went wrong in castle union algorithm. To avoid the error, append the old castle parts into the new castle convex hull
                    seglist = oldcastle.GetIntersectableSegments()
                    for s in seglist:
                        plist.append(s.p1)
                        plist.append(s.p2)  # One of both is usually not necessary but we cannot be sure for all objects. TODO: Improve this
                    
            else:
                end = True
                
        
        
        
        # All current houses evolution patterns must stop
        if (len(self.__evolutionPatterns) > 0):
            for pat in self.__evolutionPatterns[groupID]:
                if (pat.isEvolving):
                    pat.DateRange[1] = self._currentYear
            
        self.__existNewHouses = False
        
        # Update the castle expansion history
        self.__castleExpansionHistory.append({"Year": self._currentYear, "FromBattle": frombattle})
    """

    def __BattleEvent(self, battledata):
        Battles.Utils.Message.Verbose = Battles.Utils.Message.VERBOSE_RESULT

        # To control what are drawn in the battle and remove it later, set a tag for all current canvas objects
        self.__canvas.dtag("all")  # Remove all tags
        self.__canvas.addtag_all("currentcity")

        battle = BattleEvent(battledata, self.__tkinter, self.__canvas, self.__viewport, self)
        battle.PlayBattle(self._playerData, self)

    def EndBattle(self):
        # Must be called each time a battle finishes to update the internal battle events counter
        self.__currentBattleEvents -= 1
        if self.__currentBattleEvents < 0:
            self.__currentBattleEvents = 0  # This should never happens

        # Remove all objects that havent the city tag (that is, all battle objects)
        allobjs = self.__canvas.find_all()
        castleobjs = self.__canvas.find_withtag("currentcity")
        for obj in allobjs:
            if obj not in castleobjs:
                self.__canvas.delete(obj)

                # Well, this is weird. In fact, there are some castle parts that are drawn in Battles. So we redraw the castle
        # self._playerData.GetCastle().Draw(canvas =  self.__canvas, viewport = self.__viewport, moat = True, city = True, starfortress = False)
        self.DrawCastle(starfortress=False)

    def EndBattle2(self):
        # Must be called each time a battle finishes to update the internal battle events counter
        self.__currentBattleEvents -= 1
        if self.__currentBattleEvents < 0:
            self.__currentBattleEvents = 0  # This should never happens

    def DrawCastle(self, starfortress):
        self._playerData.GetCastle().Draw(canvas=self.__canvas, viewport=self.__viewport, moat=True, city=True,
                                          starfortress=starfortress, year=self._currentYear)

    def ClearDrawCastle(self):
        self._playerData.GetCastle().ClearDraw(self.__canvas)

    def __CheckCastleExpansions(self):
        print "Castle Expansion History:"
        for h in self.__castleExpansionHistory:
            print "     Year: " + str(h["Year"]) + "  Due a battle: " + str(h["FromBattle"])

    def SetTimeBetweenExpansions(self, margintime):
        self.__marginTimeBetweenExpansions = margintime

    def AllowExpansionByHistory(self):
        # Returns False if at current year a castle evolution is not allowed due a previous expansion too close in time
        if len(self.__castleExpansionHistory) == 0:
            return True

        h = self.__castleExpansionHistory[-1]
        if (self._currentYear - h["Year"]) >= self.__marginTimeBetweenExpansions:
            return True
        else:
            return False
