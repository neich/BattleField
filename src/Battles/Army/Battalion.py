from Battles.Utils.Geometry import Point2D, Vector2D, Bounding, BoundingQuad
from Battles.Utils.Message import Log
from Battles.Army import Action
from Battles.Factory import ArmyFactory
import Battles.Utils.Settings 
import Battles.Utils.Settings as settings

# Default required space for any army unit (used just as default value to initialize the bounding class)
ARMYCOMPONENT_BOUNDING = 2.0                    


def getBattalionDimensions(kind):
    return Bounding(settings.SETTINGS.Get_F('Army', 'Archers', 'Bounding/Length'), 
                    settings.SETTINGS.Get_F('Army', 'Archers', 'Bounding/Width'), 
                    settings.SETTINGS.Get_F('Army', 'Archers', 'Bounding/Height'))

def battalionFitsInCell(kind, celllength, cellwidth):
    # Returns true if current bounds fit in given cell size
    bounds = getBattalionDimensions(kind)
    return (celllength >= bounds.length) and (cellwidth >= bounds.width)



class Battalion:
    """ A generic army component class, such as  intantery, cavalry, ... This would never be used in battle, so it has dummy contents
    
    Class attr:
        bounding: Bounding box that has each one of the objects of current type: length, width and height.
    """
    
    bounding = Bounding( ARMYCOMPONENT_BOUNDING,  ARMYCOMPONENT_BOUNDING,  ARMYCOMPONENT_BOUNDING) 
    
    @staticmethod
    def GetNumberByCell(cellsize):
        # Returns the number of effective that fit in a square cell of given size
        if (cellsize < Battalion.bounding.length) or (cellsize < Battalion.bounding.width):
            return 0
        else:
            l = int(cellsize / Battalion.bounding.length)
            w = int(cellsize / Battalion.bounding.width)
            return l * w

    """ 
    Attributes:
        number: number of effective of current type
        freenumber: number of free effective of current type. Usefull when the army is placed. At the end of placement it should be 0
        action: Action definition (attack, defense....) See Battle.Action class to more info
         
        placement: Battalion placement management object
        isdead: True if current component is dead
        canvasobj : internal tkinter list of canvas objects used to draw the army component. Stored to allow refreshing their status
        army: Owner army
    """
    def __init__(self, army, number = 0):
        self._number = number             
        self._action = Action.ActionFeatures(defense = 0, attack = 0, speed = 0, reloadspeed = 0, accuracy = 0, distance = 0, stationary = False, movementpriority = 0)
          
        self._placement = Action.Placement(self)
        self._isDead = False
        self._canvasObjs = []
        self._label = "Battalion"
        self._army = army
       

