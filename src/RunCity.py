
"""
         !!! DONT USE THIS CLASS. USED ONY FOR DEBUG PURPOSES !!!!
"""


from Battles.Game.Player import Player, PlayerData
from Battles.Utils.Geometry import Point2D, Bounding, Vector2D
from Battles.Battlefield import Battlefield
from Battles.Utils.Message import *
from Battles.Army.Action import Command
from Battles.City.CityEvolution import CityEvolution, CityEvolutionPattern
from Battles.City.BattleEvent import *
import Battles.Utils.Settings


class PlayerData_1(PlayerData):
    
    def __init__(self):
        PlayerData.__init__(self)

    def BattleFieldData(self):
        battle = Battlefield.BattleField(bound = Bounding(2000.0, 2000.0), cellsize = 10.0)
        return battle
    
    def CastleData(self, castle):
        # Define the initial city
        city = [[100.0, 250.0], [110.0, 300.0], [120.0, 350.0], [150.0, 300.0], [160.0, 340.0], [180.0, 270], [150.0, 250.0], [230.0, 330.0], [200.0, 230.0], [200.0, 292.0], [330.0, 250.0], [290.0, 250.0], [255.0, 343.0], [280.0, 304.0], [238.0, 250.0], [243.0, 280.0]]
        castle.WrapOldCity(city = city, margin = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'CurtainWallOldCityMargin'), battlefieldcenter = Point2D(1000.0, 1000.0))
        castle.SetCastleOrientation(Vector2D(0.0, -1.0))
        castle.Evolve(climbings = None, attachedsiegetowers = None, battlefield = None)


class City_1(CityEvolution):


    def __init__(self):
        CityEvolution.__init__(self)
        
        # Configure the overall evolution
        self._playerData = Player(PlayerData_1())
        self._startCentury = 9
        self._endCentury = 18
        #self._endCentury = 12
        self._currentYear = (self._startCentury - 1) * 100


        # Configure the city expansion patterns
        pat0 = CityEvolutionPattern(startyear = 850, endyear = None, direction = Vector2D(-0.7, -0.7).Normalize(), housesperyear = 1)
        pat1 = CityEvolutionPattern(startyear = 850, endyear = None, direction = Vector2D(0.7, 0.7))
        pat2 = CityEvolutionPattern(startyear = 950, endyear = 1000, direction = Vector2D(0.0, -1.0))
        pat3 = CityEvolutionPattern(startyear = 950, endyear = 1500, direction = Vector2D(1.0, 0.0))
        pat4 = CityEvolutionPattern(startyear = 1001, endyear = None, direction = Vector2D(-0.7, -0.7))
        pat5 = CityEvolutionPattern(startyear = 1001, endyear = None, direction = Vector2D(0.7, -0.7))
        pat6 = CityEvolutionPattern(startyear = 1201, endyear = None, direction = Vector2D(0.7, 0.7))
        #pat7 = CityEvolutionPattern(startyear = 1201, endyear = None, direction = Vector2D(0.7, 0.7), housesperyear = 0.5)
        self.AddEvolutionPattern(pat0)
        #self.AddEvolutionPattern(pat1)
        #self.AddEvolutionPattern(pat2)
        #self.AddEvolutionPattern(pat3)
        self.AddEvolutionPattern(pat4)
        self.AddEvolutionPattern(pat5)
        self.AddEvolutionPattern(pat6)
        #self.AddEvolutionPattern(pat7)
       
        # Configure at what years the castle is expanded
        self.AddCastleExpansionDate(1000)
        self.AddCastleExpansionDate(1200)
        self.AddCastleExpansionDate(1600)
        
        # Wall length bounds for each castle expansion
        self._minWallLength = 80.0
        self._maxWallLength = 150.0

       
        
        # Activate the final starfortress construction
        data = StarFortressData()
        data.BastionRadius = 40.0
        data.RavelinRadius = 25.0
        data.RavelinMinWidth = 15.0
        data.HasHalfMoons = True
        data.HalfMoonCircleOffset = 5.0 
        data.HalfMoonLength = 45.0        
        data.CovertWayThickness = 10.0
        data.CovertWayOffset = 15.0
        data.CovertWayHasPlacesOfArms = True
        data.CovertWayPlacesOfArmsLength = 20.0        
        data.GlacisThickness = 30.0
        self.SetFinalStarFortressData(data)


