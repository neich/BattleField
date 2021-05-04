"""
         !!! DONT USE THIS CLASS. USED ONY FOR DEBUG PURPOSES !!!!
"""




"""
Main file that shows how to use the Battles code
You must create a class that inherits the PlayData class and implement the example data methods
Then, just choose the desired play mode (one game, loop with one castle construction, or global optimization)
"""
from Battles.Game.Player import Player, PlayerData
from Battles.Utils.Geometry import Point2D, Bounding, Vector2D
from Battles.Battlefield import Battlefield
from Battles.Utils.Message import *
from Battles.Army.Action import Command
import Battles.Utils.Settings




class Example_1(PlayerData):
    
    def __init__(self):
        PlayerData.__init__(self)
    
    def CastleData(self, castle):
        # A simple and miniature four-walls castle
        polyline = [Point2D(18.5, 60.0), Point2D(75.0, 70.0), Point2D(75.0, 90.0), Point2D(25.0, 90.0)]
        #polyline = [Point2D(25.0, 60.0), Point2D(75.0, 70.0), Point2D(90.0, 90.0), Point2D(35.0, 80.0)]
        castle.ConstructCurtainWall(polyline)
        castle.SetCastleOrientation(Vector2D(0.0, -1.0))
        castle.SetWallsResistance(100000)
        castle.Evolve(climbings = None, attachedsiegetowers = None, battlefield = None)
        #self.__castle.ConstructCornerTowers(rounded = False)
    

    def BattleFieldData(self):
        # A simple and small battlefield
        battle = Battlefield.BattleField(bound = Bounding(100.0, 100.0), cellsize = 10.0)
        return battle


    def ArmyDefenderData(self, defenders):
        # A simple defender army with only archers
        defenders.DefineBattalion("Archers", 200)
        #defenders.DefineBattalion("Cavalry", 2)

    
    
    def ArmyAttackerData(self, attackers):
        # A simple attacker force with infantry and archers
        attackers.DefineBattalion("Infantry", 250)
        attackers.DefineBattalion("Archers", 50)
        attackers.DefineBattalion("Cannons", 3)
            
 
    
    
    def DeployAttackersData(self, attackers, battlefield, castle):
        battlefield.DeployBattalion(position = Point2D(00.0, 20.0), lines = 1, maxpercell = -1, army = attackers, kind = "Infantry", number = -1)
        battlefield.DeployBattalion(position = Point2D(10.0, 10.0), lines = 1, maxpercell = 5, army = attackers, kind = "Archers", number = -1)
        battlefield.DeployBattalion(position = Point2D(30.0, 0.0), lines = 1, maxpercell = 1, army = attackers, kind = "Cannons", number = -1)

    
    
    def DeployDefendersData(self, defenders, castle):
        d = {"Archers": -1}#, "Cavalry": -1}
        castle.GetWall(0).DeployBattalions(army = defenders, battalions = d, placementtype = CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1)
        castle.GetWall(1).DeployBattalions(army = defenders, battalions = d, placementtype = CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1)
        castle.GetWall(2).DeployBattalions(army = defenders, battalions = d, placementtype = CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1)
        castle.GetWall(3).DeployBattalions(army = defenders, battalions = d, placementtype = CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1)
        #dt = {"Archers": -1}
        castle.GetTower(0).DeployBattalions(army = defenders, battalions = d, placementtype = CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1)
        castle.GetTower(1).DeployBattalions(army = defenders, battalions = d, placementtype = CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1)
        castle.GetTower(2).DeployBattalions(army = defenders, battalions = d, placementtype = CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1)
        castle.GetTower(3).DeployBattalions(army = defenders, battalions = d, placementtype = CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1)
  
    
    def GetConstructionHeightViews(self, castle):
        clist = [castle.GetWall(0), castle.GetWall(1), castle.GetWall(2), castle.GetWall(3)]
        return clist
    




