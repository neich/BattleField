from Battles.Utils.Geometry import BoundingQuad, Point3D
import Battles.Utils.Settings 


class Trench:
    """ Trench class. It defines the concept of a defensive zone on the battlefield where the attackers can hide at the same time that attack
        It is composed by a set of points linked to their respective battlefield cells. When the attackers search for the next move, check about the closest trenches and their
        distances to the castle targets, choosing the best option.
        The battalions that are in trench cells benefit from a defense increase skills. Also from a some movement penalty
        Note the difference between the trench and the moat objects. The moat can be integrated into the battlefield, updating the movement penalty values of their cells. But 
        threnches must be avaiable to be accessed in a fast way, due the battalions will query them in each movement step.
        By default, the trenches search is only applied to the archers, so the goal is to shoot from a defensive place
        The closest construction has to have battalions to shoot. If meanwhile the battle the closest construction loose all of its battalions, the trench search another construction 
        
        Attributes:
            battlefield: reference to the battlefield
            battlefieldcells: list of battlefield cells in the trench
            closestConstruction: closest construction object. it is calculated once in GetClosestConstruction method. Be aware to dont calculate it in the __init__, so usually
                                 the battlefield is created before the castle
            distanceClosestConstruction: distance to the closest construction
            boundingBox: trench bounding box (calculated around the cell centers for convenience)
            useless: True if trench is useless, that means that there arent any closest construction to shoot
            visitedBattalions: List with all battalions that have visited the trench. Used internally to avoid the flickering effect on some battalions entering and lefting the trench
    """
    
    def __init__(self, battlefield, cells): 
        self.__battlefield = battlefield
        self.__battlefieldCells = cells
        
            
        self.__closestConstruction = None
        self.__distanceClosestConstruction = -1

        # Calculate the bounding box 
        # Set the cells as trench cells
        self.__boundingBox = BoundingQuad()
        if (self.__battlefieldCells):
            height = 0        
            for c in self.__battlefieldCells:
                self.__boundingBox.InsertPoint(c.center)
                c.SetTrench(self, Battles.Utils.Settings.SETTINGS.Get_F('Battlefield', 'Trench', 'DefenseIncrease'), Battles.Utils.Settings.SETTINGS.Get_F('Battlefield', 'Trench', 'MovementPenalty'))
                height += c.GetAltitude()
            self.__center = Point3D().SetFrom2D(self.__boundingBox.GetCenter())
            self.__center.z = height / len(self.__battlefieldCells)
        
        
        self.__useless = False
        
        self.__visitedBattalions = []
        
        
        
        
    def IsFull(self):
        # Returns true if the trench is full, that means that all of its cells are occupied by a battalion
        for c in  self.__battlefieldCells:
            if (not c.HasBattalion()):
                return False
        return True
    
    
    def AddVisitor(self, battalion):
        # Adds a visitor
        self.__visitedBattalions.append(battalion)
        
    
    def HasVisited(self, battalion):
        # Returns true if given battalion has visted the trench in the past
        return battalion in self.__visitedBattalions
        
        
    
    def GetClosestConstruction(self, castle):
        # Returns the closest construction object. We take a center point on the bounding box to calculate this distance
        
        if (self.__useless):
            return None
        
        if ((not self.__closestConstruction) or (not self.__closestConstruction.HasBattalions())):
            self.__closestConstruction = castle.GetClosestConstruction(populated = True, posfrom = self.__center, tilesrequired = False, reachable = False)
            if (not self.__closestConstruction):
                self.__useless = True
             
        return self.__closestConstruction
   

    """
    def GetDistanceConstruction(self):
        # Returns the distance to the closest construction from the bounding box center
        
        if (self.__useless):
            return None
        
        if ((not self.__closestConstruction) or (not self.__closestConstruction.HasBattalions())):
            self.GetClosestConstruction()
            
        return self.__distanceClosestConstruction
    """
    
    
    
    def GetDistanceFromPoint(self, frompos):
        # Returns the distance from given 2D position to the bounding box center 
        return frompos.Distance(self.__center)


    def GetClosestCell(self, frompos, free = True):
        # Returns the closest cell. If free is true, then only the free cells are considered
        ret = None
        minD = -1
        
        for c in self.__battlefieldCells:
            if ((not free) or (free and not c.HasBattalion())):
                dist = frompos.Distance(c.center)
                if ((not ret) or (dist < minD)):
                    ret = c
                    minD = dist
                
        return ret
            
            
            
    def Draw(self, canvas, viewport):

        if (Battles.Utils.Settings.SETTINGS.Get_B('Battlefield', 'Trench', 'ShowOutline')):
            outline = "Black"
        else:
            outline = "LemonChiffon"
            
        for c in self.__battlefieldCells:
            bbox = c.GetBoundingQuad()
            vp1 = viewport.W2V(bbox.minPoint)
            vp2 = viewport.W2V(bbox.maxPoint)
            canvas.create_rectangle(vp1.x, vp1.y, vp2.x, vp2.y, fill="LemonChiffon", outline = outline)
        
        
    
    
    
    
    