from Action import *
from Battles.Utils.Geometry import Point2D

class Stair:
    
    """ Container class to manage the virtual stair data that is created when a battalion starts to climb a wall
        This is an army type of class, but it is not used as any other battalion. Is used only as container of a set of climbers data (not the climbers, so them are 
        isolated battalions that have the command of climb, moving themselves without the control of this class.
        This class is also usefull to create the throwers battalions
    
    Attributes:
    
        battalions: List of climbers
        position: Stair position (2D)
        defendersArmy: Army of defenders. Usefull to create trhowers and remove them
        throwers: Thrower battalion created to destroy the stair
        construction: Construction (wall usually) where the stair is deployed
        waitingBattalion: Battalion that waits to start climbing. It is usefull to know if the stair is clear from climbers and from waiting climbers
    """
    
    def __init__(self):
        self.__battalions = []
        self.__defendersArmy = None
        self.__position = Point2D()
        self.__throwers = None
        self.__construction = None
        self.__waitingBattalion = None
        
        
    # Getters and setters

    def SetPosition(self, pos):
        self.__position = pos
        
    def GetHeight(self):
        return self.__construction.GetHeight()

    def SetWaitingBattalion(self, b):
        self.__waitingBattalion = b

    def GetWaitingBattalion(self):
        return self.__waitingBattalion
        
    def SetDefendersArmy(self, da):
        self.__defendersArmy = da
        
    def GetDefendersArmy(self):
        return self.__defendersArmy
        
    def SetConstruction(self, c):
        self.__construction = c   
        
        """
        # Check if there are rubble and place the stair on his top
        h = self.__construction.GetRubbleHeight(self.__position)
        self.__position.z = h
        """
        self.__position.z = 0
         
        
    def GetConstruction(self):
        return self.__construction    
        
    def GetTopPosition(self):
        return Point3D(self.__position.x, self.__position.y, self.GetHeight())    
           
    def SetThrowers(self, t):
        self.__throwers = t
    
    def GetThrowers(self):
        return self.__throwers
    
    def GetClimbers(self):
        return self.__battalions
        
        
    def AddClimber(self, battalion):
        self.__battalions.append(battalion)
        
    def RemoveClimber(self, battalion):
        if (battalion):
            if (battalion in self.__battalions):
                self.__battalions.remove(battalion)
        
             
        if (self.IsDefeated()):      
            if (self.__throwers):
                self.__throwers.Dissolve()
        
        
    def ExistsClimber(self, climber):
        return climber in self.__battalions
        
        
    
    def IsDefeated(self):
        # The stair can be empty of climbers at the same time that other ones are waiting
        # Also, the waiting units could be defeated before start climbing
        # Note that the last climber is the waitingbattalion itself. But it becomes a climber. So waitingbattalion is None and stair battalion list is empty
        
       
        if (((not self.__waitingBattalion) or (self.__waitingBattalion.GetNumber() < 1) or self.__waitingBattalion.IsDefeated()) and (len(self.__battalions) == 0)):
            return True
        else:
            return False

    
                
    def GetClosestClimberInAttackRange(self, posfrom, castle, action):
        # Returns the closest climbing battalions to given posfrom parameter (3D point)
        # Note that returned object is a dictionary with the climber battalion and the distance
           
        ret = {"Climber": None, "MinDist": -1}
        
            
        for b in self.__battalions:
            center = b.GetCenterPosition()
            dist = math.sqrt(((posfrom.x - center.x)**2) + ((posfrom.y - center.y)**2) + ((posfrom.z - center.z)**2))
            if ((not ret["Climber"]) or (dist < ret["MinDist"])):
                if (action.InAttackRange(currPos = posfrom, targetPos = center, castle = castle, constructionTarget = None, excludeConstruction = self)):
                    ret["Climber"] = b
                    ret["MinDist"] = dist

        return ret
    
    
    
    def CreateThrower(self, movedList):
        # Creates the thrower
        
        # Let the defending line to create the thrower and place it on the most suitable position
        defendinglines = self.__construction.GetDefendingLines()
        defendinglines.CreateThrower(self, self.__defendersArmy, movedList)
        
        #self.__construction.CreateThrower(self, self.__defendersArmy, movedList)
    
    
    
    def Draw(self, canvas, viewport):
        # Draw the stair and their battalions in height view. Also, draw the thrower battalion (if it is defined) in height view. Return a list with all canvas objects
        
        ret = []
        
        h = self.GetHeight()
        
        dist = self.__construction.GetStartPosition().Distance(Point2D().SetFrom3D(self.__position))
        
        for e in self.__battalions:

            s = e.GetCenterPosition()

            p1 = Point2D(dist, h - s.z)
            p2 = Point2D(dist + e.GetBounding().length, h - (s.z + e.GetBounding().height))

            pp1 = viewport.W2V(p1)
            pp2 = viewport.W2V(p2)
            ret.append(canvas.create_rectangle(pp1.x, pp1.y, pp2.x, pp2.y, fill="red", outline="gray"))
            
            
        if (self.__throwers):
            canvobjs = self.__throwers.DrawHeightView(canvas, viewport, position = Point2D(dist, 0.0))
            if (canvobjs):
                ret.extend(canvobjs)
            
        return ret
    
    
    def RedrawAttacked(self, canvas, viewport):
        # Dont needed
        pass
    
     
    