class Example_2(Example_1):
    
    def __init__(self):
        Example_1.__init__(self)


    def BattleFieldData(self):
        battle = Battlefield.BattleField(bound = Bounding(500.0, 500.0), cellsize = 10.0)
        trenches = [
                    [[11,29], [11,30], [11, 31], [11, 32], [11, 33], [11, 34], [12, 34], [12, 35], [12, 36]],
                    [[20,7], [21,7], [22, 7], [23, 7], [20, 8], [21, 8], [22, 8], [23, 8]],
                    [[8, 8], [8, 9]],
                    [[35, 30], [35, 31], [36, 30], [37, 30], [37, 33], [35, 34], [35, 35], [37, 31]], 
                    [[30, 37], [29, 38], [28, 39], [27, 40], [26, 40], [25, 40], [24, 40]]
                     ]
        battle.SetTrenchesPositions(trenches)       
        
        return battle


    def CastleData(self, castle):
        # Define the city
        city = [[200.0, 230.0], [230.0, 231.0], [200.0, 292.0], [230.0, 233.0], [230.0, 234.0], [243.0, 234.0], [330.0, 250.0], [245.0, 333.0], [300.0, 304.0], [238.0, 230.0], [243.0, 260.0]]
        castle.WrapOldCity(city = city, margin = 20, battlefieldcenter = Point2D(250.0, 250.0))
        castle.SetWallsResistance(100000)
        castle.SetCastleOrientation(Vector2D(0.0, -1.0))
        castle.Evolve(climbings = None, attachedsiegetowers = None, battlefield = None)

        # Sets the moat object. Note that the moat geometry isn't yet calcualted until the castle is deployed in the battlefield
        castle.SetMoat(thickness = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Moat', 'Depth') * 1, depth = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Moat', 'Depth'), haswater = False)

        

    def ArmyDefenderData(self, defenders):
        defenders.DefineBattalion("Archers", 800)
 
 
    def DeployDefendersData(self, defenders, castle):
        d = {"Archers": -1}
        castle.DeployBattalions(army = defenders, battalions = d, placementtype = CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1, command = Command.DEFEND_CASTLE)
        Log('Defenders deployed: ' + defenders.GetString(), VERBOSE_RESULT)


    def ArmyAttackerData(self, attackers):
        # A simple attacker force with infantry and archers
        attackers.DefineBattalion("Infantry", 7000)
        attackers.DefineBattalion("Archers", 300)
        attackers.DefineBattalion("SiegeTowers", 3)
        attackers.DefineBattalion("Cannons", 10)


    def DeployAttackersData(self, attackers, battlefield, castle):
        battlefield.DeployBattalionRect(firstrow = 5, firstcolumn = 3, lastrow = 5, lastcolumn = 46, army = attackers, kind = "Infantry", maxPerCell = -1, command = Command.GOTO_CASTLE)
        battlefield.DeployBattalionRect(firstrow = 44, firstcolumn = 3, lastrow = 44, lastcolumn = 46, army = attackers, kind = "Infantry", maxPerCell = -1, command = Command.GOTO_CASTLE)
        battlefield.DeployBattalionRect(firstrow = 4, firstcolumn = 4, lastrow = 45, lastcolumn = 4, army = attackers, kind = "Infantry", maxPerCell = -1, command = Command.GOTO_CASTLE)
        battlefield.DeployBattalionRect(firstrow = 4, firstcolumn = 45, lastrow = 45, lastcolumn = 45, army = attackers, kind = "Infantry", maxPerCell = -1, command = Command.GOTO_CASTLE)
        
        battlefield.DeployBattalionRect(firstrow = 1, firstcolumn = 12, lastrow = 1, lastcolumn = 36, army = attackers, kind = "Archers", maxPerCell = 3, command = Command.ATTACK_CASTLE)
        battlefield.DeployBattalionRect(firstrow = 48, firstcolumn = 12, lastrow = 48, lastcolumn = 36, army = attackers, kind = "Archers", maxPerCell = 3, command = Command.ATTACK_CASTLE)
        battlefield.DeployBattalionRect(firstrow = 12, firstcolumn = 0, lastrow = 36, lastcolumn = 0, army = attackers, kind = "Archers", maxPerCell = 3, command = Command.ATTACK_CASTLE)
        battlefield.DeployBattalionRect(firstrow = 12, firstcolumn = 49, lastrow = 36, lastcolumn = 49, army = attackers, kind = "Archers", maxPerCell = 3, command = Command.ATTACK_CASTLE)
        
        Log('Attackers deployed: ' + attackers.GetString(), VERBOSE_RESULT)

        battlefield.DeploySiegeTowers(army = attackers, maxDeployed = -1, castle = castle, command = Command.ATTACK_CASTLE)

    def GetConstructionHeightViews(self, castle):
        clist = castle.GetWallsList()
        return clist



