"""
Created on May 4, 2013

@author: Albert Mas
"""
from Tkinter import *
from Battles.Factory import ArmyFactory

from Battles.Utils.Geometry import Point2D, Bounding, Viewport, GPCWrapper
from Results import *
import Battles.Utils.Message as Message
import Battles.Utils.Settings
from Battles.Army.Action import Command


class Board:
    """ Canvas board. Displays the board and controls the game
    
    Attributes:
        battlefield: Battlefield object
        castle: Castle object
        defenders: Army of defenders
        attackers: Army of attackers
        stepStatus: Current status of the game. Used for internal game control
        shoots: Internal list of shoots used in each game step
        heightViews: Internal list with all desired castle height views. 
        showBoard: True for graphics mode
        resultStatistics: Used to store results to make future statistics
        bypassedViewData: True if view data structures are given externaylly
        endControl: object to manage the battle ending. It must has implemented the method EndBattle()
    """

    # Play current status
    __STEP_INIT = 0
    __STEP_ATTACKERS_ATTACK = 1
    __STEP_ATTACKERS_MOVE = 2
    __STEP_DEFENDERS_ATTACK = 3
    __STEP_DEFENDERS_MOVE = 4

    # List with objects that have to be redrawn asynchronously. Its usually populated in those code places where there isnt the canvas object or shoot structure
    redrawObjects = []

    def __init__(self, battlefield, castle, defenders, attackers, showBoard=True, verbose=True):
        self.__battleField = battlefield
        self.__castle = castle
        self.__defenders = defenders
        self.__attackers = attackers

        self.__speed = Battles.Utils.Settings.SETTINGS.Get_I('Game', 'speed')

        self.__showBoard = showBoard

        self.__bypassedViewData = False
        self.__endControl = None

        if self.__showBoard:
            self.__masterTK = Tk()
            self.__canvas = Canvas(self.__masterTK,
                                   height=Battles.Utils.Settings.SETTINGS.Get_I('Game', 'WindowHeight'),
                                   width=Battles.Utils.Settings.SETTINGS.Get_I('Game', 'WindowWidth'), bg="white")
            self.__canvas.pack()

            self.__viewport = Viewport(Bounding(Battles.Utils.Settings.SETTINGS.Get_I('Game', 'ViewportWidth'),
                                                Battles.Utils.Settings.SETTINGS.Get_I('Game', 'ViewportHeight')),
                                       self.__battleField.GetBounding(), Point2D(x=0.0, y=0.0))

            self.__battleField.Draw(self.__canvas, self.__viewport,
                                    showgrid=Battles.Utils.Settings.SETTINGS.Get_B(category='Game', tag='ShowGrid'))
            self.__castle.Draw(self.__canvas, self.__viewport, moat=True, city=True, starfortress=False)
            self.__attackers.Draw(self.__canvas, self.__viewport)
            self.__defenders.Draw(self.__canvas, self.__viewport)

            self.__shoots = []
            self.__heightViews = []

            self.__canvas.bind("<1>", lambda event: self.__canvas.focus_set())
            self.__canvas.bind("<Key>", self.KeyPressed)

        else:
            self.__masterTK = None
            self.__canvas = None
            self.__viewport = None
            self.__shoots = None
            self.__heightViews = None

        self.__stepStatus = self.__STEP_INIT
        self.__roundsCounter = 0
        self.__resultStatistics = None

    def BypassViewData(self, tk, canvas, viewport, endcontrol):

        self.__bypassedViewData = True

        self.__masterTK = tk
        self.__canvas = canvas
        self.__viewport = viewport
        self.__showBoard = True

        self.__endControl = endcontrol

        self.__shoots = []

    def SetExternalEndControl(self, endcontrol):
        # Defines an external object to call when battle finishes. 
        # This class MUST have the EndBattle() method

        self.__endControl = endcontrol

    def SetConstructionHeightViews(self, clist):
        # Set the castle construcion elements to show in height view

        if (self.__showBoard and clist):
            for c in clist:
                hv = HeightView(c, self.__attackers)
                hv.Draw()
                self.__heightViews.append(hv)

    def Run(self, stepTime=Battles.Utils.Settings.SETTINGS.Get_I('Game', 'speed'), resultStatistics=None,
            selfloopcontrol=True):

        self.__speed = stepTime
        self.__resultStatistics = resultStatistics
        self.__roundsCounter = 0

        if (self.__showBoard):
            # Graphic mode loop

            # Draw all again to avoid some refresh and initilization problems
            self.__battleField.Draw(self.__canvas, self.__viewport,
                                    showgrid=Battles.Utils.Settings.SETTINGS.Get_B('Game', 'ShowGrid'))

            self.__castle.Draw(self.__canvas, self.__viewport, moat=True, city=True, starfortress=False)
            self.__attackers.Draw(self.__canvas, self.__viewport)
            self.__defenders.Draw(self.__canvas, self.__viewport)
            self.__castle.DrawReservedSoldiers(self.__canvas, self.__viewport, self.__defenders)

            self.__masterTK.after(self.__speed, self.Step)
            if selfloopcontrol:
                # =============================================
                # Main loop (for TK)!!! -> calls self.step()...
                # =============================================
                mainloop()

        else:
            # =============================
            # Non-graphic mode main loop!!!
            # =============================
            while (not self.IsGameOver()):
                self.Step()
            # self.__endControl.EndBattle()
        return

        # =============================================================================================================

    # This is the function called at each iteration of the game, either by the while (in non-graphic mode) or by TK
    # =============================================================================================================
    def Step(self):
        # Play step        
        if (self.__stepStatus == self.__STEP_INIT):
            self.__stepStatus = self.__STEP_ATTACKERS_ATTACK

        if (self.__showBoard):
            # Remove previous shoots
            for s in self.__shoots:
                s.Clean(self.__canvas)
            self.__shoots = []

            # List of invalidated objects (must be redrawn), except the objects related to shoots
            invalidatedList = []
        else:
            invalidatedList = None

        if (self.__stepStatus == self.__STEP_ATTACKERS_ATTACK):
            # Attackers attacking
            Message.Log('Attackers attacking')
            self.__attackers.Attack(self.__defenders, self.__castle, self.__shoots)
            # Next state
            self.__stepStatus = self.__STEP_DEFENDERS_ATTACK
        elif (self.__stepStatus == self.__STEP_DEFENDERS_ATTACK):
            # Defenders attacking
            Message.Log('Defenders attacking')
            self.__defenders.Defend(self.__attackers, self.__defenders, self.__battleField, self.__shoots,
                                    self.__castle)
            # Next state
            self.__stepStatus = self.__STEP_ATTACKERS_MOVE
        elif (self.__stepStatus == self.__STEP_ATTACKERS_MOVE):
            # Attackers move
            Message.Log('Attackers moving')
            self.__attackers.Move(self.__castle, self.__defenders, self.__battleField, invalidatedList)
            # Next state
            self.__stepStatus = self.__STEP_DEFENDERS_MOVE
        elif (self.__stepStatus == self.__STEP_DEFENDERS_MOVE):
            # Defenders move
            Message.Log('Defenders moving')
            # self.__defenders.Move(self.__castle, self.__attackers, self.__battleField, invalidatedList)
            # Next state
            self.__stepStatus = self.__STEP_ATTACKERS_ATTACK
            self.__roundsCounter += 1
            Message.Log('ROUND ' + str(self.__roundsCounter))
            # Show progress
            sys.stdout.write('.')
            if (((self.__roundsCounter % 20) == 0) and (self.__roundsCounter > 0)):
                sys.stdout.write('\n')
                # Check the castle defeat condition. If there are multiple castles, the defeated castle must to be converted to a trench zone, and all references to this castle must to
        # be removed. If there are only one castle, or all castles have been defeated, let the game to finish normally (via IsGameOver method)
        # EDIT: Not yet implmeneted. Keep it commented to get some results

        """defeatedCastle = self.__castle.GetActiveDefeatedCastle()
        if ((self.__castle.GetNCastles() > 1) and (defeatedCastle != None)):
            self.DemolishCastle(defeatedCastle)
        """
        if (self.__showBoard):
            # Draw the shoots
            if (self.__shoots):
                for s in self.__shoots:
                    s.Draw(self.__canvas, self.__viewport)
                    # Update the invalidated objects
            for o in invalidatedList:
                o.RedrawAttacked(self.__canvas, self.__viewport)
            # Update the height views
            if (self.__heightViews):
                for h in self.__heightViews:
                    h.Draw()
            # Redraw asynchronously (not thread-based, just offline from draw classical order) some objects
            for r in Board.redrawObjects:
                r.RedrawAttacked(self.__canvas, self.__viewport)
            Board.redrawObjects = []
            # Update the castle reserves
            self.__castle.DrawReservedSoldiers(self.__canvas, self.__viewport, self.__defenders)
            # Game over check
            if (not self.IsGameOver()):
                self.__masterTK.after(self.__speed, self.Step)
            else:
                if (self.__bypassedViewData):
                    self.__endControl.EndBattle()
                else:
                    self.__masterTK.destroy()

    def collectCastleData(self):
        defendersDetails = {}
        for c in self.__castle.GetCastlesList():
            for b in c.GetAllBattalions():
                armyType = b._label.split('_')[0]
                # print armyType, b.GetNumber()
                if armyType in defendersDetails:
                    defendersDetails[armyType] += b.GetNumber()
                else:
                    defendersDetails[armyType] = b.GetNumber()
        return defendersDetails

    def collectAttackersData(self):
        attackersDetails = {}
        for kb in self.__attackers.getBattalions():
            bats = self.__attackers.getBattalions()[kb]
            for b in bats.battalions:
                armyType = b._label.split('_')[0]
                # print armyType, b.GetNumber()
                if armyType in attackersDetails:
                    attackersDetails[armyType] += b.GetNumber()
                else:
                    attackersDetails[armyType] = b.GetNumber()
        return attackersDetails

    def collectEndGameData(self, result):
        result.SetRounds(self.__roundsCounter)
        print
        # print "========================================= Castle"
        defendersDetails = self.collectCastleData()
        result.addExtraInfo("defenders", defendersDetails)
        # print "========================================= attackers"
        attackersDetails = self.collectAttackersData()
        result.addExtraInfo("attackers", attackersDetails)
        # print "========================================="
        self.__resultStatistics.AddResult(result)
        # self.__resultStatistics.PrintResults('(Castle Defeated: Attackers victory)')
        # self.__resultStatistics.PrintResults('(Defenders victory)')

    def IsGameOver(self):
        # Returns true if game is finished

        if (self.__castle.IsDefeated()):
            result = self.__castle.GetDefeatReason()
            self.collectEndGameData(result)
            Message.Log('Attackers victory!!!', Message.VERBOSE_RESULT)
            Message.Log('Reason: %s' % (result.GetStringReason()), Message.VERBOSE_RESULT)
            Message.Log('Spent time: %d rounds' % (self.__roundsCounter), Message.VERBOSE_RESULT)
            return True
        elif (self.__attackers.IsDefeated(defenders=False)):
            result = ResultData(RESULT_DEFENDERS_VICTORY_ALLDEAD)
            self.collectEndGameData(result)
            Message.Log('Defenders victory!!!', Message.VERBOSE_RESULT)
            Message.Log('Reason: %s' % (result.GetStringReason()), Message.VERBOSE_RESULT)
            Message.Log('Spent time: %d rounds' % (self.__roundsCounter), Message.VERBOSE_RESULT)
            return True
        else:
            return False

        # The defenders army defeat is deactivated due it doesnt offer any statistical information about any castle weak point
        """
        elif (self.__defenders.IsDefeated(defenders = True)):
            result = ResultData(RESULT_ATTACKERS_VICTORY_ALLDEAD)
            result.SetRounds(self.__roundsCounter)
            self.__resultStatistics.AddResult(result)
            
            Message.Log('Attackers victory!!!', Message.VERBOSE_RESULT)
            Message.Log('Reason: %s' % (result.GetStringReason()), Message.VERBOSE_RESULT)
            Message.Log('Spent time: %d rounds' % (self.__roundsCounter), Message.VERBOSE_RESULT)
            return True
        """

    def DemolishCastle(self, castle):
        # Given castle must be demolished. This means that it is converted to a moat zone, and all references to it have to be removed

        if (castle == None):
            return

        # Kill all castle defenders
        # NOTE: This is not the most smart way to do it, but it assure that all references are removed in the same way than a defender is killed, assuring more stability
        dlist = castle.GetAllBattalions()
        for d in dlist:
            self.__defenders.RemoveBattalion(battalion=d, respawn=False)

        # Update attackers
        # Updating archers is not required due they search for the closest castle part to shoot each round. When the defeated castle will "disappear", they will search the other
        #   candidates.
        # Updating cannons is not required due they search for the closest castle wall to shoot each round. Because the cannons cannot move, they will remain in this place trying
        #   to shoot to the closest wall.
        # Updating siege towers imply to deactivate all of them, so they cannot change its path once they have start the movement. The turtle units will be converted to normal
        #   infantry battalions
        # Updating infantry is more complex:
        #   Infantry on battlefield: Not required due they search for the most reachable wall to climb each round
        #   Climbing infantry: All climbing battalion must to be deployed again in the battlefield. The stairs must to be destroyed

        factory = ArmyFactory()
        wlist = castle.GetWallsList()

        # Siege towers
        siegetowers = self.__attackers.GetBattalionType('SiegeTowers')
        for s in siegetowers:
            if (s.GetTargetWall() in wlist):
                self.__attackers.RemoveBattalion(battalion=s)

        # Climbers
        # Get the climbers using the stairs
        for w in wlist:
            stairs = w.GetStairs()
            for s in stairs:
                climbers = s.GetClimbers()
                waiting = s.GetWaitingBattalion()

                # To make it easy, just get the number of soldiers of both and create a new battalion in the same place (removing the climbers and waiting battalion before)

                # Get the number of soldiers and the current battlefield cell
                nsoldiers = len(climbers)
                if (waiting != None):
                    nsoldiers = waiting.GetNumber()
                    cell = waiting.GetBattlefieldCell()
                elif (len(climbers) > 0):
                    cell = climbers[0].GetBattlefieldCell()

                for c in climbers:
                    self.__attackers.RemoveBattalion(battalion=c)
                if (waiting != None):
                    self.__attackers.RemoveBattalion(battalion=waiting)

                w.RemoveClimbingStair(s)

                if (cell != None):
                    b = factory.newBattalion(self.__attackers, 'Infantry', nsoldiers)
                    b.AssignToCell(cell)
                    self.__attackers.InsertBattalion(b)
                    b.SetCommand(Command(Command.GOTO_CASTLE))

        # Castle demolishion
        # Get the castle polygon shape and check what battlefield cells are inside.
        # Reduce the battlefield cells number using the castle bounding box
        shape = castle.GetJoinsPolygon()
        gpc = GPCWrapper()
        plist = shape.GetPointsList()

        bbox = shape.GetBoundingBox()
        cells = self.__battleField.GetCellsRange(bbox)
        insidecells = []
        for c in cells:
            if (gpc.IsInside(plist, c.center)):
                insidecells.append(c)
        self.__battleField.SetTrenchesCells(cells=insidecells, append=True)

        # Finally, set the castle as defeated in the castle set
        self.__castle.SetDefeatedCastle(castle)

    # Foo code for debug purposes
    # Makes a simple zoom. Be aware, this is a foo code. It doesnt update the changing elemenets...
    def KeyPressed(self, event):
        if (event.char == "+"):
            self.__viewport.Zoom(1.5)
            offset = self.__viewport.GetOffset()
            self.__canvas.scale(ALL, offset.x, offset.y, 1.5, 1.5)
        elif (event.char == "-"):
            self.__viewport.Zoom(0.8)
            offset = self.__viewport.GetOffset()
            self.__canvas.scale(ALL, offset.x, offset.y, 0.8, 0.8)


