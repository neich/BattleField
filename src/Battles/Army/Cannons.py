from Battles.Army import Action , Battalion  
from Battles.Utils.Geometry import Bounding
from Battles.Game.Board import Shoot, Board
from Battles.Utils.Message import Log
import Battles.Utils.Settings 
import b3
 
       

"""
###############################################################################
# Attack nodes!
##############################################################################
"""
class Attack (b3.BaseNode):
    def tick(self, tick):
#    def Attack(self, against, castle, shoots):
        #print "###############################"
        #print "moving from Move node",
        #print "###############################"
        # cannons defend (from castle)
        battalion = tick.target
        castle = tick.blackboard.get('castle', tick.tree.id, None)
        #battalionarmy = tick.blackboard.get('battalionarmy', tick.tree.id, None)
        #againstarmy = tick.blackboard.get('against', tick.tree.id, None)
        #battlefield = tick.blackboard.get('battlefield', tick.tree.id, None)
        #movedList = tick.blackboard.get('movedList', tick.tree.id, None)
        shots = tick.blackboard.get('shots', tick.tree.id, None)
        
        # Cannons attack
        # Against parameter is not used here, only the castle
        # Return a list of shoot lines to be displayed
        
        #Army.ArmyComponent.Attack(battalion, against, castle, shoots)
        if (battalion.IsDefeated()):
            return b3.FAILURE
        
        if (not battalion._action.GetCommand().IsAttack()):
            return b3.FAILURE
        
        if (not battalion._placement.IsInBattlefield()):
            print 'ERROR: Current cannon battalion is not placed on battlefield'
            return b3.FAILURE
                
        # cannons have to fire against castle troops
        
        
        # Check if they are ready to shoot
        if (not battalion._action.IsReloadReady()):
            battalion._action.UpdateReloadTime()
            Log('%s reloading ...' % (battalion.GetLabel()))
            return b3.FAILURE
        battalion._action.UpdateReloadTime()
        
        
        if (castle.IsDefeated()):
            # Game end? ...
            return b3.FAILURE
        
        # Simple attack mode
        
        # Get battalion simple position to calculate an estimated distance to closest construction element
        pos = battalion._placement.GetCenterPosition()

        # Get closest construction element (with or without troops). The goal must be reachable because the goal of a cannon is to make a gateway to allow attackers enter inside the castle
        target = castle.GetClosestConstruction(populated = False, posfrom = pos, tilesrequired = True, reachable = True)
        if (target == None):
            # Game end?... no castle?... amazing!
            return b3.FAILURE
         
        # Shoot one time for each battalion cannon
        i = 0
        while (i < battalion._number):
            # Get center battle field cell position (a cannon cannot move randomly as a soldier)

            tilemanager = target.GetTileManager()

            # Get the most suitable construction tile to shoot
            # Returned target is a dictionary with tile row and column values
            tile = tilemanager.GetBestTileToShoot(pos)
            if (tile == None):
                print 'ERROR: Cannon cannot choose a fallen wall!'
                return b3.FAILURE
                
            
            # Get central tile position as reference
            targetpos = tilemanager.GetTileCenter(tile)

             
            # Calculate the shoot success
            
            # If the target is too far, the cannon doesn't shoot (or he's idiot ...)
            if (battalion._action.InAttackRange(currPos = pos, targetPos = targetpos, castle = castle, constructionTarget = target)): 
                
                hitpoint = battalion._action.ShootToConstruction(target, pos, targetpos)
                if (hitpoint["Hit"]):                    
                    Log('%s hits on construction %s' % (battalion.GetLabel(), target.GetLabel()))
                    
                    if (target.IsDefeated()):
                        # End game?
                        Log('The %s has fallen!!!' % (target.GetLabel()))
                        return b3.FAILURE
                    
                    # Check if tile is broken and it is the first one (the top tile), killing all defenders that are on top
                    if (tilemanager.IsTopTile(tile) and tile.IsHole()):
                        defenders = target.GetDefendersOverTile(tile)                        
                        for d in defenders:
                            d.Kill(-1)  # Kill whole battalion and avoid the respawn
                            # Update the drawing of defeated defenders
                            Board.redrawObjects.append(d)
                        
                    
                    
                    if (shots != None):
                        # Store the shoot
                        s = Shoot(origin = pos, destination = hitpoint["Intersection"], success = hitpoint["Hit"], attackertype = "Cannons", targetObj = target, armytype = Shoot.SHOOT_FROM_ATTACKER)
                        shots.append(s)
                
      
            i += 1
        return b3.SUCCESS
   