class Example_3(Example_2):
    def DeployAttackersData(self, attackers, battlefield, castle):
        battlefield.DeployBattalionRect(firstrow = 3, firstcolumn = 3, lastrow = 3, lastcolumn = 46, army = attackers, kind = "Infantry", maxPerCell = -1, command = Command.GOTO_CASTLE)
        battlefield.DeploySiegeTowers(army = attackers, maxDeployed = 1, castle = castle, command = Command.ATTACK_CASTLE)

        Log('Attackers deployed: ' + attackers.GetString(), VERBOSE_RESULT)


class Example_4(Example_2):
    def DeployAttackersData(self, attackers, battlefield, castle):

        battlefield.DeployBattalionRect(firstrow = 3, firstcolumn = 10, lastrow = 3, lastcolumn = 10, army = attackers, kind = "Infantry", maxPerCell = 20, command = Command.GOTO_CASTLE)        
        battlefield.DeployBattalionRect(firstrow = 3, firstcolumn = 11, lastrow = 3, lastcolumn = 11, army = attackers, kind = "Infantry", maxPerCell = -1, command = Command.STAY)        




class Example_5(Example_2):
    def BattleFieldData(self):
        battle = Battlefield.BattleField(bound = Bounding(500.0, 500.0), cellsize = 10.0)
        trenches = [
                    [[9,24], [9,25], [9, 26], [9, 27], [9, 28], [9, 29], [10, 29], [10, 30], [10, 31]]
                     ]
        battle.SetTrenchesPositions(trenches)       
        
        return battle
    
    def DeployAttackersData(self, attackers, battlefield, castle):
        battlefield.DeployBattalionRect(firstrow = 3, firstcolumn = 10, lastrow = 3, lastcolumn = 30, army = attackers, kind = "Archers", maxPerCell = 15, command = Command.ATTACK_CASTLE)        
        battlefield.DeploySiegeTowers(army = attackers, maxDeployed = 1, castle = castle, command = Command.ATTACK_CASTLE)



class Example_6(Example_2):
    
    
       
    def DeployAttackersData(self, attackers, battlefield, castle):
        battlefield.DeployBattalionRect(firstrow = 3, firstcolumn = 3, lastrow = 3, lastcolumn = 46, army = attackers, kind = "Infantry", maxPerCell = -1, command = Command.GOTO_CASTLE)
        #battlefield.DeployBattalionRect(firstrow = 0, firstcolumn = 45, lastrow = 0, lastcolumn = 45, army = attackers, kind = "Infantry", maxPerCell = -1, command = Command.GOTO_CASTLE)
        battlefield.DeployBattalionRect(firstrow = 8, firstcolumn = 26, lastrow = 8, lastcolumn = 29, army = attackers, kind = "Cannons", maxPerCell = -1, command = Command.ATTACK_CASTLE)

        Log('Attackers deployed: ' + attackers.GetString(), VERBOSE_RESULT)



