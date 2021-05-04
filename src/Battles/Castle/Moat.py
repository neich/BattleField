import math

from Battles.Castle import Construction
from Battles.Utils.Geometry import Point2D, GPCWrapper
import Battles.Utils.Settings



class Moat(Construction.Construction):
    """ Moat construction around the castle
    
    Attributes:
        hasWater: True if has water, false if it is only a hole
        thickness: Hole width
        height: Hole depth
    """
    
    def __init__(self):
        Construction.Construction.__init__(self)
        self._thickness =  Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Moat', 'Width')
        self._height = -Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Moat', 'Depth')
        self.__hasWater = Battles.Utils.Settings.SETTINGS.Get_B('Castle', 'Moat', 'HasWater')
        
    @classmethod    
    def ResetCounter(cls):
        pass
        
    def SetWater(self, w):
        self.__hasWater = w
        
    def SetDepth(self, d):
        self._height = -d
        
    def GetDepth(self):
        return -self._height    
        
    def HasWater(self):
        return self.__hasWater
        
    def GetThickness(self):
        return self._thickness  
        
    def ConstructFromCells(self, cells):
        # Construct the moat as a list of battlefield cells expanding the given battlefield cells list
        
        self._battleFieldCells = []
        
        if (len(cells) > 0):
            expand = int(math.ceil(self._thickness / cells[0].GetCellSize()))
        else:
            return
        
               
        # Calculate the moat movement penalty
        # If moat has water, the penalty movement is high
        if (self.__hasWater):
            penalty = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Moat', 'PenaltyWater') 
        else:
            # Calculate the distance to walk from top moat to down and to top again
            mw = self._thickness
            mh = -self._height 
            d = 2.0 * math.sqrt(((mw * mw) / 2.0) + (mh * mh))
            
            # Because the moat can cover more than one cell in width, get the proportional part
            cellsize = cells[0].GetCellSize()
            ncells = math.ceil(self._thickness / cellsize)
            d /= ncells
            
            if (d > cellsize):
                penalty = (cellsize / d) * Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Moat', 'PenaltyNoWater') 
            else:
                penalty = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Moat', 'PenaltyNoWater') 
       
                
        for c in cells:
            self._battleFieldCells.append(c)
            
            clist = c.GetAdjacentCells(battalionfree = False, towerfree = False, grow = expand)
            for cl in clist:
                if (cl not in self._battleFieldCells):
                    self._battleFieldCells.append(cl)
                    cl.AppendDeployedMoat(self, penalty)
        
        
    def CropInside(self, convexhull):
        # Crops the moat cells that are inside given convex hull
        
        
        clist = []

        """
        if (convexhull):
            for c in self._battleFieldCells:
                center = Point2D().SetFrom3D(c.center)
                if (not convexhull.IsInside(center)):
                    clist.append(c)
                else:
                    c.RemoveMoat()
        """
        # IsInside method is not accurate for this purpose
        # Use the GPC
        # TODO: Create a GPC instance to avoid passing the points list each time

        gpc = GPCWrapper()
        plist = convexhull.GetPointsList()

        for c in self._battleFieldCells:
            center = Point2D().SetFrom3D(c.center)
            if (not gpc.IsInside(plist, center)):
                clist.append(c)
            else:
                c.RemoveMoat()

        self._battleFieldCells = clist
            
        
    
    def RemoveCell(self, cell):
        
        if (cell in self._battleFieldCells):
            self._battleFieldCells.remove(cell)
        



        
    def Draw(self, level, canvas, viewport):
        Construction.Construction.Draw(self, level, canvas, viewport)
        return
        if (self.__hasWater):
            color = "SkyBlue"
        else:
            color = "DarkSeaGreen"
            
        # Draw each moat battlefield cell
        for c in self._battleFieldCells:
            bbox = c.GetBoundingQuad()
            vp1 = viewport.W2V(bbox.minPoint)
            vp2 = viewport.W2V(bbox.maxPoint)
            self._canvasObjs.append(canvas.create_rectangle(vp1.x, vp1.y, vp2.x, vp2.y, fill=color, outline=color))
        
    
    
    
    def RedrawAttacked(self, canvas, viewport):
        self.Draw(0, canvas, viewport)
     
     
     
    def GetClosestMoatCell(self, posfrom):
        
        ret = None
        minD = -1
        
        for c in self._battleFieldCells:
            d = ((posfrom.x - c.center.x)**2) + ((posfrom.y - c.center.y)**2) + ((posfrom.z - c.center.z)**2)
            if ((ret == None) or (d < minD)):
                ret = c
                minD = d
                
        return ret
    
    
        