class City_2(CityEvolution):


    def __init__(self):
        CityEvolution.__init__(self)
        
        # Configure the overall evolution
        self._playerData = Player(PlayerData_1())
        self._startCentury = 9
        self._endCentury = 13
        self._currentYear = (self._startCentury - 1) * 100


        # Configure the city expansion patterns
        pat0 = CityEvolutionPattern(startyear = 800, endyear = None, direction = Vector2D(-0.7, -0.7), housesperyear = 1)
        pat1 = CityEvolutionPattern(startyear = 1000, endyear = None, direction = Vector2D(-0.7, -0.7), housesperyear = 1)

        self.AddEvolutionPattern(pat0)
        self.AddEvolutionPattern(pat1)

       
        # Configure at what years the castle is expanded
        self.AddCastleExpansionDate(990)
        self.AddCastleExpansionDate(1190)
         
        # Wall length bounds for each castle expansion
        self._minWallLength = 80.0
        self._maxWallLength = 150.0
        
        

class City_3(CityEvolution):


    def __init__(self):
        CityEvolution.__init__(self)
        
        # Configure the overall evolution
        self._playerData = Player(PlayerData_1())
        self._startCentury = 9
        self._endCentury = 13
        self._currentYear = (self._startCentury - 1) * 100


        # Configure the city expansion patterns
        pat0 = CityEvolutionPattern(startyear = 800, endyear = None, direction = Vector2D(-0.7, -0.7), housesperyear = 1)
        pat1 = CityEvolutionPattern(startyear = 1000, endyear = None, direction = Vector2D(-0.7, -0.7), housesperyear = 1)
        pat2 = CityEvolutionPattern(startyear = 1100, endyear = None, direction = Vector2D(0.7, 0.7), housesperyear = 1)
        self.AddEvolutionPattern(pat0)
        #self.AddEvolutionPattern(pat1)
        self.AddEvolutionPattern(pat2)       
       
        # Configure at what years the castle is expanded
        self.AddCastleExpansionDate(990)
        self.AddCastleExpansionDate(1190)
         
        # Wall length bounds for each castle expansion
        self._minWallLength = 80.0
        self._maxWallLength = 150.0

       
        
class City_4(CityEvolution):


    def __init__(self):
        CityEvolution.__init__(self)
        
        # Configure the overall evolution
        self._playerData = Player(PlayerData_1())
        self._startCentury = 9
        self._endCentury = 18
        self._currentYear = (self._startCentury - 1) * 100


        # Configure the city expansion patterns
        pat0 = CityEvolutionPattern(startyear = 850, endyear = None, direction = Vector2D(-0.1, -0.8).Normalize(), housesperyear = 1)
        pat4 = CityEvolutionPattern(startyear = 1001, endyear = None, direction = Vector2D(-0.7, -0.7), housesperyear = 1)
        pat5 = CityEvolutionPattern(startyear = 1001, endyear = None, direction = Vector2D(0.7, -0.7), housesperyear = 1)
        pat2 = CityEvolutionPattern(startyear = 1100, endyear = None, direction = Vector2D(0.0, 1.0), housesperyear = 1)
        pat3 = CityEvolutionPattern(startyear = 1300, endyear = None, direction = Vector2D(-0.7, -0.7), housesperyear = 2)
        pat6 = CityEvolutionPattern(startyear = 1201, endyear = 1300, direction = Vector2D(0.7, 0.7), housesperyear = 1)
        self.AddEvolutionPattern(pat0)
        self.AddEvolutionPattern(pat4)
        self.AddEvolutionPattern(pat5)
        self.AddEvolutionPattern(pat2)
        self.AddEvolutionPattern(pat6)
        self.AddEvolutionPattern(pat3)
       
        # Configure at what years the castle is expanded
        self.AddCastleExpansionDate(1000)
        self.AddCastleExpansionDate(1200)
        self.AddCastleExpansionDate(1600)
        
        # Wall length bounds for each castle expansion
        self._minWallLength = 80.0
        self._maxWallLength = 150.0

       
        
        # Activate the final starfortress construction
        data = StarFortressData()
        data.BastionRadius = 40.0
        data.RavelinRadius = 25.0
        data.RavelinMinWidth = 15.0
        data.HasHalfMoons = True
        data.HalfMoonCircleOffset = 5.0 
        data.HalfMoonLength = 45.0        
        data.CovertWayThickness = 10.0
        data.CovertWayOffset = 15.0
        data.CovertWayHasPlacesOfArms = True
        data.CovertWayPlacesOfArmsLength = 20.0        
        data.GlacisThickness = 30.0
        self.SetFinalStarFortressData(data)


 





