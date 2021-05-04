"""
Created on Apr 19, 2013

@author: mussoltrek
"""

from Battles import Factory
from Battles.Utils.Geometry import Vector3D, Ray

import math
from Battles.Factory import ArmyFactory


class ArmyBattalionData:
    """ Battalion data structure used to store the list of all battalions by type (see Army class)
    
    Attributes:
        battalions: List with all battalions of a kind
        number: Number of all troops in list
        freenumber: Number of avaiable troops in list (those troops that aren't placed in game yet). Used in battalions placement methods
    """
    
    def __init__(self):
        self.battalions = []
        self.number = 0
        self.freenumber = 0
        
        


class Army:
    """ Army overall class. It contains all army structures
    
    Attributes:
        faction: True if it is an army of attackers, or false otherwise
        battalions: Dictionary with lists of all battalions (classified by type)
                    Each element is an ArmyBattalionData object                    
        
    """
    
    def __init__(self, attackers):
        self.__faction = attackers      
        self.__battalions = {}

    def getBattalions(self):
        return self.__battalions
    
    def setBattalions(self, battalions):
        self.__battalions = battalions
        
    def AreAttackers(self):
        return (self.__faction)
    
    def Reset(self):
        del self.__battalions
        self.__battalions = {}
    
    def DefineBattalion(self, kind, number, accum = False):
        # Defines a new battalion kind and avaiable troops. If a previous battalion of given kind has created, it is removed 
        obj = self.__battalions.get(kind)
        if (not accum):
            if (obj != None):
                self.__battalions.pop(kind)
            d = ArmyBattalionData()
            d.number = number
            d.freenumber = number
            self.__battalions[kind] = d
        else:
            if (not obj):
                obj = ArmyBattalionData()
            obj.number += number
            obj.freenumber += number
            self.__battalions[kind] = obj
    
        
    def GetString(self):
        s = ""
        for kind in self.__battalions:
            batdata = self.__battalions[kind]
            s += kind + " " + str(batdata.number - batdata.freenumber) + " deployed from " + str(batdata.number)
            total = 0
            for bat in self.__battalions[kind].battalions:
                total += bat.GetNumber()
            s += "(" + str(total) + ")" + '  &  '
        return s
         
    def finishedBattalions(self, kind):
        batdata = self.__battalions[kind]
        return (batdata.freenumber == 0)
    
    def getBattalionSize(self, kind):
        return self.__battalions.get(kind).GetBounding().length
    
    def getBattalionFreeNumber(self,kind):
        return self.__battalions[kind].freenumber
    
    def CropBattalionSize(self, battalion, kind, number = -1):
        # Crops the battalion of given size to avaiable troops number if their number is greater than given one
        # If number is negative, it will assign all remain effective
        
        if (not kind in self.__battalions):
            print 'ERROR: Unknown kind of battalion'
            return None
        
        batdata = self.__battalions[kind]
        
        if (batdata.freenumber == 0):
            return None
      
        if (number == -1):
            n = batdata.freenumber
        elif (batdata.freenumber < number):
            n = batdata.freenumber
        else:
            n = number
            
        battalion.SetNumber(n)
        
        return battalion
   
   
    def IsBattalionTypeAvaiable(self, kind):
        
        if (not kind in self.__battalions):
            return False
        if (self.__battalions[kind].freenumber == 0):
            return False
        return True
        
   
   
    def InsertBattalion(self, battalion, updatecounters = True):
        # Inserts given battalion into dictionary lists and updates available troops
        
        kind = Factory.ArmyFactory().GetArmyType(battalion)
        if (not self.__battalions.has_key(kind)):
            if (updatecounters):
                self.DefineBattalion(kind, battalion.GetNumber())
            else:
                self.DefineBattalion(kind, 0)
        
        self.__battalions[kind].battalions.append(battalion)
        
        if (updatecounters):
            self.__battalions[kind].freenumber -= battalion.GetNumber()
            #print "battalion.GetNumber()",battalion.GetNumber(),"self.__battalions[kind].freenumber", self.__battalions[kind].freenumber
   
   
   
    def RemoveBattalion(self, battalion, respawn = True):
        
        # Forces the internal defeat to be sure that battalion will not be used anymore
        # respawn parameter is used to allow or not the unit respawn if there are more units available (only applied to defender archers)

        battalion.Kill(battalion.GetNumber(), respawn)
        
        kind = Factory.ArmyFactory().GetArmyType(battalion)
        if (self.__battalions[kind] != None):
            if (battalion in self.__battalions[kind].battalions):  # The alternative should never happen ....
                self.__battalions[kind].battalions.remove(battalion)
            
        
        
    def HasBattalionType(self, kind):
        return self.__battalions.has_key(kind)    
   
   
   
    def GetBattalionType(self, kind):
        if (not self.HasBattalionType(kind)):
            return None
        
        return self.__battalions[kind]
        
        
   
    def Draw(self, canvas, viewport):
        for b in self.__battalions.values():
            for bb in b.battalions:
                bb.Draw(canvas, viewport)
            
 
    """
    Attack !!!!
    iterates over each battalion, ordering them to attack!
    """
    def Attack(self, against, castle, shoots):
        # Current army attack against given one onto given castle
        for b in self.__battalions.values():
            for bb in b.battalions:
                bb.Attack(against, castle, shoots)
                             
 
    """
    Defend !!!!
    iterates over each battalion, ordering them to defend!
    """
    def Defend(self, against, defenders, battlefield, shoots, castle):  
        # Current army attack against given one onto given castle
        for b in self.__battalions.values():
            for bb in b.battalions:
                bb.Defend(against, defenders, battlefield, shoots, castle)
                        

    """
    Move !!!!
    iterates over each battalion, ordering them to move!
    """
    def Move(self, castle, againstarmy, battlefield, movedList):
        # Move all troops 1 step
        for b in self.__battalions.values():
            # WARNING: Move function for a battalion could finish with a suicide when no more movements are possible (SigeTowers by example)
            # Therefore, update size value because the list size has been changed
            for battalion in b.battalions:
                battalion.Move(castle, self, againstarmy, battlefield, movedList)


    def IsDefeated(self, defenders = True):
        # Returns true if current army has been defeated
        
        # For the defenders army, all battalions have to be destroyed
        if (defenders):
            for b in self.__battalions.values():
                for bb in b.battalions:
                    if (not bb.IsDefeated()):
                        return False
        
        else:
            # For the attackers army when all battalions that can enter into the castle (infantry, siegetowers) are defeated, the game ends
            # If none of them exists anymore, the archers and cannons could kill all defenders, and it would be a true attacker victory. But this situation can fall in a deadlock
            # where the archers try to reach any target around the castle shape. So, we consider the filter as an acceptable simplification
            
            if (self.__battalions.has_key("Infantry") and self.__battalions["Infantry"] != None):
                if (self.__battalions["Infantry"].battalions):
                    return False
                
            if (self.__battalions.has_key("SiegeTowers") and self.__battalions["SiegeTowers"] != None):
                if (self.__battalions["SiegeTowers"].battalions):
                    return False
        
        return True



    def Respawn(self, died):
        # Respawn given died unit from the reserved ones (those defined battalions that are not yet deployed)
        # Returns false if there are no more avaiable units
        
        factory = ArmyFactory()
        kind = factory.GetArmyType(died)
        if (self.__battalions.has_key(kind)):
            bt = self.__battalions[kind]
            
            if (bt.freenumber > 0):
                bt.freenumber -= 1
                self.__battalions[kind] = bt
        
                return True
        
        return False

  
    def GetClosestBattalionInAttackRange(self, posfrom, castle, action, excludeConstruction, battaliontype = None):
        # Returns the closest battalion to posfrom 3D position. The attack range is checked with action parameter (the battalion that wants to attack)
        # excludeConstruction is used to exclude the intersection with given castle construction part. This is usefull to check the attack range of castle soldiers
        # Only those battalions that are fighting on the battlefield are considered
        # battaliontype specifies the type of battalion to search. None means any kind of battalion
        
        
        mindist = -1
        closest = None
        
        batdatalst = []
        if ((not battaliontype) or (not self.__battalions.has_key(battaliontype))):
            batdatalst.extend(self.__battalions.values())
        else:
            batdatalst.append(self.__battalions[battaliontype])
        
        for b in batdatalst:
            for bb in b.battalions:
                if (not bb.IsDefeated()):       # Be aware. Due this method can be called meanwhile a battalion is killed, we have to check if they are defeated
                    if (bb.IsInBattleField()):
                        center = bb.GetCenterPosition()
                        if (center == None):
                            print ("ERROR: GetClosestBattalionInAttackRange -> None battalion position")
                            continue
                        #if (action.InAttackRange(currPos = posfrom, targetPos = center, castle = castle, constructionTarget = None)):
                        # InAttackRange is a heavy cost time method. So, call it only when is necessary -> This converts Distance method into a really many times called method
                        # Check the closest condition
                        if (closest == None):
                            if (action.InAttackRange(currPos = posfrom, targetPos = center, castle = castle, constructionTarget = None, excludeConstruction = excludeConstruction)):
                                closest = bb
                                mindist = posfrom.Distance(center)
                        else:
                            #dist = posfrom.Distance(center)
                            dist = math.sqrt(((posfrom.x - center.x)**2) + ((posfrom.y - center.y)**2) + ((posfrom.z - center.z)**2))
                            if (dist < mindist):
                                if (action.InAttackRange(currPos = posfrom, targetPos = center, castle = castle, constructionTarget = None, excludeConstruction = excludeConstruction)):
                                    mindist = dist
                                    closest = bb
        
        return closest
        
        
        
    def GetBestTurtleBattalion(self, target, siegetowerpos, castle):
        # Returns the best battalion to be converted to a siege tower turtle
        # Return the closest battalion to given moat target position and siegetower position. The later condition helps to get a good battalion placement if the avaiable
        # battallions are too far from the siege tower (helping to get a more straight path to the goal)
        # Only those battalions that the path from their positions and target dont intersect with the castle, are considered
        
        minDist = -1
        closest = None
        
        b = self.__battalions["Infantry"]
        if (b == None):
            return None
        else:
            for bb in b.battalions:
                if (not bb.IsDefeated()):       # Be aware. Due this method can be called meanwhile a battalion is killed, we have to check if they are defeated
                    com = bb.GetCommand()
                    if (com.IsMove() and not com.IsCoverMoat()):
                        center = bb.GetCenterPosition()
                        dist = center.Distance(target)
                        
                        # Check if turtle path to target intersects the castle (so the turtle is stupid and cannot take a good path avoiding obstacles ..., yeah, another one TODO)
                        ray = Ray(origin = center, direction = Vector3D().CreateFrom2Points(center, target))
                        if (not castle.RayHitTest_Closest(ray = ray, exclude = None, distance = dist)):
                            
                            dist2 = center.Distance(siegetowerpos)
                            d = dist + dist2
                            if ((closest == None) or (d < minDist)):
                                minDist = d
                                closest = bb
 
        return closest



    def ExtractSoldier(self, battalion):
        # Extracts one soldier from given battalion and convert it to a battalion of 1 soldier. Then updates battalion lists
        # Returns the extracted soldier/battalion
        
        if (battalion.GetNumber() <= 0):
            return None
        
        if (battalion.GetNumber() == 1):
            return battalion
        
        factory = Factory.ArmyFactory()
        kind = factory.GetArmyType(battalion)
        
        b = battalion.GetCopy()
        b.SetNumber(1)
        battalion.SetNumber(battalion.GetNumber() - 1)
        
        self.__battalions[kind].battalions.append(b)
              
        return b
    
    
    


    # DEPRECATED!!!!
    def BreakRanks(self, battalion, storenew): 
        # Break ranks of given battalion. All units on battalion will be converted into new battalions of only 1 unit
        # Given battalion is reused as a new battalion
        # The list of new battalion is returned
        # If storenew is true, the new created battalions will be stored in the army
        
        lst = []
        
        factory = Factory.ArmyFactory()
        kind = factory.GetArmyType(battalion)
       
        i = 0
        while (i < (battalion.GetNumber() - 1)):
            b = battalion.GetCopy()
            b.SetNumber(1)

            # Be aware not use the usual methods to add and deploy battalions, so they use internal counters about free remain troops
            if (storenew):
                self.__battalions[kind].battalions.append(b)
            
            lst.append(b)
            
            i += 1

        battalion.SetNumber(1)
        #self.__battalions[kind].battalions.append(battalion)
        
        lst.append(battalion)

        return lst




def GetArmyComponentSize(armycomp):
    """ Function used to sort army components by his length
    """
    return armycomp.GetBounding().length







        