#     def FitInCell(self, celllength, cellwidth):
#         # Returns true if current bounds fit in given cell size
#         if ((celllength < self._bounding.length) or (cellwidth < self._bounding.width)):
#             return False
#         else:
#             return True


    def GetCopy(self):
        # Returns a copy of itself
        factory = ArmyFactory()
        ret = factory.newBattalionNoCrop(army = self._army, kind = factory.GetArmyType(self))
        if ret == None:
            return None
       
        ret._number = self._number
        ret._bounding = Battalion.bounding
        ret._isDead = self._isDead
        ret._canvasObjs = []
        
        ret._action = self._action.GetCopy()
        ret._placement = self._placement.GetCopy(ret)
        
        return ret

         
    def GetLabel(self):
        return self._label

         
    def SetNumber(self, n):
        # Sets the initial number of effectives
        self._number = n
         
        
    def GetNumber(self):
        return self._number
        
        
    def GetBounding(self):
        return Battalion.bounding
    
    
    def GetBoundingQuad(self):
        # Return the bounding rectangle in world coordinates
        
        center = self.GetCenterPosition()
        minP = Point2D(center.x - (Battalion.bounding.length / 2.0), center.y - (Battalion.bounding.width / 2.0))
        maxP = Point2D(center.x + (Battalion.bounding.length / 2.0), center.y + (Battalion.bounding.width / 2.0))
        # Note that this is true since the battlefield is orthonormal
        
        return BoundingQuad(minPoint = minP, maxPoint = maxP)
        
        
    def GetSoldierBoxVolume(self):
        # Returns the volume of one soldier/unit in battalion
        return Battalion.bounding.GetVolume()    
        
       
    def SetDefense(self, d): 
        self._action.SetDefense(d)  

        
    def SetExtraDefense(self, v):
        # Increases the action defense value
        self._action.SetExtraDefense(v)    

         
    def AssignToCell(self, groundcell):
        # Updates cell
        self._placement.SetBattlefieldCell(groundcell)
        groundcell.SetBattalion(self)       

        # From battlefield there are not restrictions on attack vector and angle
        self._action.SetAttackVector(Vector2D(), None)
        
        
    def AssignToConstruction(self, construction, defendingline):
        # Updates position
        self._placement.SetDefendingLine(construction, defendingline)
        
        # Updates battalion data from construction features
        construction.SetBattalionConstructionData(self, defendingline)
   
   
    def GetCommand(self):
        return self._action.GetCommand()
    
    def SetCommand(self, command, target = None, commander = None):
        #print "SetCommand:", self._label, " ->", command
        self._action.SetCommand(command, target, commander)
        
    def SetAttackVector(self, direction, angle):
        self._action.SetAttackVector(direction, angle)    
        
        
    def Attack(self, against, castle, shoots):
        pass   
        
    def Defend(self, against, defenders, battlefield, shoots, castle):
        pass   
        
    def GetDefenseVal(self):    
        return self._action.GetDefense()
    
    def GetClimbingSpeed(self):
        return self._action.GetClimbingSpeed()
    
    def GetRubbleClimbingSpeed(self):
        return self._action.GetRubbleClimbingSpeed()
    
    
    def Kill(self, number, respawn = False):
        # Kills elements in current battalion
        # If given number is -1, kills the whole battalion
        # Respawn is only allowed for defender archers
        
        if number == -1:
            number = self.GetNumber()
        
        #self._number -= number;
        self.SetNumber(self.GetNumber() - number)
        
        if self._number <= 0:
            self._isDead = True
            self._number = 0
            Log('Battalion of %s exterminated' % (self.GetLabel()))
            
        self._placement.Kill(self._number)
            

    def GetCenterPosition(self):  
        return self._placement.GetCenterPosition()

        
    def GetRandomPosition(self):
        return self._placement.GetRandomPosition()    
        

    def GetBattlefieldCell(self):
        # Returns the battlefield cell if it is deployed on it, otherwise return None
        return self._placement.GetBattlefieldCell()

        
    def DistanceSort(self, frompos):
        # Return the distance from current position to given point
        # This is a convenience method created to sort lists of batttalions by distance
        # WARNING: Due this method is used for sorting purposes, the returned distance is squared, avoiding the overload of sqrt or hypot functions
        
        center = self._placement.GetCenterPosition()
        dist = ((frompos.x - center.x)**2) + ((frompos.y - center.y)**2) + ((frompos.z - center.z)**2) 
        return dist
        
        
        
    def Draw(self, canvas, viewport):
        if self._isDead:
            return
        # This color selection is ugly. But I don't want to place too much code just for color selection for tkinter. This is not the goal 
        factory = ArmyFactory()
        fillcolor = "red"
        if factory.IsArcher(self):
            fillcolor = "Light Coral"
        if factory.IsInfantry(self):
            fillcolor = "red"
        if factory.IsCannon(self):
            fillcolor = "Dark Orange"
        if factory.IsSiegeTower(self):
            fillcolor = "Pale Violet Red"
        if Battles.Utils.Settings.SETTINGS.Get_B('Army', 'ShowOutline'):
            outline = "gray"
        else:
            outline = fillcolor

        if self._placement.IsClimbing():
            # Draw the soldier attached to the climbing wall
            s = self._placement.GetCenterPosition()                
            p = s.Copy()
            p.x = s.x - (Battalion.bounding.length / 2.0)
            p.y = s.y - (Battalion.bounding.width / 2.0)
            pv = viewport.W2V(p)
            p.x += Battalion.bounding.length
            p.y += Battalion.bounding.width
            pv2 = viewport.W2V(p)
            self._canvasObjs.append(canvas.create_rectangle(pv.x, pv.y, pv2.x, pv2.y, fill=fillcolor, width=1, outline=outline))
        elif self._placement.IsInBattlefield():
            # Draw the battalion on the battlefield

            # Get cell center
            center = self._placement.GetCenterPosition()
            cs = self._placement.GetCellSize()
            # Draw each troop element
            cols = int(cs / Battalion.bounding.length)
            rows = int(cs / Battalion.bounding.width)
           
            counter = 0
            i = 0
            p = Point2D()
            p.y = center.y- cs/2
            while (i < rows) and (counter < self._number):
                j = 0
                p.x = center.x - cs/2
                while (j < cols) and (counter < self._number):
                    pv = viewport.W2V(p)
                    pv2 = viewport.W2V(Point2D(p.x + Battalion.bounding.length, p.y + Battalion.bounding.width))
                    self._canvasObjs.append(canvas.create_rectangle(pv.x, pv.y, pv2.x, pv2.y, fill=fillcolor, width=1, outline=outline))
                    p.x = p.x + Battalion.bounding.length
                    j += 1
                    counter += 1
                p.y = p.y + Battalion.bounding.width
                i += 1

            if self._action.GetCommand().IsCoverMoat():
                halfsize = cs / 2.0
                p1 = Point2D(center.x - halfsize, center.y - halfsize)
                p3 = Point2D(center.x + halfsize, center.y + halfsize)
                p2 = Point2D(p3.x, p1.y)
                p4 = Point2D(p1.x, p3.y)
                pv1 = viewport.W2V(p1)
                pv2 = viewport.W2V(p2)
                pv3 = viewport.W2V(p3)
                pv4 = viewport.W2V(p4)
                self._canvasObjs.append(canvas.create_line(pv1.x, pv1.y, pv3.x, pv3.y, fill="black"))
                self._canvasObjs.append(canvas.create_line(pv4.x, pv4.y, pv2.x, pv2.y, fill="black"))
    
            if Battles.Utils.Settings.SETTINGS.Get_B('Army', 'ShowLabels'):
                # Text the kind of battalion
                cv = viewport.W2V(Point2D(center.x, center.y))
                self._canvasObjs.append(canvas.create_text(cv.x, cv.y, text=self.GetLabel(), fill="gray"))
        
        elif self._placement.IsInDefendingLine():
            # Draw the battalion on the construction
            # There are a lot of different construction types. So we delegate the drawing to these kind of objects
            dl = self._placement.GetDefendingLine()
            dc = self._placement.GetDefendingConstruction()
            dc.DrawBattalion(dl, self, canvas, viewport, self._canvasObjs)
      
       
    def RedrawAttacked(self, canvas, viewport):
        # Redraws the army componet after an attack
        
        if len(self._canvasObjs) > 0:
            for c in self._canvasObjs:
                canvas.delete(c)
 
        self.Draw(canvas, viewport)
        
        
    def IsDefeated(self):
        if self._isDead:
            return True
        else:
            return False

      
    def Move(self, castle, selfarmy, againsarmy, battlefield, movedList):
        pass
         
    
    def SetMovementPriority(self, p):
        self._action.SetMovementPriority(p)
        
        
    
    def IsInBattleField(self):
        return self._placement.IsInBattlefield()
    


