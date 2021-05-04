import random
import Battles.Utils.Settings 


# Century of battle. Used to choose automatically some kind of objects
Century = 19


# WARNING!: Do not confuse this class with the Factory pattern. This class is only to get creator methods avoiding cross import references between the other classes


class ArmyFactory:
    def newBattalion(self, army, kind, number):
        # Creates new army battalions of given kind and number
        # The number of troops is checked and cropped if it is greater than avaiable
        # If number is -1, gets all avaiable troops
        
        b = self.newBattalionNoCrop(army, kind)
        if b is not None:
            b = army.CropBattalionSize(battalion = b, kind = kind, number = number)
        return b
    
    
    @staticmethod
    def newBattalionNoCrop(army, kind):
        # Creates new army battalions of given kind and number
        if kind == "Archers":
            archers = __import__('Battles.Army', globals(), locals(), ['Archers'], -1)            # We use on-demand import to avoid self-references in other classes
            b = archers.Archers.Archers(army = army)
        elif kind == "Infantry":
            infantry = __import__('Battles.Army', globals(), locals(), ['Infantry'], -1)
            b = infantry.Infantry.Infantry(army = army)
        elif kind == "Cavalry":
            raise NameError('ERROR: Do we have Cavalry?')
            cavalry = __import__('Battles.Army', globals(), locals(), ['Army'], -1)
            b = cavalry.Battalion.Cavalry(army = army) 
        elif kind == "Cannons":
            cannons = __import__('Battles.Army', globals(), locals(), ['Cannons'], -1)
            b = cannons.Cannons.Cannons(army = army)
        elif kind == "SiegeTowers":
            siegetowers = __import__('Battles.Army', globals(), locals(), ['SiegeTowers'], -1)
            b = siegetowers.SiegeTowers.SiegeTowers(army = army)
        elif kind == "Throwers":
            throwers = __import__('Battles.Army', globals(), locals(), ['Throwers'], -1)
            b = throwers.Throwers.Throwers(army = army)
        elif kind == "Stair":
            stair = __import__('Battles.Army', globals(), locals(), ['Stair'], -1)
            b = stair.Stair.Stair()        
        else:
            raise NameError('Uncknown battalion kind (' + kind + ')')
        
        return b
    
    def GetArmyType(self, obj):
        if (obj.__class__.__name__ == "Archers") or (".Archers" in obj.__class__.__name__):
            return "Archers"
        elif (obj.__class__.__name__ == "Infantry") or (".Infantry" in obj.__class__.__name__):
            return "Infantry"
        elif (obj.__class__.__name__ == "Cannons") or (".Cannons" in obj.__class__.__name__):
            return "Cannons"
        elif (obj.__class__.__name__ == "SiegeTowers") or (".SiegeTowers" in obj.__class__.__name__):
            return "SiegeTowers"
        elif (obj.__class__.__name__ == "Throwers") or (".Throwers" in obj.__class__.__name__):
            return "Throwers"
        elif (obj.__class__.__name__ == "Stair") or (".Stair" in obj.__class__.__name__):
            return "Stair"
        else:
            return "ArmyComponent"
    
    
    
    def IsType(self, obj, typeobj):
        if not obj:
            return False
        elif self.GetArmyType(obj) == typeobj:
            return True
        else:
            return False
    
    def IsArcher(self, obj):
        return self.IsType(obj, "Archers")
    
    def IsInfantry(self, obj):
        return self.IsType(obj, "Infantry")
    
    def IsCannon(self, obj):
        return self.IsType(obj, "Cannons")
    
    def IsSiegeTower(self, obj):
        return self.IsType(obj, "SiegeTowers")

    def IsThrower(self, obj):
        return self.IsType(obj, "Throwers")

    def IsStair(self, obj):
        return self.IsType(obj, "Stair")
    
    
    
    
     

