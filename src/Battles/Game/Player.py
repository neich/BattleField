"""
Created on Apr 26, 2013

@author: Albert Mas
"""
# from Tkinter import *

from Battles.Army import Army
from Battles.Game import Board, Results
from Battles.Utils.Geometry import Point2D, Bounding, Viewport
from Battles.Factory import *
import Battles.Utils.Message
# from Battles.Utils.Message import VERBOSE_STATISTICS
# import Battles.Utils.Settings
import Battles.Castle.CastleSet as CastleSet
import random
import timingevent as te

class PlayerData:
    """ Player data class used to specify the initial data for castle, armies and battlefield. You must inherit and redefine the methods of this class to play with
        different example data. You can inherit this class and reimplement the desired methods with other data. Next, the usage of each method
        
           _CastleData
                Defines the castle shape. You must create a 2D point list and create the curtain wall. Optionally you can define the castle orientation and towers
                Usage:
                    polyline = [Point2D(.....]
                    castle.ConstructCurtainWall(polyline)
                    castle.SetCastleOrientation(Vector2D(...))
                    castle.SetWallsResistance(....)
                    
                In addition, you can construct automatically the castle from  the city data:
                
                    city = [{row0, col0}, {row1, col1}, ...]
                    castle.WrapCity(city)
                    ...
                    
                
            _ArmyDefenderData
                Defines the army of defenders. Sets the number and type of battalions. Usage:
                    defenders.DefineBattalion("Archers", 5)
                    defenders.DefineBattalion("Cavalry", 2)
        
            
            _ArmyAttackerData
                Like previous one, but with attackers. Usage:
                    attackers.DefineBattalion("Infantry", 30)
                    attackers.DefineBattalion("Archers", 10)
                    attackers.DefineBattalion("Cannons", 3)
                
                
            _BattleFieldData
                Creates and return the battlefield (self._battlefield must be initialized with this method). Pass a 2D bounding that defines the terrain size, and the 
                cell size. Usage:
                    return Battlefield.BattleField(bound = Bounding(2000.0, 3200.0), cellsize = 100.0)
                    
                In addition you can define trenches by a list of lists of cell coordinates
                
                    trenches = [
                    [[11,29], [11,30], [11, 31], [11, 32], [11, 33], [11, 34], [12, 34], [12, 35], [12, 36]],
                    [[20,15], [21,15], [22, 15], [23, 15], [20, 16], [21, 16], [22, 17], [23, 18]]
                     ]
                    battle.SetTrenchesPositions(trenches)       

         
            _DeployAttackersData
                Deploys the attackers battalions on the battlefield. First you must specify the starting deployment battlefield 2D point. Then you can set the number of soldiers 
                lines for each cell, and the maximum number of soldiers per cell. After, you have to specify the army object and the type of battalion. Finally, specify the
                number of soldiers to deploy. If it is -1, all soldiers will be deployed. If the battalion doesn't fit on the battlefield, only will be deployed the soldiers that 
                already fits on the ground. The rest of soldiers will remain on the army. Note that an army can have undeployed soldiers that don't play if they are not deployed.
                Usage:
                    battlefield.DeployBattalion(position = Point2D(20.0, 20.0), lines = 1, maxpercell = 5, army = self.__attackers, kind = "Infantry", number = -1)
        
                Other way to deploy battalions faster, but with less control, is the next method:
                
                    battlefield.DeployBattalionRect(firstrow, firstcolumn, lastrow, lastcolumn, army, kind)
                    
                , where the first 4 parameters define a battlefield region where to deploy battalions of given kind and from given army. The region parameters are the battlefield
                cell indices. The whole region is populated with the maximum number of troops, until the army is empty
                    
        
            _DeployDefendersData
                Deploys the defenders battalions on the castle. You must specify what battalions and the number of soldiers are deployed in each construction. To do it define
                a dictionary with each desired type of battalion as key, and the number of soldiers as value. If the number is -1, all soldiers will be deployed (if they fit).
                The deployment is made on the selected castle construction element. You can specify the max number of soldiers lines per cell. Note that this is no usefull if 
                there are not enough space in the construction, such as a small wall gateway. Only those that fit in the avaiable space will be deployed. Finally, you
                can define the deployment type with Construction.CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED or CONSTRUCTION_BATTALION_DEPLOYMENT_CONSECUTIVE to sort the 
                deployments in a sparsed or consecutive way respectively. When there are more than one kind of battalions to deploy, the system first try to place the largest
                ones.
                
                    d = {"Archers": -1, "Cavalry": -1}
                    w = castle.GetWall(0)
                    w.DeployBattalions(army = defenders, battalions = d, placementtype = Construction.CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1)
        
                
            _GetConstructionHeightViews
                Defines the height views to show (related to the castle construction parts, such are the walls). You have to return a list with all desired construction parts.
                The return value must be assigned to self.
        
    """

    def __init__(self):
        pass

    def CastleData(self, castle):
        """"n = 2
        if (n == 1):
            # A simple four-walls castle 
            polyline = [Point2D(1450.0, 3000.0), Point2D(1550.0, 3000.0), Point2D(1550.0, 3100.0), Point2D(1450.0, 3100.0)]
            castle.ConstructCurtainWall(polyline)
        elif (n == 2):
            # A simple and miniature four-walls castle
            polyline = [Point2D(18.5, 60.0), Point2D(75.0, 70.0), Point2D(75.0, 90.0), Point2D(25.0, 90.0)]
            #polyline = [Point2D(25.0, 60.0), Point2D(75.0, 70.0), Point2D(90.0, 90.0), Point2D(35.0, 80.0)]
            castle.ConstructCurtainWall(polyline)
            castle.SetCastleOrientation(Vector2D(0.0, -1.0))
            castle.SetWallsResistance(100000)
            #self.__castle.ConstructCornerTowers(rounded = False)
        elif (n == 3):
            polyline = [Point2D(55.0, 80.0), Point2D(75.0, 60.0), Point2D(75.0, 90.0), Point2D(25.0, 90.0)]
            castle.ConstructCurtainWall(polyline)
            castle.SetWallsResistance(100000)
        """

    def BattleFieldData(self):
        """"n = 2
        if (n == 1):
            # A simple battlefield
            battle = Battlefield.BattleField(bound = Bounding(2000.0, 3200.0), cellsize = 100.0)
            return battle
        elif (n == 2):
            # A simple and small battlefield
            battle = Battlefield.BattleField(bound = Bounding(100.0, 100.0), cellsize = 10.0)
            return battle
        """

    def ArmyDefenderData(self, defenders):
        """"n = 2
        if (n == 2):
            # A simple defender army with only archers
            defenders.DefineBattalion("Archers", 5)
            defenders.DefineBattalion("Cavalry", 2)
            
        if (n == 3):
            defenders.DefineBattalion("Archers", 20)    
        """

    def ArmyAttackerData(self, attackers):
        """"n = 2
        if (n == 2):
            # A simple attacker force with infantry and archers
            attackers.DefineBattalion("Infantry", 30)
            attackers.DefineBattalion("Archers", 10)
            attackers.DefineBattalion("Cannons", 3)
        """

    def DeployAttackersData(self, attackers, battlefield, castle):
        """"n = 2
        if (n == 1):
            pass
        if (n == 2):
            battlefield.DeployBattalion(position = Point2D(20.0, 20.0), lines = 1, maxpercell = 5, army = attackers, kind = "Infantry", number = -1)
            battlefield.DeployBattalion(position = Point2D(30.0, 10.0), lines = 1, maxpercell = 3, army = attackers, kind = "Archers", number = -1)
            battlefield.DeployBattalion(position = Point2D(30.0, 0.0), lines = 1, maxpercell = 1, army = attackers, kind = "Cannons", number = -1)
        """

    def DeployDefendersData(self, defenders, castle):
        """"n = 2
        if (n == 1):
            pass
        if (n == 2):
            d = {"Archers": -1, "Cavalry": -1}
            w = castle.GetWall(0)
            w.DeployBattalions(army = defenders, battalions = d, placementtype = Construction.CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1)
            #w.DeployBattalions(army = defenders, battalions = [da], placementtype = Construction.CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1)
            #w.DeployBattalions(army = defenders, battalions = d, placementtype = Construction.CONSTRUCTION_BATTALION_DEPLOYMENT_CONSECUTIVE, linespercell = 1)
        if (n == 3):
            d1 = {"Archers": 5}
            d2 = {"Archers": 5}
            d3 = {"Archers": 5}
            d4 = {"Archers": 5}
            w1 = castle.GetWall(0)
            w1.DeployBattalions(army = defenders, battalions = d1, placementtype = Construction.CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1)
            w2 = self.__castle.GetWall(1)
            w2.DeployBattalions(army = defenders, battalions = d2, placementtype = Construction.CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1)
            w3 = self.__castle.GetWall(2)
            w3.DeployBattalions(army = defenders, battalions = d3, placementtype = Construction.CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1)
            w4 = self.__castle.GetWall(3)
            w4.DeployBattalions(army = defenders, battalions = d4, placementtype = Construction.CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1)
        """

    def GetConstructionHeightViews(self, castle):
        """"n = 2
        if (n == 2):
            clist = [castle.GetWall(0), castle.GetWall(1), castle.GetWall(2), castle.GetWall(3)]
            return clist
            pass
        if (n == 1):
            clist = [self.__castle.GetWall(0)]
            return clist
        """