class HeightView:
    """ View class to paint the castle contruction height views
    
    Attributes:
        window: Child window (height view)
        canvas: Internal canvas
        viewport: Internal viewport
        construction: Construction to display
        enemyarmy: Enemy army (used to get extra data to display on construction)
    """

    def __init__(self, construction, enemyarmy):
        self.__construction = construction

        self.__view = Toplevel()
        self.__canvas = Canvas(self.__view, height=Battles.Utils.Settings.SETTINGS.Get_I('Game', 'HeightViewHeight'),
                               width=Battles.Utils.Settings.SETTINGS.Get_I('Game', 'HeightViewWidth'), bg="white")
        self.__canvas.pack()
        self.__view.title(construction.GetLabel())

        self.__enemyarmy = enemyarmy

        # Creates the viewport
        cb = self.__construction.GetBoundingHeightView()
        self.__viewport = Viewport(viewSize=Bounding(Battles.Utils.Settings.SETTINGS.Get_I('Game', 'HeightViewWidth'),
                                                     Battles.Utils.Settings.SETTINGS.Get_I('Game', 'HeightViewHeight')),
                                   worldSize=cb)
        # Center view (approx)
        center = Point2D(cb.length * 0.05, cb.width * 0.1)
        self.__viewport.SetOffset(center)

        self.__construction.DrawHeightView(self.__enemyarmy, self.__canvas, self.__viewport)

    def Draw(self):
        self.__construction.DrawHeightView(self.__enemyarmy, self.__canvas, self.__viewport)


