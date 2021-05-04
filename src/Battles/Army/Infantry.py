from math import floor, ceil

from Battles.Army import Action, Battalion
from Battles.Utils.Geometry import Bounding, Point3D
from Battles import Factory
from Battles.Utils.Message import Log, VERBOSE_WARNING
from Battles.Army.Action import Command
import Battles.Utils.Settings
import b3
from b3.decorators.ifThenElse import IfThenElse


"""
###############################################################################
# Move nodes!
##############################################################################
"""
class IsNotDefeated (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        if battalion.IsDefeated():
            return b3.FAILURE
        return b3.SUCCESS

class IsOnMoveCommand (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        if not battalion._action.GetCommand().IsMove():
            return b3.FAILURE
        return b3.SUCCESS

class IsWaitingForClimbing (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        if battalion._action.GetCommand().IsWaitingForClimbing():
            return b3.SUCCESS
        else:
            return b3.FAILURE

class WaitingClimbers (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        selfarmy = tick.blackboard.get('selfarmy', tick.tree.id, None)
        movedList = tick.blackboard.get('movedList', tick.tree.id, None)

        # The battalion is waiting to start climbing
        
        # Extract one soldier, convert it into a new battalion, and command it to start climbing
        # The last extracted soldier will be the same battalion, that will have only one soldier. In this case, the battalion is not anymore on the battlefield
        # The next soldier will wait until the new soldier has climbed enough to have an empty space into the virtual stair
        
        if not battalion._action.IsMoveReady(displacement = Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Infantry', 'Bounding/Length'), climb = True):
            return b3.FAILURE                      
        if battalion.GetNumber() == 1:
            newbattalion = battalion     # The last soldier to climb is itself. So the current battalion is transformed to a climber battalion
        else:       
            newbattalion = selfarmy.ExtractSoldier(battalion)
            if not newbattalion:
                print("ERROR: Attempt to extract a soldier from an empty battalion!")
                return b3.FAILURE            
        wallpos = battalion.GetCommand().GetTarget()     # See at the end of battlefield movement to get the target dictionary description
        newbattalion._placement.SetClimbingWall(wall = wallpos['Wall'], stairposition = wallpos['Position'].Copy(), clearprevious = False, stair = wallpos['Stair'])
        newbattalion._action.SetCommand(Command.GOTO_CASTLE, wallpos['Wall'])
        
        # We dont need to move the extracted soldier, so now its climbing. It will move when its Move method will be called
        # Because the ExtractSoldier method performs an append to the army lists, we hope (python facts) that the movement is done in the same turn
        if movedList:
            movedList.append(newbattalion)
            movedList.append(battalion)          # Current battalion has changed the number of soldiers
        return b3.SUCCESS

class HandleClimbing (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        movedList = tick.blackboard.get('movedList', tick.tree.id, None)
        if battalion._placement.IsClimbing():
            # Just climb
            battalion._placement.MoveTo(None, movedList)
            return b3.SUCCESS
        return b3.SUCCESS

class IsInBattlefield (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        if  not battalion._action.GetCommand().IsWaitingForClimbing() and \
            not battalion._placement.IsClimbing() and \
            battalion._placement.IsInBattlefield():
            return b3.SUCCESS
        return b3.FAILURE

class TraverseCurrCell (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        currcell = battalion._placement.GetBattlefieldCell()       
        # Check if they are ready to move
        if not battalion._action.IsMoveReady(displacement = currcell.GetCellSize(), penalty = currcell.GetPenalty()):
            Log('%s: ... moving ...' % (battalion.GetLabel()))
            return b3.FAILURE
        tick.blackboard.set('currcell', currcell, tick.tree.id, None)
        return b3.SUCCESS
             
class SelectNextCells (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        currcell = tick.blackboard.get('currcell', tick.tree.id, None)
        
        # Get the suitable cell to move
        lstc = currcell.GetAdjacentCells(battalionfree = False, towerfree = True)  # Collision check with other battalions is performed next
        
        # Avoid entering into a bad cell
        for lc in lstc:
            if battalion._placement.IsBadCell(lc):
                lstc.remove(lc)
        
        if not lstc:
            print "ERROR: Infantry.Move -> None cell to move!"
            return b3.FAILURE

        # Give more priority to non visited cells or wall-attached cells
        lstnoprev = []
        nonvisited = True
        for c in lstc:
            if (not battalion._placement.IsVisitedCell(c)) or c.HasWalls() or c.HasBattalion():
                lstnoprev.append(c)
        if not lstnoprev:
            
            # If all of near cells are already visited, this is a bad cell. Note that cells are previously filtered by castle obstacles (except walls), so the battalion is
            # very close to a tower or it is in a battlefield cell that produces a deadlock on the battalion advancement.
            battalion._placement.SetBadCell(currcell)
            
            nonvisited = False
            lstnoprev = lstc    # Use already visited cells if there arent any nonvisited
                           
        # Check those cells with battalions and their movement priority
        lstcell = []
        for c in lstnoprev:
            if (c.HasBattalion() and battalion._action.AvaiablePassThrough(c.GetBattalion())) or (not c.HasBattalion()):
                lstcell.append(c)
                                            
        if (not lstcell) and nonvisited:
            
            # Choose another path with already visited cells
            lstcell = []
            for c in lstc:
                if (c.HasBattalion() and battalion._action.AvaiablePassThrough(c.GetBattalion())) or (not c.HasBattalion()):
                    lstcell.append(c)
             
        if not lstcell:
            Log('%s: We can\'t move, sir!' % (battalion.GetLabel())) # Wait until blocking battalions let the movement
            return b3.FAILURE
        
        tick.blackboard.set('lstcell', lstcell, tick.tree.id, None)
        return b3.SUCCESS

class IsCoveringMoat (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        if battalion._action.GetCommand().IsCoverMoat():
            return b3.SUCCESS
        else:
            return b3.FAILURE

class MoveOnMoat (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        movedList = tick.blackboard.get('movedList', tick.tree.id, None)
        currcell = tick.blackboard.get('currcell', tick.tree.id, None)
        lstcell = tick.blackboard.get('lstcell', tick.tree.id, None)
        
        # Go to cover the targeted moat cell
        targetcell = battalion._action.GetCommand().GetTarget()                    
        if targetcell == currcell:
            return b3.FAILURE         # Stay until new goal is set
        nextcell = lstcell[0]                           
        minD = ((targetcell.center.x - nextcell.center.x)**2) + ((targetcell.center.y - nextcell.center.y)**2)   # Because we are searching the nearest cell, dont care about the sqrt
        for c in lstcell[1:]:
            d = ((targetcell.center.x - c.center.x)**2) + ((targetcell.center.y - c.center.y)**2)
            if d < minD:
                minD = d
                nextcell = c
        battalion._placement.MoveTo(nextcell, movedList)  
        return b3.SUCCESS
         
class Move (b3.BaseNode):
    def tick(self, tick):
#    def Move(self, castle, selfarmy, againstarmy, battlefield, movedList):
        #print "###############################"
        #print "moving from Move node",
        #print "###############################"
        battalion = tick.target
        castle = tick.blackboard.get('castle', tick.tree.id, None)
        movedList = tick.blackboard.get('movedList', tick.tree.id, None)
        # Moves troops (usually in battlefield)
        # The moved troops are stored into movedList (used for drawing update reasons)
        #print "Army Move!!!", self.GetCommand().GetType()
        lstcell = tick.blackboard.get('lstcell', tick.tree.id, None)
        # Move troops on the battlefield
        # =============================================================================
        # Choose the nearest target
        pos = battalion._placement.GetCenterPosition()
        # Get closest construction element (with or without troops)
        target = castle.GetClosestWall(populated = False, posfrom = pos)
        if target == None:
            Log("WARNING: Battalion without goal - None closest wall to attack", VERBOSE_WARNING)
            return b3.FAILURE
        
        tilesmanager = target.GetTileManager()
        hasgateway = tilesmanager.HasGateways()
                        
        # Choose the closest battlefield cell to closest construction
        cell = None # just some initializatio values...
        minD = 0 
        for c in lstcell:
            
            # Choose a random cell position to get the closest goal. This tries to avoid the "crazy selection". 
            # "crazy selection" : From current cell, named Y by example, search the around cell that is closer to selected goal, X by example. Then, on the next call, 
            # choose again Y cell due it is closer to other target
            fuzzycellpoint = c.GetRandomCellPosition()   

            if hasgateway:
                #d = tilesmanager.GetDistanceClosestGateway(c.center)
                d = tilesmanager.GetDistanceClosestGateway(fuzzycellpoint)
            else:
                #d = target.DistanceFromPoint(c.center)
                d = target.DistanceFromPoint(fuzzycellpoint)

            if (not cell) or (d < minD):
                    minD = d
                    cell = c
         
        # Move    
        battalion._placement.MoveTo(cell, movedList)
        tick.blackboard.set('cell', cell, tick.tree.id, None)
        return b3.SUCCESS
        
class ArrivedToWalls (b3.BaseNode):
    def tick(self, tick):
        cell = tick.blackboard.get('cell', tick.tree.id, None)
        # Check if the troops have achieved any castle part
        # NOTE and TODO: We expect that only walls are ready to be climbed 
        if cell.HasWalls():
            return b3.SUCCESS
        else:
            return b3.FAILURE
            
class HasGateways (b3.BaseNode):
    def tick(self, tick):
        cell = tick.blackboard.get('cell', tick.tree.id, None)
        w = cell.GetClosestWall()
        tilesmanager = w.GetTileManager()        
        # Force the battalion to go to closest gateway (if there are any) instead of climbing
        if tilesmanager.HasGateways():
            return b3.SUCCESS
        else:
            return b3.FAILURE

class ProceedToGateway (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        selfarmy = tick.blackboard.get('selfarmy', tick.tree.id, None)
        againstarmy = tick.blackboard.get('againstarmy', tick.tree.id, None)
        movedList = tick.blackboard.get('movedList', tick.tree.id, None)
        # Moves troops (usually in battlefield)
        # The moved troops are stored into movedList (used for drawing update reasons)
        #print "Army Move!!!", self.GetCommand().GetType()
        cell = tick.blackboard.get('cell', tick.tree.id, None)
        # Move troops on the battlefield
        # =============================================================================
        w = cell.GetClosestWall()
        tilesmanager = w.GetTileManager()
        
        # Force the battalion to go to closest gateway (if there are any) instead of climbing

        # Bet sure that battalion is in front of a gateway
        gatewayindex = tilesmanager.GetCloseGateway(cell.center, Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Infantry', 'SearchRadiusGoToRumble'))
        if gatewayindex != None:
            
            # Convert all battalion units into "free" climbers and let them to start climbing all together    
            ntroops = battalion.GetNumber()                        
            while ntroops > 0:
                newbattalion = selfarmy.ExtractSoldier(battalion)
                
                # Project a random position on the gateway. Be aware about climbers placed just at the tile edges (they should be placed in other tile columns due
                # precision facts)
                gp = tilesmanager.GetRandomGatewayPosition(gatewayindex = gatewayindex, marginleft = 0.0, marginright = Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Infantry', 'Bounding/Length') / 2.0)
                if not gp:
                    print "ERROR: None random gateway position obtained -> Wrong gateway index"
                    return b3.FAILURE
                
                gpos = Point3D().SetFrom2D(gp)
                gpos.z = cell.GetAltitude()
                
                # Create a stair for each "free" climber to avoid problems with climbing structure
                stair = w.CreateClimbingStair(stairposition = gpos, defendersarmy = againstarmy, climber = newbattalion, movedList = movedList)
                
                # Set the new soldier placement and command
                newbattalion._placement.SetClimbingWall(wall = w, stairposition = gpos, clearprevious = False, stair = stair)
                newbattalion._action.SetCommand(Command.GOTO_CASTLE, w)
                
                if movedList:
                    movedList.append(newbattalion)
            
                ntroops -= 1
            
            if movedList:
                movedList.append(battalion)     
        return b3.SUCCESS
                    
class StartClimbing (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        againstarmy = tick.blackboard.get('againstarmy', tick.tree.id, None)
        movedList = tick.blackboard.get('movedList', tick.tree.id, None)
        # Moves troops (usually in battlefield)
        # The moved troops are stored into movedList (used for drawing update reasons)
        #print "Army Move!!!", self.GetCommand().GetType()
        cell = tick.blackboard.get('cell', tick.tree.id, None)
        # Move troops on the battlefield
        # =============================================================================

        # Set the command of waiting to climb
        # For each movement a new soldier, converted to a battalion of only one soldier, will start climbing. Meanwhile, the others will wait
        
        # Calculate the climbing start position from projecting a random point in current cell to wall
        w = cell.GetClosestWall()
        stairpos = w.Project(cell.GetRandomCellPosition())
        stairpos.z = cell.GetAltitude() 
        stair = w.CreateClimbingStair(stairposition = stairpos, defendersarmy = againstarmy, climber = battalion,  movedList = movedList)
        
        battalion.SetCommand(Command.WAITFOR_CLIMBING, {"Wall": w, "Position": stairpos, "Stair": stair})
        
        # Reset the movement counter, so we are changing the movement type
        battalion._action.ResetMoveReady()
        
        # Set a high movement priority to avoid that any turtle or siege tower (or anything) switch the battalion position meanwhile it is climbing 
        battalion._action.SetMovementPriority(Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Infantry', 'MovementPriorityWaitingClimbing'))
        return b3.SUCCESS

"""
 ##############################################################################
 #
 #   Infantry Trees !!!
 #
 ##############################################################################

"""
def createTree():
    #global infantryAttackingTree
    #infantryAttackingTree = b3.BehaviorTree()
    #infantryAttackingTree.id = 'infantryAttackingTree'
    #node1 = b3.Sequence([
    #    Attack()
    #    ])
    #infantryAttackingTree.root = node1

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

    global infantryMovingTree
    infantryMovingTree = b3.BehaviorTree()
    infantryMovingTree.id = 'infantryMovingTree'
    node3 = b3.Sequence([
        IsNotDefeated(),
        IsOnMoveCommand(),
        IfThenElse( IsWaitingForClimbing(),  # I should have written this node looooooong before! ;-)
                        WaitingClimbers(),
                        HandleClimbing()
        ),
        IfThenElse( IsInBattlefield(),      # definitely! ;-)
                        b3.Sequence([
                            TraverseCurrCell(),
                            SelectNextCells(),
                            IfThenElse(IsCoveringMoat(),
                                            MoveOnMoat(),
                                            b3.Sequence([
                                                Move(),
                                                IfThenElse(ArrivedToWalls(),
                                                           IfThenElse(HasGateways(),
                                                                        ProceedToGateway(),
                                                                        StartClimbing()
                                                               )
                                                           )
                                            ])
                                       ),                
                        ]),
                   ),
        ])
    infantryMovingTree.root = node3

    resetBlackboard()

def resetBlackboard():
    global infantryBlackboards
    infantryBlackboards = {}
    #print "Infantry's tree created!!!"
    

"""
 ##############################################################################
 #
 #   Infantry !!!
 #
 ##############################################################################
 
""" 
class Infantry(Battalion.Battalion):
    """ Basic ground soldier. Its goal is to climb the castle walls. They dont attack, only advance if it is possible
    
    """
    
    infantryCounter = 0     # Internal counter for labeling purposes
    
    def __init__(self, army, number = 0):
        Battalion.Battalion.__init__(self, army = army, number = number)
        self._action = Action.ActionFeatures( defense = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Infantry', 'Defense'), 
                                              attack = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Infantry', 'Attack'), 
                                              speed = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Infantry', 'Defense'), 
                                              reloadspeed = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Infantry', 'Reload'), 
                                              accuracy = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Infantry', 'Accuracy'), 
                                              distance = Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Infantry', 'Distance'),
                                              climbspeed = Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Infantry', 'ClimbSpeed'),
                                              stationary = Battles.Utils.Settings.SETTINGS.Get_B('Army', 'Infantry', 'Stationary'),
                                              movementpriority = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Infantry', 'MovementPriority'))
        self._bounding = Bounding( Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Infantry', 'Bounding/Length'), 
                                   Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Infantry', 'Bounding/Width'), 
                                   Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Infantry', 'Bounding/Height'))       
        self._label = "Infantry_" + str(Infantry.infantryCounter)
        Infantry.infantryCounter += 1
        #print 'Infantry ->', Infantry.infantryCounter,
          
        self._action.SetRubbleClimgingSpeed(Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Infantry', 'RubbleClimbSpeed'))  
        blackboard = b3.Blackboard()
        infantryBlackboards[self._label] = blackboard
          
        
    @classmethod      
    def ResetCounter(cls):
        cls.infantryCounter = 0        
    
    
#     def GetCopy(self):
#         print "getCopy!!! (Infantry.infantryCounter", Infantry.infantryCounter, ")",
#         ret = Battalion.Battalion.GetCopy(self)
#         if (ret == None):
#             return None
#         
#         #ret._label = "Infantry_" + str(Infantry.infantryCounter)
#         #Infantry.infantryCounter += 1
#         #blackboard = b3.Blackboard()
#         #infantryBlackboards[ret._label] = blackboard
#         print "|| copiedLabel:", self._label, " newLabel:", ret._label, " Infantry.infantryCounter", Infantry.infantryCounter
#         return ret
        

    def Move(self, castle, selfarmy, againstarmy, battlefield, movedList):
        #print "###################### Move!!!", self.GetCommand().GetType()
        myBlackboard = infantryBlackboards[self._label]
        myBlackboard.set('selfarmy', selfarmy, infantryMovingTree.id, None)
        myBlackboard.set('battlefield', battlefield, infantryMovingTree.id, None)
        myBlackboard.set('againstarmy', againstarmy, infantryMovingTree.id, None)
        myBlackboard.set('movedList', movedList, infantryMovingTree.id, None)
        myBlackboard.set('castle', castle, infantryMovingTree.id, None)
        myBlackboard.set('command', self.GetCommand().GetType(), infantryMovingTree.id, None)
        infantryMovingTree.tick(self, myBlackboard)
        return


    def Kill(self, number, respawn = False):
        # The infantry battalion has some defeats
        # Respawn is only allowed for defender archers

        Battalion.Battalion.Kill(self, number)
        
        if self.IsDefeated() and self._action.GetCommand().IsCoverMoat():
            # Call to other battalion to replace the moat covering if his commander (the siege tower) is still alive
            com = self._action.GetCommand().GetCommander()
            
            factory = Factory.ArmyFactory()
            if (com != None) and factory.IsSiegeTower(com):
                if not com.IsDefeated():
                    #com.CreateTurtle()
                    com.RemoveTurtle()  # Remove the siege tower turtle and force it to create a new one in the next siege tower Move call
                    
        if self.IsDefeated() and self._action.GetCommand().IsWaitingForClimbing():
            # Update the linked stair and release the throwers
            wallpos = self.GetCommand().GetTarget()
            wallpos['Stair'].RemoveClimber(None)    # Force to check if stair and linked thrower must be deleted
            
         
    def RedrawAttacked(self, canvas, viewport):            
        # Controls when the attacked battalion is climbing. In this case, redraw the throwers too. Otherwise, do the usual
        if self._placement.IsClimbing():
            stair = self._placement.GetClimbingStair()
            t = stair.GetThrowers()
            if t:
                t.RedrawAttacked(canvas, viewport)
        
        Battalion.Battalion.RedrawAttacked(self, canvas, viewport)
         
            
              
    # DEPRECATED!!!!
    def CalculateClimbingSpeeds(self, battalionlist, meanSpeed):
                            
        # To simulate the climbing we imagine a stair where all soldiers try to climb with it. If we consider the soldiers going up stairs in order
        # they have to wait the previous one to start to climb. This waiting should be the soldier bounding height.
        # Then, and using some example values, the first soldier, with a speed of 1m/turn and a wall of 12m, spends 12 turns to get the top. The second one have to wait
        # until the soldier body is fully on the stair, that is the bounding height. Taking as example a bounding height of 2m, the second soldiers spends 14 turns
        # to get the top. This process repeats for other soldiers using the sequence t_i = 12 + (2 * i).
        
        if not battalionlist:
            return
        
        if Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Infantry', 'ClimbSpeed') <= 0:
            return
        
        if meanSpeed:
        
            # Because we don't want to simulate the stairs climbing (there are too many ways to climb a wall, and our "climbing" is just a representation of reaching
            # a castle wall), we consider the mean spent turns for all soldiers of battalion. Due it's a numeric sequence, this mean time can be represented
            # as (t_(n/2) + t((n/2)+1)) / 2, where n is the number of battalion soldiers.
            # So, considering all variables, we have for each soldier of THIS battalion:
            #         climbingSpeed = wallHeight / ((t(floor(battalionSize / 2)) + t(ceil(battalionSize / 2)) / 2)
            #         t(i) = (wallHeight / defaultClimbingSpeed) + (soldierBoundingHeight * i)
            
            ihalf = floor(len(battalionlist) / 2.0) 
            iihalf = ceil(len(battalionlist) / 2.0)
            if ihalf == iihalf:
                iihalf += 1
            wallheight = battalionlist[0]._placement.GetClimbingWall().GetHeight()

            for nb in battalionlist:
                cs = nb._action.GetClimbingSpeed()
                if cs > 0:
                    ws = wallheight / nb._action.GetClimbingSpeed()
                    ti = ws + (nb._bounding.height * ihalf)
                    tii = ws + (nb._bounding.height * iihalf)
                    newspeed = wallheight / ((ti + tii) / 2.0)
                else:
                    newspeed = 0
                nb._action.SetClimbingSpeed(newspeed)

        
        else:
            
            # We can simulate the stairs climbing assigning a different speed for each soldier. Note that we are not simulating a real stair climbing, just an approximation
            # of what a battalion would do in front of an enemy castle wall.
            # As stated before, the climbing speed for each soldier is:
            #         climbingSpeed(i) = wallHeight / t(i)
            #         t(i) = (wallHeight / defaultClimbingSpeed) + (soldierBoundingHeight * i)
            
            wallheight = battalionlist[0]._placement.GetClimbingWall().GetHeight()
             
            i = 0
            while i < len(battalionlist):
                b = battalionlist[i]
                cs = b._action.GetClimbingSpeed()
                if cs > 0:
                    ws = wallheight / b._action.GetClimbingSpeed()
                    ti = ws + (battalionlist[i]._bounding.height * i)
                    newspeed = wallheight / ti
                else:
                    newspeed = 0
                    
                battalionlist[i]._action.SetClimbingSpeed(newspeed)
                i += 1
        

if __name__ != "__main__":
    createTree()
