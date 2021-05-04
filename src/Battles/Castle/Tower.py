from Battles.Castle import Construction, BattalionConstruction
from Battles.Utils.Geometry import *
from Battles.Factory import ConstructionFactory
from Battles.Army.Action import Command
import Battles.Utils.Settings 



class Tower(Construction.Construction):
    """ Tower construction class
    
    Attributes:
        center: Center 2D position
        height: Tower height
        slope: Exterior and bottom slope. See at Geometry.Slope
        ceiling: Ceiling data
    """
    
    towerCounter = 0
    
    
    
    def __init__(self):
        Construction.Construction.__init__(self)
        self._height =  Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Tower', 'InnerHeight')
        self._thickness =  Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Tower', 'Thickness')
        self._defenseIncrease =  Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Tower', 'DefenseIncrease')
        self._center = Point2D()
        #self._slope = None
        #self._ceiling = {"altitude": (self._height -  Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Wall', 'MerlonHeight'))}
        
        self._defendingLines = BattalionConstruction.BattalionConstruction(height = self._height, cellsize = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Tower', 'BattalionGridCellSize/Small'))

        self._label = 'Tower_' + str(Tower.towerCounter)
        Tower.towerCounter += 1
        

    def Copy(self):
        pass

    #def GetBattalionAltitude(self, defendingline):
        #return self.__ceiling["altitude"]
    
    @classmethod    
    def ResetCounter(cls):
        cls.towerCounter = 0        
    
        
    def SetPosition(self, center, wallA, wallB, castlevector):
        # Sets the central tower position between given walls
        self._center = center
        
        
    def GetPosition(self):
        return self._center     
        
    def Draw(self, level, canvas, viewport):
        Construction.Construction.Draw(self, level, canvas, viewport)
        
        # Shape
        l = len(self._shape2D)
        if (l > 0):
            p1 = self._shape2D[0]
            i = 1
            while (i < l):
                p2 = self._shape2D[i]
                vp1 = viewport.W2V(p1)
                vp2 = viewport.W2V(p2)
                self._canvasObjs.append(canvas.create_line(vp1.x, vp1.y, vp2.x, vp2.y, fill=self.GetLevelColor(level), width="2"))
                
                p1 = p2
                i += 1
                
            if (l > 2):
                # Close shape
                p1 = self._shape2D[0]
                p2 = self._shape2D[l-1]
                vp1 = viewport.W2V(p1)
                vp2 = viewport.W2V(p2)
                self._canvasObjs.append(canvas.create_line(vp1.x, vp1.y, vp2.x, vp2.y, fill=self.GetLevelColor(level), width="2"))
                
        if (Battles.Utils.Settings.SETTINGS.Get_B('Castle', 'ShowLabels')):
            # Text the kind of battalion
            cv = viewport.W2V(self.GetPosition())
            self._canvasObjs.append(canvas.create_text(cv.x, cv.y, text=self.GetLabel(), fill="blue"))
                
                
                
    def JoinShape(self, obj, invert = False):
        # Creates and join current shape with given object's shape
        # Usually the tower shape does not change joining with other objects, such are walls. So, perform a nice "inverted passing shoot" to wall object
        # Invert parameter is unused
       
        factory = ConstructionFactory()
        
        if (factory.IsWall(obj)):
            obj.JoinShape(self, invert = True)
        

    def IsDefeated(self):
        # Returns true if tower is defeated
        
        """
        tile = self.GetBrokenTile()
        if (tile != None):
            return True
        """
        
        return False


    def GetDefeatReason(self):
        # If tower is defeated, returns a result object (None otherwise)
        """
        if (self.IsDefeated()):
            
            tile = self.GetBrokenTile()
            if (tile == None):
                print('A defeated wall non-climbed doesnt have any broken tile!!')
                return None
            
            
            result = Results.ResultDataHoleConstruction(self.GetLabel(), self.GetTileCenter(tile[0], tile[1]))
            
            return result
        
        else:
            return None        
        """
        return None


    def GetDefenseAngle(self):
        #return TOWER_DEFENSE_ANGLE
        h = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Tower', 'DefenseAngle/H')
        v = Battles.Utils.Settings.SETTINGS.Get_A('Castle', 'Tower', 'DefenseAngle/V')
        return {'H': h, 'V': {'bottom': v[0], 'top': v[1]}}        


    def GetRequiredAroundSpace(self):
        pass


    def IsCloser(self, point):
        # Returns true if given 2D point is enough close to current tower
        return (point.Distance(self._center) <= self.GetRequiredAroundSpace())



    def GetMinDistance(self, constr):

        factory = ConstructionFactory()
        
        if (factory.IsWall(constr)):
            # WARNING: We avoid to check the minimum distance from the two wall vertices due this function is used by the castle union
            # algorithm. Due the nature of that algorithm, we are more interested into get the minimum distance from the first vertex
            # Be aware changing this code     
            
            d1 = self.GetPosition().Distance(constr.GetStartPosition())
            d2 = self.GetPosition().Distance(constr.GetEndPosition())

            if (d1 <= d2):
                return d1
            else:
                return d2
            
 
        elif (factory.IsTower(constr)):
            
            return self.GetPosition().Distance(constr.GetPosition())
        
        else:
            return 0.0
        



class SquaredTower(Tower):
    """ Squared shape tower. The shape vertices order are: [bottom-left, bottom-right, top-right, top-left]
        Be aware about the screen coordinates when check the shape vertices order. Bottom means it's drawn at top
    
    Attributes:
        side: Square side length (in meters)
        shape3D and normal3D: 3D geometry used to calculate ray hits. Calculated in SetPosition method. 
        bounding3D: list of 3D bounding boxes for each castle side. Used to calculate the ray hits
        
    """
    
    def __init__(self):
        Tower.__init__(self)
        self.__side =  Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Tower', 'SquareSide')
        self.__shape3D = []
        self.__normal3D = []
        self.__bounding3D = []
    

    def Copy(self):
        # Copy just the minimum required data to get the tower properties without "disturbing" references to other objects

        # Common squared tower data
        tower = SquaredTower()
        tower.__side = self.__side

        # Common tower data
        tower._height =  self._height
        tower._thickness =  self._thickness
        tower._defenseIncrease =  self._defenseIncrease
        tower._center = self._center
        #tower._slope = None
        #tower._ceiling["altitude"] = self._ceiling["altitude"]
        tower._defendingLines = BattalionConstruction.BattalionConstruction(height = self._height, cellsize = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Tower', 'BattalionGridCellSize/Small'))
        tower._label = 'Tower_' + str(Tower.towerCounter)
        Tower.towerCounter += 1

        # Common construction data
        tower._axis2D = []
        for p in self._axis2D:
            tower._axis2D.append(p.Copy())

        return tower


    def GetSideLength(self):
        return self.__side
    
    def SetPosition(self, center, wallA, wallB, castlevector):
        # Places a squared tower between given walls. The castlevector parameter is used to rotate the tower shape at same direction than castle orientation
        
        Tower.SetPosition(self, center, wallA, wallB, castlevector)
        """
        bisec = wallA.GetBisector(wallB)
        axisdirection = bisec["bisector"]

        # Distance from center to most external vertex (square half diagonal)
        d = math.sqrt((self.__side / 2.0)**2 + (self.__side / 2.0)**2)
        """
         
        # Calculate the tower shape
        p = center.Copy()
        p.Move(castlevector, self.__side / 2.0)
        v = castlevector.Copy()
        v.Rotate(90)
        p.Move(v, -self.__side / 2.0)       # Bottom-left
        self._shape2D.append(p.Copy())
        p.Move(v, self.__side)              # Bottom-right
        self._shape2D.append(p.Copy())
        p.Move(castlevector, -self.__side)   # Top-right
        self._shape2D.append(p.Copy())
        p.Move(v, -self.__side)             # Top-left
        self._shape2D.append(p.Copy())
        
        """
        # The axis starts at center and go though given axis direction to the external squared tower vertex
        p = center.Copy()
        p.Move(axisdirection, d)
        self._axis2D.append([center, p])
         
        # Two additional axis segments from last one to the intersection with adjacent walls
        
        # Get the points over wall shapes at fixed distance from common points between walls
        segA = wallA.GetExteriorSegment()
        segB = wallB.GetExteriorSegment()
        vA = wallA.GetWallVector()
        vB = wallB.GetWallVector()
        pA = segA[1].Copy()
        pA.Move(vA, -TOWER_OFFSET_WALL)
        self._axis2D.append([p.Copy(), pA])
        pB = segB[0].Copy()
        pB.Move(vB, TOWER_OFFSET_WALL)
        self._axis2D.append([p.Copy(), pB])
        """
        
        # Calculate the axis. Due the axis is used (currently) to place the battalions, copy the tower shape and reduce it
        
        p1 = center.Copy()
        p1.Move(castlevector, (self.__side - self._thickness) / 2.0)
        v = castlevector.Copy()
        v.Rotate(90)
        p1.Move(v, -(self.__side - self._thickness) / 2.0)       # Bottom-left
        p2 = p1.Copy()
        p2.Move(v, (self.__side - self._thickness))              # Bottom-right
        p3 = p2.Copy()
        p3.Move(castlevector, -(self.__side - self._thickness))   # Top-right
        p4 = p3.Copy()
        p4.Move(v, -(self.__side - self._thickness))             # Top-left
        self._axis2D.append(Segment2D(p1, p2))
        self._axis2D.append(Segment2D(p2, p3))
        self._axis2D.append(Segment2D(p3, p4))
        self._axis2D.append(Segment2D(p4, p1))
        
        
        # Set the defending lines
        i = 0
        while (i < len(self._axis2D)):
            self._defendingLines.SetDefendingLine(i, self._axis2D[i])
            i += 1
        
        
        
        # Calculate the 3D geometry used to check impacts
        self.__shape3D = []
        self.__normal3D = []
        self.__bounding3D = []
        n = 0
        while (n < 4):
            lst = []

            if (n < 3):
                i1 = n
                i2 = n + 1
            else:
                i1 = 3
                i2 = 0
            
            lst.append(Point3D(self._shape2D[i1].x, self._shape2D[i1].y, 0))
            lst.append(Point3D(self._shape2D[i2].x, self._shape2D[i2].y, 0))
            lst.append(Point3D(self._shape2D[i2].x, self._shape2D[i2].y, self._height))
            lst.append(Point3D(self._shape2D[i1].x, self._shape2D[i1].y, self._height))
          
            self.__shape3D.append(lst)
            
            # Calculate 3D normal
            v = Segment2D(self._shape2D[i1], self._shape2D[i2]).GetNormal()
            self.__normal3D.append(Vector3D().SetFrom2D(v))
 
            # Calculate the face 3D bounding
            bbox = BoundingBox()
            for p in lst:
                bbox.InsertPoint(p)
            self.__bounding3D.append(bbox)

      
            n += 1
            
            
            
        
        
    def GetNormalVector(self, index = 0):
        # Returns the tower 3D normal vector by indexed side
        # Do not confuse with normal3D. Both can return the same vector, but they are used in different contexts and are suitable to be changed in the future
        
        if ((index < 0) or (index > 3)):
            print "ERROR: Index out of bounds for tower normal vector"
            return None
        
        normal = self._axis2D[index].GetNormal()
        return Vector3D(normal.val[0], normal.val[1], 0.0)
        
        
        
    def DistanceFromPoint(self, posfrom, squared = False):
        # Calculate the distance from given point to tower
        # Work in 2D to simplify
        
        p = Point2D(posfrom.x, posfrom.y)
        minD = -1
        for ax in self._axis2D:
            d = ax.DistanceToPoint(p, squared)
            if ((d < minD) or (minD == -1)):
                minD = d
                
        return minD
    
        
        
    def DeployInBattleField(self, battlefield):
        # Deploys current tower into given battlefield. Each battlefield cell will be linked with all  castle parts that intersect with it
        # Because the tower can be rotated (from castle vector), and can cover many battlefield cells, intersects the four sides as segments with the battlefield
        # In theory, the inner tower are shouldn't be accessed never by attackers due the tower shape is closed
                
        i = 0 
        while (i < 4):
            if (i == 3):
                lst = battlefield.RayTraversal(self._shape2D[3], self._shape2D[0])
            else:   
                lst = battlefield.RayTraversal(self._shape2D[i], self._shape2D[i+1])
            for c in lst:
                c.AppendDeployedConstruction(self)
                self._battleFieldCells.append(c)
            i += 1



    def GetRequiredAroundSpace(self):
        # Return the required around space to be deployed between walls
        
        #required = math.sqrt(2.0 * (tower.GetSideLength()**2))
        # The squared tower will be placed ever on the wall, so the required space is the tower side length
        return self.GetSideLength()





    def GetIntersectableSegments(self):
        
        ret = []
        
        i = 0 
        while (i < len(self._shape2D)):
            if (i == (len(self._shape2D) - 1)):
                inext = 0
            else:
                inext = i + 1
            
            ret.append(Segment2D(self._shape2D[i], self._shape2D[inext]))
            
            i += 1
            
        return ret
    
    
    

    ###########################################################################33
    # BATTALION RELATED METHODS
    ###########################################################################33
  
  
    def _DeployBattalion(self, army, kind, number, placetype, linespercell = -1, maxpercell = -1, command = Command.DEFEND_CASTLE):


        # If by settings definition, the tower doesnt have cannons, choose the small grid setting to deploy small units (aka archers)
        # By the other hand, if cannons are allowed, but they cannot be deployed, allow the small grid size to deploy archers.
        # Note that the last condition depends on the previously sorting on the battalions to deploy by size. The cannons are deployed first, and then the archers. So, if
        # the cannons cannot be deployed (size, available, ...), the archers should occupy its place
        i = 0
        while (i < 4):
            if ((not army.HasBattalionType("Cannons") or ((kind == 'Archers') and not self._defendingLines.HasCannons(index = i)))):
                self._defendingLines.SetCellSize(index = i, cellsize = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Tower', 'BattalionGridCellSize/Small'))
            else:
                self._defendingLines.SetCellSize(index = i, cellsize = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Tower', 'BattalionGridCellSize/Large'))

            self._defendingLines.DeployBattalion(i, self, army, kind, number, placetype, linespercell, maxpercell, command)

            i += 1

        # WARNING: Given number of troops to deploy will be used for each tower side. By example, number = 3 means 3 battalions for each tower side



        
    ###########################################################################33
    # TILES RELATED METHODS
    ###########################################################################33
 
 
 
         
    ###########################################################################33
    # ACTION RELATED METHODS
    ###########################################################################33

        
       
    def RecieveImpact(self, ray):
        # Checks if given ray impacts on any squared tower side
        # To simplify the algorithm, the hiding tower parts by walls are not considered (TODO: Consider the hiding tower parts)
        # See at class definition the shape vertices order
        
        i = 0
        dmin = -1
        hitmin = None
        
        while (i < 4):
            if (ray.HitRectangle(self.__shape3D[i], self.__bounding3D[i], self.__normal3D[i])):
                if ((hitmin == None) or (ray.GetLength() < dmin)):
                    dmin = ray.GetLength()
                    hitmin = ray.GetHitPoint()
            
            i += 1

        return hitmin
            
 
  
    def RayHitTest(self, ray):

       # Do the check in 2D -> easy and cheap (TODO: Do it (well) in 3D)
        ray2d = Ray2D().SetFrom3D(ray)
        seglist = self.GetIntersectableSegments()
        for seg in seglist:
            if (ray2d.HitSegment3(seg)):
                ray.SetHitPoint(Point3D().SetFrom2D(ray2d.GetHitPoint()))
                return True
        return False


        """# Checks if given ray intersects with tower.
        # This method is similar to ReceiveImpact, but them are not used for the same. Here we only want to know if ray hits the tower, and it's used to check the 
        # avaiability of a suitable shoot.
        
        i = 0
        
        while (i < 4):
            if (ray.HitRectangle(self.__shape3D[i], self.__bounding3D[i], self.__normal3D[i])):
                return True
            
            i += 1

        return False
        """
        
  
  
  
  
  
        
    
class RoundedTower(Tower):
    """ Rounded shape tower
    
    Attributes:
        radius: Radius of tower base
    """
    
    def __init__(self):
        Tower.__init__(self)
        self.__radius =  Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Tower', 'CircleRadius')
        
    def Copy(self):
        # Copy just the minimum required data to get the tower properties without "disturbing" references to other objects

        # Common rounded tower data
        tower = RoundedTower()
        tower.__radius = self.__radius

        # Common tower data
        tower._height =  self._height
        tower._thickness =  self._thickness
        tower._defenseIncrease =  self._defenseIncrease
        tower._center = self._center
        #tower._slope = self._slope
        # tower._ceiling["altitude"] = self._ceiling["altitude"]
        tower._defendingLines = BattalionConstruction.BattalionConstruction(height = self._height, cellsize = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Tower', 'BattalionGridCellSize/Small'))
        tower._label = 'Tower_' + str(Tower.towerCounter)
        Tower.towerCounter += 1

        # Common construction data
        tower._axis2D = []
        for p in self._axis2D:
            tower._axis2D.append(p.Copy())

        return tower



    def GetRadius(self):
        return self.__radius    
        
    def SetPosition(self, center, wallA, wallB, castlevector):
        # Places the rounded tower between given walls. 
        Tower.SetPosition(self, center, wallA, wallB, castlevector)
        
        # Rounded towers don't use a polygonal shape to be drawn
        self._shape2D = []

        # Sets a rounded defending line
        self._defendingLines.SetDefendingRoundedLine(0, self._center, self.__radius - (self._thickness * 0.1))


    def GetBoundingBox(self):
        
        bbox = BoundingBox()
        bbox.min = Point2D(self._center.x - self.__radius, self._center.y - self.__radius)
        bbox.max = Point2D(self._center.x + self.__radius, self._center.y + self.__radius)
        return bbox
    
    def GetBounding(self):
        
        bound = BoundingQuad()
        bound.InsertPoint(Point2D(self._center.x - self.__radius, self._center.y - self.__radius)) 
        bound.InsertPoint(Point2D(self._center.x + self.__radius, self._center.y + self.__radius))
        return bound
         
       
    def Draw(self, level, canvas, viewport):
        Construction.Construction.Draw(self, level, canvas, viewport)
    
        bbox = self.GetBoundingBox()
    
        vp1 = viewport.W2V(Point2D().SetFrom3D(bbox.min))
        vp2 = viewport.W2V(Point2D().SetFrom3D(bbox.max))
    
        self._canvasObjs.append(canvas.create_oval(vp1.x, vp1.y, vp2.x, vp2.y, outline=self.GetLevelColor(level), width="2"))
    



        
    def DistanceFromPoint(self, posfrom, squared = False):
        if (not squared):
            dist = posfrom.Distance(Point3D().SetFrom2D(self._center))
            return dist - self.__radius
        else:
            dist = (posfrom.x - self._center.x)**2 + (posfrom.y - self._center.y)**2 + (posfrom.z)**2
            return dist - (self.__radius)**2
    
    
    
    def DeployInBattleField(self, battlefield):
        # Deploys current tower into given battlefield. Each battlefield cell will be linked with all  castle parts that intersect with it
        # To check what battlefield cells intersect, consider only the cell vertices. Obviously, this not covers all the cases, but most of them
                
        self._battleFieldCells = battlefield.CircleIntersects(self._center, self.__radius)
        for cell in self._battleFieldCells:
            cell.AppendDeployedConstruction(self)    
 
 
    def RecieveImpact(self, ray):
        # Checks if given ray impacts on current rounded tower
        # To simplify the algorithm, the hiding tower parts by walls are not considered (TODO: Consider the hiding tower parts)
        
        
        if (ray.HitCylinder(center = self._center, radius = self.__radius, height = self._height)):
            return ray.GetHitPoint()
        else: 
            return None
      


    def GetRequiredAroundSpace(self):
        # Return the required around space to be deployed between walls
        
        return self.GetRadius()



    def GetIntersectableSegments(self):
        
        c = Circle(self._center, self.__radius)
        p = c.GetPolygon(12)
        return p
    
    
    


    ###########################################################################33
    # ACTION RELATED METHODS
    ###########################################################################33

 
               
        
    def RayHitTest(self, ray):
        return self.RecieveImpact(ray)
  
  
    ###########################################################################33
    # BATTALION RELATED METHODS
    ###########################################################################33
       
    
    def SetBattalionConstructionData(self, battalion, defendingline):
        # Updates given battalion with construction data
        
        # Increase the defense factor
        battalion.SetExtraDefense(self._defenseIncrease)

        
        # Change the attack vector, so each battalion unit has a different one inside the same defending line
        
        p = self.GetBattalionCellPosition(defendingline, battalion)
        v = Vector2D().CreateFrom2Points(self._center, Point2D().SetFrom3D(p))      
        
        battalion.SetAttackVector(Vector3D().SetFrom2D(v), self.GetDefenseAngle())


   
  
    def _DeployBattalion(self, army, kind, number, placetype, linespercell = -1, maxpercell = -1, command = Command.DEFEND_CASTLE):

        if ((not army.HasBattalionType("Cannons") or ((kind == 'Archers') and not self._defendingLines.HasCannons(index = 0)))):
            self._defendingLines.SetCellSize(index = 0, cellsize = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Tower', 'BattalionGridCellSize/Small'))
        else:
            self._defendingLines.SetCellSize(index = 0, cellsize = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Tower', 'BattalionGridCellSize/Large'))

        self._defendingLines.DeployBattalion(0, self, army, kind, number, placetype, linespercell, maxpercell, command)





