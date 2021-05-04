import math

from Battles.Utils.Geometry import Vector2D, Point3D, Vector3D, Sphere, Ray
from Battles.Factory import *
from Battles.Utils.Message import *
import Battles.Utils.Settings


class ActionFeatures:
    """ Action features of any element in a battle  
    Attributes:
        defense: defense value 
        attack: attack value
        speed: speed movement (meters/minute)
        reloadspeed: time to reload and fight again (minutes)
        accuracyFactor: accuracy factor in attack (%)
        distance: max distance of action (meters)
        movementpriority: priority of movement applied when two or more battalions want to occupy the same cell. The most priority battalion will switch his position with the 
                          desired cell if its battalion has a lower priority
        
        attackVector: Central proposal attack direction (attacker/defender frontal view vector). This is a suggestion only. The battlefield troops don't have attack vector
                      because they can attack to anything. By the other hand, castle troops are constrained to shoot in a direction (wall troops shoot on normal wall direction 
                      as central attack vector)
        attackAngle: Angle range to shoot. None value means no restrictions. Otherwise, the angle has this form:
                                    {'H': h_angle, 'V':{'bottom': v_angle_bottom, 'top':v_angle_top}}
                    , where h_angle is the horizontal angle range around the attack vector, v_angle_bottom is the maximum bottom vertical angle from a ground parallel vector, and
                    v_angle_top is for the top vertical angle. All of them must be positive
    
        reloadCounter: Internal counter to control the reload time. Each attack step is increased. The attacker cannot shoot again until the counter is equal to reloadspeed param
        displacementCounter : Internal counter to control the troops movement. From speed value and distance to move, the counter increases 1 for each step. When it achieves the
                              speed parameter value, the movement has done
        
        defenseExtra: Defense increase value (or decrease) applied to a battalion taking into account terrain or castle current position
        
        stationary: False if by definition the battalion cannot move, such as the cannons. Dont confuse this setting with STAY command
        
        command: Command object
        
        initialReload: False by default. If it is true, an initial reload is needed at first shoot
        
        
        Deffense/Attack values: 
                       0-100 is considered as actions between humans
                       101-1000 is considered when constructions are involved

                       By example, a soldier cannot have an attack factor greater than 100, but a cannon yes. In addittion, a cannon can fire on
                       a curtain wall or over a group of infantery. Obviously, the attack factor is much greater than the maximum attack factor of a human
    
                       0 defense means no shields, like archers
                       100 defense means the maximum human shield (armor and shield)
                       Attack factors are related to defense factors. 0 attack means a sheep
                       100 attack means the maximum human attack, with sword, lance, etc.
                       
        Accuracy factor:
                        It is used to influence on attack value. When an archer (or cannon) shoots, the accuracy factor means the proportion of aiming. Considering 
                        the human field of view, that is the aiming range, and only taking into account a 2D view, the accuracy is the % of human aiming angle. A 100%
                        of accuracy means 0 of lack of aiming. A 0% of accuracy means 120 (human field of view) of lack of aiming
                        
        
    
    """                   
    
    
    def __init__(self, defense, attack, speed, reloadspeed, accuracy, distance, stationary, movementpriority, climbspeed = 0):
        self.__defense = defense
        self.__attack = attack
        self.__speed = speed
        self.__reloadSpeed = reloadspeed
        self.__accuracyFactor = accuracy
        self.__distance = distance
        self.__climbingSpeed = climbspeed
        self.__movementPriority = movementpriority
        
        self.__rubbleClimbingSpeed = 0
        
        self.__attackVector = Vector2D()
        self.__attackAngle = None
        
        self.__reloadCounter = 0
        self.__initialReload = False
        self.__displacementCounter = 0
        
        self.__defenseExtra = 0
        
        self.__stationary = stationary
        
        self.__command = Command(Command.STAY)
        

    
    def GetCopy(self):
        # Returns a copy of itself
        
        ret = ActionFeatures(defense = self.__defense, 
                             attack = self.__attack, 
                             speed = self.__speed, 
                             reloadspeed = self.__reloadSpeed, 
                             accuracy = self.__accuracyFactor, 
                             distance = self.__distance, 
                             stationary = self.__stationary, 
                             movementpriority = self.__movementPriority, 
                             climbspeed = self.__climbingSpeed)
        
        ret.__defenseExtra = self.__defenseExtra
        ret.__attackVector = self.__attackVector.Copy()
        ret.__attackAngle = self.__attackAngle
        
        ret.__rubbleClimbingSpeed = self.__rubbleClimbingSpeed
        
        ret.__command = self.__command.GetCopy()
        
        return ret
    

    def SetExtraDefense(self, d):
        self.__defenseExtra = d

    def SetDefense(self, d):
        self.__defense = d
        
    def GetDefense(self):
        return (self.__defense + self.__defenseExtra)

    def GetClimbingSpeed(self):
        return self.__climbingSpeed

    def SetClimbingSpeed(self, s):
        self.__climbingSpeed = s

    def GetRubbleClimbingSpeed(self):
        return self.__rubbleClimbingSpeed
    
    def SetRubbleClimgingSpeed(self, s):
        self.__rubbleClimbingSpeed = s


    def SetAttackVector(self, vector, angle):
        self.__attackVector.SetFrom3D(vector)
        self.__attackAngle = angle

    def SetReloadTime(self, t):
        self.__reloadSpeed = t
        
    def GetReloadTime(self):
        return self.__reloadSpeed

    def SetInitialReload(self, b):
        self.__initialReload = b

    def SetStationary(self, b):
        self.__stationary = b
        
    def GetDistance(self):
        return self.__distance

    def SetCommand(self, command, target = None, commander = None):
        self.__command.ChangeCommand(command, target, commander)

    def GetCommand(self):
        return self.__command
    
 

    def InAttackRange(self, currPos, targetPos, castle, constructionTarget, excludeConstruction = None):
        # Returns true if targetPos is in attack range from currPos
        # Given castle is used to check if shoot should intersect with any castle part, returning False. 
        # If the attacker aim to any castle battalion, constructionTarget object is used to discard the target's construction from intersection test
        # If the attacker shoots from a construction (its a defender), excludeConstruction is used to avoid the castle self intersection check
         
        # Check the distance
        #dist = currPos.Distance(targetPos)
        #dist = math.sqrt(((currPos.x - targetPos.x)**2) + ((currPos.y - targetPos.y)**2))
        #dist = math.hypot(currPos.x - targetPos.x, currPos.y - targetPos.y)
        dist = math.sqrt(((currPos.x - targetPos.x)**2) + ((currPos.y - targetPos.y)**2) + ((currPos.z - targetPos.z)**2))
        if (dist > self.__distance):
            return False
        else:
            # Check the attack direction and angle
            
            if (not self.__attackVector.IsNull()):
                
                if (not self.__attackAngle):
                    return False

                # Check horizontal angle                
                vec = Vector2D()
                vec.val[0] = targetPos.x - currPos.x
                vec.val[1] = targetPos.y - currPos.y
                l = math.hypot(vec.val[0], vec.val[1])
                if (l == 0):
                    vec.val[0] = 0
                    vec.val[1] = 0
                else:
                    vec.val[0] /= l
                    vec.val[1] /= l

                dotprod = (self.__attackVector.val[0] * vec.val[0]) + (self.__attackVector.val[1] * vec.val[1])
                if (dotprod > 1):
                    dotprod = 1
                if (dotprod < -1):
                    dotprod = -1
                ang = math.degrees(math.acos(dotprod))

                if (ang > (self.__attackAngle['H'] / 2.0)):
                    return False
                else:
                    
                    # Check the vertical angle
                    vec2 = Vector2D()
                    vec2.val[0] = math.fabs(targetPos.x - currPos.x)
                    vec2.val[1] = targetPos.z - currPos.z
                    l2 = math.hypot(vec2.val[0], vec2.val[1])
                    if (l2 == 0):
                        vec2.val[0] = 0
                        vec2.val[1] = 0
                    else:
                        vec2.val[0] /= l2
                        vec2.val[1] /= l2
                        
                    dotprod2 = vec2.val[0]      # The reference vector is a ground parallel vector, that is <1,0>, so the dotprod can be simplified
                    if (dotprod > 1):
                        dotprod = 1
                    if (dotprod < -1):
                        dotprod = -1
                    ang2 = math.degrees(math.acos(dotprod2))
                    
                    if (((targetPos.z <= currPos.z) and (ang2 > self.__attackAngle['V']['bottom'])) or
                        ((targetPos.z > currPos.z) and (ang2 > self.__attackAngle['V']['top']))):
                            return False
                         
            
            attackvec = Vector3D().CreateFrom2Points(currPos, targetPos)
            
            if (constructionTarget != None):
                # Check the castle intersection when the attacker aims to the castle
                r = Ray(origin = currPos, direction = attackvec)
                
                # Check the ray intersection on all castle parts and get the closest (the first intersection)
                # If the closest is not the target, means that is occluded
                if (not constructionTarget.RayHitTest(r)):
                    return False
                else:
                    distr = r.GetLength()
                    r.Reset()   # Resets the previous hitpoint calculated in constructionTarget.RayHitTest(r)
                    if (castle.RayHitTest_Closest(ray = r, exclude = constructionTarget, distance = distr) != None):
                        return False
                    else:
                        return True
             
            if (excludeConstruction != None):

                # Check the castle intersection when the attacker shoots from the castle
                r = Ray(origin = currPos, direction = attackvec)
                if (castle.RayHitTest(r, excludeConstruction)):
                    distr = r.GetLength()
                    if (distr < dist):
                        return False
                    else:
                        return True
                else:
                    return True
                """
                constr = castle.RayHitTest_Closest(ray = r, exclude = excludeConstruction, distance = r.GetLength())
                if (constr != None):


                    
                    # We have to check if the intersection is done against an exterior wall or not
                    # The battalion placement could be under or behind the wall
                    factory = ConstructionFactory()
                    if (factory.IsWall(constr)):
                        # The most easy way to check it is to compare the wall normal vector and attack vector to check if both are visible
                        wnorm = constr.GetNormalVector()
                        if (wnorm.DotProd(attackvec) > 0):
                            # Not visible. This should be the wall back
                            return False
                        else:
                            return True     # Front wall hit

                    else:
                        return False    # Tower hit
                        
                else:
                    return True     # None castle part occludes the shot
                """
                 
                 
            return True
        
        
        
         
             

    def UpdateReloadTime(self):
        # Updates the internal counter 1 unit time 
        self.__reloadCounter += 1
        if (self.__reloadCounter >= self.__reloadSpeed):
            self.__reloadCounter = 0
            self.__initialReload = False
            
        
    def IsReloadReady(self):
        if ((self.__reloadCounter == 0) and not self.__initialReload):
            return True
        else:
            return False    
        

    def GetReloadRemainingTime(self, percentage, nextt):
        # Returns the remaining reload time
        # If percentage is true, returns the remaining time in %1
        # If nextt is true the returned time becomes increased by 1 time unit
        
        time = self.__reloadCounter
        if (nextt):
            time += 1
        
        if (percentage):
            return float(time) / float(self.__reloadSpeed)
        else:
            return self.__reloadSpeed - time



    def ShootToArmy(self, target):
        # Shoots to an army element
        # Returns true if shooter (current object) hits target (passed by parameter)
        # The target is updated if any element is killed
        # soldier param is the soldier index on battalion, used only to shoot on a specific soldier if target has broken ranks
        
        # Calculate the accuracy angle factor as a percentage of the field of view
        fov =  Battles.Utils.Settings.SETTINGS.Get_F('Army', 'HumanFieldOfView')
        aimangle = fov - (fov * self.__accuracyFactor / 100)
        aimfactor = math.cos(math.radians(aimangle))
        
        # The aimfactor reduces the attack value
        attack = self.__attack * aimfactor
        defense = target.GetDefenseVal()
        
        
        hit = self.Shoot(attack, defense)
        if (hit):
            target.Kill(1)
       
        return hit
       
       
       
       
    def Shoot(self, attackval, defenseval):
        
        # Calculate the shoot success between two units with given attack and defense values
        # Returns true if the attack success
        
        # If target is stronger (has more defense) than attacker, get the proportion factor between them
        # Then launch a random number. If it is smaller than factor, the strong defense fails
        # Note that  strong defenses against weak attackers have small factors, decreasing the probability to make a fail
        
        # If the attacker is stronger than target, we have to consider the probability of attack fail. Like the previous case, but on the opposite way
        
        # Note that this is required, otherwise the stronger ever will win over the weaker. ... Oh wait, this is exactly how the things would succeed.... wait....
        # Let me show you an example. If an archer is placed in a castle wall, it increases his defense value. If we don't use this heuristic, the archer attacker 
        # cannot win, never. And this isn't true. A lost arrow can hit on a wall archer. Or using a better example, when a wall archer shoots, he loose his defense factor.
        # Taking into account of all parameters is not cheap. So, I think that this is a well fitted idea.
        
        hit = False
        #random.seed()
        r = random.random()
        
        if (attackval <= defenseval):
            factor = attackval / defenseval
            if (r <= factor):
                hit = True
        else: 
            factor = defenseval / attackval
            if (random.random >= factor):
                hit = True
        
        return hit
    
    
    
    
    def ShootDuel(self, target):
        # Like Shoot method, but taking the current attack and defense values from current object and given one respectively
        return self.Shoot(self.__attack, target.GetDefenseVal())
        
        
        
  
    def ShootToConstruction(self, target, frompos, targetpos):
        # Shoots to a construction target. Usually by a cannon
        # The targetpos parameter is where attacker points. But the precision factor can modify it
        # In addition, the final shooting point can hit any other construction part (see NOTE bellow)
        # Returns a dictionary with hit result -> {"Hit": True/False, "Intersection": Point3D()}
        
        ret = {"Hit": False, "Intersection": Point3D()}
        
        # Aiming consideration: We are going to calculate a shoot in a direction sampled by a cosinus distribution
        # From the aiming point of view, the shooter points to a far point, and if accuracy factor is 100%, it should hit the target.
        # So, the sphere used to sample the cosinus distribution should has the target distance as radius.
        # Then, we can use the accuracy factor to get a percentage of shooting distance. With this consideration, bad accuracy factors means
        # sampling on small spheres, so the shoot can fail 
        dist = frompos.Distance(targetpos) 
        accuracy = dist * self.__accuracyFactor / 100.0
 
        direction = Vector3D()
        direction.CreateFrom2Points(frompos, targetpos)
        sph = Sphere(position = frompos, radius = accuracy)
        v = sph.GetRayCosine(direction)
        

        # Check hit on the castle
        # NOTE : The intersection test over whole castle geometry has a high cost. The process is simplified considering only target.
        #        If shoot doesn't hits target, the shoot fails
        
        ray = Ray(origin = frompos, direction = v, energy = self.__attack)
        hitpoint = target.RecieveImpact(ray)
        
        if (hitpoint != None):
            ret["Hit"] = True
            ret["Intersection"] = hitpoint
            
        return ret
        
  
  
  
    def ShootToBattlefield(self, battlefield, frompos, targetpos):
        # Shoots to battlefield. Usually, by a cannon
        # The targetpos parameter is where attacker points. But the precision factor can modify it
        # Returns a dictionary with the hit result and final cell -> {"Hit": True/False, "Intersection": Point3D(), "Cell": GroundCell}
        
        
        ret = {"Hit": False, "Intersection": Point3D(), "Cell": None}
        
        # Aiming consideration: We are going to calculate a shoot in a direction sampled by a cosinus distribution
        # From the aiming point of view, the shooter points to a far point, and if accuracy factor is 100%, it should hit the target.
        # So, the sphere used to sample the cosinus distribution should has the target distance as radius.
        # Then, we can use the accuracy factor to get a percentage of shooting distance. With this consideration, bad accuracy factors means
        # sampling on small spheres, so the shoot can fail 
        dist = frompos.Distance(targetpos) 
        accuracy = dist * self.__accuracyFactor / 100.0
 
        direction = Vector3D()
        direction.CreateFrom2Points(frompos, targetpos)
        sph = Sphere(position = frompos, radius = accuracy)
        v = sph.GetRayCosine(direction)
        

        
        # Check hit on the battlefield
          
        ray = Ray(origin = frompos, direction = v, energy = self.__attack)
        hitpoint = battlefield.RayIntersects(ray)
        
        
        if (hitpoint != None):
            ret["Intersection"] = hitpoint.Copy()
            ret["Cell"] = battlefield.GetCellFromPoint(hitpoint)
            ret["Battalion"] = None 

            if (not ret["Cell"].HasBattalion()):
                ret["Hit"] = False
            else:           
                
                battalion = ret["Cell"].GetBattalion()
                ret["Battalion"] = battalion

                # If battlefield battalion has only 1 unit (cannons, siege towers), the method will be the classic one (attack against defense)
                # Otherwise, we have to calculate the number of killed units into the battalion
                if (battalion.GetNumber() == 1):
                    
                    if (self.ShootDuel(battalion)):
                        ret["Hit"] = True
                        battalion.Kill(1)
                    else:
                        ret["Hit"] = False
                
                else:
                  
                    # Shooting against battlefield is usually done by cannons. The main difference is that a cannon ball can kill more than one unit. To know how many units are killed
                    # we follow the next algorithm.
                    # When a cannon shoot hits on a cell, and considering that a cannon ball doesnt explode, the ball go trough the cell until it touch the ground. If any soldier is in its
                    # path, dies. But we dont have any predefined soldier position inside the battalion. To solve it, we are going to work with densities.
                    # We can get the cell soldiers density with 
                    #     celldensity = battalion_size / cell_volume
                    # The cannon ball path inside the cell can be modelled as a cylinder. So, 
                    #     nhits = celldensity * cylinder_volume
                    # But this has a problem, so we are considering that each unit has the same volume in the battlefield cell, and this is not true (think on a cannon)
                    # So we need to consider the occupied volume ratio. Then
                    #    cellratio = (battalion_size * soldier_volume) / cell_volume
                    # Because we want to keep the same ratio for cylinder, we get
                    #    (nkills * soldier_volume) = cellratio * cylinder_volume
                    #    nkills = battalion_size * cylinder_volume / cell_volume
                    
                    
                    bbox = ret["Cell"].GetBoundingBox()
                    ray.Reset()
                    
                    if (ray.HitBox(bbox)):
                        clength = ret["Intersection"].Distance(ray.GetHitPoint())
                     
                        bvol = bbox.GetVolume()
                        if (bvol == 0):
                            ret["Hit"] = False  # Some battalions can have 0 height, such are the siege towers when are in construction phase
                        else:
                            svolume = battalion.GetSoldierBoxVolume()
                            cellratio = (battalion.GetNumber() * svolume) / bvol
                            cvolume = Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Cannons', 'BallRadius') * Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Cannons', 'BallRadius') * math.pi * clength
                            nhits = (cellratio * cvolume) / svolume
                            
                           
                            if (nhits >= 1):
                                battalion.Kill(math.ceil(nhits))
                                ret["Hit"] = True
                            else:
                                ret["Hit"] = False
                    else:
                        ret["Hit"] = False
             
             
        return ret
  
  
  
        
    def IsMoveReady(self, displacement, penalty = 1.0, climb = False):
        # Check if troop is ready to move
        # We have to check the cell size and unit speed (meters/minute or meters/step)
        # A new step is considered for each time this function is called 
        # Displacement parameter is the required displacement in meters
        # penalty parameter is a % value of reduction over unit speed (max : 1)
        # If climb is True takes the climbing speed. Otherwise, the speed parameter
 
        if (self.__stationary):
            return False
 
        if (not self.__command.IsMove()):
            return False
 
        if ((penalty >= 0) and (penalty < 0.00001)):
            return False
        
        if (climb):
            speed = self.__climbingSpeed * penalty
        else:
            speed = self.__speed * penalty
        
        
        if (speed >= displacement):
            return True
        
        self.__displacementCounter += speed
        if (self.__displacementCounter >= displacement):
            self.__displacementCounter = 0
            return True
        else:
            return False
            

    def ResetMoveReady(self):
        self.__displacementCounter = 0



    def AvaiablePassThrough(self, battalion):
        # Returns true if current battalion movement priority is higuer than given one
        return (self.__movementPriority > battalion._action.__movementPriority)

    def SetMovementPriority(self, p):
        self.__movementPriority = p


        
        
        
      
        
          
  
  
  
  
  
