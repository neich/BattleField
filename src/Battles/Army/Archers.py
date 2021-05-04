from Battles.Army import Action, Battalion
from Battles.Utils.Geometry import Bounding
from Battles.Utils.Message import Log
from Battles.Game.Board import Shoot
from Battles.Factory import ConstructionFactory
import b3

import Battles.Utils.Settings


"""
###############################################################################
# Attack nodes!
##############################################################################
"""
class IsDefeated (b3.BaseNode):
    def tick(self, tick):
        #print "isDefeated"
        battalion = tick.target
        #against = tick.blackboard.get('against', tick.tree.id, None)
        #shoots = tick.blackboard.get('shoots', tick.tree.id, None)
        #castle = tick.blackboard.get('castle', tick.tree.id, None)
        if (battalion.IsDefeated()):
            return b3.FAILURE
        else:
            return b3.SUCCESS

class IsCorrectCommand (b3.BaseNode):
    def tick(self, tick):
        #print "isCorrectCommand"
        battalion = tick.target
        currCommand = tick.blackboard.get('command', tick.tree.id, None)
        #against = tick.blackboard.get('against', tick.tree.id, None)
        #shoots = tick.blackboard.get('shoots', tick.tree.id, None)
        #castle = tick.blackboard.get('castle', tick.tree.id, None)
        if (not battalion.GetCommand().isCommand(currCommand)):
            return b3.FAILURE
        else:
            return b3.SUCCESS

class IsMoveCommand (b3.BaseNode):
    def tick(self, tick):
        #print "isCorrectCommand"
        battalion = tick.target
        #currCommand = tick.blackboard.get('command', tick.tree.id, None)
        #against = tick.blackboard.get('against', tick.tree.id, None)
        #shoots = tick.blackboard.get('shoots', tick.tree.id, None)
        #castle = tick.blackboard.get('castle', tick.tree.id, None)
        if (battalion.GetCommand().IsMove()):
            return b3.SUCCESS
        else:
            return b3.FAILURE

class IsInBattlefield (b3.BaseNode):
    def tick(self, tick):
        #print "isDefendingLine"
        # Archers defend (from castle)
        #startTime =
        battalion = tick.target
        #against = tick.blackboard.get('against', tick.tree.id, None)
        #defenders = None
        #battlefield = None
        #shoots = tick.blackboard.get('shoots', tick.tree.id, None)
        #castle = tick.blackboard.get('castle', tick.tree.id, None)

        if (not battalion._placement.IsInBattlefield()):
            print 'ERROR: Current archers battalion is not placed on battlefield'
            return b3.FAILURE
        else:
            return b3.SUCCESS


class IsReloading (b3.BaseNode):
    def open(self, tick):
        pass
    def tick(self, tick):
        #print "defending from Defend node",
        # Archers defend (from castle)
        #startTime =
        battalion = tick.target
        #against = tick.blackboard.get('against', tick.tree.id, None)
        #defenders = None
        #battlefield = None
        #shoots = tick.blackboard.get('shoots', tick.tree.id, None)
        #castle = tick.blackboard.get('castle', tick.tree.id, None)

        # Archers have to fire against battlefield troops
        # Check if they are ready to shoot
        if (not battalion._action.IsReloadReady()):
            battalion._action.UpdateReloadTime()
            Log('%s reloading ...' % (battalion.GetLabel()))
            return b3.FAILURE
        else:
            return b3.SUCCESS