class Example_7(Example_6):
    
    def ArmyDefenderData(self, defenders):
        defenders.DefineBattalion("Archers", 800)
        defenders.DefineBattalion("Cannons", 100)
        
    
    def DeployDefendersData(self, defenders, castle):
        c = {"Cannons": -1}
        castle.DeployBattalions(army = defenders, battalions = c, placementtype = CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1, command = Command.DEFEND_CASTLE)
        
        d = {"Archers": -1}
        castle.DeployBattalions(army = defenders, battalions = d, placementtype = CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1, command = Command.DEFEND_CASTLE)
        
        Log('Defenders deployed: ' + defenders.GetString(), VERBOSE_RESULT)
   
    
    def DeployAttackersData(self, attackers, battlefield, castle):
        battlefield.DeployBattalionRect(firstrow = 3, firstcolumn = 3, lastrow = 3, lastcolumn = 46, army = attackers, kind = "Infantry", maxPerCell = -1, command = Command.GOTO_CASTLE)
        battlefield.DeployBattalionRect(firstrow = 1, firstcolumn = 26, lastrow = 1, lastcolumn = 29, army = attackers, kind = "Cannons", maxPerCell = -1, command = Command.ATTACK_CASTLE)
        battlefield.DeployBattalionRect(firstrow = 1, firstcolumn = 10, lastrow = 1, lastcolumn = 20, army = attackers, kind = "Archers", maxPerCell = 15, command = Command.ATTACK_CASTLE)        
        battlefield.DeploySiegeTowers(army = attackers, maxDeployed = 1, castle = castle, command = Command.ATTACK_CASTLE)

        Log('Attackers deployed: ' + attackers.GetString(), VERBOSE_RESULT)
        
   
    def BattleFieldData(self):
        battle = Battlefield.BattleField(bound = Bounding(500.0, 500.0), cellsize = 10.0)
        return battle
        
    





class Example_8(Example_6):
    
    
        
    def ArmyDefenderData(self, defenders):
        defenders.DefineBattalion("Archers", 800)
        defenders.DefineBattalion("Cannons", 100)
        
        
    def ArmyAttackerData(self, attackers):
        attackers.DefineBattalion("Infantry", 7000)
        attackers.DefineBattalion("Archers", 300)
        attackers.DefineBattalion("Cannons", 300)


    def DeployDefendersData(self, defenders, castle):
        c = {"Cannons": -1}
        castle.DeployBattalions(army = defenders, battalions = c, placementtype = CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1, command = Command.DEFEND_CASTLE)
        d = {"Archers": -1}
        castle.DeployBattalions(army = defenders, battalions = d, placementtype = CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1, command = Command.DEFEND_CASTLE)
        Log('Defenders deployed: ' + defenders.GetString(), VERBOSE_RESULT)


    def DeployAttackersData(self, attackers, battlefield, castle):
        battlefield.DeployBattalionRect(firstrow = 3, firstcolumn = 3, lastrow = 3, lastcolumn = 46, army = attackers, kind = "Infantry", maxPerCell = -1, command = Command.GOTO_CASTLE)
        #battlefield.DeployBattalionRect(firstrow = 8, firstcolumn = 26, lastrow = 8, lastcolumn = 29, army = attackers, kind = "Cannons", maxPerCell = -1, command = Command.ATTACK_CASTLE)
        battlefield.DeployCannons(army = attackers, maxDeployed = -1, maxPerWall = -1, castle = castle, command = Command.ATTACK_CASTLE)


        Log('Attackers deployed: ' + attackers.GetString(), VERBOSE_RESULT)





