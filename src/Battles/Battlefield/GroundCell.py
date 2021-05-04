from random import uniform
   


from Battles.Utils.Geometry import Point2D, Point3D, BoundingQuad, BoundingBox
from Battles.Factory import ConstructionFactory
import Battles.Utils.Settings 


   
    
class GroundCell:
    """ Ground subdivision unit on the battle field
    
    Attributes:
        movementPenalty: negative factor to apply to troops movement (such as height, terrain difficulties, etc.)
        battleField: related battlefield
        battalion: effectives deployed at current cell
        index: cell index into the grid
        constructions: list with all castle construction elements deployed on this cell
        moat: moat object on terrain
        center: cell center (this increase the memory, but improve the performance due its queried many times)
        city: true if cell is at castle inside, that is the city/town
        trench : reference to the trench object if current cell falls on it.
        river: reference to a river if current cell falls on it
    """
    
    def __init__(self, battlefield, row, column):
        self.__battleField = battlefield
        self.__movementPenalty =  Battles.Utils.Settings.SETTINGS.Get_F('Battlefield', 'GroundCell', 'MovementPenalty')
        self.__defenseIncrease = Battles.Utils.Settings.SETTINGS.Get_F('Battlefield', 'GroundCell', 'DefenseIncrease')
        self.__battalion = None
        self.__index = {"row": row, "column": column}
        self.__groundHeight =  Battles.Utils.Settings.SETTINGS.Get_F('Battlefield', 'GroundCell', 'Height')
        self.__constructions = []
        self.__moat = None
        self.__city = False
        self.__trench = None
        self.__river = None
        
        cellsize = self.__battleField.GetCellSize()
        self.center = Point3D((self.__index["column"] * cellsize) + (cellsize / 2), (self.__index["row"] * cellsize) + (cellsize / 2), self.__groundHeight)
        
        
    def Reset(self):
        # Removes the cell battalions
        self.__battalion = None
        
        # Removes the linked constructions
        self.__constructions = []
        
        self.__movementPenalty =  Battles.Utils.Settings.SETTINGS.Get_F('Battlefield', 'GroundCell', 'MovementPenalty')
        self.__defenseIncrease = Battles.Utils.Settings.SETTINGS.Get_F('Battlefield', 'GroundCell', 'DefenseIncrease')
        
        self.__trench = None
        self.__city = False
        self.__moat = None
        self.__river = None
        

    def GetRow(self):
        return self.__index["row"]

    def GetColumn(self):
        return self.__index["column"]

            
    def GetBattlefield(self):
        return self.__battleField 
        
    def GetAltitude(self):
        return self.__groundHeight
        
    def GetRow(self):
        return self.__index["row"]
    
    def GetColumn(self):
        return self.__index["column"]    
    
    def GetCellSize(self):
        return self.__battleField.GetCellSize()
        
        
    def GetRandomCellPosition(self):
        # Returns an uniform random cell position (well, not exactly an uniform distribution, but near to it)
        
        pos = self.center
        size = self.GetCellSize()
        
        #seed()
        x = uniform(pos.x - (size / 2), pos.x + (size / 2))
        y = uniform(pos.y - (size / 2), pos.y + (size / 2))
    
        return Point3D(x, y, pos.z)
        

    
    def RedrawAttacked(self, canvas, viewport):
        
        # Convenience method to redraw a cell
        bbox = self.GetBoundingQuad()
        vp1 = viewport.W2V(bbox.minPoint)
        vp2 = viewport.W2V(bbox.maxPoint)
        canvas.create_rectangle(vp1.x, vp1.y, vp2.x, vp2.y, fill="white")
        
 
 
    ###########################################################################33
    # BATTLEFIELD RELATED METHODS
    ###########################################################################33
 
        
    def GetPenalty(self):
        return self.__movementPenalty    
        

    def SetTrench(self, t, defenseincrease, movementpenalty):
        
        # Check overlappings
        """if (self.HasBattalion()):
            print "ERROR: Trench overlapping a battalion cell"
        if (self.HasConstructions()):
            print "ERROR: Trench overlapping a construcion cell"
        if (self.HasMoat()):
            print "ERROR: Trench overlapping a moat cell"
        if (self.IsCity()):
            print "ERROR: Trench overlapping a city cell"
        if (self.HasTrench()):
            print "ERROR: Trench overlapping a trench cell"
        """
        
        # Allow to continue if there is any error due its too difficult to control input errors from here. So, show an error message and let the user to check it
        self.__battalion = None
        self.__constructions = []
        self.__moat = None
        self.__city = False
        self.__river = None
        
        self.__trench = t
        self.__defenseIncrease = defenseincrease
        self.__movementPenalty = movementpenalty
    
    
    def HasTrench(self):
        return (self.__trench != None)
    
    def GetTrench(self):
        return self.__trench
    
    
    def SetRiver(self, river):
        self.__battalion = None
        self.__moat = None
        self.__trench = None
        self.__city = False
        
        self.__river = river
        self.__movementPenalty = Battles.Utils.Settings.SETTINGS.Get_F('Battlefield', 'River', 'PenaltyMovement')

        
        
    def HasRiver(self):
        return (self.__river != None)
        
    def GetRiver(self):
        return self.__river
    
    
    def IsAvailable(self):
        if (self.HasRiver() or self.HasBattalion() or self.HasConstructions() or self.HasMoat() or self.IsCity()):
            return False
        else:
            return True 
    
    
    
    ###########################################################################33
    # BATTALION RELATED METHODS
    ###########################################################################33
    
        
    def SetBattalion(self, battalion):

        self.__battalion = battalion
        
        # Update the terrain settings for new battalion place
        self.__battalion.SetExtraDefense(self.__defenseIncrease)
        
        
    
    def RemoveBattalion(self):
        self.__battalion = None
    
        
    def GetBattalion(self):
        return self.__battalion
        
    def HasBattalion(self):
        if (self.__battalion != None):
            return True
        else:
            return False
    
               
    def MoveTroopsFromCell(self, cell):
        # Move the troops stored in given cell to current one
        self.SetBattalion(cell.__battalion)
        cell.__battalion = None
 
        # If it is a trench update the visitors list
        if (self.__trench):
            self.__trench.AddVisitor(self.__battalion)
            
            
   
    
    def GetAdjacentCells(self, battalionfree = True, towerfree = True, grow = 1):
        # Returns a list with adjacent cells
        # If free is true only returns the free cells
        # grow parameter indicates the number of grown adjacent columns and rows
        # City cells are not considered
         
        lst = []
        i = int(-grow)
        while (i < (grow + 1)):
            row = self.__index["row"] + i
            j = int(-grow)
            while (j < (grow + 1)):
                col = self.__index["column"] + j
                if ((row != self.__index["row"]) or (col != self.__index["column"])): 
                    cell = self.__battleField.GetCell(row, col)
                    if (cell != None):
                        if (not cell.IsCity()):
                            if ((battalionfree and (not cell.HasBattalion())) or (not battalionfree)):
                                if ((towerfree and (not cell.HasTowers())) or (not towerfree)):
                                    lst.append(cell)
                            
                j += 1
                    
            i += 1
        
        return lst


    
    
    
    ###########################################################################33
    # CONSTRUCTION RELATED METHODS
    ###########################################################################33
    
        
    def HasConstructions(self):
        return (len(self.__constructions) > 0)
    
    def HasThisConstruction(self, constr):
        return constr in self.__constructions
    
    def GetConstructions(self):
        return self.__constructions
    
    
    def HasWalls(self):
        factory = ConstructionFactory()
        for c in self.__constructions:
            if (factory.IsWall(c)):
                return True
        return False
    
    
    def HasTowers(self):
        factory = ConstructionFactory()
        for c in self.__constructions:
            if (factory.IsTower(c)):
                return True
        return False
     
        
    def HasMoat(self):
        return self.__moat != None    


    def HasWaterMoat(self):
        if (self.__moat != None):
            if (self.__moat.HasWater()):
                return True

        return False


    def GetMoat(self):
        return self.__moat
 
 
    def SetCity(self, b):
        self.__city = b
        
   
        
 
    def IsCity(self):
        return self.__city     
         
         
    def AppendDeployedConstruction(self, construction):
        """
        # Check overlappings
        if (self.HasBattalion()):
            print "ERROR: Construction overlapping a battalion cell"
        if (self.HasMoat()):
            print "ERROR: Construction overlapping a moat cell"
        if (self.IsCity()):
            print "ERROR: Construction overlapping a city cell"
        if (self.HasTrench()):
            print "ERROR: Construction overlapping a trench cell"
        """
        # Allow to continue if there is any error due its too difficult to control input errors from here. So, show an error message and let the user to check it
        self.__trench = None
        self.__moat = None
        self.__battalion = None
        self.__city = False
        self.__river = None
        
        
        if (not (construction in self.__constructions)):
            self.__constructions.append(construction)
            
            
            
        
    def RemoveConstruction(self, construction):
        i = 0
        while (i < len(self.__constructions)):
            if (self.__constructions[i] == construction):
                del self.__constructions[i]
                return 
            i += 1


    def AppendDeployedMoat(self, moat, penalty):
        self.__moat = moat
        self.__movementPenalty *= penalty
            
                 
    def RemoveMoat(self):
        if (self.__moat != None):
            self.__moat.RemoveCell(self)
        self.__moat = None
        self.__movementPenalty =  Battles.Utils.Settings.SETTINGS.Get_F('Battlefield', 'GroundCell', 'MovementPenalty')           
    
    
    def GetClosestConstruction(self, fromPos = None):
        # Returns the closest castle construction deployed in current cell
        # Given position is in 3D, but only 2D data is taken into account
        # TODO: Consider the height to calculate distances
        
        if (fromPos == None):
            fromPos = self.center
            
        ret = None    
            
        for c in self.__constructions:
            dist = c.DistanceFromPoint(fromPos)
            if (ret == None):
                ret = c
                mindist = dist
            elif (dist < mindist):
                ret = c
                mindist = dist
    
        return ret
        
        
    def GetClosestWall(self, fromPos = None):
        # Like Getclosestconstruction but only with walls
        
        if (fromPos == None):
            fromPos = self.center
            
        ret = None    
            
        factory = ConstructionFactory()
        for c in self.__constructions:
            if (factory.IsWall(c) and c.IsReachable()):
                dist = c.DistanceFromPoint(fromPos)
                if (ret == None):
                    ret = c
                    mindist = dist
                elif (dist < mindist):
                    ret = c
                    mindist = dist
    
        return ret
        


    
    
    ###########################################################################33
    # GEOMETRY RELATED METHODS
    ###########################################################################33
    

    def GetBoundingQuad(self):
        
        p1 = Point2D()
        p2 = Point2D()
        
        cellsize = self.__battleField.GetCellSize()
        p1.x = self.__index["column"] * cellsize
        p1.y = self.__index["row"] * cellsize
        p2.x = p1.x + cellsize
        p2.y = p1.y + cellsize

        bq = BoundingQuad()
        bq.InsertPoint(p1)
        bq.InsertPoint(p2)
        return bq
        
     
    def GetBoundingBox(self):
        
        quad = self.GetBoundingQuad()
        if (self.HasBattalion()):
            bbox = self.GetBattalion().GetBounding()
            height = bbox.height
        else:
            height = 0.0
            
        bbox = BoundingBox(minP = Point3D(quad.minPoint.x, quad.minPoint.y, self.__groundHeight), maxP = Point3D(quad.maxPoint.x, quad.maxPoint.y, self.__groundHeight + height))
        return bbox
       
        
    def DistanceFromPoint(self, frompos):
        # Convenience distance method to allow calling a distance method with independence of class
        # Its better to get center attribute
        
        return frompos.Distance(self.center)
        
    
    def CircleIntersects(self, center, radius):
        # Return a list with all cells that intersect with given circle. Only are checked the cell vertices and cell center
        
        bbox = self.GetBoundingQuad()
        
        if (bbox.minPoint.IsInCircle(center, radius)):
            return True
        if (bbox.maxPoint.IsInCircle(center, radius)):
            return True
        
        
        p = Point2D(bbox.minPoint.x, bbox.maxPoint.y)
        if (p.IsInCircle(center, radius)):
            return True
        p = Point2D(bbox.maxPoint.x, bbox.minPoint.y)
        if (p.IsInCircle(center, radius)):
            return True
        
        p = Point2D().SetFrom3D(self.center)
        if (p.IsInCircle(center, radius)):
            return True
        
        return False
    
    
    
    
    
    
    