class Attack (b3.BaseNode):
    def tick(self, tick):
        #print "###############################"
        #print "attacking from Attack node",
        #print "###############################"
        battalion = tick.target
        #against = tick.blackboard.get('against', tick.tree.id, None)
        shoots = tick.blackboard.get('shoots', tick.tree.id, None)
        castle = tick.blackboard.get('castle', tick.tree.id, None)

        # Archers have to fire against castle troops

        # Check if they are ready to shoot
        battalion._action.UpdateReloadTime()

        # Simple attack mode

        # Get battalion simple position to calculate an estimated distance to closest construction element
        # A 2D point is enough to get the closest construction element
        pos = battalion._placement.GetCenterPosition()
        # Get closest construction element with troops. Dont worry if it isnt reachable, so archers goal is to kill defender units
        c = castle.GetClosestConstruction(populated = True, posfrom = pos, tilesrequired = False, reachable = False)
        if (c == None):
            # Game end?
            return b3.FAILURE

        # Shoot as many arrows as troops number
        nshoots = 0
        i = 0
        while (i < battalion._number):
            # Get a random construction battalion. First get archers and throwers. Then, cannons
            target = c.GetRandomBattalion()
            # Get random battle field cell position
            pos = battalion._placement.GetRandomPosition()
            # Get cell position
            cpos = target.GetCenterPosition()

            # Calculate the shoot success
            # If the target is too far, the archer doesn't shoot (or he's idiot ...)
            if (battalion._action.InAttackRange(currPos = pos, targetPos = cpos, castle = castle, constructionTarget = c)):
                nshoots += 1
                hit = battalion._action.ShootToArmy(target)
                if (hit):
                    Log('%s kill 1 of %s' % (battalion.GetLabel(), target.GetLabel()))
                if (shoots != None):
                    # Store the shoot
                    s = Shoot(origin = pos, destination = cpos, success = hit, attackertype = "Archers",
                              targetObj = target, armytype = Shoot.SHOOT_FROM_ATTACKER)
                    shoots.append(s)
                # Check if target construction has more troops. If not, get again the closest populated construction
                if (not c.HasBattalions()):
                    # Get closest construction element with troops
                    c = castle.GetClosestConstruction(populated = True, posfrom = pos, tilesrequired = False, reachable = False)
                    if (c == None):
                        # Game end?
                        return b3.FAILURE
            i += 1

        # We use a simple heuristic to know if the battalion has to move, calculating if more than a half units have shoot to the construction
        # This is an empirical decision. The aiming is random. If all units have aimed to a too far position, all of them will fail
        # By the other hand, the alternative would be to search if there any construction point in attack range, spending a lot of computational time
        # and turns trying to shoot. Unfortunately this produces a side effect on trenches, where some battalions can left the trench, loosing its defensive factor
        if (battalion._number > 0):
            stay = False
            if ((float(nshoots) / float(battalion._number)) >= Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Archers', 'ShootsToStay')):
                # Introduce a new decision factor about trenchs. If battalion is not in any trench and there is anyone near, it has to move, althought current position will be effective
                # Its assumed the principle of archer conservation ...
                battlefield = battalion._placement.GetBattlefieldCell().GetBattlefield()
                targett = battlefield.GetClosestTrench(frompos = battalion._placement.GetCenterPosition(), free = True,
                                                       searchradius = Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Archers', 'SearchRadiusTrench'),
                                                       castle = castle, battalion = battalion)
                if (not targett):
                    stay = True
            battalion._action.SetStationary(stay)

        return b3.SUCCESS


"""
###############################################################################
# Defend  nodes!
##############################################################################
"""
class IsDefendingLine (b3.BaseNode):
    def tick(self, tick):
        #print "isDefendingLine"
        # Archers defend (from castle)
        #startTime =
        battalion = tick.target
        #against = tick.blackboard.get('against', tick.tree.id, None)
        #defenders = None
        #battlefield = None
        #shoots = tick.blackboard.get('shoots', tick.tree.id, None)
        #castle = tick.blackboard.get('castle', tick.tree.id, None)

        if (not battalion._placement.IsInDefendingLine()):
            print 'ERROR: Current archers battalion is not placed on a defending line'
            return b3.FAILURE
        else:
            return b3.SUCCESS


class AcquireTargetForDefense (b3.BaseNode): #acquire a suitable target
    def tick(self, tick):
        battalion = tick.target
        castle = tick.blackboard.get('castle', tick.tree.id, None)
        against = tick.blackboard.get('against', tick.tree.id, None)
        # Get battalion simple position to calculate an estimated distance to closest construction element
        pos = battalion._placement.GetCenterPosition()
        # Get the most suitable battalion to shoot.
        # Give the priority to the climbers of current wall or adjacent walls (if current battalion is placed on a tower
        target = battalion._GetClimberInAttackRange(frompos = pos, castle = castle)
        # If none target is climbing the near walls (or it is not accessible), search the other battalions
        if (not target):
            # Get the closest enemy battalion
            target = against.GetClosestBattalionInAttackRange(posfrom = pos, castle = castle, action = battalion._action,
                                                              excludeConstruction = battalion._placement.GetDefendingConstruction())
            if (not target):
                # There is not anyone to shoot in range
                return b3.FAILURE
        tick.blackboard.set('target', target, tick.tree.id, None)
        return b3.SUCCESS


class Defend (b3.BaseNode):
    def tick(self, tick):
        #print "defending from Defend node",
        # Archers defend (from castle)
        #startTime =
        battalion = tick.target
        against = tick.blackboard.get('against', tick.tree.id, None)
        #defenders = None
        #battlefield = None
        shoots = tick.blackboard.get('shoots', tick.tree.id, None)
        castle = tick.blackboard.get('castle', tick.tree.id, None)
        target = tick.blackboard.get('target', tick.tree.id, None)

        battalion._action.UpdateReloadTime()

        # Simple defend mode

        defaultdoublecheck = Battles.Utils.Settings.SETTINGS.Get_B('Army', 'Archers', 'DefenseShootDoubleCheck')

        # Shoot as many arrows as troops number, each archer shots ONE arrow at a time
        i = 0
        while (i < battalion._number):
            # Get random construction cell position
            pos = battalion._placement.GetRandomPosition()
            # Get the most suitable point to attack
            cpos = target._placement.GetRandomPosition()

            # Calculate the shoot success
            # If the target is too far or the attack angle is too graze, the archer doesn't shoot (or he's idiot ...)
            # The range attack is checked before, but with cell central points. That is, the archer first search the most suitable battalion to shoot. Then some
            # random data is take into account with real positions on cells. This could succeed with a shoot fail.
            doublecheck = False
            if (defaultdoublecheck):
                doublecheck = battalion._action.InAttackRange(currPos = pos, targetPos = cpos, castle = castle,
                                                              constructionTarget = None,
                                                              excludeConstruction = battalion._placement.GetDefendingConstruction())
            if ((not defaultdoublecheck) or (defaultdoublecheck and doublecheck)):
                if (battalion._action.ShootToArmy(target)):
                    # Kills one element
                    hit = True
                    if (target.IsDefeated()):
                        against.RemoveBattalion(target)
                    else:
                        Log('%s kill 1 of %s' % (battalion.GetLabel(), target.GetLabel()))
                else:
                    hit = False
                if (shoots != None):
                    # Store the shoot
                    s = Shoot(origin = pos, destination = cpos, success = hit, attackertype = "Archers",
                              targetObj = target, armytype = Shoot.SHOOT_FROM_DEFENDER)
                    shoots.append(s)
                # Check if battalion is defeated and get another one (check it here to allow storing the shoot)
                if (target.IsDefeated()):
                    target = battalion._GetClimberInAttackRange(frompos = pos, castle = castle)
                    if (not target):
                        target = against.GetClosestBattalionInAttackRange(posfrom = pos, castle = castle,
                                                                          action = battalion._action,
                                                                          excludeConstruction = battalion._placement.GetDefendingConstruction())
                        if (target == None):
                            return b3.FAILURE

            i += 1
        return b3.SUCCESS


"""
###############################################################################
# Move nodes!
##############################################################################
"""
class AcquireCandidateCells (b3.BaseNode):
    def tick(self, tick):
        battalion = tick.target
        # The archers cannot break ranks
        currcell = battalion._placement.GetBattlefieldCell()
        # Check if they are ready to move
        if (not battalion._action.IsMoveReady(displacement = currcell.GetCellSize(), penalty = currcell.GetPenalty())):
            Log('%s: ... moving ...' % (battalion.GetLabel()))
            return b3.FAILURE
        # Get the suitable cell to move
        listAdjacentCells = currcell.GetAdjacentCells(battalionfree = False, towerfree = True)  # Collision check with other battalions is performed next
        # Check those cells with battalions and their movement priority
        lstcell = []
        for c in listAdjacentCells:
            if ((c.HasBattalion() and battalion._action.AvaiablePassThrough(c.GetBattalion())) or (not c.HasBattalion())):
                lstcell.append(c)
        if (len(lstcell) == 0):
            Log('%s: We can\'t move, sir!' % (battalion.GetLabel()))
            return b3.FAILURE
        tick.blackboard.set('candidateCellList', lstcell, tick.tree.id, None)
        return b3.SUCCESS


class selectDestinationTarget (b3.BaseNode):
    def tick(self, tick):
        # Archers defend (from castle)
        #startTime =
        battalion = tick.target
        #selfarmy = tick.blackboard.get('selfarmy', tick.tree.id, None)
        #againstarmy = tick.blackboard.get('against', tick.tree.id, None)
        castle = tick.blackboard.get('castle', tick.tree.id, None)
        # Choose the target to move. It can be a castle construction or a trench where attack the castle construction
        # Choose the closest construction target
        pos = battalion._placement.GetCenterPosition()
        target = castle.GetClosestConstruction(populated = True, posfrom = pos, tilesrequired = False, reachable = False)
        if (not target):
            # Game end?... no castle?... amazing!.. oh... wait... castle without troops... well.. this shit can happen... ok
            return b3.FAILURE
        tdist = target.DistanceFromPoint(pos)
        tick.blackboard.set('destination', (target, tdist), tick.tree.id, None)
        return b3.SUCCESS


class doesDestinationNeedCorrection (b3.BaseNode):
    def tick(self, tick):
        # Archers defend (from castle)
        #startTime =
        battalion = tick.target
        #selfarmy = tick.blackboard.get('selfarmy', tick.tree.id, None)
        #againstarmy = tick.blackboard.get('against', tick.tree.id, None)
        castle = tick.blackboard.get('castle', tick.tree.id, None)
        (target, tdist) = tick.blackboard.get('destination', tick.tree.id, None)
        # Choose the target to move. It can be a castle construction or a trench where attack the castle construction
        # Choose the closest construction target
        pos = battalion._placement.GetCenterPosition()
        # The archer only will choose the closest trench if he is in attack range. Otherwise, he would jump from one trench to another, like a butterfly, forgiving its real reason to exist on life ....
        if (battalion._action.InAttackRange(currPos = pos, targetPos = target.GetRandomBattalion().GetCenterPosition(),
                                            castle = castle, constructionTarget = target)):
            return b3.SUCCESS # yep, it does...
        else:
            return b3.FAILURE #It doesn't need correction


class correctDestinationTarget (b3.BaseNode):
    def tick(self, tick):
        # Archers defend (from castle)
        #startTime =
        battalion = tick.target
        #selfarmy = tick.blackboard.get('selfarmy', tick.tree.id, None)
        #againstarmy = tick.blackboard.get('against', tick.tree.id, None)
        battlefield = tick.blackboard.get('battlefield', tick.tree.id, None)
        castle = tick.blackboard.get('castle', tick.tree.id, None)
        (target, tdist) = tick.blackboard.get('destination', tick.tree.id, None)
        # Choose the target to move. It can be a castle construction or a trench where attack the castle construction
        # Choose the closest construction target
        pos = battalion._placement.GetCenterPosition()
        # The archer only will choose the closest trench if he is in attack range. Otherwise, he would jump from one trench to another, like a butterfly, forgiving its real reason to exist on life ....
        # Choose the closest trench
        #targett = battlefield.GetClosestTrench(frompos = pos, free = True, target = targetc, maxdist = tdist, castle = castle, battalion = battalion)
        target_trench = battlefield.GetClosestTrench(frompos = pos, free = True,
                                                     searchradius = Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Archers', 'SearchRadiusTrench'),
                                                     castle = castle, battalion = battalion)
        if (target_trench):
            targett = target_trench.GetClosestCell(pos, free = True)
            if (targett):
                target = targett        # This should never happen
        tick.blackboard.set('destination', (target, tdist), tick.tree.id, None)
        return b3.SUCCESS


class selectFinalDestinationCell (b3.BaseNode):
    def tick(self, tick):
        # Archers defend (from castle)
        #selfarmy = tick.blackboard.get('selfarmy', tick.tree.id, None)
        #againstarmy = tick.blackboard.get('against', tick.tree.id, None)
        lstcell = tick.blackboard.get('candidateCellList', tick.tree.id, None)
        (target, tdist) = tick.blackboard.get('destination', tick.tree.id, None)
        # Choose the closest battlefield cell to closest construction
        cell = None
        minD = tdist
        for c in lstcell:
            d = target.DistanceFromPoint(c.center)
            if (d < minD):
                    minD = d
                    cell = c
        if (cell == None):
            """
            Log('%s: We are in the best position, sir!' % (battalion.GetLabel()))
            return
            """
            # This case happens usually when a battalion that wants to go to a specific wall (because is closer than others) is occluded by another battalion
            # or by any construction object. The situation could be a deadlock, so to avoid stopped units, we search again a near cell but discarding the minimum
            # distance to the chosen target. With this, the battalion could find another route, maybe to another target
            i = 0
            minD = -1
            while (i < len(lstcell)):
                c = lstcell[i]
                d = target.DistanceFromPoint(c.center)
                if ((i == 0) or (d < minD)):
                    minD = d
                    cell = c
                i += 1
        tick.blackboard.set('finalCell', cell, tick.tree.id, None)
        return b3.SUCCESS


class Move (b3.BaseNode):
    def tick(self, tick):
        #print "###############################"
        #print "moving from Move node",
        #print "###############################"
        # Archers defend (from castle)
        battalion = tick.target
        movedList = tick.blackboard.get('movedList', tick.tree.id, None)

        cell = tick.blackboard.get('finalCell', tick.tree.id, None)
        battalion._placement.MoveTo(cell, movedList)
        return b3.SUCCESS

"""
 ##############################################################################
 #
 #   Archer Trees !!!
 #
 ##############################################################################

"""
def createTree():
    global archerAttackingTree
    archerAttackingTree = b3.BehaviorTree()
    archerAttackingTree.id = 'archerAttackingTree'
    node1 = b3.Sequence([
        IsDefeated(),
        IsCorrectCommand(),
        IsInBattlefield(),
        IsReloading(),
        Attack()
        ])
    archerAttackingTree.root = node1

    global archerDefendingTree
    archerDefendingTree = b3.BehaviorTree()
    archerDefendingTree.id = 'archerDefendingTree'
    node2 = b3.Sequence([
        IsDefeated(),
        IsCorrectCommand(),
        IsDefendingLine(),
        IsReloading(),
        AcquireTargetForDefense(),
        Defend()
        ])
    archerDefendingTree.root = node2

    global archerMovingTree
    archerMovingTree = b3.BehaviorTree()
    archerMovingTree.id = 'archerMovingTree'
    node3 = b3.Sequence([
        IsDefeated(),
        IsMoveCommand(),
        IsInBattlefield(),
        AcquireCandidateCells(),
        b3.Sequence([
            selectDestinationTarget(),
            b3.Priority([
                b3.Inverter(doesDestinationNeedCorrection()),
                correctDestinationTarget(),
            ]),
        ]),
        selectFinalDestinationCell(),
        Move()
        ])
    archerMovingTree.root = node3

    resetBlackboard()

def resetBlackboard():
    global archerBlackboards
    archerBlackboards = {}
    #print "Archer's tree created!!!"

"""
 ##############################################################################
 #
 #   Archers !!!
 #
 ##############################################################################

"""
class Archers(Battalion.Battalion):
    """ Soldiers with archs. They can attack curtain wall defenses
    """

    archersCounter = 0     # Internal counter for labeling purposes

    def __init__(self, army, number = 0):
        Battalion.Battalion.__init__(self, army = army, number = number)
        self._action = Action.ActionFeatures(defense = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Archers', 'Defense'),
                                             attack = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Archers', 'Attack'),
                                             speed = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Archers', 'Speed'),
                                             reloadspeed = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Archers', 'Reload'),
                                             accuracy = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Archers', 'Accuracy'),
                                             distance = Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Archers', 'Distance'),
                                             stationary = Battles.Utils.Settings.SETTINGS.Get_B('Army', 'Archers', 'Stationary'),
                                             movementpriority = Battles.Utils.Settings.SETTINGS.Get_I('Army', 'Archers', 'Accuracy'))
        self._bounding = Bounding(Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Archers', 'Bounding/Length'),
                                  Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Archers', 'Bounding/Width'),
                                  Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Archers', 'Bounding/Height'))
        self._label = "Archers_" + str(Archers.archersCounter)
        Archers.archersCounter += 1
        blackboard = b3.Blackboard()
        archerBlackboards[self._label] = blackboard
        #print 'Archers ->', Archers.archersCounter,

    @classmethod 
    def ResetCounter(cls):
        cls.archersCounter = 0


    def Move(self, castle, selfarmy, againstarmy, battlefield, movedList):
        # Moves troops (usually in battlefield)
        # The moved troops are stored into movedList (used for drawing update reasons)
        # The goal of archers movement (only if they are attackers) is to reach a better placement to shoot
        # Archers attack
        # Return a list of shoot lines to be displayed
        #print "###################### Move!!!", self.GetCommand().GetType()
        myBlackboard = archerBlackboards[self._label]
        #myBlackboard.set('selfarmy', selfarmy, archerDefendingTree.id, None)
        myBlackboard.set('battlefield', battlefield, archerMovingTree.id, None)
        #myBlackboard.set('againstarmy', againstarmy, archerDefendingTree.id, None)
        myBlackboard.set('movedList', movedList, archerMovingTree.id, None)
        myBlackboard.set('castle', castle, archerMovingTree.id, None)
        myBlackboard.set('command', self.GetCommand().GetType(), archerMovingTree.id, None)
        archerMovingTree.tick(self, myBlackboard)
        return


    def Attack(self, against, castle, shoots):
        # Archers attack
        # Return a list of shoot lines to be displayed
        #print "###################### Attack!!!", self.GetCommand().GetType()
        myBlackboard = archerBlackboards[self._label]
        myBlackboard.set('against', against, archerAttackingTree.id, None)
        myBlackboard.set('shoots', shoots, archerAttackingTree.id, None)
        myBlackboard.set('castle', castle, archerAttackingTree.id, None)
        myBlackboard.set('command', self.GetCommand().GetType(), archerAttackingTree.id, None)
        archerAttackingTree.tick(self, myBlackboard)
        return


    def Defend(self, against, defenders, battlefield, shoots, castle):
        # Archers defend (from castle)
        #print "Defend tree.id", archerDefendingTree.id
        myBlackboard = archerBlackboards[self._label]
        myBlackboard.set('against', against, archerDefendingTree.id, None)
        myBlackboard.set('shoots', shoots, archerDefendingTree.id, None)
        myBlackboard.set('castle', castle, archerDefendingTree.id, None)
        myBlackboard.set('command', self.GetCommand().GetType(), archerDefendingTree.id, None)
        archerDefendingTree.tick(self, myBlackboard)
        return


    def Kill(self, number, respawn = True):
        # Defender archers can be respawned with castle reserved units (only if respawn is True)
        # WARNING: Only one unit in the battalion is respawned
        if (number == -1):
            # The death comes by wall tile destruction. So, the respawn is not possible
            Battalion.Battalion.Kill(self, number)
        else:
            if ((not self._action.GetCommand().IsDefend()) or (not self._placement.IsInDefendingLine())):
                Battalion.Battalion.Kill(self, number)
            else:
                if (respawn and not self._army.Respawn(self)):
                    Battalion.Battalion.Kill(self, number)
                else:
                    self._isDead = False
                    self._number = 1


    def _GetClimberInAttackRange(self, frompos, castle):
        # For the defender action, returns the most suitable climber to attack from adjacent walls or towers

        # Get current construction
        dconstr = self._placement.GetDefendingConstruction()
        if (not dconstr):
            return None         # Current archer is not deployed as a defender on a castle

        factory = ConstructionFactory()
        if (factory.IsWall(dconstr)):
            # Because the climbers only climb on walls, and aiming to adjacent walls of a wall is not feasible, only check the aim to climbers of current wall
            #return dconstr.GetClosestClimberInAttackRange(posfrom = frompos, castle = castle, action = self._action)

            # WARNING: We consider that climbers of the itself wall are not avaiable to shoot due the grazing angle
            return None
        elif (factory.IsTower(dconstr)):
            # Get the nearest climber from adjacent walls
            walls = dconstr.GetAdjacentConstructions()
            target1 = None
            target2 = None

            if (factory.IsWall(walls[0])):
                target1 = walls[0].GetClosestClimberInAttackRange(posfrom = frompos, castle = castle, action = self._action)
            if (factory.IsWall(walls[1])):
                target2 = walls[1].GetClosestClimberInAttackRange(posfrom = frompos, castle = castle, action = self._action)

            if (target1 and not target2):
                return target1
            elif ((not target1) and target2):
                return target2
            elif ((not target1) and (not target2)):
                return None
            else:
                d1 = frompos.Distance(target1.GetCenterPosition())
                d2 = frompos.Distance(target2.GetCenterPosition())
                if (d1 <= d2):
                    return target1
                else:
                    return target2

if __name__ != "__main__":
    createTree()