class Command:

    """
    Type of command for units
    
    Attributes:
        type: Command type
        target: Target related to command
        commander: Who controls the unit. None by default (none commander, or user commander)
    """
    
    # Type of commands
    STAY = 0                # Stationary state. Do not do anything
    ATTACK_CASTLE = 1       # Attack to castle. Suitable for archers, cannons or siege towers
    GOTO_CASTLE = 2         # Go to castle. Suitable for infantry 
    DEFEND_CASTLE = 3       # Defend the castle. Suitable for defender archers
    COVER_MOAT = 4          # Move to target moat cell and cover it
    WAITFOR_CLIMBING = 5    # Waiting for start the wall climbing. Its the previous state of CLIMB_WALL and is used to stop the soldiers of a battalion and force them to
                            # climb one by one
    THROW_STAIR = 6         # Defenders type of command to throw "things" away from wall and to a stair full of climbers
    
    def __init__(self, typecom, target = None, commander = None):
        self.__type = typecom
        self.__target = target
        self.__commander = commander
  
    def GetCopy(self):
        # Returns a copy of itself
        ret = Command(self.__type, self.__target, self.__commander)
        return ret
    
    def GetType(self):
        return self.__type
    
    def GetTarget(self):
        return self.__target
    
    def GetCommander(self):
        return self.__commander
    
    
    def ChangeCommand(self, newtype, newtarget, newcommander):
        self.__type = newtype
        self.__target = newtarget
        self.__commander = newcommander
    
    def IsMove(self):
        # Return true if current command allow the movement
        # note that WAITFOR_CLIMBING means stay, but is used into a movement context
        return (self.__type == Command.ATTACK_CASTLE) or \
                (self.__type == Command.GOTO_CASTLE) or \
                (self.__type == Command.COVER_MOAT) or \
                (self.__type == Command.WAITFOR_CLIMBING)
    
    def IsAttack(self):
        return (self.__type == Command.ATTACK_CASTLE)
        
    def IsCoverMoat(self):
        return (self.__type == Command.COVER_MOAT)
    
    def IsDefend(self):
        return (self.__type == Command.DEFEND_CASTLE)
    
    def IsWaitingForClimbing(self):
        return (self.__type == Command.WAITFOR_CLIMBING)
    
    def IsTrhowing(self):
        return (self.__type == Command.THROW_STAIR)
    
    def isCommand(self, code):
        return self.__type == code
    
    
    