class Player:
    """ Battle player. You can play in graphical mode for one battle, play a loop of Battles, or play a set of castle evolutions.
        Before use it you must specify the data class with initial game data (castle shape, armies and battlefield)
    
        WARNING: Only one curtain wall is allowed at the first stage -> TODO: Allow multiple initial curtain walls
     
    Attributes:
        
        castle: CastleSet object (containing just the first castle)
        attackers: Attackers army
        defenders: Defenders army
        battlefield: Battlefield where attackers are deployed against castle
        board: Battle controller
        data: PlayData class with initial castle shape, armies placements and definitions, and battlefield structure
        
        loopsforeachtest: Playing loops for each test (for each castle shape)
        
        maxevolutions: Max number of castle evolutions. -1 means the castle evolves until none evolution is possible (eternal defeat)
        evolve_tkinter: window manager used to show the castle evolutions
        evolve_canvas: canvas used to show the castle evolutions
        evolve_viewport:
        evolve_result: data to control the evolution ending and final results from evolve process  
    """

    def __init__(self, data):
        self.initData()
        self.__data = data

    def initData(self):
        self.__castle = CastleSet.CastleSet()
        self.__attackers = Army.Army(attackers=True)
        self.__defenders = Army.Army(attackers=False)
        self.__battlefield = None

        self.__board = None
        self.__loopsforeachtest = 20

        self.__isCastleConstructed = False
        self.__progress = ['attack!', 'fight!', 'aaarghh!', 'ouch!', 'booummm!', 'die!', 'fortheglory!', 'surrender!',
                           'itsagooddaytodie', 'honour!', 'defend!', 'formyking!', 'theresistanceisfutile', 'ayesir!',
                           ' #*&fu*k?#@!']

        self.__maxEvolutions = 5
        self.__evolve_tkinter = None
        self.__evolve_canvas = None
        self.__evolve_viewport = None
        self.__evolve_result = {"Evolutions": 0, "Invictus": False, "EternealDefeat": False}
        # Evolutions: number of done evolutions  Invictus: True if castle cannot be defeated   EternalDefeat: True if castle cannot evolve any more

    def _resetData(self, removeCastle=False, removeBattleField=False, resetCounters=True):
        # Resets play data to be able to run another game
        # Some data is retained, such as the castle constructions (without battalions and broken parts) and the battlefield structure. This can be changed with given 
        # input flag parameters
        # If resetCounters is true, the object counters will be initialized

        if removeCastle:
            del self.__castle
            self.__castle = CastleSet.CastleSet()
            self.__isCastleConstructed = False
        else:
            self.__castle.Reset()

        if removeBattleField and (self.__battlefield != None):
            del self.__battlefield
            self.__battlefield = None
        elif self.__battlefield != None:
            self.__battlefield.Reset()

        # All battalions become deleted    
        self.__attackers.Reset()
        self.__defenders.Reset()

        # Reset internal factory counters
        if resetCounters:
            ResetCounters()

    def SetLoopsForEachTest(self, n):
        self.__loopsforeachtest = n

    def SetMaxCastleEvolutions(self, n):
        self.__maxEvolutions = n

    def SetTimePeriod(self, time):
        Battles.Factory.Century = time

    def SetVerboseLevel(self, v):
        Battles.Utils.Message.Verbose = v

    def Play(self, speed=Battles.Utils.Settings.SETTINGS.Get_I('Game', 'speed'), showGraphics=True,
             resultStatistics=None):
        # Plays a game. Uses current battle data and shows an own view with the battle progress

        if resultStatistics == None:
            resultStatistics = Results.Results()

        # Battles.Utils.Message.Log('################################', Battles.Utils.Message.VERBOSE_RESULT)
        # Battles.Utils.Message.Log('#   Starting simulation...     #', Battles.Utils.Message.VERBOSE_RESULT)
        # Battles.Utils.Message.Log('################################', Battles.Utils.Message.VERBOSE_RESULT)

        self.CreateBattlefield()
        self.CreateCastle()
        self.BuildArmies()
        self.DeployArmies()
        self.SetupGameBoard(showGraphics)
        self.StartBattle(speed, showGraphics, resultStatistics)

    def CreateBattlefield(self):
        # Plays a game. Uses current battle data and shows an own view with the battle progress
        # Create the castle
        if not self.__isCastleConstructed:
            self.__data.CastleData(self.__castle)
            self.__isCastleConstructed = True

        # Create the battlefield
        if self.__battlefield == None:
            self.__battlefield = self.__data.BattleFieldData()

    def CreateCastle(self):
        # Deploys castle in the battlefield        
        self.__castle.DeployInBattleField(self.__battlefield)

    def BuildArmies(self):
        # Create both armies
        self.__data.ArmyAttackerData(self.__attackers)
        self.__data.ArmyDefenderData(self.__defenders)

    def getArmies(self):
        return {'attackers': self.__attackers, 'defenders': self.__defenders}

    def setArmies(self, armies):
        self.__attackers = armies['attackers']
        self.__defenders = armies['defenders']

    def DeployArmies(self, offset=None):
        # Deploys armies
        # Battles.Utils.Message.Log('   ###########################################',
        ##                           Battles.Utils.Message.VERBOSE_RESULT)
        # Battles.Utils.Message.Log('   #            Deploy Armies                #',
        ##                           Battles.Utils.Message.VERBOSE_RESULT)
        # Battles.Utils.Message.Log('   ###########################################',
        ##                           Battles.Utils.Message.VERBOSE_RESULT)
        self.__data.DeployAttackersData(self.__attackers, self.__battlefield, self.__castle, offset)
        self.__data.DeployDefendersData(self.__defenders, self.__castle)

    def SetupGameBoard(self, showGraphics=True):
        # Setup the game controller (board)
        # # Battles.Utils.Message.Log('   ###########################################',
        # #                           Battles.Utils.Message.VERBOSE_RESULT)
        # # Battles.Utils.Message.Log('   #            Setup game board             #',
        # #                           Battles.Utils.Message.VERBOSE_RESULT)
        # # Battles.Utils.Message.Log('   ###########################################',
        # #                           Battles.Utils.Message.VERBOSE_RESULT)
        self.__board = Board.Board(self.__battlefield, self.__castle, self.__defenders, self.__attackers,
                                   showBoard=showGraphics)
        clist = self.__data.GetConstructionHeightViews(self.__castle)
        self.__board.SetConstructionHeightViews(clist)

    def StartBattle(self, speed, showGraphics=True, resultStatistics=None):
        # Start the battle
        # # Battles.Utils.Message.Log('   ###########################################',
        # #                           Battles.Utils.Message.VERBOSE_RESULT)
        # # Battles.Utils.Message.Log('   #            Starting Battle              #',
        # #                           Battles.Utils.Message.VERBOSE_RESULT)
        # # Battles.Utils.Message.Log('   ###########################################',
        # #                           Battles.Utils.Message.VERBOSE_RESULT)
        self.__board.Run(stepTime=speed, resultStatistics=resultStatistics, selfloopcontrol=True)

        # Battles.Utils.Message.Log('Battle finished', Battles.Utils.Message.VERBOSE_RESULT)

    def PlayLoop(self):

        # random.seed()

        results = Results.Results()

        # Battles.Utils.Message.Log('The Battles for honor and glory have begun!!!!', Battles.Utils.Message.VERBOSE_EXTRA)

        i = 0
        while i < self.__loopsforeachtest:

            lastverbose = Battles.Utils.Message.Verbose
            Battles.Utils.Message.Verbose = Battles.Utils.Message.VERBOSE_STATISTICS

            self.Play(speed=1, showGraphics=False, resultStatistics=results)

            Battles.Utils.Message.Verbose = lastverbose

            self._resetData(removeCastle=False, removeBattleField=False, resetCounters=True)
            # sys.stdout.write('.')
            # sys.stdout.write('  ' + self.__progress[(int) (random.random() * len(self.__progress))])
            sys.stdout.write('  ' + random.choice(self.__progress))
            if ((i % 10) == 0) and (i > 0):
                sys.stdout.write('\n')

            i += 1

        sys.stdout.write('\n')
        results.CalculateResults()
        results.PrintResults()

    def DrawCastleShape(self, canvas=None, city=False, starfortress=False, resetData=True):

        # Draws the castle and city shape. If canvas is none, creates a new tkinter and canvas and executes a mainloop to show the window permanently

        # Setup window data
        if not canvas:
            loop = True
            tkr = Tk()
            canvas = Canvas(tkr, height=Battles.Utils.Settings.SETTINGS.Get_I('Game', 'WindowHeight'),
                            width=Battles.Utils.Settings.SETTINGS.Get_I('Game', 'WindowWidth'), bg="white")
            canvas.pack()
        else:
            loop = False

        # For the first evolution, we must draw the initial castle shape. We cannot do it here because the castle has not been yet initialized.
        # But we cannot do it later, because the window is invalidated only when main thread is released waiting the "after" calling (see below)
        # For that reason we  create here the castle and battlefield data
        self.__data.CastleData(self.__castle)
        self.__isCastleConstructed = True
        self.__battlefield = self.__data.BattleFieldData()
        viewport = Viewport(Bounding(Battles.Utils.Settings.SETTINGS.Get_I('Game', 'WindowWidth'),
                                     Battles.Utils.Settings.SETTINGS.Get_I('Game', 'WindowHeight')),
                            self.__battlefield.GetBounding(), Point2D(x=0.0, y=0.0))
        self.__castle.Draw(canvas, viewport, moat=False, city=city, starfortress=starfortress)

        if resetData:
            self._resetData(removeCastle=False, removeBattleField=False, resetCounters=False)

        if loop:
            mainloop()

    def DrawTerrain(self, canvas, viewport):
        # Draw the terrain relevant objects (river, ...) Remember that moat is a part of the castle

        self.__battlefield.DrawTerrain(canvas, viewport)

    def PlayCastleEvolution(self):

        # random.seed()

        self.__evolve_result["Evolutions"] = 0
        self.__evolve_result["Invictus"] = False
        self.__evolve_result["EternalDefeat"] = False

        # Setup window data
        self.__evolve_tkinter = Tk()
        self.__evolve_canvas = Canvas(self.__evolve_tkinter,
                                      height=Battles.Utils.Settings.SETTINGS.Get_I('Game', 'WindowHeight'),
                                      width=Battles.Utils.Settings.SETTINGS.Get_I('Game', 'WindowWidth'), bg="white")
        self.__evolve_canvas.pack()

        Battles.Utils.Message.Verbose = Battles.Utils.Message.VERBOSE_STATISTICS

        # Battles.Utils.Message.Log('The Battles for honor and glory have begun!!!! (castle evolution mode)',
        #                           Battles.Utils.Message.VERBOSE_EXTRA)

        # For the first evolution, we must draw the initial castle shape. We cannot do it here because the castle has not been yet initialized.
        # But we cannot do it later, because the window is invalidated only when main thread is released waiting the "after" calling (see below)
        # For that reason we  create here the castle and battlefield data
        self.__data.CastleData(self.__castle)
        self.__isCastleConstructed = True
        self.__battlefield = self.__data.BattleFieldData()
        self.__evolve_viewport = Viewport(Bounding(Battles.Utils.Settings.SETTINGS.Get_I('Game', 'WindowWidth'),
                                                   Battles.Utils.Settings.SETTINGS.Get_I('Game', 'WindowHeight')),
                                          self.__battlefield.GetBounding(), Point2D(x=0.0, y=0.0))
        self.__castle.Draw(self.__evolve_canvas, self.__evolve_viewport, moat=False, city=False, starfortress=False)
        self._resetData(removeCastle=False, removeBattleField=False, resetCounters=False)

        self.__evolve_tkinter.after(1000, self.__PlayCastleEvolution_Step)
        mainloop()

    def __PlayCastleEvolution_Step(self):

        # Battles.Utils.Message.Log('A new battle has started (castle evolution mode)',
        #                           Battles.Utils.Message.VERBOSE_EXTRA)
        results = Results.Results()
        # print "#######################################################  Player.__PlayCastleEvolution_Step !!!"

        self.__evolve_canvas.delete("all")

        # Battles.Utils.Message.Log('Current Evolution Step: ' + str(self.__evolve_result["Evolutions"]),
        #                           Battles.Utils.Message.VERBOSE_STATISTICS)

        i = 0
        while i < self.__loopsforeachtest:

            self.Play(speed=1, showGraphics=False, resultStatistics=results)
            self._resetData(removeCastle=False, removeBattleField=False, resetCounters=False)

            # sys.stdout.write('  ' + self.__progress[(int) (random.random() * len(self.__progress))])
            sys.stdout.write('  ' + random.choice(self.__progress))
            if ((i % 10) == 0) and (i > 0):
                sys.stdout.write('\n')

            i += 1

        # Gather results        
        sys.stdout.write('\n')
        results.CalculateResults()
        results.PrintResults()

        # Evolve and update evolving status
        self.__evolve_result["EternalDefeat"] = not self.__castle.Evolve(results.GetClimbedConstructions(self.__castle),
                                                                         results.GetSiegeTowersAttachments(
                                                                             self.__castle), self.__battlefield)
        self.__evolve_result["Invictus"] = results.DefendersInvictus()
        self.__evolve_result["Evolutions"] += 1

        # Show new castle
        self.__castle.Draw(self.__evolve_canvas, self.__evolve_viewport, moat=False, city=False, starfortress=False)

        # Reset data (be aware to do it after showing the evolved castle)
        self._resetData(removeCastle=False, removeBattleField=False, resetCounters=False)

        del results

        # Check termination condition
        if (((self.__maxEvolutions != -1) and (self.__evolve_result["Evolutions"] >= self.__maxEvolutions)) or
                self.__evolve_result["Invictus"] or self.__evolve_result["EternalDefeat"]):
            # Battles.Utils.Message.Log('Castle has evolved ' + str(self.__evolve_result["Evolutions"]) + ' times',
            #                           Battles.Utils.Message.VERBOSE_EXTRA)

            #if self.__evolve_result["Invictus"]:
                # Battles.Utils.Message.Log('Best castle construction ever!', Battles.Utils.Message.VERBOSE_EXTRA)
            #elif self.__evolve_result["EternalDefeat"]:
                # Battles.Utils.Message.Log('Worst castle construction ever!', Battles.Utils.Message.VERBOSE_EXTRA)

            self.__evolve_tkinter.destroy()
        else:

            self.__evolve_tkinter.after(100, self.__PlayCastleEvolution_Step)

    def GetCastle(self):
        return self.__castle

    def SetCastle(self, castle):
        # WARNING!: Use this function only if you has already a well defined castle. Otherwise, use the classical
        # Player wrapper data methods
        self.__castle = castle
        # self.__data.CastleData(self.__castle)
        self.__isCastleConstructed = True

    def GetBattlefield(self):
        return self.__battlefield

    def GetBoard(self):
        return self.__board

    def PlayOnCityEvolution(self, battleEvent, cityEvolution):
        # Plays a battle on a city evolution context. That is, the battle is executed, the results 
        # managed, and the city continues growing (other play methods work in a context
        # where when a battle or a battle loop ends, all data is destroyed, so the game ends)
        # Note that is the battleEvent object who manages the armies deployment

        # Battles.Utils.Message.Log('Starting battle...', Battles.Utils.Message.VERBOSE_RESULT)

        # Create the battlefield
        """if (self.__battlefield == None):
            self.__battlefield = self.__data.BattleFieldData()
        else:
            self.__battlefield.Reset()
        battleEvent.SetBattleFieldData(self.__battlefield)
        """
        if self.__battlefield != None:
            self.__battlefield.Reset()  # Clean the battlefield for each play
        self.__battlefield = self.__data.BattleFieldData()
        battleEvent.SetBattleFieldData(self.__battlefield)

        # Deploys castle in the battlefield
        self.__castle.DeployInBattleField(self.__battlefield)

        # Creates and deploys the defenders. Undeploy the previous ones attached to the castle. Note that is not convenient call the Reset method for the castle, so we want
        # to keep the castle structure
        self.__defenders.Reset()
        self.__castle.UnDeployBattalions()
        battleEvent.SetDeployDefenders(self.__defenders, self.__castle)

        # Creates and deploy the attackers
        self.__attackers.Reset()
        battleEvent.SetDeployAttackersData(self.__attackers, self.__battlefield, self.__castle)

        # Setup the game controller (board)
        self.__board = Board.Board(self.__battlefield, self.__castle, self.__defenders, self.__attackers,
                                   showBoard=False)

        # Bypass the view controls, if the battle must to be visualised into the castle evolution canvas, or just the ending function
        # to allow the city evolution after the battle (each battle is a new thread that has to notify his ending to the main city
        # evolution thread)

        if battleEvent.GetNSimulations() == 1:
            self.__board.BypassViewData(battleEvent.tkinter, battleEvent.canvas, battleEvent.viewport,
                                        battleEvent.endcontrol)
        else:
            self.__board.SetExternalEndControl(battleEvent.endcontrol)

        # Start the set of battle simulations
        # If battleEvent has the flag 'RepeatUntilDefendersWin' activated, the whole simulation will repeat until the castle is invictus or good enough
        end = False
        while not end:
            end = True

            results = Results.Results()

            print "   ############################################################"
            print "   # going to perform " + str(battleEvent.GetNSimulations()) + " battle simulations!!"
            print "   ############################################################"
            te.timing_event_start('Simulation batch')
            loop = 0
            while loop < battleEvent.GetNSimulations():
                """
                print "Defenders: " + self.__defenders.GetString()
                print "Attackers: " + self.__attackers.GetString()
                """
                # print "(" + str(loop) + ")  " + random.choice(self.__progress)
                if ((loop % 10) == 0) and (loop > 0):
                    sys.stdout.write('\n')

                # Start the battle
                self.__board.Run(stepTime=Battles.Utils.Settings.SETTINGS.Get_I('Game', 'speed'),
                                 resultStatistics=results, selfloopcontrol=False)

                if battleEvent.GetNSimulations() > 1:
                    # If there are only one battle, a new thread is launched, and the execution continues here. So, we have to avoid
                    # the data reset
                    self.__battlefield.Reset()
                    battleEvent.SetBattleFieldData(self.__battlefield)
                    self.__castle.UnDeployBattalions()
                    self.__castle.Respawn()
                    self.__castle.DeployInBattleField(self.__battlefield)
                    self.__defenders.Reset()
                    battleEvent.SetDeployDefenders(self.__defenders, self.__castle)
                    self.__attackers.Reset()
                    battleEvent.SetDeployAttackersData(self.__attackers, self.__battlefield, self.__castle)

                loop += 1

            # # Battles.Utils.Message.Log('Battle finished', Battles.Utils.Message.VERBOSE_RESULT)

            if battleEvent.GetNSimulations() > 1:
                results.CalculateResults()
                results.PrintResults()

                # Decide which kind of castle evolution perform from the statistical results
                if results.DefendersInvictus():
                    pass
                    # Battles.Utils.Message.Log('Current castle design is perfect! None evolution is needed',
                    #                           Battles.Utils.Message.VERBOSE_STATISTICS)
                elif results.MeanDefendersWin():
                    pass
                    # Battles.Utils.Message.Log('Current castle design is good enough in mean. None evolution is needed',
                    #                           Battles.Utils.Message.VERBOSE_STATISTICS)
                else:
                # Battles.Utils.Message.Log('Current castle design should be improved',
                    #                           Battles.Utils.Message.VERBOSE_STATISTICS)

                    """
                    # Get the weakest wall and attack point
                    wall = self.__castle.GetConstructionByLabel(results.GetWeakestConstruction())
                    if (not wall):
                        print "ERROR: Weakest wall does not exist!"
                        return


                    #weakpoint = results.GetWeakestPoint()

                    # Try to evolve with the weakest points, choosing the weakest ones first
                    weakpointlist = results.GetSortedWeakPointList()

                    evolved = False
                    wpi = 0
                    while (not evolved and (wpi < len(weakpointlist))):
                        if (self.__castle.EvolveWall(wall, weakpointlist[wpi]["weakPoint"], battleEvent.canvas)):
                            evolved = True

                        else:
                            wpi += 1
                    """
                    # Battles.Utils.Message.Log('Starting upgrading things ....',
                    #                           Battles.Utils.Message.VERBOSE_STATISTICS)
                    # Instead of evolving only the weakest construction for each play, evolve the weak point of each construction
                    weakpointlist = results.GetSortedWeakPointList()
                    evolved = False
                    wpi = 0
                    while wpi < len(weakpointlist):
                        wall = self.__castle.GetConstructionByLabel(weakpointlist[wpi]["label"])
                        if not wall:
                            print "ERROR: Weakest wall " + weakpointlist[wpi]["label"] + " does not exist!"
                        else:
                            if self.__castle.EvolveWall(wall, weakpointlist[wpi]["weakPoint"], battleEvent.canvas):
                                evolved = True
                        wpi += 1
                    # Battles.Utils.Message.Log('Ending upgrading things ....', Battles.Utils.Message.VERBOSE_STATISTICS)

                    castleexpanded = False
                    if not evolved:
                        # Battles.Utils.Message.Log('Cannot upgrade. Evolving the whole city',
                        #                           Battles.Utils.Message.VERBOSE_STATISTICS)

                        if cityEvolution.AllowExpansionByHistory() and battleEvent.AllowCastleExpansion():
                            cityEvolution.ExpandCastle(frombattle=True, battlefield=self.__battlefield)
                        else:
                            pass
                            # Battles.Utils.Message.Log("City expansion cancelled (from battle) due a previous one",
                            #                           Battles.Utils.Message.VERBOSE_RESULT)

                        castleexpanded = True  # Finish the battle simulation on castle expansion

                    else:
                        self.__castle.CreateCastleShape()

                        # Battles.Utils.Message.Log('A new tower has been inserted, or an old one has been upgraded',
                        #                           Battles.Utils.Message.VERBOSE_STATISTICS)

                    cityEvolution.DrawCastle(starfortress=False)

                    # Repeat the whole simulation until the castle is good enough
                    if battleEvent.IsRepeatUntilDefendersWin() and not castleexpanded:
                        end = False

                        self.__battlefield.Reset()
                        battleEvent.SetBattleFieldData(self.__battlefield)
                        self.__castle.UnDeployBattalions()
                        self.__castle.Respawn()
                        self.__castle.DeployInBattleField(self.__battlefield)
                        self.__defenders.Reset()
                        battleEvent.SetDeployDefenders(self.__defenders, self.__castle)
                        self.__attackers.Reset()
                        battleEvent.SetDeployAttackersData(self.__attackers, self.__battlefield, self.__castle)

            te.timing_event_stop('Simulation batch', 'Finished simulation batch of {0}'.format(battleEvent.GetNSimulations()))