class Shoot:
    """ Shoot class. It represents the attack from any troop element
    
    Attributes:
        origin: shoot origin 2D point
        destination : shoot origin 2D point
        success: True or False if shoot hits or fails
        attackerType: Class name of attacker
        paintObj: internal tkinter object used to draw the shoot. Stored to allow erasing it
        target: target object
        army: 0 for a shoot from attackers, and 1 for a shoot from defenders (see constants bellow)
    """

    # TYPE OF ARMY SHOOTS
    SHOOT_FROM_ATTACKER = 0
    SHOOT_FROM_DEFENDER = 1

    def __init__(self, origin, destination, success, attackertype, targetObj, armytype):

        self.__origin = origin
        self.__destination = destination
        self.__success = success
        self.__attackertype = attackertype
        self.__paintObj = None
        self.__target = targetObj
        self.__armyType = armytype

    def Draw(self, canvas, viewport):

        p1 = viewport.W2V(self.__origin)
        p2 = viewport.W2V(self.__destination)

        if (self.__attackertype == "Archers"):

            if (self.__success):
                if (self.__armyType == Shoot.SHOOT_FROM_ATTACKER):
                    color = "Yellow"
                elif (self.__armyType == Shoot.SHOOT_FROM_DEFENDER):
                    color = "orange"
                else:
                    color = "black"

                self.__paintObj = canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill=color)

            else:
                if (self.__armyType == Shoot.SHOOT_FROM_ATTACKER):
                    color = "Thistle"
                elif (self.__armyType == Shoot.SHOOT_FROM_DEFENDER):
                    color = "yellow green"
                else:
                    color = "black"

                self.__paintObj = canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill=color)


        elif (self.__attackertype == "Cannons"):

            if (self.__success):
                if (self.__armyType == Shoot.SHOOT_FROM_ATTACKER):
                    color = "Yellow"
                elif (self.__armyType == Shoot.SHOOT_FROM_DEFENDER):
                    color = "orange"
                else:
                    color = "black"

                self.__paintObj = canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill=color, width=5)

            else:

                if (self.__armyType == Shoot.SHOOT_FROM_ATTACKER):
                    color = "Thistle"
                elif (self.__armyType == Shoot.SHOOT_FROM_DEFENDER):
                    color = "yellow green"
                else:
                    color = "black"

                self.__paintObj = canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill=color, width=5)

        if (self.__success):
            self.__target.RedrawAttacked(canvas, viewport)

    def Clean(self, canvas):
        if (self.__paintObj != None):
            canvas.delete(self.__paintObj)
