from Battles.Army import Action, Battalion  
from Battles.Utils.Geometry import Bounding, Point2D
from Battles.Game.Board import Shoot, Board
from Battles.Factory import ArmyFactory
import Battles.Utils.Settings 
import b3

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
        #castle = tick.blackboard.get('castle', tick.tree.id, None)
        #selfarmy = tick.blackboard.get('selfarmy', tick.tree.id, None)
        againstarmy = tick.blackboard.get('against', tick.tree.id, None)
        #battlefield = tick.blackboard.get('battlefield', tick.tree.id, None)
        #movedList = tick.blackboard.get('movedList', tick.tree.id, None)
        shots = tick.blackboard.get('shots', tick.tree.id, None)
        
#    def Defend(battalion, against, defenders,  battlefield, shoots, castle):
        
        if (battalion.IsDefeated()):
            return
        
        if (battalion._stair.IsDefeated()):     # This is a final stage check to know if the throwers must be dissolved, that is when there are not more climbers
            battalion.Dissolve()                 # Due the dissolve can be produced for many reasons, and its difficult to control all messages between all implied battalions
                                            # and structures, we place here this final update
            return                              
        
        if (not battalion._action.GetCommand().IsTrhowing()):
            return 
        
        if (not battalion._placement.IsInDefendingLine()):
            print 'ERROR: Current throwers battalion is not placed on a defending line'
            return 

        
        # Check if they are ready to throw
        # Note that we update the reload time in SetNumber and Kill method
        if (not battalion._action.IsReloadReady()):
            battalion._action.UpdateReloadTime()
            return 
        battalion._action.UpdateReloadTime()

        # The attack is directed to the stair climbers, without searching the nearest target        
        # The damage value is THROWERS_ATTACK / (distance * THORWERS_DISTANCE)        
        # In addition, each climber try to defense using his defense value, like usual attack procedure
        
        frompos = battalion.GetCenterPosition()
        
        # Attack each climbing battalion
        climbers = battalion._stair.GetClimbers()   # Note that this climbers list dont are the full units on the stair, so there can be others waiting to start climbing

        i = 0
        while (len(climbers) > i):
            target = climbers[i]  

            distance = frompos.z - target.GetCenterPosition().z
            distfact = Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Throwers', 'Distance') * distance
            if (distfact == 0):
                attack = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Throwers', 'Attack')
            else:
                attack = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Throwers', 'Attack') / distfact
            
            if (battalion._action.Shoot(attack, target.GetDefenseVal())):
                # Kills one element
                hit = True
                target.Kill(1)
                if (target.IsDefeated()):
                    againstarmy.RemoveBattalion(target)
 
            else: 
                hit = False
                i += 1
  
            # The shoot wont be drawn due the difficulty on showing the shoot in height view (we should have the height view at this point), 
            # we use the square-fill method (see DrawHeightView method). By other hand, store the shoot to allow the redrawing of attacked unit
         
            if (shots != None):
                # Store the shoot
                s = Shoot(origin = frompos, destination = target.GetCenterPosition(), success = hit, attackertype = "Throwers", targetObj = target, armytype = Shoot.SHOOT_FROM_DEFENDER)
                shots.append(s)
          
                # If the stair is defeated, the battalion will dissolve itbattalion. Then, we need to clear the 2D battalion shape
                if (battalion._stair.IsDefeated()):
                    s2 = Shoot(origin = frompos, destination = target.GetCenterPosition(), success = hit, attackertype = "Throwers", targetObj = battalion, armytype = Shoot.SHOOT_FROM_DEFENDER)
                    shots.append(s2)
                    
                    # In addition, at this point new battalions have been created because the thrower has been dissolved. To allow the redraw, include them as attacked
                    # TODO: Clear this fucking patch and create a nice redraw system for any object
                    
                    for b in battalion._dissolvedBattalions:
                        sb = Shoot(origin = frompos, destination = target.GetCenterPosition(), success = hit, attackertype = "Throwers", targetObj = b, armytype = Shoot.SHOOT_FROM_DEFENDER)
                        shots.append(sb)

                    battalion._dissolvedBattalions = []
             