class ConstructionFactory:
    def newConstruction(self, kind):
        if kind == "Wall":
            walls = __import__('Battles.Castle', globals(), locals(), ['Wall'], -1)
            c = walls.Wall.Wall()
            
        elif kind == "SquaredTower":
            towers = __import__('Battles.Castle', globals(), locals(), ['Tower'], -1)
            c = towers.Tower.SquaredTower()
            
        elif kind == "RoundedTower":
            towers = __import__('Battles.Castle', globals(), locals(), ['Tower'], -1)
            c = towers.Tower.RoundedTower()
            
        elif kind == "Tower":
            towers = __import__('Battles.Castle', globals(), locals(), ['Tower'], -1)
            bastions = __import__('Battles.Castle', globals(), locals(), ['Bastion'], -1)
            # Choose a kind of tower from current century
            timerange_sq = Battles.Utils.Settings.SETTINGS.Get_A(category = 'Castle', tag = 'Tower', subtag = 'TimeRange/Squared')
            timerange_rn = Battles.Utils.Settings.SETTINGS.Get_A(category = 'Castle', tag = 'Tower', subtag = 'TimeRange/Rounded')
            timerange_bt = Battles.Utils.Settings.SETTINGS.Get_A(category = 'Castle', tag = 'Tower', subtag = 'TimeRange/Bastion')
            
            squared = timerange_sq[0] <= Century <= timerange_sq[1]
            rounded = timerange_rn[0] <= Century <= timerange_rn[1]
            bastion = timerange_bt[0] <= Century <= timerange_bt[1]
            if squared and rounded:
                # Choose randomly the kind of tower
                #random.seed
                if random.random() < 0.5:
                    c = towers.Tower.SquaredTower()
                else:
                    c = towers.Tower.RoundedTower()
            elif rounded and bastion:
                # Choose randomly the kind of tower
                #random.seed
                if random.random() < 0.5:
                    c = bastions.Bastion.Bastion()
                else:
                    c = towers.Tower.RoundedTower()               
            elif squared:
                c = towers.Tower.SquaredTower()
            elif rounded:
                c = towers.Tower.RoundedTower()
            elif bastion:
                c = bastions.Bastion.Bastion()
            else:
                c = None
            
               
        elif kind == "Moat":
            moats = __import__('Battles.Castle', globals(), locals(), ['Moat'], -1)
            c = moats.Moat.Moat()
            
        else:
            c = None
            
        return c
    
    
    
    def newConstructionBastion(self):
        # Used to create a bastion without considering the current year
        
        bastions = __import__('Battles.Castle', globals(), locals(), ['Bastion'], -1)
        return bastions.Bastion.Bastion()
    
    
    
    
    def IsWall(self, obj):
        if not obj:
            return False
        if (obj.__class__.__name__ == "Wall") or (".Wall" in obj.__class__.__name__):
            return True
        else:
            return False
    
    def IsTower(self, obj):
        if not obj:
            return False
        if self.IsSquaredTower(obj) or self.IsRoundedTower(obj) or self.IsBastion(obj):
            return True
        else:
            return False
    
    def IsSquaredTower(self, obj):
        if not obj:
            return False
        if (obj.__class__.__name__ == "SquaredTower") or (".Tower" in obj.__class__.__name__):
            return True
        else:
            return False 
    
    def IsRoundedTower(self, obj):
        if not obj:
            return False
        if (obj.__class__.__name__ == "RoundedTower") or (".Tower" in obj.__class__.__name__):
            return True
        else:
            return False
    
    def IsBastion(self, obj):
        if not obj:
            return False
        if (obj.__class__.__name__ == "Bastion") or (".Bastion" in obj.__class__.__name__):
            return True
        else:
            return False
 
    
 
    def IsMoat(self, obj):
        if not obj:
            return False
        if (obj.__class__.__name__ == "Moat") or (".Moat" in obj.__class__.__name__):
            return True
        else:
            return False
 


    def IsRoundedTowerTime(self):

        timerange_bt = Battles.Utils.Settings.SETTINGS.Get_A(category = 'Castle', tag = 'Tower', subtag = 'TimeRange/Rounded')

        if (Century >= timerange_bt[0]) and (Century <= timerange_bt[1]):
            return True
        else:
            return False



    def IsBastionTime(self):
             
        timerange_bt = Battles.Utils.Settings.SETTINGS.Get_A(category = 'Castle', tag = 'Tower', subtag = 'TimeRange/Bastion')

        if (Century >= timerange_bt[0]) and (Century <= timerange_bt[1]):
            return True
        else:
            return False
        
 
    
       
def ResetCountersAndBlackboards():
    # Reset all static counters used to label walls, towers, battalions, ...
    
    # Walls
    walls = __import__('Battles.Castle', globals(), locals(), ['Wall'], -1)
    #c = walls.Wall.Wall()
    walls.Wall.Wall.ResetCounter()
    
    # Towers
    towers = __import__('Battles.Castle', globals(), locals(), ['Tower'], -1)
    #c = towers.Tower.Tower()
    towers.Tower.Tower.ResetCounter()
    
    # Moats
    moats = __import__('Battles.Castle', globals(), locals(), ['Moat'], -1)
    #c = moats.Moat.Moat()
    moats.Moat.Moat.ResetCounter()
    
    
    # Infantry
    infantry = __import__('Battles.Army', globals(), locals(), ['Infantry'], -1)
    #c = infantry.Infantry.Infantry()
    infantry.Infantry.Infantry.ResetCounter()
    infantry.Infantry.resetBlackboard()
    
    # Archers
    archers = __import__('Battles.Army', globals(), locals(), ['Archers'], -1)            # We use on-demand import to avoid self-references in other classes
    #c = archers.Archers.Archers()
    archers.Archers.Archers.ResetCounter()
    archers.Archers.resetBlackboard()
    
    # Cannons
    cannons = __import__('Battles.Army', globals(), locals(), ['Cannons'], -1)
    #c = cannons.Cannons.Cannons()
    cannons.Cannons.Cannons.ResetCounter()
    cannons.Cannons.resetBlackboard()
    
    # Siege Towers
    siegetowers = __import__('Battles.Army', globals(), locals(), ['SiegeTowers'], -1)
    #c = siegetowers.SiegeTowers.SiegeTowers()
    siegetowers.SiegeTowers.SiegeTowers.ResetCounter()
    siegetowers.SiegeTowers.resetBlackboard()
 
    # throwers
    throwers = __import__('Battles.Army', globals(), locals(), ['Throwers'], -1)
    #c = throwers.Throwers.Throwers()
    throwers.Throwers.Throwers.ResetCounter()
    throwers.Throwers.resetBlackboard()
    
    # bastions
    bastions = __import__('Battles.Castle', globals(), globals(), ['Bastion'], -1)
    #c = bastions.Bastion.Bastion()
    bastions.Bastion.Bastion.ResetCounter()
    
    
    
    
    