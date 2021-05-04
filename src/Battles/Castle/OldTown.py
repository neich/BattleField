
from Battles.Utils.Geometry import Point2D, ConvexHull, BoundingQuad
import Battles.Utils.Settings 



class OldTown:
    """
    Inner town, inside the castle
    
    Attributes:
    
        ConvexHull: Convex hull around city that matches with the castle walls (without towers and moats)
        Castle: Link to the castle
        Buildings: List of predefined buildings
        BattleFieldCells: List of city battlefield cells
    
    """


    def __init__(self, castle):
        self.__convexhull = None
        self.__buildings = []
        self.__castle = castle
        self.__battleFieldCells = []
        
       
    def GetConvexHull(self): 
        return self.__convexhull  
        
        
    def Draw(self, canvas, viewport):

        # Draw each city battlefield cell
        if (Battles.Utils.Settings.SETTINGS.Get_B('City', 'DisplayOldTownGrid')):
            for c in self.__battleFieldCells:
                bbox = c.GetBoundingQuad()
                vp1 = viewport.W2V(bbox.minPoint)
                vp2 = viewport.W2V(bbox.maxPoint)
                canvas.create_rectangle(vp1.x, vp1.y, vp2.x, vp2.y, fill="light yellow")
        
        # Draw the buildings
        housesize = Battles.Utils.Settings.SETTINGS.Get_F('City', 'Houses', 'Size')
        for p in self.__buildings:
            vp1 = viewport.W2V(Point2D(p[0]-housesize, p[1]-housesize))
            vp2 = viewport.W2V(Point2D(p[0]+housesize, p[1]+housesize))
            canvas.create_rectangle(vp1.x, vp1.y, vp2.x, vp2.y, fill="Ghost White")
    

    
    
    def Wrap(self, city, margin, battlefieldcenter):
        # From a list of 2D points, constructs the convex hull around the castle with specified margin
        # battlefieldcenter is a Point2D with the center of the battlefield. To avoid biased results due some castle walls are closest to the attackers than others, c
        # enter here the city in the battle field
        # Calculate the bounding box and the displacement of it from the battlefield center. Then, apply this displacement to all city coordinates
        
        box = BoundingQuad()
        for c in city:
            box.InsertPoint(Point2D(c[0], c[1]))
        center = box.GetCenter()
        distx = battlefieldcenter.x - center.x
        disty = battlefieldcenter.y - center.y
        for c in city:
            c[0] += distx
            c[1] += disty 
        
        
        self.__buildings = city
        
        self.__convexhull = ConvexHull(city)
        self.__convexhull.Calculate()
        self.__convexhull.SetMargin(margin)
         
         
         
    def DeployInBattleField(self, battlefield):
        # Deploy the city into the battlefield
        
        self.__battleFieldCells = battlefield.DeployCity(self.__convexhull)   




