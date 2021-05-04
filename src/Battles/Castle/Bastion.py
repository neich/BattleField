import math

from Battles.Castle import Construction, Tower, BattalionConstruction
from Battles.Utils.Geometry import Circle, Vector2D, Ray2D, Point2D, Segment2D, Vector3D, Point3D, BoundingBox
from Battles.Army.Action import Command
import Battles.Utils.Settings 


class Bastion(Tower.Tower):
    """ Class for bastion objects. Althought visually are very different from towers, the construction and goal are very similar. In fact, bastions are created to remove
        the black zones that rounded towers produce. In addition, bastions are created around a virtual circular tower.
        The bastions are stored in the castle towers structure, making it easy to manage
        We assume an empty bastion type
        
    Attributes:
        
        virtualCircleRadius: Radius of the virtual circle used to construct the bastion around
        externalWalls: List of 2D segments with the external bastion walls. The vertices are stored from left to right sorting order
        internalWalls: List of 2D segments with the internal bastion walls. The vertices are stored from left to right sorting order
        shape3D and normal3D: 3D geometry used to calculate ray hits. Calculated in SetPosition method. 
        bounding3D: list of 3D bounding boxes for each castle side. Used to calculate the ray hits
    
    """

    bastionCounter = 0
    
    def __init__(self):
        Construction.Construction.__init__(self)    
        # Do not call tower constructor. Most of Tower initializations have to be controlled here (wall thickness, height, defending line creation)    
        self._height =  Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Bastion', 'Height')
        self._thickness =  Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Bastion', 'Thickness')
        self._defenseIncrease =  Battles.Utils.Settings.SETTINGS.Get_I('Castle', 'Tower', 'DefenseIncrease')
        self._center = Point2D()
        self.__slope = None
        self.__ceiling = {"altitude": (self._height -  Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Wall', 'MerlonHeight'))}
        
        self._defendingLines = BattalionConstruction.BattalionConstruction( height = self._height, cellsize = Battles.Utils.Settings.SETTINGS.Get_F('Castle','Bastion', 'BattalionGridCellSize/Small'))

        
        self.__virtualCircleRadius = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Bastion', 'VirtualCircleRadius')
        # The relation between the circle radius and thickness is important. The radius cannot be NEVER less than thickness
        # If both are close, the bastion will be almost closed
        # Because we are humans, and humans usually place the warning messages in a distant hole in their minds, the system clamps the radius to the thickness if radius is less
        # Note that this condition of equality is just an approximation of the closed condition. We should consider some trigonometry to get accurate results. Let this as 
        # another nice TODO task...
        if (self.__virtualCircleRadius < self._thickness):
            self.__virtualCircleRadius = self._thickness
            
            
            
       
        self.__externalWalls = []
        self.__internalWalls = []
       
       
        self._label = 'Bastion_' + str(Bastion.bastionCounter)
        Bastion.bastionCounter += 1
        
        self.__shape3D = []
        self.__normal3D = []
        self.__bounding3D = []
       
    @classmethod
    def ResetCounter(cls):
        cls.bastionCounter = 0        
       
       
    def SetVirtualCircleRadius(self, r):
        self.__virtualCircleRadius = r   
        if (self.__virtualCircleRadius < self._thickness):      # See init method to know more about it
            self.__virtualCircleRadius = self._thickness


    def GetVirtualCircleRadius(self):
        return self.__virtualCircleRadius
    
    
       
    def SetPosition(self, center, wallA, wallB, castlevector):
        # Places the bastion on given position, having given walls as side construction elements. castlevector is ignored
        
        Tower.Tower.SetPosition(self, center, wallA, wallB, castlevector)
    
        self._shape2D = []
        self.__externalWalls = []
        self.__internalWalls = []
        self._axis2D = []
        
        
    
        # The bastion is constructed to cover all black zones. It has four sides (diamond style). The most external sides are used to defend the castle. The other ones are used
        # as defensive flanks. The flanks are perpendicular to the side walls. The external faces are constructed from the tangent point of virtual circle and a vector with
        # the origin placed at the side wall final point (the wall point that isnt the bastion center point). So, the exterior faces orientation match with these vectors (one for
        # each side). Their segments start at intersection point between both, and ends at intersection with flanks. The flanks are perpendicular segments that start at wall point
        # where the virtual circle intersects with the wall (sorry if it is not clear, I cannot explain better without a draw)
        
        # Calculate the tangent points from each wall
        wp1 = wallA.GetStartPosition()
        wp2 = wallB.GetEndPosition()
        
        circle = Circle(center = center, radius = self.__virtualCircleRadius)
        tg1 = circle.TangentPointsFromPoint(wp1)
        tg2 = circle.TangentPointsFromPoint(wp2)
        
        # For discarding the non-valid tangent points, calculate the vectors to the wall vertices and check them with the normal wall
        vec1_1 = Vector2D().CreateFrom2Points(tg1[0], wp1)
        vec1_2 = Vector2D().CreateFrom2Points(tg1[1], wp1)
        if (vec1_1.DotProd(wallA.GetNormalVector()) <= 0):
            vec1 = vec1_1
            tangent1 = tg1[0]
        else:
            vec1 = vec1_2
            tangent1 = tg1[1]
            
        vec2_1 = Vector2D().CreateFrom2Points(tg2[0], wp2)
        vec2_2 = Vector2D().CreateFrom2Points(tg2[1], wp2)
        if (vec2_1.DotProd(wallB.GetNormalVector()) <= 0):
            vec2 = vec2_1
            tangent2 = tg2[0]
        else:
            vec2 = vec2_2
            tangent2 = tg2[1]
            
       
        # Calculate the external vertex of bastion
        ray1 = Ray2D(origin = wp1, direction = vec1.Invert())
        ray2 = Ray2D(origin = wp2, direction = vec2.Invert())
        if (not ray1.HitRay(ray2)):
            print "ERROR: The bastion cannot be constructed. The external vertex cannot be calculated"
            return
        
        ext = ray1.GetHitPoint()
        
        # Calculate the flanks
        # Project the wall point where starts/ends the bastion over the exterior bastion walls
        prj1 = center.Copy()
        prj1.Move(wallA.GetWallVector(), - self.__virtualCircleRadius)
        prj1.Move(wallA.GetNormalVector(), wallA.GetThickness() / 2.0)
        prj2 = center.Copy()
        prj2.Move(wallB.GetWallVector(), self.__virtualCircleRadius)
        prj2.Move(wallB.GetNormalVector(), wallB.GetThickness() / 2.0)
        
        prjray1 = Ray2D(origin = prj1, direction = Vector2D().SetFrom3D(wallA.GetNormalVector()))
        prjray2 = Ray2D(origin = prj2, direction = Vector2D().SetFrom3D(wallB.GetNormalVector()))
        if ((not prjray1.HitRay(ray1)) or (not prjray2.HitRay(ray2))):
            print "ERROR: The bastion cannot be constructed. The flank walls cannot be calculated"
            return
        
        flank1 = prjray1.GetHitPoint()
        flank2 = prjray2.GetHitPoint()
        
        
        # Store the bastion exterior walls
        # Be aware about the vertices order (from left to right)
        self.__externalWalls.append(Segment2D(prj1, flank1))
        self.__externalWalls.append(Segment2D(flank1, ext))
        self.__externalWalls.append(Segment2D(ext, flank2))
        self.__externalWalls.append(Segment2D(flank2, prj2))
        
        
        # Calculate the internal walls
        
        # For the starting and ending internal vertices, simply extend the adjacent walls by the bastion thickness
        prj2int = prj2.Copy()
        prj2int.Move(wallB.GetNormalVector(), -wallB.GetThickness())
        prj2int.Move(wallB.GetWallVector(), -self._thickness)
        prj1int = prj1.Copy()
        prj1int.Move(wallA.GetNormalVector(), -wallA.GetThickness())
        prj1int.Move(wallA.GetWallVector(), self._thickness)
        # For the other vertices, calculate the intersection between bisector of each angle and  starting and ending points
        # To avoid the intersection segment algorithm and bisector computation, we apply some simple geometry. We need the distance from starting and ending points to move them
        # by the same direction than exterior walls. The movement distance, for each bastion side, will be:
        #        d = exteriorwall_length + wall_width - x
        #        x = tan(ang) * bastion_thickness
        #        ang = angle_between_exterior_walls/2
        ang1 = self.__externalWalls[0].AngleBetween(self.__externalWalls[1])
        x1 = math.tan(math.radians(ang1/2.0)) * self._thickness
        d1 = wallA.GetThickness() + self.__externalWalls[0].GetLength() - x1
        flankint1 = prj1int.Copy()
        flankint1.Move(self.__externalWalls[0].GetDirection(), d1)
        ang2 = self.__externalWalls[3].AngleBetween(self.__externalWalls[2])
        x2 = math.tan(math.radians(ang2/2.0)) * self._thickness
        d2 = wallA.GetThickness() + self.__externalWalls[3].GetLength() - x2
        flankint2 = prj2int.Copy()
        flankint2.Move(self.__externalWalls[3].GetDirection(), -d2)
        # For the last internal vertex we are going to follow a similar procedure. We only need to consider one bastion side/flank and some data already calculated
        #        dd = exteriorwall_flank_length - x - b
        #        b = tan(beta) * bastion_thickness
        #        beta = angle_between_flanks/2
        beta = self.__externalWalls[1].AngleBetween(self.__externalWalls[2])
        dd = self.__externalWalls[1].GetLength() - x1 - (math.tan(math.radians(beta / 2.0)) * self._thickness)
        extint = flankint1.Copy()
        extint.Move(self.__externalWalls[1].GetDirection(), dd)
        
        """
        flankint2 = prj2int.Copy()
        flankint2.Move(wallB.GetNormalVector(), self.__externalWalls[3].GetLength())
        flankint1 = prj1int.Copy()
        flankint1.Move(wallA.GetNormalVector(), self.__externalWalls[0].GetLength())
        
        extintray1 = Ray2D(origin = flankint1, direction = self.__externalWalls[1].GetDirection())
        extintray2 = Ray2D(origin = flankint2, direction = self.__externalWalls[2].GetDirection().Invert())
        if (not extintray1.HitRay(extintray2)):
            print "ERROR: The bastion cannot be constructed. Internal walls cannot be calculated"
            return
        extint = extintray1.GetHitPoint()   
        """
        
        # Store the bastion interior walls
        # Be aware about the vertices order (from left to right), same than exterior walls
        self.__internalWalls.append(Segment2D(prj1int, flankint1))
        self.__internalWalls.append(Segment2D(flankint1, extint))
        self.__internalWalls.append(Segment2D(extint, flankint2))
        self.__internalWalls.append(Segment2D(flankint2, prj2int))
        
        
        # Calculate the bastion axis. In addition, set the defending lines on the axis
        i = 0
        while (i < len(self.__externalWalls)):
            a1 = Segment2D(self.__externalWalls[i].p1, self.__internalWalls[i].p1).GetMidPoint()
            a2 = Segment2D(self.__externalWalls[i].p2, self.__internalWalls[i].p2).GetMidPoint()
            self._axis2D.append(Segment2D(a1, a2))
            
            # For the exterior flanks, the cellsize must be greater due the cannons are placed there
            # Note that this is the default case for cannons deployment. If we havent cannons to deploy, the size of exterior flanks cells has to be the same than the internal
            # In this latter case, the cellsize should be changed on _DeployBattalion method
            if ((i >= 1) and (i <= 2)):
                self._defendingLines.SetDefendingLine(index = i, segment = self._axis2D[i], cellsize = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Bastion', 'BattalionGridCellSize/Large'))
            else:
                self._defendingLines.SetDefendingLine(index = i, segment = self._axis2D[i], cellsize = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Bastion', 'BattalionGridCellSize/Small'))
            
            i += 1
            
        
 
        
        # Now we have all bastion 2D coordinates
        self._shape2D = []
        self._shape2D.append(prj1)
        self._shape2D.append(flank1)
        self._shape2D.append(ext)
        self._shape2D.append(flank2)
        self._shape2D.append(prj2)
        self._shape2D.append(prj2int)
        self._shape2D.append(flankint2)
        self._shape2D.append(extint)
        self._shape2D.append(flankint1)
        self._shape2D.append(prj1int)
        
        
        
        # Calculate the 3D geometry used to check impacts. To simplify we use a virtual plane on the bastion axis (like walls)
        self.__shape3D = []
        self.__normal3D = []
        self.__bounding3D = []
        i = 0
        while (i < len(self._axis2D)):
            lst = [Point3D(self._axis2D[i].p1.x, self._axis2D[i].p1.y, self._height),
                   Point3D(self._axis2D[i].p2.x, self._axis2D[i].p2.y, self._height),
                   Point3D(self._axis2D[i].p2.x, self._axis2D[i].p2.y, 0),
                   Point3D(self._axis2D[i].p1.x, self._axis2D[i].p1.y, 0)]

            self.__shape3D.append(lst)
            
            # Calculate 3D normal
            self.__normal3D.append(Vector3D().SetFrom2D(self._axis2D[i].GetNormal()))
 
            # Calculate the face 3D bounding
            bbox = BoundingBox()
            for p in lst:
                bbox.InsertPoint(p)
            self.__bounding3D.append(bbox)

      
            i += 1

        
    def GetRequiredAroundSpace(self):
        # To get the required around space we need to calculate the full bastion shape. This is not useful since this method is called before the bastion shape is constructed
        # But we can get an approximation using the bastion circle radius and thickness, so the interior flanks are perpendicular to the adjacent walls and tangent to this circle
        
        return self.__virtualCircleRadius + self._thickness
    
        
        
    def GetStartPosition(self, exterior = True):
        
        if (exterior):
            return self.__externalWalls[0].p1.Copy()
        else:
            return self.__internalWalls[0].p1.Copy()
        
    def GetEndPosition(self, exterior = True):
        
        if (exterior):
            return self.__externalWalls[3].p2.Copy()
        else:
            return self.__internalWalls[3].p2.Copy()
        
        
    def GetFlankSegment(self, right, front):
        # Returns the bastion flank segment from given parameters. If right is False, considers the left side, or the right side otherwise.
        # If front is False considers the rear bastion flanks, or the front ones otherwise
        
        if (right and front):
            return self.__externalWalls[2]
        elif (right and not front):
            return self.__externalWalls[3]
        elif (not right and front):
            return self.__externalWalls[1]
        else:
            return self.__externalWalls[0]
    
    
    
    def DeployInBattleField(self, battlefield):
        # Deploys current battalion into given battlefield. Each battlefield cell will be linked with all  castle parts that intersect with it
        # In theory, the inner battalion are shouldn't be accessed never by attackers 
                
        i = 0 
        nverts = len(self._shape2D)
        while (i < nverts):
            if (i == (nverts - 1)):
                lst = battlefield.RayTraversal(self._shape2D[nverts - 1], self._shape2D[0])
            else:   
                lst = battlefield.RayTraversal(self._shape2D[i], self._shape2D[i+1])
            for c in lst:
                c.AppendDeployedConstruction(self)
                self._battleFieldCells.append(c)
            i += 1
            
            
            
    def GetNormalVector(self, index = 0):
        # Returns the tower 3D normal vector by indexed side
        # Do not confuse with normal3D. Both can return the same vector, but they are used in different contexts and are suitable to be changed in the future
        
        if ((index < 0) or (index >= len(self.__externalWalls))):
            print "ERROR: Index out of bounds for bastion normal vector"
            return None
        
        normal = self._axis2D[index].GetNormal()
        return Vector3D(normal.val[0], normal.val[1], 0.0)
            
            
            
    def DistanceFromPoint(self, posfrom, squared = False):
        # Calculate the distance from given point to bastion
        # Work in 2D to simplify
        
        p = Point2D(posfrom.x, posfrom.y)
        minD = -1
        for ex in self.__externalWalls:
            d = ex.DistanceToPoint(p, squared)
            if ((d < minD) or (minD == -1)):
                minD = d
                
        return minD
            

    def GetIntersectableSegments(self):
        return self.__externalWalls


    ###########################################################################33
    # BATTALION RELATED METHODS
    ###########################################################################33
  
  
    def _DeployBattalion(self, army, kind, number, placetype, linespercell = -1, maxpercell = -1, command = Command.DEFEND_CASTLE):
        
        # WARNING: Given number of troops to deploy will be used for each bastion flank. By example, number = 3 means 3 battalions for each bastion flank
        
        # Check if defender army has cannons to deploy (or defined). If not, resize the external flanks cellsize to allow full deployment of archers
        if (not army.HasBattalionType("Cannons")):
            self._defendingLines.SetCellSize(index = 1, cellsize = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Bastion', 'BattalionGridCellSize/Small'))
            self._defendingLines.SetCellSize(index = 2, cellsize = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Bastion', 'BattalionGridCellSize/Small'))
        
        i = 0 
        while (i < len(self.__externalWalls)):
            
            self._defendingLines.DeployBattalion(i, self, army, kind, number, placetype, linespercell, maxpercell, command)
            
            i += 1
            


            
    ###########################################################################33
    # ACTION RELATED METHODS
    ###########################################################################33
            
 
  
    def RayHitTest(self, ray):

        # Do the check in 2D -> easy and cheap (TODO: Do it (well) in 3D)
        ray2d = Ray2D().SetFrom3D(ray)
        seglist = self.GetIntersectableSegments()
        for seg in seglist:
            if (ray2d.HitSegment3(seg)):
                ray.SetHitPoint(Point3D().SetFrom2D(ray2d.GetHitPoint()))
                return True
        return False

        """# Checks if given ray intersects with bastion.
        # We want to know if ray hits the bastion, and it's used to check the  avaiability of a suitable shoot.
        
        i = 0
        
        while (i < len(self.__shape3D)):
            if (ray.HitRectangle(self.__shape3D[i], self.__bounding3D[i], self.__normal3D[i])):
                return True
            
            i += 1

        return False
        """
        
    