class Example_9(Example_6):
    
    def ArmyDefenderData(self, defenders):
        pass
        
        
    def ArmyAttackerData(self, attackers):
        pass


    def DeployDefendersData(self, defenders, castle):
        pass

    def DeployAttackersData(self, attackers, battlefield, castle):
        pass



    def CastleData(self, castle):
        # Define the city
        city = [[200.0, 230.0], [230.0, 231.0], [200.0, 292.0], [230.0, 233.0], [230.0, 234.0], [243.0, 234.0], [330.0, 250.0], [245.0, 333.0], [300.0, 304.0], [238.0, 230.0], [243.0, 260.0]]
        castle.WrapOldCity(city = city, margin = 60, battlefieldcenter = Point2D(250.0, 250.0))
        castle.SetWallsResistance(100000)
        castle.SetCastleOrientation(Vector2D(0.0, -1.0))
        castle.Evolve(climbings = None, attachedsiegetowers = None, battlefield = None)

        """data = StarFortressData()
        data.RavelinRadius = 25.0
        data.RavelinMinWidth = 15.0
        data.HasHalfMoons = True
        data.HalfMoonCircleOffset = 5.0 
        data.HalfMoonLength = 30.0        
        data.CovertWayThickness = 10.0
        data.CovertWayOffset = 5.0
        data.CovertWayHasPlacesOfArms = True
        data.CovertWayPlacesOfArmsLength = 10.0        
        data.GlacisThickness = 15.0
        
        castle.ConstructStarFortress(data)
        """

        # Sets the moat object. Note that the moat geometry isn't yet calcualted until the castle is deployed in the battlefield
        castle.SetMoat(thickness = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Moat', 'Depth') * 1, depth = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Moat', 'Depth'), haswater = False)






""" Start to play. Have fun!!
"""

"""
data = Example_9()
play = Player(data)
play.SetLoopsForEachTest(2)
play.SetMaxCastleEvolutions(5)
play.SetTimePeriod(19)
play.SetVerboseLevel(VERBOSE_RESULT)
#play.PlayCastleEvolution()



play.DrawCastleShape()
                     

#play.Play(speed = 1)


#play.PlayLoop()

#profile.run('play.Play(speed = 1)')
#profile.run('play.PlayLoop()')
"""



""" Gus Demo
"""

def StarFortress():
    # Change bastion radius at 30
    data = Example_9()
    play = Player(data)
    play.SetLoopsForEachTest(2)
    play.SetMaxCastleEvolutions(5)
    play.SetTimePeriod(19)
    play.SetVerboseLevel(VERBOSE_RESULT)
    play.DrawCastleShape(canvas = None, city = False, starfortress = True, resetData = True)

def CannonsAttackers():
    # Change bastion radius at 20
    data = Example_8()
    play = Player(data)
    play.SetLoopsForEachTest(2)
    play.SetMaxCastleEvolutions(5)
    play.SetTimePeriod(19)
    play.SetVerboseLevel(VERBOSE_RESULT)
    play.Play(speed = 1)
    
    
def AttackNorthernWall():    
    data = Example_7()
    play = Player(data)
    play.SetLoopsForEachTest(2)
    play.SetMaxCastleEvolutions(5)
    play.SetTimePeriod(19)
    play.SetVerboseLevel(VERBOSE_RESULT)
    play.Play(speed = 1)


def ClimbingOnHoles():
    #Make infantry invincible
    data = Example_6()
    play = Player(data)
    play.SetLoopsForEachTest(2)
    play.SetMaxCastleEvolutions(5)
    play.SetTimePeriod(19)
    play.SetVerboseLevel(VERBOSE_RESULT)
    play.Play(speed = 1)


def StandardSquareAttackNoCannonsSiegeTowers():
    data = Example_2()
    play = Player(data)
    play.SetLoopsForEachTest(2)
    play.SetMaxCastleEvolutions(5)
    play.SetTimePeriod(15)
    play.SetVerboseLevel(VERBOSE_RESULT)
    play.Play(speed = 1)
    

def SimpleInfantry():
    data = Example_3()
    play = Player(data)
    play.SetLoopsForEachTest(2)
    play.SetMaxCastleEvolutions(5)
    play.SetTimePeriod(8)
    play.SetVerboseLevel(VERBOSE_RESULT)
    play.Play(speed = 1)

def SimpleArchers():
    data = Example_5()
    play = Player(data)
    play.SetLoopsForEachTest(2)
    play.SetMaxCastleEvolutions(5)
    play.SetTimePeriod(12)
    play.SetVerboseLevel(VERBOSE_RESULT)
    play.Play(speed = 1)




#SimpleArchers()
#SimpleInfantry()
#StandardSquareAttackNoCannonsSiegeTowers()
#ClimbingOnHoles()
#AttackNorthernWall()
CannonsAttackers()
#StarFortress()