"""
###############################################################################
# Defend nodes!
##############################################################################
"""
class Defend (b3.BaseNode):
    def tick(self, tick):
        #print "###############################"
        #print "moving from Move node",
        #print "###############################"
        # cannons defend (from castle)
        battalion = tick.target
        castle = tick.blackboard.get('castle', tick.tree.id, None)
        #battalionarmy = tick.blackboard.get('battalionarmy', tick.tree.id, None)
        againstarmy = tick.blackboard.get('against', tick.tree.id, None)
        battlefield = tick.blackboard.get('battlefield', tick.tree.id, None)
        #movedList = tick.blackboard.get('movedList', tick.tree.id, None)
        shots = tick.blackboard.get('shots', tick.tree.id, None)
        
#    def Defend(battalion, against, defenders, battlefield, shoots, castle): they shoot shots 
        # Cannons defend (from castle)
        
        if (battalion.IsDefeated()):
            return b3.FAILURE
        
        if (not battalion._action.GetCommand().IsDefend()):
            return b3.FAILURE
        
        if (not battalion._placement.IsInDefendingLine()):
            print 'ERROR: Current cannon  is not placed on a defending line'
            return b3.FAILURE

        # Cannons have to fire against battlefield troops
        
        # Check if they are ready to shoot
        if (not battalion._action.IsReloadReady()):
            battalion._action.UpdateReloadTime()
            Log('%s reloading ...' % (battalion.GetLabel()))
            return b3.FAILURE
        battalion._action.UpdateReloadTime()
        
        # Simple defend mode
        
        # Get battalion simple position to calculate an estimated distance to closest construction element
        pos = battalion._placement.GetCenterPosition()
        
        # Get the most suitable battalion to shoot.
        
        # Get the closest enemy battalion
        # Cannons have a priority on targets: cannons, cannons and infantry/cannons
        target = againstarmy.GetClosestBattalionInAttackRange(posfrom = pos, castle = castle, action = battalion._action, excludeConstruction = battalion._placement.GetDefendingConstruction(), battaliontype = "Cannons") 
        if (not target):
            target = againstarmy.GetClosestBattalionInAttackRange(posfrom = pos, castle = castle, action = battalion._action, excludeConstruction = battalion._placement.GetDefendingConstruction(), battaliontype = "cannons") 
            if (not target):
                target = againstarmy.GetClosestBattalionInAttackRange(posfrom = pos, castle = castle, action = battalion._action, excludeConstruction = battalion._placement.GetDefendingConstruction(), battaliontype = None) 
                if (not target):
                    return b3.FAILURE

        # Shoot as many times as troops number
        i = 0
        while (i < battalion._number):
            
            # Get the most suitable point to attack
            cpos = target._placement.GetRandomPosition()
        
            
            # Calculate the shoot success
            
            # If the target is too far or the attack angle is too graze, the cannon doesn't shoot (or he's idiot ...)
            # The range attack is checked before, but with cell central points. That is, the cannon first search the most suitable battalion to shoot. Then some
            # random data is take into account with real positions on cells. This could succeed with a shoot fail.
            doublecheck = False
            if (Battles.Utils.Settings.SETTINGS.Get_B('Army','Cannons','DefenseShootDoubleCheck')):
                doublecheck = battalion._action.InAttackRange(currPos = pos, targetPos = cpos, castle = castle, constructionTarget = None, excludeConstruction = battalion._placement.GetDefendingConstruction())
            if ((not Battles.Utils.Settings.SETTINGS.Get_B('Army','Cannons','DefenseShootDoubleCheck')) or (Battles.Utils.Settings.SETTINGS.Get_B('Army','Cannons','DefenseShootDoubleCheck') and doublecheck)): 
                
                hit = False
                finaltarget = target
                hitpos = cpos
                
                hitsuccess = battalion._action.ShootToBattlefield(battlefield, pos, cpos)
                if (hitsuccess["Hit"]):
                    
                    hit = True
                    finaltarget = hitsuccess["Battalion"]   # Final shooted target could be another than initial target for aiming reasons
                    if (finaltarget.IsDefeated()):
                        againstarmy.RemoveBattalion(finaltarget)
                    
                    
                    """
                    # This will happens ever.... if the battlefield isnt a stamp, obviously....
                    # We need to check if the shoot has hit on anyone (perhaps, not the target, but another victim ....)
                    
                    if (hitsuccess["Cell"].HasBattalion()):
                        
                        
                        # We need to know how many soldiers have been killed
                        # Take in consideration that all battalion is affected. Then, each soldier will pass a test between his defensive value and cannon attack value, in weighted random way
                        finaltarget = hitsuccess["Cell"].GetBattalion()
                        j = 0
                        k = 0 
                        while (j < finaltarget.GetNumber()):
                            if (battalion._action.ShootDuel(finaltarget)):
                                
                                if (not hit):
                                    hit = True
                                    hitpos = hitsuccess["Intersection"]

                                k += 1
                            j += 1
                    
                        finaltarget.Kill(k)
                        if (finaltarget.IsDefeated()):
                            against.RemoveBattalion(finaltarget)
                            
                      """      
       
                if (shots != None):
                    # Store the shoot
                    s = Shoot(origin = pos, destination = hitpos, success = hit, attackertype = "Cannons", targetObj = finaltarget, armytype = Shoot.SHOOT_FROM_DEFENDER)
                    shots.append(s)
                
                
                # Check if battalion is defeated and get another one (check it here to allow storing the shoot)
                # Note that we could be killed another target. Here we check if we need to aim to another target
                if (target.IsDefeated()):
                    target = againstarmy.GetClosestBattalionInAttackRange(posfrom = pos, castle = castle, action = battalion._action, excludeConstruction = battalion._placement.GetDefendingConstruction(), battaliontype = "Cannons") 
                    if (not target):
                        target = againstarmy.GetClosestBattalionInAttackRange(posfrom = pos, castle = castle, action = battalion._action, excludeConstruction = battalion._placement.GetDefendingConstruction(), battaliontype = "cannons") 
                        if (not target):
                            target = againstarmy.GetClosestBattalionInAttackRange(posfrom = pos, castle = castle, action = battalion._action, excludeConstruction = battalion._placement.GetDefendingConstruction(), battaliontype = None) 
                            if (not target):
                                return b3.FAILURE
       
            i += 1
        return b3.SUCCESS