class Placement:
    """ Placement management class for battalions. It controls where the battalion is placed. 
    
        Attributes:
            battalion: Reference to owner battalion class
            battlefieldCell: If battalion is an attacker, the cell where it is placed 
            defendingLine: Construction element where troops are placed and placement. The object is a dictionary with data:
                            {"Construction": construction_object, "DefendingLine": index_defendingline}
            climbing: Dictionary with the climbing wall, current battalion 3D position, and current climbing stair (linked with wall climbing stairs list)
            placementType : Kind of placement 
            
            badCells: Battle field cells marked as bad due the battalion enters into a deadlock zone. Usefull for infantry units
            visitedCells: List of battalion visited cells. Usefull for infantry units
    """
    
    # Placement types
    UNKNOWN = 0
    BATTLEFIELD = 1
    DEFENDINGLINE = 2
    CLIMBING = 3
    
    
    def __init__(self, battalion):
        self.__battalion = battalion
        self.__battlefieldCell = None
        self.__defendingLine = {"Construction": None, "DefendingLine": -1}
        self.__climbing = {"Wall": None, "Position": Point3D(), "Stair": None}
        self.__placementType = Placement.UNKNOWN       
   
        self.__badCells = []
        self.__visitedCells = []
        
    def GetCopy(self, battalion):
        # Return a copy of self object. Given battalion is the new battalion where the copied data will be stored 
        ret = Placement(battalion)
        ret.__placementType = self.__placementType
        
        if (self.__placementType == Placement.BATTLEFIELD):
            ret.__battlefieldCell = self.__battlefieldCell
            ret.__badCells = self.__badCells
            ret.__visitedCells = self.__visitedCells
        elif (self.__placementType == Placement.DEFENDINGLINE):
            ret.__defendingLine["Construction"] = self.__defendingLine["Construction"]
            ret.__defendingLine["DefendingLine"] = self.__defendingLine["DefendingLine"]
        elif (self.__placementType == Placement.CLIMBING):
            ret.__climbing["Wall"] = self.__climbing["Wall"]
            ret.__climbing["Position"] = self.__climbing["Position"]    
            ret.__climbing["Stair"] = self.__climbing["Stair"]
        return ret
    
    def IsInBattlefield(self):
        return self.__placementType == Placement.BATTLEFIELD
        
    def IsInDefendingLine(self):
        return self.__placementType == Placement.DEFENDINGLINE    
        
    def IsClimbing(self):
        return self.__placementType == Placement.CLIMBING
        
    def GetBattlefieldCell(self):
        return self.__battlefieldCell    
            
    def GetClimbingWall(self):
        return self.__climbing["Wall"]
    
    def GetClimbingStair(self):
        return self.__climbing["Stair"]
    
    def GetDefendingLine(self):
        return self.__defendingLine["DefendingLine"]
    
    def GetDefendingConstruction(self):
        return self.__defendingLine["Construction"]
    
    def SetBattlefieldCell(self, cell):
        self.__placementType = Placement.BATTLEFIELD
        self.__battlefieldCell = cell
        
        self.__defendingLine["Construction"] = None
        self.__defendingLine["DefendingLine"] = -1
        self.__climbing["Wall"] = None
        self.__climbing["Position"] = Point3D()
        self.__climbing["Stair"] = None
        
        
    def SetDefendingLine(self, construction, defendingline):
        self.__placementType = Placement.DEFENDINGLINE                
        self.__defendingLine["Construction"] = construction
        self.__defendingLine["DefendingLine"] = defendingline
         
        self.__battlefieldCell = None
        self.__climbing["Wall"] = None
        self.__climbing["Position"] = Point3D()
        self.__climbing["Stair"] = None
    
    
    
    def SetClimbingWall(self, wall = None, stairposition = None, clearprevious = True, stair = None):
        # Set the climbing wall and position of current battalion
        # If wall is None, choose the closest wall. Otherwise, the climbing wall will be the given one
        # If stairposition isnt None, the battalion is placed on this position (the position over the wall is not checked in this case)
        # If clearprevious is true, previous placement types are cleared (such as the battlefield bidirectional links)
        # A stair must to be provided
        
        if (not stair):
            print "ERROR SetClimbingWall -> None stair is provided"
            return
        
        self.__placementType = Placement.CLIMBING
        
        # Get target wall (the closest has to be the target one)
        if (wall):
            self.__climbing["Wall"] = wall
        else:
            self.__climbing["Wall"] = self.__battlefieldCell.GetClosestWall()
        if (stairposition):
            self.__climbing["Position"] = stairposition
        else:
            self.__climbing["Position"] = self.__climbing["Wall"].Project(self.__battlefieldCell.GetRandomCellPosition())
        
            
        # Removes the defensive battlefield factor
        self.__battalion.SetExtraDefense(0)
        
        # Updates the wall climbers list
        self.__climbing["Stair"] = stair
        self.__climbing["Stair"].AddClimber(self.__battalion)
         
            
        self.__defendingLine["Construction"] = None
        self.__defendingLine["DefendingLine"] = -1
        self.__battlefieldCell = None
        if (clearprevious):
            if ((self.__battlefieldCell != None) and self.__battlefieldCell.HasBattalion()):
                self.__battlefieldCell.RemoveBattalion()

        
         
        
    def Kill(self, remain):
        # Kills one soldier from the battalion. 
        # Updates the structure placement if remain is 0 (that is, whole battalion is eliminated)
        # WARNING: Batttalion is not deleted from army lists
        
        if ((remain > 0) and (self.__placementType == Placement.CLIMBING)):
            print("ERROR: A climbing battalion is killed but not defeated!!")
            
        if (remain <= 0):
            if (self.__placementType == Placement.BATTLEFIELD):
                self.__battlefieldCell.RemoveBattalion() 
            elif (self.__placementType == Placement.DEFENDINGLINE):
                self.__defendingLine["Construction"].RemoveBattalion(self.__defendingLine["DefendingLine"], self.__battalion)
            elif (self.__placementType == Placement.CLIMBING):
                #self.__climbing["Wall"].RemoveClimber(self.__battalion)
                self.__climbing["Stair"].RemoveClimber(self.__battalion)
                if (self.__climbing["Stair"].IsDefeated()):
                    self.__climbing["Wall"].RemoveClimbingStair(self.__climbing["Stair"])
             
            self = Placement(self.__battalion)
        
        
        
        
    def GetCenterPosition(self):
        # Get the center point of current battalion. Index is used only for climbing soldiers 
         
        if (self.__placementType == Placement.BATTLEFIELD):
            return self.__battlefieldCell.center
        elif (self.__placementType == Placement.DEFENDINGLINE):     
            return self.__defendingLine["Construction"].GetBattalionCellPosition(self.__defendingLine["DefendingLine"], self.__battalion) 
        elif (self.__placementType == Placement.CLIMBING):
            return self.__climbing["Position"]
    
    
    def GetRandomPosition(self):
        # Get a random point of current battalion. Index is used only for climbing soldiers 
         
        if (self.__placementType == Placement.BATTLEFIELD):
            return self.__battlefieldCell.GetRandomCellPosition()
        elif (self.__placementType == Placement.DEFENDINGLINE):     
            return self.__defendingLine["Construction"].GetRandomBattalionCellPosition(self.__defendingLine["DefendingLine"], self.__battalion) 
        elif (self.__placementType == Placement.CLIMBING):
            
            # Since the random position on battlefield and defending lines are calculated on the battalion placement, we are going to calculate a bounding around the soldier and
            # calculate the point on it. To avoid working with a cube (the soldier is moving in all 3 dimensions), we get random positions on the three axis
            
            bounding = self.__battalion.GetBounding()
            #random.seed()
            rx = random.uniform(0, bounding.length * 2.0)
            ry = random.uniform(0, bounding.width * 2.0)
            rz = random.uniform(0, bounding.height * 2.0)

            pos = self.__climbing["Position"].Copy()
            # Lets do simplify more and don't consider the wall rotation. This is not accurate, but is much faster than vector operations
            pos.x = (pos.x - bounding.length) + rx
            pos.y = (pos.y - bounding.width) + ry
            pos.z = (pos.z - bounding.height) + rz
            
            return pos
            
        return Point3D()    
    
    
            
            
    def GetCellSize(self):
        if (self.__placementType == Placement.BATTLEFIELD):
            return self.__battlefieldCell.GetCellSize()
        elif (self.__placementType == Placement.DEFENDINGLINE):    
            print("*******WARNING!!!! -> GetCellSize of defending lines not defined yet!!!!")
        elif (self.__placementType == Placement.CLIMBING):
            print("*******WARNING!!!! -> GetCellSize of climbing soldiers not defined yet!!!!")
        return 0.0   
            
            
            
    def SwitchBattlefieldCell(self, battalionplacement):
        # Switch the battlefield cell positions between current and given one battalions
        
        if (self.IsInBattlefield() and battalionplacement.IsInBattlefield()):
            nextcell = battalionplacement.__battlefieldCell
            oldcell = self.__battlefieldCell
            
            nextcell.SetBattalion(self.__battalion)
            self.__battlefieldCell = nextcell
            
            oldcell.SetBattalion(battalionplacement.__battalion)
            battalionplacement.__battlefieldCell = oldcell
        else:
            Log('ERROR: Only battelfield battalions can switch their positions', VERBOSE_WARNING)
            
            
        
    
    def MoveTo(self, newplace, movedList):
        # Moves current battalion to given new position. The parameter type is not restricted and depends on the current placement. For battlefield placement, the 
        # parameter is the next cell. For climbing soliders, the parameter can be none
        # The moved battalions (the current one and the others required for this movement) will be stored in given movedList parameter
        
        if (self.__placementType == Placement.BATTLEFIELD):
            
            cell = newplace
            
            # Collision management    
            # If next cell to move is populated with a battalion with less priority, do a switch between both
            if (cell.HasBattalion()):
                occlude = cell.GetBattalion()
                if (self.__battalion._action.AvaiablePassThrough(occlude)):    
                    self.SwitchBattlefieldCell(occlude._placement)
                    if (movedList != None):
                        movedList.append(self.__battalion)
                        movedList.append(occlude)
            else:
                cell.MoveTroopsFromCell(self.__battlefieldCell)
                self.__battlefieldCell = cell
                
                if (movedList != None):
                    movedList.append(self.__battalion)
                
            self.SetVisitedCell(cell)


        
        elif (self.__placementType == Placement.DEFENDINGLINE):    
            print("*******WARNING!!!! -> MoveTo of defending lines not defined yet!!!!")
            
        elif (self.__placementType == Placement.CLIMBING):
            # The soldier will climb the wall by one step
            # Each time this function is called, the climber advance one step
            # The climber is only a 3D point with climber position
            # Returns true if climber reaches the top of the wall

            climbwall = self.__climbing["Wall"]
            climber = self.__climbing["Position"]
            
            
            # Check if climber has achieved his target
            if (climbwall.GetTileManager().IsInHole(climber) or (climber.z >= climbwall.GetHeight())):

                climbwall.SetClimbedBattalion(self.__battalion, climber)
                Log(climbwall.GetLabel() + ' has been climbed!!. Victory for the attackers!!!!')

            else:
    
                # The wall can have rubble. In this case the climber climbs the rubble. The rubble climbing has a different speed than usual climbing
                # Also, the rubble climbing doesnt create any thrower (logical, so there arent any wall top to place it)
                rubbleheight = climbwall.GetTileManager().GetRubbleHeight(climber)
                if (rubbleheight > climber.z):
                    climber.z += self.__battalion.GetRubbleClimbingSpeed()
                else:
                    # Usual climbing
                    climber.z += self.__battalion.GetClimbingSpeed()
                    
                    
                
                
                """
                # In addition, each climber goes to the nearest hole in the wall. If there aren't any hole, just climbs up
                tp = climbwall.GetNearestHolePosition(climber)
                if (tp != None):
                    dist2hole = tp.Distance(climber)
                else:
                    dist2hole = climbwall.GetLength() * climbwall.GetHeight()     # Just an enough big dummy value
                    
                dist2top = climbwall.GetHeight() - climber.z; 
                
                if ((tp == None) or (dist2top < dist2hole)):
                    climber.z += self.__battalion.GetClimbingSpeed()
                    if (climber.z >= climbwall.GetHeight()):
                        climbwall.SetClimbedBattalion(self.__battalion, climber)
                        Log(climbwall.GetLabel() + ' has been climbed!!. Victory for the attackers!!!!')
    
                else:
                    v = Vector3D().CreateFrom2Points(climber, tp)
                    climber.Move(v, self.__battalion.GetClimbingSpeed())
                    if (climbwall.IsInHole(climber)):
                        climbwall.SetClimbedBattalion(self.__battalion, climber)
                        Log(climbwall.GetLabel() + ' has been climbed!!. Victory for the attackers!!!!')
                """
    
                # Check for each movement if stair has any throwers (the avaiability of defenders to create a thrower battalion can change) 
                if (not self.__climbing["Stair"].GetThrowers()):
                    self.__climbing["Stair"].CreateThrower(movedList)


            if (movedList != None):
                movedList.append(self.__battalion)
            
            
            
            
    def SetBadCell(self, cell):
        if (not cell in self.__badCells):
            self.__badCells.append(cell)
        
    def IsBadCell(self, cell):
        #return (cell in self.__badCells)
        return False
    
    def SetVisitedCell(self, cell):
        if (not cell in self.__visitedCells):
            self.__visitedCells.append(cell) 
            
    def IsVisitedCell(self, cell):
        #return (cell in self.__visitedCells)
        return False
        
        
        
        
        