"""   
     
     
# Cavalry
CAVALRY_DEFENSE = 100
CAVALRY_ATTACK = 100
CAVALRY_SPEED = 500
CAVALRY_RELOAD = 1
CAVALRY_ACCURACY = 70
CAVALRY_DISTANCE = 2
CAVALRY_BOUNDING_LENGTH = 4.0
CAVALRY_BOUNDING_WIDTH = 4.0
CAVALRY_BOUNDING_HEIGHT = 4.0
CAVALRY_STATIONARY = False
CAVALRY_MOVEMENT_PRIORITY = 3

class Cavalry(Battalion):
    def __init__(self, army, number = 0):
        Battalion.__init__(self, army = army, number = number)
        self._action = Action.ActionFeatures( defense = CAVALRY_DEFENSE,
                                              attack = CAVALRY_ATTACK, 
                                              speed = CAVALRY_SPEED, 
                                              reloadspeed = CAVALRY_RELOAD, 
                                              accuracy = CAVALRY_ACCURACY, 
                                              distance = CAVALRY_DISTANCE,
                                              stationary = CAVALRY_STATIONARY)
        Battalion.bounding = Bounding( CAVALRY_BOUNDING_LENGTH, 
                                   CAVALRY_BOUNDING_WIDTH, 
                                   CAVALRY_BOUNDING_HEIGHT)
       
        
        
        
 
  
  # Catapults
CATAPULTS_DEFENSE = 1000
CATAPULTS_ATTACK = 1000
CATAPULTS_SPEED = 0
CATAPULTS_RELOAD = 10
CATAPULTS_ACCURACY = 30
CATAPULTS_DISTANCE = 200
CATAPULTS_BOUNDING_LENGTH = 20.0
CATAPULTS_BOUNDING_WIDTH = 20.0 
CATAPULTS_BOUNDING_HEIGHT = 40.0
CATAPULTS_STATIONARY = True
CATAPULTS_MOVEMENT_PRIORITY = 90                # Only God and cannons can move a catapult

      
class Catapults(Battalion):
    def __init__(self, number = 0):
        Battalion.__init__(self, number)
        self._action = Action.ActionFeatures( defense = CATAPULTS_DEFENSE, 
                                              attack = CATAPULTS_ATTACK, 
                                              speed = CATAPULTS_SPEED, 
                                              reloadspeed = CATAPULTS_RELOAD, 
                                              accuracy = CATAPULTS_ACCURACY, 
                                              distance = CATAPULTS_DISTANCE,
                                              stationary = CATAPULTS_STATIONARY)
        Battalion.bounding = Bounding( CATAPULTS_BOUNDING_LENGTH, 
                                   CATAPULTS_BOUNDING_WIDTH, 
                                   CATAPULTS_BOUNDING_HEIGHT)



# Mortars
MORTARS_DEFENSE = 300
MORTARS_ATTACK = 5000
MORTARS_SPEED = 0
MORTARS_RELOAD = 5
MORTARS_ACCURACY = 50 
MORTARS_DISTANCE = 1000
MORTARS_BOUNDING_LENGTH = 4.0
MORTARS_BOUNDING_WIDTH = 4.0
MORTARS_BOUNDING_HEIGHT = 1.0
MORTARS_STATIONARY = True
MORTARTS_MOVEMENT_PRIORITY = 4                  

class Mortars(Battalion):
    def __init__(self, number = 0):
        Battalion.__init__(self, number)        
        self._action = Action.ActionFeatures( defense = MORTARS_DEFENSE, 
                                              attack = MORTARS_ATTACK, 
                                              speed = MORTARS_SPEED, 
                                              reload = MORTARS_RELOAD, 
                                              accuracy = MORTARS_ACCURACY, 
                                              distance = MORTARS_DISTANCE,
                                              stationary = MORTARS_STATIONARY)
        Battalion.bounding = Bounding( MORTARS_BOUNDING_LENGTH, 
                                   MORTARS_BOUNDING_WIDTH, 
                                   MORTARS_BOUNDING_HEIGHT)
        
 
# Miners
MINERS_DEFENSE = 5
MINERS_ATTACK = 1000000
MINERS_SPEED = 1
MINERS_RELOAD = 10000
MINERS_ACCURACY = 90
MINERS_DISTANCE = 0
MINERS_BOUNDING_LENGTH = 2.0
MINERS_BOUNDING_WIDTH = 2.0
MINERS_BOUNDING_HEIGHT = 2.0
MINERS_STATIONARY = False
MINERS_MOVEMENT_PRIORITY = 4
       
class Miners(Battalion):
    def __init__(self, number = 0):
        Battalion.__init__(self, number)        
        self._action = Action.ActionFeatures( defense = MINERS_DEFENSE, 
                                              attack = MINERS_ATTACK, 
                                              speed = MINERS_SPEED, 
                                              reloadspeed = MINERS_RELOAD, 
                                              accuracy = MINERS_ACCURACY, 
                                              distance = MINERS_DISTANCE,
                                              stationary = MINERS_STATIONARY)
        Battalion.bounding = Bounding( MINERS_BOUNDING_LENGTH, 
                                   MINERS_BOUNDING_WIDTH,
                                   MINERS_BOUNDING_HEIGHT)

"""

