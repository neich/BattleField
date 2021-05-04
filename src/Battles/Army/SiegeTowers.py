from Battles.Army import Action , Battalion  
from Battles.Utils.Geometry import Bounding
from Battles.Game.Board import Shoot
from Battles.Utils.Message import Log
from Battles.Army.Action import Command
import Battles.Utils.Settings   
import b3
  

"""
###############################################################################
# Move nodes!
##############################################################################
"""
class IsNotDefeated (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        #castle = tick.blackboard.get('castle', tick.tree.id, None)
        selfarmy = tick.blackboard.get('selfarmy', tick.tree.id, None)
        #againstarmy = tick.blackboard.get('against', tick.tree.id, None)
        #battlefield = tick.blackboard.get('battlefield', tick.tree.id, None)
        #movedList = tick.blackboard.get('movedList', tick.tree.id, None)

        if (battalion.IsDefeated()):
            print "################################ Siege Tower Defeated!!!"
            selfarmy.RemoveBattalion(battalion)
            return b3.FAILURE
        return b3.SUCCESS

class HasValidPath (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        #castle = tick.blackboard.get('castle', tick.tree.id, None)
        selfarmy = tick.blackboard.get('selfarmy', tick.tree.id, None)
        #againstarmy = tick.blackboard.get('against', tick.tree.id, None)
        #battlefield = tick.blackboard.get('battlefield', tick.tree.id, None)
        #movedList = tick.blackboard.get('movedList', tick.tree.id, None)

        if (len(battalion._path) == 0):
            # This should never happen. The only explanation is a wrong initial path calculation in a weird situation that I cannot understand (the path calculation
            # controls when resulting path is empty or null, and choose another one. See Battlefield.DeploySiegeTowersOnCenteredLine)
            # Just as a precaution, if this happens take the drastic action of killing this unit (aka, doing suicide by stupidy calculating a simple path ....)
            print "WARNING: A crazy siege tower has a null path. Suiciding it (no glory)"
            battalion.Kill(1)
            selfarmy.RemoveBattalion(battalion)
            return b3.FAILURE
        return b3.SUCCESS

class UpdateConstructionStatus (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        #castle = tick.blackboard.get('castle', tick.tree.id, None)
        #selfarmy = tick.blackboard.get('selfarmy', tick.tree.id, None)
        #againstarmy = tick.blackboard.get('against', tick.tree.id, None)
        #battlefield = tick.blackboard.get('battlefield', tick.tree.id, None)
        #movedList = tick.blackboard.get('movedList', tick.tree.id, None)

        if (battalion._status == SiegeTowers.CONSTRUCTING):
            # The tower is constructing. Wait to move it until the construction is done
            battalion._constructionStatus += 1
            if (battalion._constructionStatus >= (Battles.Utils.Settings.SETTINGS.Get_I('Army', 'SiegeTowers', 'ConstructionTimePerLevel') * battalion._nLevels)):            
                # The path is clear. Move the tower when it is ready
                battalion._status = SiegeTowers.MOVING
        return b3.SUCCESS

class HasMoat(b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        if (battalion._moatCells):
            return b3.SUCCESS
        else:
            return b3.FAILURE

class HasTurtle(b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        if (battalion._turtle):
            return b3.SUCCESS
        else:
            return b3.FAILURE

class CreateTurtle(b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        castle = tick.blackboard.get('castle', tick.tree.id, None)
        battalion.CreateTurtle(castle)  # If the turtle creation failed previously, try again. The unavailable condition could change if any battalion receives a change of command
        return b3.SUCCESS

class HandleTurtle (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        #castle = tick.blackboard.get('castle', tick.tree.id, None)
        #selfarmy = tick.blackboard.get('selfarmy', tick.tree.id, None)
        #againstarmy = tick.blackboard.get('against', tick.tree.id, None)
        #battlefield = tick.blackboard.get('battlefield', tick.tree.id, None)
        movedList = tick.blackboard.get('movedList', tick.tree.id, None)
            
        # The turtle moves independently
        
        # If there aren't enough available battalions, the turtle wont be created after CreateTurtle call
        # If turtle is already in a moat, increase the covering progress
        cell = battalion._turtle._placement.GetBattlefieldCell()
        if ((cell != None) and cell.HasMoat()):
            battalion._coverMoatHeight += (Battles.Utils.Settings.SETTINGS.Get_F('Army', 'SiegeTowers', 'CoverMoatSpeed') * battalion._turtle.GetNumber())
            
            if (battalion._coverMoatHeight >= cell.GetMoat().GetDepth()):
                # When moat is covered, go the next one
                
                if (movedList):
                    movedList.append(cell)
                    movedList.append(battalion._turtle)
                # moat = cell.GetMoat()
                cell.RemoveMoat()
                battalion._moatCells = battalion._moatCells[1:]
                battalion._coverMoatHeight = 0

                # Stop covering the moat if turtle has achieved the path end or any castle wall
                # In addition, stops too when next cell does not have moat. This is a strange case that can happens due precision problems
                # calculating the turtle path
                if ((not battalion._moatCells) or cell.HasConstructions() or ((len(battalion._moatCells) > 0) and not cell.HasMoat())):
                    # Deprecated
                    # The turtle has finished the main task of clearing the siege tower path. Now, it can clear other moat parts
                    # To do it, search the nearest moat cell and insert in in pathMoat list. This way we can reuse the code of covering moat
                    # nextcell = moat.GetClosestMoatCell(cell.center)
                    # battalion._moatCells.append(nextcell)
                    
                    # Convert the battalion to a simple infantry one and command it to climb the siege tower targeted wall
                    battalion._turtle.SetCommand(command=Command.GOTO_CASTLE, target=cell, commander=battalion)
                    battalion._turtle.SetDefense(Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Infantry', 'Defense'))
                    battalion._turtle = None
                else:                
                    battalion._turtle.SetCommand(command=Command.COVER_MOAT, target=battalion._moatCells[0], commander=battalion)    
        # Move the turtle
        # Well, in fact, dont do anything, so as army member, the turtle will be moved on the overall process of moving troops
        return b3.SUCCESS

class ReadyToMove (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        # Move the tower when it is constructed        
        if ((battalion._status == SiegeTowers.MOVING) and (battalion._action.GetCommand().IsMove())):
            return b3.SUCCESS
        else:
            return b3.FAILURE
                
class SelectNextCell (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        cell = battalion._placement.GetBattlefieldCell()        
        # Check if they are ready to move
        if (not battalion._action.IsMoveReady(displacement = cell.GetCellSize(), penalty = cell.GetPenalty())):
            Log('%s: ... moving ...' % (battalion.GetLabel()))
            return b3.FAILURE            
        # Follow the path
        # Check the first movement
        if (cell == battalion._path[0]):
            battalion._path = battalion._path[1:]
            if (not battalion._path):
                return b3.FAILURE
        nextcell = battalion._path[0]
        tick.blackboard.set('nextcell', nextcell, tick.tree.id, None)
        return b3.SUCCESS
                        
class Move (b3.BaseNode):
    def tick(self, tick):
#    def Move(self, castle, selfarmy, againstarmy, battlefield, movedList):
        #print "###############################"
        #print "moving from Move node",
        #print "###############################"
        battalion = tick.target
        #castle = tick.blackboard.get('castle', tick.tree.id, None)
        selfarmy = tick.blackboard.get('selfarmy', tick.tree.id, None)
        #againstarmy = tick.blackboard.get('against', tick.tree.id, None)
        #battlefield = tick.blackboard.get('battlefield', tick.tree.id, None)
        movedList = tick.blackboard.get('movedList', tick.tree.id, None)
        nextcell = tick.blackboard.get('nextcell', tick.tree.id, None)

        # If moat isnt yet covered, wait
        if (not nextcell.HasMoat()):

            battalion._path = battalion._path[1:]    
                
            battalion._placement.MoveTo(nextcell, movedList)
    
            # Check if tower has arrived (so, the game ends?)
            if (not battalion._path):
                battalion._targetWall.SetAttachedSiegeTower(battalion, nextcell.center)
        else:
            # Special case: The turtle has been killed, and the tower cannot advance
            # A first solution would be let it stay on its place. The archers can kill the defenders while infantry climbs the wall
            # The problem here is what happens when there are not more soldiers to climb, and this is difficult and dirty to check here
            # So, the best solution is to destroy the tower
            if (not battalion._turtle):
                print "WARNING: A siege tower is alone without anything to do. Suiciding it by boring factor (no honour)"
                battalion.Kill(1)
                selfarmy.RemoveBattalion(battalion)
            return b3.FAILURE
        return b3.SUCCESS


"""
###############################################################################
# Attack nodes!
##############################################################################
"""
class IsAttacking (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target        
        # Siege towers attack
        if (battalion._action.GetCommand().IsAttack()):
            return b3.SUCCESS
        else:
            return b3.FAILURE

class IsInBattlefield (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target        
        # Siege towers attack
        if (battalion._placement.IsInBattlefield()):
            return b3.SUCCESS
        else:
            print 'ERROR: Current siege towers battalion is not placed on battlefield'
            return b3.FAILURE

class ReadyToShoot (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target        
        # Siege towers attack                
        # Siege towers have to fire against castle troops
        # Check if they are ready to shoot
        if (not battalion._action.IsReloadReady()):
            battalion._action.UpdateReloadTime()
            battalion('%s reloading ...' % (battalion.GetLabel()))
            return b3.FAILURE
        battalion._action.UpdateReloadTime()
        return b3.SUCCESS

class SelectPosAndClosestConstruction (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        castle = tick.blackboard.get('castle', tick.tree.id, None)
        
        # Siege towers attack
        # Simple attack mode        
        # Get battalion simple position to calculate an estimated distance to closest construction element
        # A 2D point is enough to get the closest construction element
        pos = battalion._placement.GetCenterPosition()
        # Get closest construction element with troops. Dont worry if it isnt reachable, so siege tower attack goal is to kill any defender units
        c = castle.GetClosestConstruction(populated = True, posfrom = pos, tilesrequired = False, reachable = False)
        if (c == None):
            # Game end?
            return b3.FAILURE
        tick.blackboard.set('posAndConstruction', (pos, c), tick.tree.id, None)
        return b3.SUCCESS

class Attack (b3.BaseNode):
    def tick(self, tick):
#    def Attack(self, against, castle, shoots):
        #print "###############################"
        #print "attacking from Attack node",
        #print "###############################"
        battalion = tick.target
        #against = tick.blackboard.get('against', tick.tree.id, None)
        shoots = tick.blackboard.get('shoots', tick.tree.id, None)
        castle = tick.blackboard.get('castle', tick.tree.id, None)
        (pos, c) = tick.blackboard.get('posAndConstruction', tick.tree.id, None)
        
        # Siege towers attack
        # Simple attack mode
        
        # Each siege tower has a number of archers placed in each level. Shoot for each one        
        i = 0
        while (i < battalion._number):            
            l = 0            
            while (l < battalion._nLevels):                
                # Set the shoot level
                pos.z = Battles.Utils.Settings.SETTINGS.Get_F('Army', 'SiegeTowers', 'LevelHeight') * l
                j = 0
                while (j < battalion._nArchersPerLevel):                   
                    # Get a random construction battalion
                    target = c.GetRandomBattalion()
                    # Get random battle field cell position
                    pos = battalion._placement.GetRandomPosition()
                    # Get cell position
                    cpos = target.GetCenterPosition()
                     
                    # Calculate the shoot success
                    # If the target is too far, the archer doesn't shoot (or he's idiot ...)
                    if (battalion._action.InAttackRange(currPos = pos, targetPos = cpos, castle = castle, constructionTarget = c)):                         
                        hit = battalion._action.ShootToArmy(target)
                        if (hit):
                            Log('%s kill 1 of %s' % (battalion.GetLabel(), target.GetLabel()))
               
                        if (shoots != None):
                            # Store the shoot
                            s = Shoot(origin = pos, destination = cpos, success = hit, attackertype = "Archers", targetObj = target, armytype = Shoot.SHOOT_FROM_ATTACKER)
                            shoots.append(s)
                        
                        # Check if target construction has more troops. If not, get again the closest populated construction
                        if (not c.HasBattalions()):
                            # Get closest construction element with troops
                            c = castle.GetClosestConstruction(populated = True, posfrom = pos, tilesrequired = False, reachable = False)
                            if (c == None):
                                # Game end?
                                return b3.FAILURE
                    
                    j += 1 
                
                l += 1
                
            i += 1
        return b3.SUCCESS

       
"""
 ##############################################################################
 #
 #   SiegeTower Trees !!!
 #
 ##############################################################################

"""
def createTree():
    global siegeTowerAttackingTree
    siegeTowerAttackingTree = b3.BehaviorTree()
    siegeTowerAttackingTree.id = 'siegeTowerAttackingTree'
    node1 = b3.Sequence([
        IsNotDefeated(),
        IsAttacking(),
        IsInBattlefield(),
        ReadyToShoot(),
        SelectPosAndClosestConstruction(),
        Attack()
    ])
    siegeTowerAttackingTree.root = node1

#     global siegeTowerDefendingTree
#     siegeTowerDefendingTree = b3.BehaviorTree()
#     siegeTowerDefendingTree.id = 'siegeTowerDefendingTree'
#     node2 = b3.Sequence([
#         IsDefeated(),
#         IsCorrectCommand(),
#         IsDefendingLine(),
#         IsReloading(),
#         AcquireTargetForDefense(),
#         Defend()
#         ])
#     siegeTowerDefendingTree.root = node2

    global siegeTowerMovingTree
    siegeTowerMovingTree = b3.BehaviorTree()
    siegeTowerMovingTree.id = 'siegeTowerMovingTree'
    node3 = b3.Sequence([
        IsNotDefeated(),
        HasValidPath(),
        UpdateConstructionStatus(),
        b3.Priority([b3.Inverter(HasMoat()),            # if not (HasMoat is False): 
            b3.Sequence([                               #
                b3.Priority([HasTurtle(),               #     if (hasTurtle is False):
                    CreateTurtle()]),                   #         createTurtle
                b3.Priority([b3.Inverter(HasTurtle()),  #     if not (hasTurtle is False):
                    HandleTurtle()]),                   #         HandleTurtle
            ]),
        ]),
        b3.Sequence([ReadyToMove(),                     # if (ReadyToMove is True):
                     SelectNextCell(),                  #    SelectNextCell
                     Move()                             #    Move !
        ])
    ])
    siegeTowerMovingTree.root = node3

    resetBlackboard()


def resetBlackboard():
    global siegeTowerBlackboards
    siegeTowerBlackboards = {}
    #print "SiegeTowers's tree created!!!"
    

"""
 ##############################################################################
 #
 #   SiegeTowers !!!
 #
 ##############################################################################

"""
class SiegeTowers(Battalion.Battalion):     
    """ Siege towers battalion. This is a battalion of only 1 unit that attack only one preselected wall
        This is a special unit. Initially, it is not "visible" until its is constructed along the play. First, some infantry is choosen to make a some kind of "turtle"
        and go to make a gateway over the moat of targeted wall. If the turtle is defeated, another one is commanded. When the gateway is constructed, the siege tower
        start to advance to the wall. The siege tower contains an archers battalion. The archers can be defeated. In this case, the nearest archers battalion will populate the 
        siege tower. In addition, the siege tower can be defeated. The siege tower has the same height than targeted wall. When the siege tower arrives to the wall, the game ends
       
        Attributes:
        
        targetWall: targeted wall
        path: list of battlefield cells in the form of a path to the targeted wall
        status: status of siege tower (see bellow)
        moatCells: list of path cells that are moat. Initially, they are some of the path cells. When the turtle clears the path, the list contain other moat cells to clear
        army: link to itself army. Its used to get access to infantry and archers, and to create turtles or populate the tower with archers
        turtle: Infantry battalion taken from army used to cover the moat
        constructionStatus: Current time of siege tower constructing. When it achieves the default time to construct (multiplied by number of levels), it starts to move or
                            waits for turtle finishing tasks
        coverMoatHeight: Internal counter to cover moats
        nLevels: Tower levels. There be enough levels to cover the wall height
    """
    
    siegetowersCounter = 0     # Internal counter for labeling purposes
    
    # Siege tower status values
    CONSTRUCTING = 0        # Initial status. The siege tower is constructing and the turtle has sent to cover the moat
    MOVING = 2              # There are a clear way along the path
    EMPTY = 3               # The siege tower is empty of archers (they have been killed). It waits until a new archers battalion arrives
    
    
    def __init__(self, army, number = 0):
        Battalion.Battalion.__init__(self, army = army, number = number)
        self._action = Action.ActionFeatures(defense = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'SiegeTowers', 'Defense'), 
                                             attack = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'SiegeTowers', 'Attack'), 
                                             speed = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'SiegeTowers', 'Speed'), 
                                             reloadspeed = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'SiegeTowers', 'Reload'), 
                                             accuracy = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'SiegeTowers', 'Accuracy'), 
                                             distance = Battles.Utils.Settings.SETTINGS.Get_F('Army', 'SiegeTowers', 'Distance'), 
                                             stationary = Battles.Utils.Settings.SETTINGS.Get_B('Army', 'SiegeTowers', 'Stationary'),
                                             movementpriority = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'SiegeTowers', 'MovementPriority'))
        self._bounding = Bounding(Battles.Utils.Settings.SETTINGS.Get_F('Army', 'SiegeTowers', 'Bounding/Length'), 
                                  Battles.Utils.Settings.SETTINGS.Get_F('Army', 'SiegeTowers', 'Bounding/Width'), 
                                  Battles.Utils.Settings.SETTINGS.Get_F('Army', 'SiegeTowers', 'Bounding/Height'))
        self._label = "SiegeTowers_" + str(SiegeTowers.siegetowersCounter)
        SiegeTowers.siegetowersCounter += 1
        #print 'SiegeTowers ->', SiegeTowers.siegetowersCounter
        
        self._targetWall = None
        self._path = []
        self._status = SiegeTowers.CONSTRUCTING
        self.__army = None  
        self._moatCells = []
        self._turtle = None
        self._nLevels = 0
        
        self._constructionStatus = 0
        
        self._coverMoatHeight = 0
        
        self._nArchersPerLevel = (self._bounding.length * self._bounding.width) / (Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Archers', 'Bounding/Length') * Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Archers', 'Bounding/Width'))
        blackboard = b3.Blackboard()
        siegeTowerBlackboards[self._label] = blackboard
  
    @classmethod   
    def ResetCounter(cls):
        cls.siegetowersCounter = 0        
        
    
    def GetCopy(self):
        #print "getCopy!!! (SiegeTowers.siegetowersCounter", SiegeTowers.siegetowersCounter, ")",
        raise NameError('SiegeTowers.getCopy!!! -> why do we need this?')
        ret = Battalion.Battalion.GetCopy(self)
        if (ret == None):
            return None
        #ret._label = "SiegeTowers_" + str(SiegeTowers.siegetowersCounter)
        #SiegeTowers.siegetowersCounter += 1
        
        # TODO: Be aware with the simple copy of next member data. There are structures and pointers to objects ...
        ret._targetWall = self._targetWall
        ret._path = self._path
        ret._status = self._status
        ret.__army = self.__army
        ret._moatCells = self._moatCells
        ret._turtle = self._turtle
        ret._nLevels = self._nLevels
        ret._constructionStatus = self._constructionStatus
        ret._coverMoatHeight = self._coverMoatHeight
        ret._nArchersPerLevel = self._nArchersPerLevel
        #blackboard = b3.Blackboard()
        #siegeTowerBlackboards[ret._label] = blackboard
        #print "|| copiedLabel:", self._label, " newLabel:", ret._label, " SiegeTowers.siegetowersCounter", SiegeTowers.siegetowersCounter
        return ret
        
        
    def SetTargetWall(self, wall, path):
        self._targetWall = wall
        self._path = path 
        
        self._nLevels = (wall.GetHeight() / Battles.Utils.Settings.SETTINGS.Get_F('Army', 'SiegeTowers', 'LevelHeight')) + 1
        
        for c in self._path:
            if (c.HasMoat()):
                self._moatCells.append(c)



    def GetTargetWall(self):
        return self._targetWall


    def SetArmy(self, army):
        self.__army = army
        
        
    def IsPathClear(self):
        # Return true if path is clear to advance the siege tower
        if (not self._path):
            return False

        for c in self._path:
            if (c.HasMoat()):
                return False
        return True
        
        
    def CreateTurtle(self, castle):
        if (self.__army == None):
            print("ERROR: Siege tower cannot send a turtle due there arent any army attached")
            return
        
        # Take an infantry battalion
        self._turtle = self.__army.GetBestTurtleBattalion(target = self._moatCells[0].center, siegetowerpos = self.GetCenterPosition(), castle = castle)
        if (not self._turtle):
            return
        
        self._turtle.SetCommand(command = Command.COVER_MOAT, target = self._moatCells[0], commander = self)
        self._turtle.SetMovementPriority(4)
        
        # Increase the defensive skills
        self._turtle.SetDefense(Battles.Utils.Settings.SETTINGS.Get_I('Army', 'SiegeTowers', 'TurtleDefense'))
            
            
    def RemoveTurtle(self):
        self._turtle = None    
        
     
    def Move(self, castle, selfarmy, againstarmy, battlefield, movedList):
        #print "###################### Move!!!", self.GetCommand().GetType()
        myBlackboard = siegeTowerBlackboards[self._label]
        myBlackboard.set('selfarmy', selfarmy, siegeTowerMovingTree.id, None)
        myBlackboard.set('battlefield', battlefield, siegeTowerMovingTree.id, None)
        #myBlackboard.set('againstarmy', againstarmy, siegeTowerMovingTree.id, None)
        myBlackboard.set('movedList', movedList, siegeTowerMovingTree.id, None)
        myBlackboard.set('castle', castle, siegeTowerMovingTree.id, None)
        myBlackboard.set('command', self.GetCommand().GetType(), siegeTowerMovingTree.id, None)
        siegeTowerMovingTree.tick(self, myBlackboard)
        return


    def Attack(self, against, castle, shoots):
        #print "###################### Attack!!!", self.GetCommand().GetType()
        myBlackboard = siegeTowerBlackboards[self._label]
        myBlackboard.set('against', against, siegeTowerAttackingTree.id, None)
        myBlackboard.set('shoots', shoots, siegeTowerAttackingTree.id, None)
        myBlackboard.set('castle', castle, siegeTowerAttackingTree.id, None)
        myBlackboard.set('command', self.GetCommand().GetType(), siegeTowerAttackingTree.id, None)
        siegeTowerAttackingTree.tick(self, myBlackboard)
        return


    def Kill(self, number, respawn = False):
        # The siege tower has been defeated
        # Respawn is only allowed for defender archers

        # Release the turtle
        if (self._turtle):
            self._turtle._action.SetCommand(Command.GOTO_CASTLE)
            self._turtle.SetMovementPriority(Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Infantry', 'MovementPriority'))
            self._turtle.SetDefense(Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Infantry', 'Defense'))
        
        Battalion.Battalion.Kill(self, 1)
 

if __name__ != "__main__":
    createTree()