"""
 ##############################################################################
 #
 #   cannon Trees !!!
 #
 ##############################################################################

"""
def createTree():
#     global throwerAttackingTree
#     throwerAttackingTree = b3.BehaviorTree()
#     throwerAttackingTree.id = 'throwerAttackingTree'
#     node1 = b3.Sequence([
#         Attack()
#         ])
#     throwerAttackingTree.root = node1

    global throwerDefendingTree
    throwerDefendingTree = b3.BehaviorTree()
    throwerDefendingTree.id = 'throwerDefendingTree'
    node2 = b3.Sequence([
        Defend()
        ])
    throwerDefendingTree.root = node2

#     global cannonMovingTree
#     cannonMovingTree = b3.BehaviorTree()
#     cannonMovingTree.id = 'cannonMovingTree'
#     node3 = b3.Sequence([
#         Move()
#         ])
#     cannonMovingTree.root = node3
 
    resetBlackboard()


def resetBlackboard():
    global throwerBlackboards
    throwerBlackboards = {}
    #print "Thrower's tree created!!!"


"""
 ##############################################################################
 #
 #   Throwers !!!
 #
 ##############################################################################
 
""" 
class Throwers(Battalion.Battalion):
    
    """
        Battalion with the duty of throw "things" from top of walls to climber attackers
        This kind of battalion is created when a stair is placed on a wall and a set of attackers start to climb on it
        To create it a small set of closest soldiers/battalions are joined to create this new unit
        It can throw things after some time
        When the climbers are defeated, the battalion is dissolved
        The battalion can be attacked, like others. For each hit, one soldier falls. This increases the time for throwing
        
    Attributes:
    
        stair: Stair to attack    
        dissolvedBattalions: Helper list to store temporally the new created battalions when thrower is dissolved and redraw them    
    """
    
    throwersCounter = 0
    
    def __init__(self, army, number = 0):
        Battalion.Battalion.__init__(self, army = army, number = number)
        self._action = Action.ActionFeatures(defense = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Throwers', 'Defense'), 
                                             attack = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Throwers', 'Attack'), 
                                             speed = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Throwers', 'Speed'), 
                                             reloadspeed = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Throwers', 'Reload'), 
                                             accuracy = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Throwers', 'Accuracy'), 
                                             distance = Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Throwers', 'Distance'),
                                             stationary = Battles.Utils.Settings.SETTINGS.Get_B('Army', 'Throwers', 'Stationary'),
                                             movementpriority = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Throwers', 'MovementPriority'))
        self._bounding = Bounding(Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Throwers', 'Bounding/Length'), 
                                  Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Throwers', 'Bounding/Width'), 
                                  Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Throwers', 'Bounding/Height'))
        self._label = "Throwers_" + str(Throwers.throwersCounter)
        Throwers.throwersCounter += 1
        # print 'Throwers ->', Throwers.throwersCounter
        
        self._action.SetInitialReload(False)
        
        self._stair = None
        
        self._dissolvedBattalions = []
        blackboard = b3.Blackboard()
        throwerBlackboards[self._label] = blackboard
        
    @classmethod    
    def ResetCounter(cls):
        cls.archersCounter = 0        
        


    def GetCopy(self):
        ret = Battalion.Battalion.GetCopy(self)
        if (ret == None):
            return None
        
        ret._label = "Throwers_" + str(Throwers.throwersCounter)
        Throwers.throwersCounter += 1

        return ret
    
    
    def SetNumber(self, n):
        Battalion.Battalion.SetNumber(self, n)
        
        # The bounding depend on the number of units in the battalion.
        # All of them are converted archers
        self._bounding.length = Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Archers', 'Bounding/Length') * n
        self._bounding.width = Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Archers', 'Bounding/Width')
        
        self.UpdateReloadTime()
        
        
        
    def UpdateReloadTime(self):    
        # Update the reload time from the battalion size
        if (self._number > 0):
            size = self._number
        else:
            size = 1
        self._action.SetReloadTime(self._action.GetReloadTime() / size)
        
        
        
    def SetStair(self, s):
        self._stair = s
    
    
    def Dissolve(self):
        # Dissolve current battalion. All remaining troops are converted into archers battalions again, and replaced in the wall
        
        factory = ArmyFactory()
        
        army = self._stair.GetDefendersArmy()
        

        construction = self._stair.GetConstruction()
        index_dl = self._placement.GetDefendingLine()
        defendingline = construction.GetDefendingLine(index_dl)
        
        # get the most suitable new positions for the dissolved battalions
        lstpos = defendingline.GetSubPositions(center = self.GetCenterPosition(), number = self.GetNumber(), bounding = self.GetBounding())
        
        # Creates the archers battalions and reassign them to the wall defending positions
        i = 0
        while ( i < self._number):
            
            b = factory.newBattalionNoCrop(army = army, kind = "Archers")
            army.InsertBattalion(battalion = b, updatecounters = False)            
            b.SetNumber(1)
            
            b.SetCommand(command = Action.Command.DEFEND_CASTLE)
            defendingline.InsertBattalion(b, lstpos[i])
            b.AssignToConstruction(construction, index_dl)
            
            self._dissolvedBattalions.append(b)
            Board.redrawObjects.append(b)
            
            
            i += 1
        
        # Remove the battalion 
        army.RemoveBattalion(self)
        #defendingline.RemoveBattalion(self)
        
        Board.redrawObjects.append(self)
        
        
        
        
        
    def Kill(self, number, respawn = False):
        # Kill current thrower
        # Respawn is only allowed for defender archers

        Battalion.Battalion.Kill(self, number, respawn)      # Battalion.Kill method calls SetNumber method, so the reload time is updated
        
        self.UpdateReloadTime()          # Reload time is calculated from the number of units in the thrower battalion
        
        if (self.IsDefeated()):
            self._stair.SetThrowers(None)
            
        
    def Defend(self, against, defenders, battlefield, shots, castle):
        #print "Defend tree.id", cannonDefendingTree.id
        myBlackboard = throwerBlackboards[self._label]
        myBlackboard.set('against', against, throwerDefendingTree.id, None)
        #myBlackboard.set('battlefield', battlefield, throwerDefendingTree.id, None)
        myBlackboard.set('shots', shots, throwerDefendingTree.id, None)
        #myBlackboard.set('castle', castle, throwerDefendingTree.id, None)
        myBlackboard.set('command', self.GetCommand().GetType(), throwerDefendingTree.id, None)
        throwerDefendingTree.tick(self, myBlackboard)
        return
        
        
    def DrawHeightView(self, canvas, viewport, position):
        # Draw the battalion in height view. Draw an empty rectangle, and fills it with the remaining reload time (max reload time means empty rectangle)
        # Given position is the center of battalion
        # Returns the canvas object
        
        ret = []
        
            
        
        # Draw the empty battalion bounding rectangle
        p1 = Point2D(position.x - (self.GetBounding().length / 2.0), position.y) 
        p2 = Point2D(position.x + (self.GetBounding().length / 2.0), position.y - self.GetBounding().height)
        pp1 = viewport.W2V(p1)
        pp2 = viewport.W2V(p2)
        
        if (self._action.IsReloadReady()):
            # The battalion is going to attack, so it must be shown as a filed rectangle at 100%
            ret.append(canvas.create_rectangle(pp1.x, pp1.y, pp2.x, pp2.y, fill="DarkBlue", outline="gray"))
        else:
            ret.append(canvas.create_rectangle(pp1.x, pp1.y, pp2.x, pp2.y, fill=None, outline="gray"))
    
            # Draw the filled rectangle from the reload remaining time
            remain = self._action.GetReloadRemainingTime(percentage = True, nextt = False)        
            p2 = Point2D(position.x + (self.GetBounding().length / 2.0), (position.y - self.GetBounding().height) * (remain))
            pp2 = viewport.W2V(p2)
            ret.append(canvas.create_rectangle(pp1.x, pp1.y, pp2.x, pp2.y, fill="DarkBlue", outline="gray"))

        return ret


if __name__ != "__main__":
    createTree()
