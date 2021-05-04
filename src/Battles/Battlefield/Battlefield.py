from math import ceil, floor, fabs
import random

from Battles.Utils.Geometry import Point2D, Bounding, Vector2D, Segment2D, Point3D, Vector3D, BoundingBox, GPCWrapper
from Battles.Utils.Message import *
from Battles.Factory import ArmyFactory
from Battles.Army.Action import Command
from Battles.Battlefield import GroundCell, Trench
from Battles.Castle.Wall import GetWallLength_Sort
import Battles.Utils.Settings
import Battles.Army.Battalion as Battalion


class BattleField:
    """ Terrain where attackers advance to the castle.
        The field is discretised in fields where troops advance. The castle doesn't fit to the cells 
        
        Attributes:
            cells: cells list indexed as an array (length matches with row size and width with columns size)
            cellsize: cell size (length of any side of squared cell). WARNING: The cell size must be enough big to contain any army object
            bounding: bounding terrain defined by two points (rectangle)
            trenches: array of trenches zones
            rivers: array of rivers
            
    """

    def __init__(self, bound=Bounding(Battles.Utils.Settings.SETTINGS.Get_F('Battlefield', 'size'),
                                      Battles.Utils.Settings.SETTINGS.Get_F('Battlefield', 'size')),
                 cellsize=Battles.Utils.Settings.SETTINGS.Get_F('Battlefield', 'GroundCell', 'Size')):
        # Terrain defined by bounding of Point2D and an array with cells of cellsize size
        self.__bounding = bound  # TerrainBound type
        self.__cellsize = cellsize

        self.__trenches = []
        self.__rivers = []

        # Create the cells array
        nrows = int(bound.width / self.__cellsize)
        ncols = int(bound.length / self.__cellsize)
        self.__cellsarraysize = {"rows": nrows, "columns": ncols}
        i = 0
        self.__cells = []
        while (i < nrows):
            j = 0
            self.__cells.append([])
            row = []
            while (j < ncols):
                row.append(GroundCell.GroundCell(self, i, j))
                j += 1
            self.__cells[i] = row
            i += 1

    def GetBounding(self):
        return self.__bounding

    def GetCellSize(self):
        return self.__cellsize

    def Draw(self, canvas, viewport, showgrid):
        # Draw the battlefield grid with given TKinter Canvas

        if (showgrid):
            x1 = 0
            y1 = 0
            x2 = self.__cellsarraysize["columns"] * self.__cellsize
            y2 = self.__cellsarraysize["rows"] * self.__cellsize

            i = 0
            y = 0
            while (i <= self.__cellsarraysize["rows"]):
                pw1 = viewport.W2V(Point2D(x1, y))
                pw2 = viewport.W2V(Point2D(x2, y))
                canvas.create_line(pw1.x, pw1.y, pw2.x, pw2.y, fill="gray")
                y = y + self.__cellsize
                i += 1

            j = 0
            x = 0
            while (j <= self.__cellsarraysize["columns"]):
                pw1 = viewport.W2V(Point2D(x, y1))
                pw2 = viewport.W2V(Point2D(x, y2))
                canvas.create_line(pw1.x, pw1.y, pw2.x, pw2.y, fill="gray")
                x = x + self.__cellsize
                j += 1

        self.DrawTerrain(canvas, viewport)

    def DrawTerrain(self, canvas, viewport):

        # Draw the relevant terrain elements (trenches, river, ....)

        # Draw the trenches
        for t in self.__trenches:
            t.Draw(canvas, viewport)

        # Draw the rivers
        for r in self.__rivers:
            r.Draw(canvas, viewport)

    def Reset(self):
        # Cleans the battlefield of battalions and constructions links
        for row in self.__cells:
            for col in row:
                col.Reset()

        self.__trenches = []
        self.__rivers = []

    def DeployCity(self, convexhull):
        # Deploys the castle interior, that is the city/town, to the battlefield.
        # Calculate all cells inside the castle convexhull and mark them as city cells
        # Return a list with all city cells

        ret = []

        if (not convexhull):
            return ret

        i = 0
        while (i < self.__cellsarraysize["rows"]):
            j = 0
            while (j < self.__cellsarraysize["columns"]):
                c = self.__cells[i][j]
                if (convexhull.IsInside(c.center)):
                    c.SetCity(True)
                    ret.append(c)
                else:
                    c.SetCity(False)

                j += 1
            i += 1

        return ret

    ###########################################################################33
    # CELL ACCESS RELATED METHODS
    ###########################################################################33

    def GetCell(self, row, column):
        if ((row < 0) or (row >= self.__cellsarraysize["rows"])):
            return None
        elif ((column < 0) or (column >= self.__cellsarraysize["columns"])):
            return None
        else:
            return self.__cells[row][column]

    def GetCellFromPoint(self, point, fit=False):
        # Returns the cell that encloses given 2D point
        # Remember that battlefield grid starts at 0,0
        # If fit is True and position falls over the battlefield, returns the closer cell to the respective battlefield edge

        col = int(floor(point.x / self.__cellsize))
        row = int(floor(point.y / self.__cellsize))

        if (col < 0):
            if (fit):
                col = 0
            else:
                return None

        if (row < 0):
            if (fit):
                row = 0
            else:
                return None

        if (col >= self.__cellsarraysize["columns"]):
            if (fit):
                col = self.__cellsarraysize["columns"] - 1
            else:
                return None

        if (row >= self.__cellsarraysize["rows"]):
            if (fit):
                row = self.__cellsarraysize["rows"] - 1
            else:
                return None

        return self.__cells[row][col]

    # Return a list of cells that falls inside given bounding box
    def GetCellsRange(self, bbquad):

        lst = []

        cmin = self.GetCellFromPoint(bbquad.minPoint)
        cmax = self.GetCellFromPoint(bbquad.maxPoint)

        if ((cmin == None) or (cmax == None)):
            return lst

        i = cmin.GetRow()
        while (i <= cmax.GetRow()):
            j = cmin.GetColumn()
            while (j <= cmax.GetColumn()):
                lst.append(self.__cells[i][j])

        return lst

    # DEPRECATED!!!!
    # Too heavy computation for huge battlefields
    def GetClosestCell(self, populated, posfrom):
        # Returns the closest cell to given position. If populated is True, returns only a populated cell        

        mindist = -1
        near = None

        i = 0
        while (i < self.__cellsarraysize["rows"]):
            j = 0
            while (j < self.__cellsarraysize["columns"]):
                c = self.__cells[i][j]
                if ((c.HasBattalion() and populated) or (populated == False)):
                    if (near == None):
                        near = c
                        mindist = posfrom.Distance(c.center)
                    else:
                        dist = posfrom.Distance(c.center)
                        if (dist < mindist):
                            mindist = dist
                            near = c
                j += 1
            i += 1

        return near

    # DEPRECATED!!!!
    # Too heavy computation for huge battlefields
    def GetClosestCellInAttackRange(self, populated, posfrom, castle, action):
        # Returns the closest cell to given position that is in attack range. If populated is True, returns only a populated cell
        # An Action object is passed to check the range

        mindist = -1
        near = None

        i = 0
        while (i < self.__cellsarraysize["rows"]):
            j = 0
            while (j < self.__cellsarraysize["columns"]):

                c = self.__cells[i][j]

                # Check if is populated
                if ((c.HasBattalion() and populated) or (populated == False)):

                    center = c.center

                    # Check if is in attack range
                    if (
                    action.InAttackRange(currPos=posfrom, targetPos=center, castle=castle, constructionTarget=None)):

                        # Check the closest condition
                        if (near == None):
                            near = c
                            mindist = posfrom.Distance(center)
                        else:
                            dist = posfrom.Distance(center)
                            if (dist < mindist):
                                mindist = dist
                                near = c
                j += 1
            i += 1

        return near

    ###########################################################################33
    # GEOMETRY RELATED METHODS
    ###########################################################################33

    def RayTraversal(self, pStart, pEnd, direction=None):
        # Performs a ray traversal from pStart to pEnd on battlefield. Returns a list of all intersected cells
        # If pEnd is None, direction is taken as the ray direction and the traversal stop at the battlefield bounds

        ret = []

        if (((pEnd != None) and (pStart.x > pEnd.x)) or ((pEnd == None) and (direction.val[0] < 0))):
            # Avoid traversal in X negative (the order is not important for this algorithm)
            if (pEnd != None):
                ret = self.RayTraversal(pStart=pEnd, pEnd=pStart, direction=None)
                ret.reverse()
                return ret
            else:
                # Get the starting point from the battlefield bound and traces the ray to the original starting point
                start = pStart.Copy()
                if (direction.val[0] == 0.0):
                    if (direction.val[1] < 0):
                        tx = -self.__bounding.width
                    else:
                        tx = self.__bounding.width
                else:
                    tx = fabs(pStart.x / direction.val[0])
                if (direction.val[1] == 0.0):
                    """if (direction.val[0] < 0):
                        ty = -self.__bounding.length
                    else:
                        ty = self.__bounding.length
                    """
                    ty = self.__bounding.length
                else:
                    ty = fabs(pStart.y / direction.val[1])
                start.Move(direction, min(tx, ty))
                if (start.x < 0):
                    start.x = 0
                elif (start.x > self.__bounding.length):
                    start.x = self.__bounding.length
                if (start.y < 0):
                    start.y = 0
                elif (start.y > self.__bounding.width):
                    start.y = self.__bounding.width
                ret = self.RayTraversal(pStart=start, pEnd=pStart, direction=None)
                ret.reverse()
                return ret

        if (pEnd != None):
            rayvec = Vector2D()
            rayvec.CreateFrom2Points(pStart, pEnd)
        else:
            rayvec = direction

        # Set a delta value to avoid self intersections after movement
        delta = self.__cellsize / 100.0

        cursor = pStart.Copy()
        cursor.Move(rayvec, delta)

        cell = self.GetCellFromPoint(cursor)
        if (cell == None):
            print 'ERROR: Ray out of bounds'
            return ret

        row = cell.GetRow()
        col = cell.GetColumn()

        end = False

        if (pEnd != None):
            length = delta
            maxlength = pStart.Distance(pEnd)
            if (length > maxlength):
                end = True

        cell = self.GetCell(row, col)
        if (cell == None):
            if (pEnd != None):
                print 'ERROR: Ray out of bounds'
            end = True

        while (not end):

            ret.append(cell)

            # Get real cell coordinates
            bound = cell.GetBoundingQuad()

            # Calculate the intersection in tangent space
            # Get the distance between current point and X and Y axis that define the limits of cell
            # Then, divide them by the ray vector to get a magnitude of displacement on each axis
            # Get the minimum displacement because is the first intersection
            # Also check axis-aligned cases

            if ((rayvec.val[0] >= 0) and (rayvec.val[0] < 0.00001) and (rayvec.val[1] >= 0) and (
                    rayvec.val[1] < 0.00001)):
                print 'ERROR: Null vector'
                return ret
            elif ((rayvec.val[0] >= 0) and (rayvec.val[0] < 0.00001)):
                if (rayvec.val[1] < 0):
                    t = cursor.y - bound.minPoint.y
                    row -= 1
                else:
                    t = bound.maxPoint.y - cursor.y
                    row += 1
                """if (rayvec.val[1] < 0):
                    row -= 1
                    t = (cursor.y - bound.maxPoint.y) / -rayvec.val[1]
                else:
                    row += 1
                    t =  (bound.maxPoint.y - cursor.y) / rayvec.val[1]
                """
            elif ((rayvec.val[1] >= 0) and (rayvec.val[1] < 0.00001)):
                col += 1
                t = (bound.maxPoint.x - cursor.x) / rayvec.val[0]
            else:

                tx = (bound.maxPoint.x - cursor.x) / rayvec.val[0]

                if (rayvec.val[1] < 0):
                    ty = (cursor.y - bound.minPoint.y) / -rayvec.val[1]
                    nextrow = -1  # Get the previous row
                else:
                    ty = (bound.maxPoint.y - cursor.y) / rayvec.val[1]
                    nextrow = 1

                if (tx > ty):
                    row += nextrow
                    t = ty
                elif (tx < ty):
                    col += 1
                    t = tx
                else:
                    col += 1
                    row += nextrow
                    t = tx

            # Advance to next cell
            t += delta
            cursor.Move(rayvec, t)

            if (pEnd != None):
                length = cursor.Distance(pStart)
                maxlength = pStart.Distance(pEnd)
                if (length > maxlength):
                    end = True

            cell = self.GetCell(row, col)
            if (cell == None):
                if (pEnd != None):
                    print 'ERROR: Ray out of bounds'
                end = True

        return ret

    def CircleIntersects(self, center, radius):
        # Return a list with all cells that intersect with given circle. Only are checked the cell vertices and cell center

        lst = []

        # Get cell that matches with circle center        
        col = int(floor(center.x / self.__cellsize))
        row = int(floor(center.y / self.__cellsize))
        if ((col >= self.__cellsarraysize["columns"]) or (row >= self.__cellsarraysize["rows"])):
            return None

        # Get the surrounding cells with radius as distance from center cell
        dist = int(floor(radius / self.__cellsize))
        col0 = col - dist
        row0 = row - dist
        col1 = col + dist
        row1 = row + dist
        if (col0 < 0):
            col0 = 0
        if (row0 < 0):
            row0 = 0
        if (col1 >= self.__cellsarraysize["columns"]):
            col1 = self.__cellsarraysize["columns"] - 1
        if (row1 >= self.__cellsarraysize["rows"]):
            row1 = self.__cellsarraysize["rows"] - 1

        i = row0
        while (i <= row1):
            j = col0
            while (j <= col1):
                c = self.__cells[i][j]
                if (c.CircleIntersects(center, radius)):
                    lst.append(c)
                j += 1
            i += 1

        """
        i = 0
        while (i < self.__cellsarraysize["rows"]):
            j = 0
            while (j < self.__cellsarraysize["columns"]):
                
                c = self.__cells[i][j]
                if (c.CircleIntersects(center, radius)):
                    lst.append(c)
        
        
                j += 1
            i += 1
        """

        return lst

    def RayIntersects(self, ray):
        # Return the battlefield intersection point of given ray, or none if the ray doesnt intersect

        # Get the battlefield 3D square. Be aware about the vertices order (the normal vector must be <0,0,1>)
        rect = [Point3D(0.0, 0.0, 0.0), Point3D(self.__bounding.length, 0.0, 0.0),
                Point3D(self.__bounding.length, self.__bounding.width, 0.0), Point3D(0.0, self.__bounding.height, 0.0)]

        if (ray.HitRectangle(rect, BoundingBox(minP=rect[0], maxP=rect[2]), Vector3D(0.0, 0.0, 1.0))):
            return ray.GetHitPoint()
        else:
            return None

    ###########################################################################33
    # BATTALION RELATED METHODS
    ###########################################################################33

    def DeployBattalion(self, position, lines, army, kind, number, maxpercell=-1, maxrows=-1, maxcols=-1,
                        command=Command.STAY):
        # Deploys a battalion in the battlefield region defined by given 2D position and expanded in given lines
        # Given army object is the army where new battalions will be stored
        # maxpercell parameter sets the maximum elements per cell. If it is 0, the full cell will be used. 
        # The battalion type (kind) must match with the armycomponent class name
        # If lines is -1, deploys the battalions vertically with one battalion per column
        # maxrows and maxcols limit the number of generated rows and cols. If they are -1, there arent any limit (until the battlefield bound)
        # command parameter tells to the units what is the current command

        if ((number == 0) or (maxrows == 0) or (maxcols == 0) or (maxpercell == 0)):
            return False

        factory = ArmyFactory()

        battalion = factory.newBattalion(army, kind, number)

        if (battalion == None):
            raise NameError('ERROR: Wrong battalion type')
            return False

        if ((lines == 0) or (battalion.GetNumber() <= 0)):
            raise NameError('ERROR: You must specify a number greater than 0 for lines or battalion size')

        # Check if each effective bounding fits into cell size
        if (not battalion.FitInCell(self.__cellsize, self.__cellsize)):
            Log('Given battalion cannot be deployed due effective bounding is greater than cell size', VERBOSE_WARNING)
            return False

        # Get position cell
        colPos = int(position.x / self.__cellsize)
        rowPos = int(position.y / self.__cellsize)

        if ((rowPos < 0) or (colPos < 0) or (colPos >= self.__cellsarraysize["columns"]) or (
                rowPos >= self.__cellsarraysize["rows"])):
            raise NameError('ERROR: The position is out of the terrain bounds')

        if ((rowPos + lines) > self.__cellsarraysize["rows"]):
            raise NameError('ERROR: The number of lines exceed the terrain bounds')

        # Get the number of effective for each line and for each cell
        nforeachcell = battalion.GetNumberByCell(self.__cellsize)
        if ((maxpercell > 0) and (maxpercell < nforeachcell)):
            nforeachcell = maxpercell

        if (lines > 0):
            nforeachline = int(battalion.GetNumber() / lines)
        else:
            nforeachline = nforeachcell

        if ((nforeachline == 0) or (nforeachcell == 0)):
            Log('Too small battalion', VERBOSE_WARNING)
            return False

        # Get the number of estimated columns
        cols = ceil(nforeachline / nforeachcell)
        if ((colPos + cols) > self.__cellsarraysize["columns"]):
            Log('Too few lines to deploy a too wide battalion', VERBOSE_WARNING)
            # return False
            cols = self.__cellsarraysize["columns"] - colPos
            nforeachline = nforeachcell * cols
        if ((maxcols > 0) and (cols > maxcols)):
            cols = maxcols
            nforeachline = nforeachcell * cols

        # Get the maximum number of lines
        if (lines > 0):
            nlines = lines
        else:
            nlines = self.__cellsarraysize["rows"] - rowPos

        if ((maxrows > 0) and (nlines > maxrows)):
            nlines = maxrows

        # Deploys the troops line by line
        i = 0
        while (i < nlines):
            j = 0
            ne = battalion.GetNumber()
            byline = 0
            while ((ne > 0) and (byline < nforeachline)):

                cell = self.__cells[i + rowPos][j + colPos]

                # Check if remain troops fit into the next cell
                if (ne < nforeachcell):
                    ncell = ne
                else:
                    ncell = nforeachcell

                # Check if we have reached the end of line
                if ((byline + ncell) > nforeachline):
                    ncell = nforeachline - byline

                ne = ne - ncell
                byline = byline + ncell

                b = factory.newBattalion(army, kind, ncell)
                b.AssignToCell(cell)
                army.InsertBattalion(b)
                b.SetCommand(command)

                j += 1

            i += 1

        return True

    def DeployBattalionRect(self, firstrow, firstcolumn, lastrow, lastcolumn, army, kind, maxPerCell=-1,
                            command=Command.STAY):
        # Deploys army troops on battlefield region. The battalions will be deployed to fill the whole region. If there aren't enough troops, it will left empty the rest of region
        # NOTE that region is defined by cell indices, not by real positions
        # maxPerCell parameter limits the maximum number of troops per cell (or -1 if there aren't limit)
        # command parameter tells to the units what is the current command

        if ((firstrow < 0) or (firstrow >= self.__cellsarraysize["rows"]) or
                (firstcolumn < 0) or (firstcolumn >= self.__cellsarraysize["columns"]) or
                (lastrow < 0) or (lastrow >= self.__cellsarraysize["rows"]) or
                (lastcolumn < 0) or (lastcolumn >= self.__cellsarraysize["columns"]) or
                (firstrow > lastrow) or (firstcolumn > lastcolumn)):
            print('ERROR: Wrong battlefield region')
            return

        factory = ArmyFactory()
        # battalion = factory.newBattalion(army, kind, -1)
        # if (not battalion):
        #    return

        nforeachcell = Battalion.Battalion.GetNumberByCell(self.__cellsize)
        if ((maxPerCell > 1) and (maxPerCell < nforeachcell)):
            nforeachcell = maxPerCell

        # print "nforeachcell:", nforeachcell
        for i in range(firstrow, lastrow + 1):
            for j in range(firstcolumn, lastcolumn + 1):
                # print "processing cell (", i, ",", j, ")",
                c = self.__cells[i][j]
                if ((c != None) and c.IsAvailable() and not army.finishedBattalions(kind)):
                    b = factory.newBattalion(army, kind, nforeachcell)
                    b.AssignToCell(c)
                    army.InsertBattalion(b)
                    b.SetCommand(command)
                else:
                    print "WARNING: either no cell, not available or finished battalions!"

    def DeploySiegeTowers(self, army, maxDeployed, castle, command=Command.ATTACK_CASTLE):
        # Special deployment for siege towers. The placement is calculated from the best castle walls to attack
        # If maxDeployed is -1 all siege towers will be deployed

        # If castle has a moat with water, discard anny attack with siege towers
        if (castle.GetMoat() and castle.GetMoat().HasWater()):
            print('ERROR: The siege towers cannot be deployed due the castle has a moat with water')
            return

        # Debug purposes.... remove after check siege towers creation.... but we aware to get a good maximum loop number for above loop
        factory = ArmyFactory()
        battalion = factory.newBattalion(army, "SiegeTowers", maxDeployed)

        # Get the wall segments and search for the longest one
        # Only the enough long walls are considered, because the too short ones cannot be attacked
        lst = castle.GetWallsList()
        seglst = []
        for w in lst:
            if ((w.GetLength() > self.__cellsize) and w.IsReachable()):
                seglst.append({'Wall': w, 'Segment': Segment2D(w.GetStartPosition(), w.GetEndPosition())})

        # We do not consider any decent sort method due there are only too few walls

        if (len(seglst) == 0):
            print('ERROR: There arent any good wall to be targeted by siege towers')
            return

        i = 0
        while (i < battalion.GetNumber()):

            seg = seglst[0]['Segment']
            maxL = seg.GetLength()
            jmax = 0
            j = 1
            while (j < len(seglst)):
                if (seglst[j]['Segment'].GetLength() > maxL):
                    seg = seglst[j]['Segment']
                    maxL = seg.GetLength()
                    jmax = j
                j += 1

            # Update the list splitting the selected segment to avoid reselecting it again
            mid = seg.GetMidPoint()
            seg1 = Segment2D(seg.p1, mid)
            seg2 = Segment2D(mid, seg.p2)
            selwall = seglst[jmax]['Wall']
            if (seg1.GetLength() > self.__cellsize):
                seglst.append({'Wall': selwall, 'Segment': seg1})
            if (seg2.GetLength() > self.__cellsize):
                seglst.append({'Wall': selwall, 'Segment': seg2})
            del seglst[jmax]
            if (len(seglst) == 0):
                print('ERROR: There are any good wall to target the siege tower')
                return

            # The siege tower will advance in straight line to the wall. Get and store the cells that must visit
            clst = self.RayTraversal(pStart=mid, pEnd=None, direction=Vector2D().SetFrom3D(seg.GetNormal()))
            if (len(clst) < 2):
                Log('The siege tower cannot be placed (try again)!!', VERBOSE_WARNING)
                continue

            # Check if clst[0] has already any battalion 
            clst.reverse()
            while (clst[0].HasBattalion()):
                clst = clst[1:]
                if (not clst):
                    Log('The siege tower cannot be placed (too much battalions in his path) (try again)!!',
                        VERBOSE_WARNING)
                    continue

            # Check if path has any trench or cannon (remember, only god can move cannons...), and discard it if it is
            discard = False
            k = 0
            while (not discard and (k < len(clst))):
                if (clst[k].HasTrench()):
                    Log('The siege tower cannot be placed because a trench is in its path. Try again!', VERBOSE_WARNING)
                    discard = True
                elif (clst[k].HasBattalion() and factory.IsCannon(clst[k].GetBattalion()) and False):
                    Log('The siege tower cannot be placed due a cannon is in its path. Try again!', VERBOSE_WARNING)
                    discard = True
                elif (clst[k].HasRiver()):
                    Log('The siege tower cannot be placed due the river is in its path. Try again!', VERBOSE_WARNING)
                    discard = True
                k += 1
            if (discard):
                continue

            # Create the battalion unit with calculated path, selected wall, and starting point, that will be the farthest point (that is, the last cell in path)
            b = factory.newBattalion(army, 'SiegeTowers', 1)
            if (b != None):
                b.SetTargetWall(wall=selwall, path=clst)
                b.SetArmy(army)
                b.SetCommand(command)
                b.AssignToCell(clst[0])
                army.InsertBattalion(b)
            else:
                # No more avaiable troops
                Log('There arent enough siege towers to deploy', VERBOSE_WARNING)
                return

            i += 1

    def DeployCannons(self, army, maxDeployed, maxPerWall, castle, command=Command.ATTACK_CASTLE):
        # Special automatic deployment for cannons. The placement is calculated from the best castle walls to attack 
        # If maxDeployed is -1 all cannons will be deployed (if it is possible)
        # maxPerWall is the maximum number of cannons commanded to attack the same wall. -1 means all of avaliable cannons will be placed (warning, this could spend all of cannons
        # units for the first selected wall)

        # A set of cannons will be deployed for each wall. The longest walls have more preference
        lst = castle.GetWallsList()
        lst.sort(key=GetWallLength_Sort, reverse=True)

        # Discard the too short walls
        wlst = []
        short = False
        i = 0
        while ((i < len(lst)) and not short):
            w = lst[i]
            if ((w.GetLength() <= self.__cellsize) or not w.IsReachable()):
                short = True
            else:
                wlst.append(w)
            i += 1

        factory = ArmyFactory()

        for w in wlst:

            b = factory.newBattalion(army, 'Cannons', 1)
            if (not b):
                return

            # Deploy maxPerWall (or less) cannons in front of wall. From the middle point, place the first cannon as far as cannon shoot distance is. Then, the other cannons
            # are placed around it following the same direction than wall (maximize the shoot effectiveness)

            seg = Segment2D(w.GetStartPosition(), w.GetEndPosition())
            mid = seg.GetMidPoint()
            norm = seg.GetNormal()
            mid.Move(norm, b.GetSuitableDeploymentDistance())

            ccwall = 0

            cell = self.GetCellFromPoint(point=mid, fit=True)
            if (cell.IsAvailable()):
                b.AssignToCell(cell)
                army.InsertBattalion(b)
                b.SetCommand(command=command, target=w)
                ccwall = 1

            # To get the beside cannon deployments, trace two rays, with same orientation but opposite directions. Then we can deploy as much cannons as required in both sides
            clst = self.RayTraversal(pStart=mid, pEnd=None, direction=seg.GetDirection().Invert())

            # The deployment is limited by: max number of cannons per wall, available cannons, wall size

            i = 1  # i=0 is the already deployed cannon
            stop = ((ccwall >= int(maxPerWall / 2.0)) and (maxPerWall != -1)) or (i >= len(clst))
            while (not stop):

                # Cannons cannot be deployed away from wall
                dist = mid.Distance(clst[i].center)
                stop = dist >= (w.GetLength() / 2.0)
                if (not stop):

                    # Check the cell contents
                    if (clst[i].IsAvailable()):

                        # Creates cannon 
                        b = factory.newBattalion(army, 'Cannons', 1)
                        stop = (b == None)
                        if (not stop):
                            # Deploys the cannon
                            b.AssignToCell(clst[i])
                            army.InsertBattalion(b)
                            b.SetCommand(command=command, target=w)

                            ccwall += 1
                            i += 1

                            stop = ((ccwall >= int(maxPerWall / 2.0)) and (maxPerWall != -1)) or (i >= len(clst))

                    else:

                        i += 1
                        stop = (i >= len(clst))

            clst = self.RayTraversal(pStart=mid, pEnd=None, direction=seg.GetDirection())

            i = 1  # i=0 is the already deployed cannon
            stop = ((ccwall >= int(maxPerWall / 2.0)) and (maxPerWall != -1)) or (i >= len(clst))
            while (not stop):

                # Cannons cannot be deployed away from wall
                dist = mid.Distance(clst[i].center)
                stop = dist >= (w.GetLength() / 2.0)
                if (not stop):

                    # Check the cell contents
                    if (clst[i].IsAvailable()):

                        # Creates cannon 
                        b = factory.newBattalion(army, 'Cannons', 1)
                        stop = (b == None)
                        if (not stop):
                            # Deploys the cannon
                            b.AssignToCell(clst[i])
                            army.InsertBattalion(b)
                            b.SetCommand(command=command, target=w)

                            ccwall += 1
                            i += 1

                            stop = ((ccwall >= int(maxPerWall / 2.0)) and (maxPerWall != -1)) or (i >= len(clst))

                    else:

                        i += 1
                        stop = (i >= len(clst))

    def DeployOnCenteredLine(self, center, direction, alternativedirection, army, kind, maxpercell, groupsize,
                             groupdistance, command, castle):
        # Deploys a given kind of battalion of given army onto the battle field following a centered line
        # The line is centered at center 2D position and has the given line direction
        # The battalions are deployed along the line. If any cell is filled with any other battalion or construction, uses the given alternative direction to get a new cell
        # and continues along the respective parallel line
        # We can create battalions groups for each line with groupsize as each group size, and groupdistance as distance between them. If groupsize is -1 there isnt groups

        factory = ArmyFactory()

        b = factory.newBattalion(army, kind, maxpercell)
        if (not b):
            return

        # Get the number of effective for each  cell
        nforeachcell = b.GetNumberByCell(self.__cellsize)
        if ((maxpercell > 0) and (maxpercell < nforeachcell)):
            nforeachcell = maxpercell

        b = factory.newBattalion(army, kind, nforeachcell)
        if (not b):
            return

            # Deploys the central battalion. Checks if given position is already occupied (take the parallel line with alternative direction in this case)
        stop = False
        cell = self.GetCellFromPoint(point=center, fit=True)
        while (not stop):
            if (cell.IsAvailable()):
                b.AssignToCell(cell)
                army.InsertBattalion(b)
                b.SetCommand(command=command, target=castle.GetClosestWall(populated=True, posfrom=cell.center))

                stop = True

            else:

                # Get the parallel line
                # Unfortunately, we cannot optmize the algorithm cutting the ray traversal to a some number of cells due the nature of the raytraversal algorithm. It reverse
                # the ray if is inverted from the X axis. Then it reverses the result at the end
                parallel = self.RayTraversal(pStart=Point2D().SetFrom3D(cell.center), pEnd=None,
                                             direction=alternativedirection)
                if (len(parallel) < 2):
                    print "ERROR DeployOnCenteredLine -> Not enough space to place any battalion of " + kind
                    return
                cell = parallel[1]

        # To go through the centered line trace two rays with same orientation but opposite directions
        clstright = self.RayTraversal(pStart=Point2D().SetFrom3D(cell.center), pEnd=None, direction=direction)
        clstleft = self.RayTraversal(pStart=Point2D().SetFrom3D(cell.center), pEnd=None,
                                     direction=direction.Copy().Invert())

        # Go through both line sides at the same time to get a well balanced deployment

        hasgroups = (groupsize >= 1)
        groupsize_left = floor(groupsize / 2.0)
        groupsize_right = groupsize_left
        if ((groupsize % 2.0) == 0):
            # count the already inserted point
            groupsize_left += 1
        currentgroupsize_left = 0
        currentgroupsize_right = 0

        i_left = 1  # i=0 -> pStart -> center
        i_right = 1
        stop_left = (len(clstleft) < 2)
        stop_right = (len(clstright) < 2)
        while ((not stop_left) or (not stop_right)):

            if (not stop_left):

                cell = clstleft[i_left]

                # Check the cell contents
                if (cell.IsAvailable()):

                    # Creates a new battalion 
                    b = factory.newBattalion(army, kind, nforeachcell)
                    stop_left = (b == None)  # Not enough troops
                    if (not stop_left):

                        # Deploys the battalion
                        b.AssignToCell(cell)
                        army.InsertBattalion(b)
                        b.SetCommand(command=command, target=castle.GetClosestWall(populated=True, posfrom=cell.center))

                        i_left += 1
                        if (i_left >= len(clstleft)):
                            stop_left = True
                        else:
                            # Check the group condition    
                            if (hasgroups):
                                currentgroupsize_left += 1
                                if (currentgroupsize_left >= groupsize_left):

                                    currentgroupsize_left = 0

                                    # The first deployed group share the size at left and right. Then, each group must have the original group size
                                    groupsize_left = groupsize

                                    # Increase the cell index until the distance from current cell to the new one is greater than groupdistance
                                    dist = cell.center.Distance(clstleft[i_left].center)
                                    while ((dist < groupdistance) and not stop_left):
                                        i_left += 1
                                        if (i_left >= len(clstleft)):
                                            stop_left = True
                                        else:
                                            dist = cell.center.Distance(clstleft[i_left].center)

                else:

                    # Change to the parallel line
                    # Unfortunately, we cannot optimize the algorithm cutting the ray traversal to a some number of cells due the nature of the raytraversal algorithm. It reverse
                    # the ray if is inverted from the X axis. Then it reverses the result at the end

                    parallel = self.RayTraversal(pStart=Point2D().SetFrom3D(cell.center), pEnd=None,
                                                 direction=alternativedirection)
                    if (len(parallel) < 2):
                        stop_left = True  # Not enough space for more deployments
                    else:
                        clstleft = self.RayTraversal(pStart=Point2D().SetFrom3D(parallel[1].center), pEnd=None,
                                                     direction=direction.Copy().Invert())
                        if (len(clstleft) < 2):
                            stop_left = True
                        else:
                            i_left = 0  # i=1 -> new cell, empty now

            if (not stop_right):

                cell = clstright[i_right]

                # Check the cell contents
                if (cell.IsAvailable()):

                    # Creates a new battalion 
                    b = factory.newBattalion(army, kind, nforeachcell)
                    stop_right = (b == None)  # Not enough troops
                    if (not stop_right):

                        # Deploys the battalion
                        b.AssignToCell(cell)
                        army.InsertBattalion(b)
                        b.SetCommand(command=command, target=castle.GetClosestWall(populated=True, posfrom=cell.center))

                        i_right += 1
                        if (i_right >= len(clstright)):
                            stop_right = True
                        else:
                            # Check the group condition    
                            if (hasgroups):
                                currentgroupsize_right += 1
                                if (currentgroupsize_right >= groupsize_right):
                                    currentgroupsize_right = 0

                                    # The first deployed group share the size at left and right. Then, each group must have the original group size
                                    groupsize_right = groupsize

                                    # Increase the cell index until the distance from current cell to the new one is greater than groupdistance
                                    dist = cell.center.Distance(clstright[i_right].center)
                                    while ((dist < groupdistance) and not stop_right):
                                        i_right += 1
                                        if (i_right >= len(clstright)):
                                            stop_right = True
                                        else:
                                            dist = cell.center.Distance(clstright[i_right].center)


                else:

                    # Change to the parallel line
                    # Unfortunately, we cannot optimize the algorithm cutting the ray traversal to a some number of cells due the nature of the raytraversal algorithm. It reverse
                    # the ray if is inverted from the X axis. Then it reverses the result at the end

                    parallel = self.RayTraversal(pStart=Point2D().SetFrom3D(cell.center), pEnd=None,
                                                 direction=alternativedirection)
                    if (len(parallel) < 2):
                        stop_right = True  # Not enough space for more deployments
                    else:
                        clstright = self.RayTraversal(pStart=Point2D().SetFrom3D(parallel[1].center), pEnd=None,
                                                      direction=direction)
                        if (len(clstright) < 2):
                            stop_right = True
                        else:
                            i_right = 0  # i=0 -> new cell, empty now

    def DeploySiegeTowersOnCenteredLine(self, center, direction, alternativedirection, army, mindistance, command,
                                        castle):
        # Special case for DeployOnCenteredLine. The algorithm changes to deploy the siege tower checking its path to its target. From the deployment point, first get a 
        # flank line free from other battalions. Then check each path from current cell to the nearest wall. If its clear, deploy the unit. Otherwise, check the side cells
        # If there is enough cells (battlefield limits reached), the siege tower is not deployed
        # mindistance is used to set a minimum distance between deploymens. Note that this is a minimum distance, not a fixed one. Because we are deploying at left and right
        # at the same time, and its hard to control the distance to the last deployed siege towers, we only can assure that the minimum distance, not a fixed one

        factory = ArmyFactory()

        # Search the central position. Checks if given position is already occupied (take the parallel line with alternative direction in this case)
        cell = self.GetCellFromPoint(point=center, fit=True)
        while (not cell.IsAvailable()):

            # Get the parallel line
            # Unfortunately, we cannot optmize the algorithm cutting the ray traversal to a some number of cells due the nature of the raytraversal algorithm. It reverse
            # the ray if is inverted from the X axis. Then it reverses the result at the end
            parallel = self.RayTraversal(pStart=Point2D().SetFrom3D(cell.center), pEnd=None,
                                         direction=alternativedirection)
            if (len(parallel) < 2):
                print "ERROR DeployOnCenteredLine -> Not enough space to place any siege tower"
                return
            cell = parallel[1]

        # Get the side cells where the siege tower can be deployed if current cell is not avaiable
        clstright = self.RayTraversal(pStart=Point2D().SetFrom3D(cell.center), pEnd=None, direction=direction)
        clstleft = self.RayTraversal(pStart=Point2D().SetFrom3D(cell.center), pEnd=None,
                                     direction=direction.Copy().Invert())

        leftside = True  # Switch variable to use left or right cells list each time

        if (len(clstright) < 2):
            stop_right = True
        else:
            stop_right = False

        if (len(clstleft) < 2):
            stop_left = True
            leftside = False
        else:
            stop_left = False

        i_left = 1
        i_right = 1
        deployed = False
        while (not deployed):

            # Get the closest wall as suitable target
            targetwall = castle.GetClosestWall(populated=False, posfrom=cell.center)
            if (targetwall == None):
                Log("WARNING: Siege tower dont deployed due it cannot find the closest wall", VERBOSE_WARNING)
                return

            # The siege tower must advance to the wall in a perpendicular way. So, a path is traced from the siege tower and using the wall normal vector as the direction
            # If the first cell with any deployed construction found is the target wall, the path is correct. Otherwise, we have to move the siege tower
            # NOTE that this method is significantly different from the automatic siege tower deployment. Here, because we depend on the flank position, we cannot decide what to
            # wall attack.

            # WARNING: The last conclusion is WRONG. The path should be created from the initial siege tower position and targeted wall center position. Using the wall
            # normal in too graze angles could be an error. The central wall position is the most suitable place to attack. I keep the last comment because Im not sure
            # about the origin reasons to use this conclusion ... :-S

            # clstfront = self.RayTraversal(pStart = Point2D().SetFrom3D(cell.center), pEnd = None, direction = Vector2D().SetFrom3D(targetwall.GetNormalVector()))
            clstfront = self.RayTraversal(pStart=Point2D().SetFrom3D(cell.center), pEnd=targetwall.GetMidPoint(),
                                          direction=None)
            if (len(clstfront) >= 2):

                # Check the path content
                i_path = 1
                stop_path = False
                discard = False
                while (not stop_path):
                    cpath = clstfront[i_path]
                    # Check for any battalions, trenches or constructions different from the target wall
                    if (cpath.HasRiver() or
                            cpath.HasWaterMoat() or
                            (cpath.HasBattalion() and factory.IsCannon(cpath.GetBattalion())) or
                            (cpath.HasConstructions() and not cpath.HasThisConstruction(targetwall))
                    ):
                        discard = True
                        stop_path = True
                    elif ((cpath.HasConstructions() and cpath.HasThisConstruction(targetwall))
                          or cpath.IsCity()):
                        stop_path = True
                    else:
                        i_path += 1
                        if (i_path >= len(clstfront)):
                            discard = True
                            stop_path = True

                if (not discard):

                    # The path is checked and correct. Deploy the siege tower
                    b = factory.newBattalion(army, 'SiegeTowers', 1)
                    if (b != None):
                        b.SetTargetWall(wall=targetwall, path=clstfront)
                        b.SetArmy(army)
                        b.SetCommand(command)
                        b.AssignToCell(cell)
                        army.InsertBattalion(b)

                        # To avoid unnecessary computations, check here if we have more siege towers to deploy
                        if (not army.IsBattalionTypeAvaiable("SiegeTowers")):
                            deployed = True
                        else:

                            # Apply the next deployment distance to each side
                            dist = 0
                            while ((dist < mindistance) and not stop_left):
                                i_left += 1
                                if (i_left >= (len(clstleft))):
                                    stop_left = True
                                else:
                                    dist = cell.center.Distance(clstleft[i_left].center)
                            dist = 0
                            while ((dist < mindistance) and not stop_right):
                                i_right += 1
                                if (i_right >= (len(clstright))):
                                    stop_right = True
                                else:
                                    dist = cell.center.Distance(clstright[i_right].center)

                            if (stop_left and stop_right):
                                print "ERROR: No more siege towers can be deployed"
                                return
                            elif (stop_left):
                                leftside = False
                            elif (stop_right):
                                leftside = True

                    else:
                        # No more avaiable troops
                        deployed = True

            if ((len(clstfront) < 2) or not deployed):
                # Choose another starting cell
                if (leftside):
                    cell = clstleft[i_left]
                    i_left += 1
                    if (i_left >= len(clstleft)):
                        stop_left = True
                else:
                    cell = clstright[i_right]
                    i_right += 1
                    if (i_right >= len(clstright)):
                        stop_right = True
                if (stop_left and stop_right):
                    print "ERROR: Siege tower cannot be deployed"
                    return
                elif (stop_left):
                    leftside = False
                elif (stop_right):
                    leftside = True
                else:
                    leftside = not leftside

                # Check the avaiability of the cell
                if (not cell.IsAvailable()):
                    while (not cell.IsAvailable()):

                        # Get the parallel line
                        # Unfortunately, we cannot optmize the algorithm cutting the ray traversal to a some number of cells due the nature of the raytraversal algorithm. It reverse
                        # the ray if is inverted from the X axis. Then it reverses the result at the end
                        parallel = self.RayTraversal(pStart=Point2D().SetFrom3D(cell.center), pEnd=None,
                                                     direction=alternativedirection)
                        if (len(parallel) < 2):
                            print "ERROR DeployOnCenteredLine -> Not enough space to place the siege tower"
                            return
                        cell = parallel[1]

                    # Get the side cells where the siege tower can be deployed if current cell is not avaiable
                    clstright = self.RayTraversal(pStart=Point2D().SetFrom3D(cell.center), pEnd=None,
                                                  direction=direction)
                    if (len(clstright) < 2):
                        stop_right = True
                    else:
                        i_right = 0
                    clstleft = self.RayTraversal(pStart=Point2D().SetFrom3D(cell.center), pEnd=None,
                                                 direction=direction.Copy().Invert())
                    if (len(clstleft) < 2):
                        stop_left = True
                    else:
                        i_left = 0

                        ###########################################################################33

    # TRENCH RELATED METHODS
    ###########################################################################33

    def SetTrenchesPositions(self, tlst):
        # From a list of trenches positions (list of lists), where each point is a pair of coordinates on the battlefield grid (indexed coordinates), create the trenches objects

        self.__trenches = []

        for t in tlst:
            cells = []
            for tt in t:
                cells.append(self.GetCell(tt[0], tt[1]))
            trench = Trench.Trench(self, cells)

            self.__trenches.append(trench)

    def SetTrenchesCells(self, clist, append):
        # Construct the trenches from an unique list of battlefield cells

        if (not append):
            self.__trenches = []

        trench = Trench.Trench(self, clist)

        self.__trenches.append(trench)

    def GetClosestTrench(self, frompos, free=True, searchradius=1.0, castle=None, battalion=None):
        # Returns the closest trench to given 2D position that satisfies the next conditions:
        # If free is True, the trench has to have avaiable places
        # The distance between frompos and trench must be less than searchradius
        # If battalion is not None, the battalion cannot has had visited previously the trench (avoiding the flickering effect)

        if (not castle):
            return None

        ret = None
        minD = -1

        for t in self.__trenches:
            if ((free and not t.IsFull()) or not free):
                if ((not battalion) or (battalion and not t.HasVisited(battalion))):
                    dist = t.GetDistanceFromPoint(frompos)
                    if (dist < searchradius):
                        if ((not ret) or (minD > dist)):
                            minD = dist
                            ret = t

        return ret

    # Old method to get the closest trench based on the distance between trench and nearest construction
    """    
    def GetClosestTrench(self, frompos, free = True, target = None, maxdist = -1, castle = None, battalion = None):
        # Returns the closest trench to given 2D position that satisfies the next conditions:
        # If free is True, the trench has to have avaiable places
        # If given target is not None, trench closest construction must match with this target
        # If maxdist is not -1, the distance from trench to the closest construction cannot be greater than given one
        # If battalion is not None, the battalion cannot has had visited previously the trench (avoiding the flickering effect)
 
        if (not castle):
            return None
        
        ret = None
        minD = -1
        

        for t in self.__trenches:
            if ((free and not t.IsFull()) or not free):
                if ((not battalion) or (battalion and not t.HasVisited(battalion))):
                    if (not target or (target == t.GetClosestConstruction(castle))):
                        if ((maxdist == -1) or (maxdist > t.GetDistanceConstruction())):
                            dist = t.GetDistanceFromPoint(frompos)
                            if ((not ret) or (minD > dist)):
                                minD = dist
                                ret = t
        

                
                
        return ret
     """

    def DeployRandomTrenches(self):
        # Deploy random trenches allong all battlefield

        # random.seed()

        i = 0
        while (i < self.__cellsarraysize["rows"]):
            j = 0
            while (j < self.__cellsarraysize["columns"]):
                c = self.__cells[i][j]

                # First check if current cell could be a trench
                if (random.random() < Battles.Utils.Settings.SETTINGS.Get_F('Battlefield', 'Trench',
                                                                            'RandomDeployment')):

                    # Second, start following the consecutive cells in random direction until the random filter cut it off
                    lst = [c]
                    inext = i
                    jnext = j
                    tries = 0
                    while ((random.random() < Battles.Utils.Settings.SETTINGS.Get_F('Battlefield', 'Trench',
                                                                                    'RandomDeploymentConsecutive')) and (
                                   tries < Battles.Utils.Settings.SETTINGS.Get_F('Battlefield', 'Trench',
                                                                                 'RandomDeploymentMaxTries'))):

                        xrand = int(floor(random.random() * 3) - 1 + inext)
                        yrand = int(floor(random.random() * 3) - 1 + jnext)

                        if (xrand < 0):
                            xrand = 0
                        if (yrand < 0):
                            yrand = 0
                        if (xrand >= self.__cellsarraysize["rows"]):
                            xrand = self.__cellsarraysize["rows"] - 1
                        if (yrand >= self.__cellsarraysize["columns"]):
                            yrand = self.__cellsarraysize["columns"] - 1

                        cnext = self.__cells[xrand][yrand]

                        if (c.IsAvailable()):
                            c = cnext
                            inext = xrand
                            jnext = yrand
                            lst.append(c)

                        tries += 1

                    # Add all collected cells as trenches
                    trench = Trench.Trench(self, list(set(lst)))
                    self.__trenches.append(trench)

                j += 1
            i += 1

    ###########################################################################33
    # RIVER RELATED METHODS
    ###########################################################################33

    def DeployRiver(self, river):

        # Store and deploys given river into the battlefield
        self.__rivers.append(river)

        # Check for each cell if it falls on the river shape
        # This is not the most efficient way to do it, but for now is not required to construct any kind of acceleration structure only for this task, that should be performed
        # only one time per execution

        # WARNING: If a cell is already on a river, only is considered the last river deployed

        bound = river.GetBounding()
        cellmin = self.GetCellFromPoint(point=bound.minPoint, fit=True)
        cellmax = self.GetCellFromPoint(point=bound.maxPoint, fit=True)

        row = cellmin.GetRow()
        while (row < cellmax.GetRow()):
            col = cellmin.GetColumn()
            while (col < cellmax.GetColumn()):
                cell = self.__cells[row][col]
                if (river.IsInside(Point2D().SetFrom3D(cell.center))):
                    cell.SetRiver(river)
                    river.AddBattlefieldCell(cell)
                col += 1
            row += 1

    def CheckShapeOnRiver(self, poly):
        # Checks if given 2D polygon intersects to any river, and modify it to avoid the intersection

        if (len(self.__rivers) == 0):
            return

        # Work only with the polygon points
        vertices = poly.GetPointsList()

        # First perform a 2D shape clipping difference between the incoming polygon and the river polygon. Because rivers are a set of closed polygons, GPC library could
        # generates wrong shapes, with some vertices inside the rivers (for precision problems and just where the river polyogons intersect).
        # For that reason, after the clipping difference is generated, a new algorithm process each vertex checking if it falls inside a river

        # NOTE: Both algorithms should be enough to solve the problem, but the first one generates wrong vertices inside rivers polygons, and the second one cannot solve some situations
        # , with a high level of casuistics (like the castle joins algorithm). So, the combination between both methods produces reasonable good results

        # Shape clipping difference
        gpc = GPCWrapper()

        # Get the river whole polygon
        riverpoly = self.__rivers[0].GetPointsList()
        i = 1
        while (i < len(self.__rivers)):
            riverpoly = gpc.Union(plist1=riverpoly, plist2=self.__rivers[i].GetPointsList())
            i += 1

        # Perform the difference between given vertices list and each river bounding
        verticeslist = gpc.Difference(plist1=vertices, plist2=riverpoly)

        # Due the difference operation can generates more than one polygon, we can have more than one vertices list
        # To simplify the problem, we choose the largest one, so in many cases the polygon with largest area will be the correct one (imagine a polygon that overlaps and pass
        # over a river just a few meters)
        vertices = gpc.GetLargestPolygon(verticeslist)
        if (vertices == None):
            return

        # Now, clean the resulting shape checking those vertices that fall in a river
        end = False
        while (not end):

            end = True

            # Check if there are vertices close or inside any river
            # Move them to avoid the intersection
            i = 0
            while (i < len(vertices)):

                cell = self.GetCellFromPoint(vertices[i])
                if (cell and cell.HasRiver()):

                    end = False

                    # Calculate the smallest 2D angle between the vector constructed with current and last point, and the river main direction
                    # The smallest angle need is because we can consider two river vectors (main direction and negative direction). The smallest angle helps avoiding too much degenerated polygons
                    river = cell.GetRiver()
                    axisriver = river.GetClosestAxisSegment(vertices[i])
                    axisvec = Vector2D().CreateFrom2Points(axisriver.p1, axisriver.p2)
                    axisvecneg = axisvec.Copy().Invert()

                    polyvec = Vector2D().CreateFrom2Points(vertices[i - 1], vertices[i])

                    # Get the angles between last vertex and current one, and the river directions
                    # If any of them is close to 0, apply a small offset to avoid obtaining the same final vertex (this would be an infinite loop)
                    ang1 = polyvec.AngleBetween(axisvec)
                    if (ang1 < 1.0):
                        ang1 += 1.0
                        axisvec.Rotate(1.0)
                    ang2 = polyvec.AngleBetween(axisvecneg)
                    if (ang2 < 1.0):
                        ang2 += 1.0
                        axisvecneg.Rotate(1.0)

                    # Choose the smallest angle and related vector                    
                    if (ang1 < ang2):
                        ang = ang1
                        vec = axisvec
                    else:
                        ang = ang2
                        vec = axisvecneg

                    # If angle is less than 45, transform current segment to be parallel to the river
                    # Otherwise, just approach the current vertex to the last one, and wait for the next loop 
                    newp = vertices[i - 1].Copy()
                    newseg = Segment2D(vertices[i - 1], vertices[i])
                    if (ang > 45.0):
                        newp.Move(polyvec, newseg.GetLength() * 0.9)
                        dist = newp.Distance(vertices[i - 1])
                        if (dist < Battles.Utils.Settings.SETTINGS.Get_F('City', 'MinWallLength')):
                            # Too much close
                            vertices.pop(i)
                            continue
                        elif (dist > Battles.Utils.Settings.SETTINGS.Get_F('City', 'MaxWallLength')):
                            # Too much long
                            newp = vertices[i - 1].Copy()
                            newp.Move(polyvec, dist / 2.0)

                    else:
                        newp.Move(vec, newseg.GetLength())

                    newseg = Segment2D(vertices[i - 1], newp)
                    j = 0
                    stop = False
                    while ((j < len(self.__rivers)) and not stop):
                        pnt = self.__rivers[j].IntersectAxis(newseg)
                        if (pnt != None):
                            stop = True
                            newp = pnt

                        j += 1

                    vertices[i] = newp

                    # Repeat the process until none vertex has to move, so the new position could fall into the river again (too complex to 
                    # solve all cases in one loop)

                i += 1

            # Purge some bad vertices (too short and too long segments)
            k = 0
            while (k < len(vertices)):
                seg = Segment2D(vertices[k - 1], vertices[k])
                dist = seg.GetLength()
                if (dist < Battles.Utils.Settings.SETTINGS.Get_F('City', 'MinWallLength')):
                    vertices.pop(k)
                    k += 1
                elif (dist > Battles.Utils.Settings.SETTINGS.Get_F('City', 'MaxWallLength')):
                    l = k
                    while (dist > Battles.Utils.Settings.SETTINGS.Get_F('City', 'MaxWallLength')):
                        seg.p1.Move(seg.GetDirection(), Battles.Utils.Settings.SETTINGS.Get_F('City', 'MaxWallLength'))
                        vertices.insert(l, seg.p1.Copy())
                        dist -= Battles.Utils.Settings.SETTINGS.Get_F('City', 'MaxWallLength')
                        l += 1
                    k = l + 1
                else:
                    k += 1

        # Convert the vertices list to segments list
        poly.shape = []
        i = 0
        while (i < len(vertices)):
            if (vertices[i - 1].Distance(vertices[i]) > Battles.Utils.Settings.SETTINGS.Get_F('City', 'MinWallLength')):
                poly.shape.append(Segment2D(vertices[i - 1], vertices[i]))
            i += 1

        # TODO: This algorithm has problems in these cases:
        #
        #    - Self-crossing polygons can be generated removing or moving vertices that fall on a river