"""
 ##############################################################################
 #
 #   cannon Trees !!!
 #
 ##############################################################################

"""
def createTree():
    global cannonAttackingTree
    cannonAttackingTree = b3.BehaviorTree()
    cannonAttackingTree.id = 'cannonAttackingTree'
    node1 = b3.Sequence([
        Attack()
        ])
    cannonAttackingTree.root = node1

    global cannonDefendingTree
    cannonDefendingTree = b3.BehaviorTree()
    cannonDefendingTree.id = 'cannonDefendingTree'
    node2 = b3.Sequence([
        Defend()
        ])
    cannonDefendingTree.root = node2

#     global cannonMovingTree
#     cannonMovingTree = b3.BehaviorTree()
#     cannonMovingTree.id = 'cannonMovingTree'
#     node3 = b3.Sequence([
#         Move()
#         ])
#     cannonMovingTree.root = node3
 
    resetBlackboard()

def resetBlackboard():
    global cannonBlackboards
    cannonBlackboards = {}
    #print "cannons's tree created!!!"


"""
 ##############################################################################
 #
 #   Cannons !!!
 #
 ##############################################################################
 
""" 
class Cannons(Battalion.Battalion):     
    """ Cannons artillery battalion. They can attack walls and towers
    """
    
    cannonsCounter = 0     # Internal counter for labeling purposes
    
    def __init__(self, army, number = 0):
        Battalion.Battalion.__init__(self, army = army, number = number)
        self._action = Action.ActionFeatures(defense = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Cannons', 'Defense'), 
                                             attack = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Cannons', 'Attack'), 
                                             speed = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Cannons', 'Speed'), 
                                             reloadspeed = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Cannons', 'Reload'), 
                                             accuracy = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Cannons', 'Accuracy'), 
                                             distance = Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Cannons', 'Distance'), 
                                             stationary = Battles.Utils.Settings.SETTINGS.Get_B('Army', 'Cannons', 'Stationary'),
                                             movementpriority = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Cannons', 'MovementPriority'))
        self._bounding = Bounding(Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Cannons', 'Bounding/Length'), 
                                  Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Cannons', 'Bounding/Width'), 
                                  Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Cannons', 'Bounding/Height'))
        self._label = "Cannons_" + str(Cannons.cannonsCounter)
        Cannons.cannonsCounter += 1
        # print 'Cannons ->', Cannons.cannonsCounter
        blackboard = b3.Blackboard()
        cannonBlackboards[self._label] = blackboard

        
    @classmethod
    def ResetCounter(cls):
        cls.cannonsCounter = 0        
        


#     def GetCopy(self):
#         ret = Battalion.Battalion.GetCopy(self)
#         if (ret == None):
#             return None
#         
#         #ret._label = "Cannons_" + str(Cannons.cannonsCounter)
#         #Cannons.cannonsCounter += 1
# 
#         return ret



    def SetAttackVector(self, direction, angle):
        # Sets the shoot vector restrictions from construction where it is deployed.
        # But for cannons, check if construction restrictions are less restrictive than cannon restrictions
        
        h = Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Cannons', 'ShootAngle/H')
        v = Battles.Utils.Settings.SETTINGS.Get_A('Army', 'Cannons', 'ShootAngle/V')
        
        if (angle['H'] < h):
            h = angle['H']
        
        if (angle['V']['bottom'] < v[0]):
            v[0] = angle['V']['bottom']
            
        if (angle['V']['top'] < v[1]):
            v[1] = angle['V']['top']
           
        
        self._action.SetAttackVector(direction, {'H': h, 'V': {'bottom': v[0], 'top': v[1]}})    


    def GetSuitableDeploymentDistance(self):
        # Returns the suitable distance to place the cannon from the wall
        return Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Cannons', 'DefaultPlacementDistance') * self._action.GetDistance()

 
    def Attack(self, against, castle, shots):
        #print "###################### Attack!!!", self.GetCommand().GetType()
        myBlackboard = cannonBlackboards[self._label]
        myBlackboard.set('against', against, cannonAttackingTree.id, None)
        myBlackboard.set('shots', shots, cannonAttackingTree.id, None)
        myBlackboard.set('castle', castle, cannonAttackingTree.id, None)
        myBlackboard.set('command', self.GetCommand().GetType(), cannonAttackingTree.id, None)
        cannonAttackingTree.tick(self, myBlackboard)
        return


    def Defend(self, against, defenders, battlefield, shots, castle):
        #print "Defend tree.id", cannonDefendingTree.id
        myBlackboard = cannonBlackboards[self._label]
        myBlackboard.set('against', against, cannonDefendingTree.id, None)
        myBlackboard.set('battlefield', battlefield, cannonDefendingTree.id, None)
        myBlackboard.set('shots', shots, cannonDefendingTree.id, None)
        myBlackboard.set('castle', castle, cannonDefendingTree.id, None)
        myBlackboard.set('command', self.GetCommand().GetType(), cannonDefendingTree.id, None)
        cannonDefendingTree.tick(self, myBlackboard)
        return

if __name__ != "__main__":
    createTree()