class City_5(CityEvolution):


    def __init__(self):
        CityEvolution.__init__(self)
        
        # Configure the overall evolution
        self._playerData = Player(PlayerData_1())
        self._startCentury = 9
        self._endCentury = 12
        self._currentYear = (self._startCentury - 1) * 100


        # Configure the city expansion patterns
        pat0 = CityEvolutionPattern(startyear = 850, endyear = 1100, direction = Vector2D(-0.3, -0.5).Normalize(), housesperyear = 1)
        pat4 = CityEvolutionPattern(startyear = 950, endyear = 1100, direction = Vector2D(0.7, -0.7), housesperyear = 1)
        pat5 = CityEvolutionPattern(startyear = 1103, endyear = 1200, direction = Vector2D(0.7, -0.7), housesperyear = 1)
        self.AddEvolutionPattern(pat0)
        self.AddEvolutionPattern(pat4)
        self.AddEvolutionPattern(pat5)
       
        # Configure at what years the castle is expanded
        self.AddCastleExpansionDate(1101)
        self.AddCastleExpansionDate(1102)
        self.AddCastleExpansionDate(1103)
        
        # Battle events
        bat1 = BattleEventData()
        bat1.year = 975
        bat1.simulations = 1
        bat1.AddDefenderBattalions(battaliontype = "Archers", number = 600)
        
        bat1flank1 = BattleEventDataFlank()
        bat1flank1.approachVector = Vector2D(0.7, 0.7).Normalize()
        #bat1flank1.approachOrigin = Point2D(1000.0, 0.0)
        #bat1flank1.approachVector = Vector2D(-0.9, 0.9).Normalize()
        bat1flank1.standDistance = 100.0
        bat1flank1.AddAttackerBattalions(battaliontype = "Infantry", number = 100, command = Command.GOTO_CASTLE)
        bat1flank1.AddAttackerBattalions(battaliontype = "Archers", number = 50, battalionsize = 5, command = Command.ATTACK_CASTLE)
        bat1flank1.AddAttackerBattalions(battaliontype = "Cannons", groupsize = 3, groupdistance = 30, number = 9, battalionsize = 1, command = Command.ATTACK_CASTLE)
        #bat1flank1.AddAttackerBattalions(battaliontype = "SiegeTowers", number = 1, battalionsize = 1, command = Command.ATTACK_CASTLE)
        
        bat1flank2 = BattleEventDataFlank()
        bat1flank2.approachVector = Vector2D(-0.7, 0.7).Normalize()
        bat1flank2.standDistance = 100.0
        bat1flank2.AddAttackerBattalions(battaliontype = "Infantry", number = 100, command = Command.GOTO_CASTLE)
        bat1flank2.AddAttackerBattalions(battaliontype = "Archers", number = 50, battalionsize = 5, command = Command.ATTACK_CASTLE)
        bat1flank2.AddAttackerBattalions(battaliontype = "Cannons", groupsize = 3, groupdistance = 30, number = 9, battalionsize = 1, command = Command.ATTACK_CASTLE)
        
        bat1flank3 = BattleEventDataFlank()
        bat1flank3.approachVector = Vector2D(0.0, 1.0).Normalize()
        bat1flank3.standDistance = 50
        bat1flank3.AddAttackerBattalions(battaliontype = "Cannons", number = 10, command = Command.ATTACK_CASTLE, battalionsize = 1, groupsize = 1, groupdistance = 20)
        bat1flank3.AddAttackerBattalions(battaliontype = "Infantry", number = 100, command = Command.GOTO_CASTLE)
        
        bat1.AddFlank(bat1flank1)
        bat1.AddFlank(bat1flank2)
        bat1.AddFlank(bat1flank3)
        
        self.AddBattleEvent(bat1)
        

        bat2 = BattleEventData()
        bat2.year = 1105
        bat2.simulations = 1
        bat2.AddDefenderBattalions(battaliontype = "Archers", number = 2000)
        
        bat2flank1 = BattleEventDataFlank()
        bat2flank1.approachVector = Vector2D(0.7, -0.7).Normalize()
        bat2flank1.standDistance = 50.0
        bat2flank1.AddAttackerBattalions(battaliontype = "Cannons", groupsize = 3, groupdistance = 30, number = 9, battalionsize = 1, command = Command.ATTACK_CASTLE)
        bat2flank1.AddAttackerBattalions(battaliontype = "Infantry", number = 300, command = Command.GOTO_CASTLE)
        bat2flank1.AddAttackerBattalions(battaliontype = "Archers", number = 200, battalionsize = 5, command = Command.ATTACK_CASTLE)
        bat2flank1.AddAttackerBattalions(battaliontype = "Infantry", number = 500, command = Command.GOTO_CASTLE)
        bat2flank1.AddAttackerBattalions(battaliontype = "SiegeTowers", number = 5, groupdistance = 50, command = Command.ATTACK_CASTLE)
        bat2.AddFlank(bat2flank1)

        self.AddBattleEvent(bat2)


        # Add checkpoints to know the castle expansion status
        self.AddCastleExpansionChecking(1107)

         
        # Wall length bounds for each castle expansion
        self._minWallLength = 80.0
        self._maxWallLength = 150.0





#----------------------------------------------------------------------------------------------------


print "STARTING THE TIME MACHINE"


cityevolve = City_5()
cityevolve.Start()


print "TIME MACHINE STOPPED"



