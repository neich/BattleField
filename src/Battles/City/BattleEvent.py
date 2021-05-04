from Battles.Utils.Geometry import Ray2D
import Battles.Utils.Message
import Battles.Utils.Settings
from Battles.Utils.Geometry import *
from Battles.Castle.BattalionConstruction_XXX import *

class BattleEventDataFlank():
    
    """ Attackers flank data for BattleEventData
    
    Attributes:
        approachVector: Direction of attack
        approachOrigin: Position where attackers come from. Its combined with approachVector to get a more accurate deployment. If it is not defined, only is used the approach vector
                        , considering the castle bounding center as the battleground center
        standDistance: Distance from castle where the attackers start the battle
        attackers: List of attackers definitions: {"Type": class_name, "Number": nSoldiers}. Used to construct the battalions. See AddBattalions method to get more information
    """
    
    def __init__(self):
        
        self.approachVector = Vector2D()
        self.approachOrigin = None
        self.standDistance = -1.0
        self.attackers = []
        
        
    def AddAttackerBattalions(self, battaliontype, number, command, battalionsize = -1, groupsize = -1, groupdistance = -1):
        # Inserts a new type of troops in the army. The type of troops is defined in battaliontype, with the class name. The number parameter is the number of total troops to deploy
        # The battalionsize is the maximum number of soldiers per battalion (note that this could be limited by the battlefield cell size). -1 means maximum size
        # The command is the main order (see Command class)
        
        # The order of calls of this method is important. First type will be deployed first on the battlefield, and the others will be 
        # deployed rear them. Note that this allows to define the same kind of troops at different levels or attack lines. Note too that some kind of troops have preferences over
        # the others and over this sorting too, such are the cannons or the siege towers.
        
        # groupsize allows to deploy groups of battalions, with a distance between them of groupsditance. This parameter is usefull for deploy cannons batteries
        # If groupsize is -1, all battalions are grouped together. You can define the deployment sparse factor defining a groupsize of 1 and some groupsdistance
        
        
        self.attackers.append({"Type": battaliontype, "Number": number, "BattalionsSize": battalionsize, "Command": command, "GroupSize": groupsize, "GroupDistance": groupdistance})







class BattleEventData():
    
    """ Data support class for the BattleEvent
    
    Attributes:
    
        year: battle year
        simulations: Number of simulations (1 by default). WARNING: 1 simulation is only for display and demo purposes. None castle evolution will be performed
        repeat_until_defenders_win: Activate the simulation repeat (the whole simulation, so the number of "simulations") until defenders win (as % of Battles)
                                    This is for debug and study purposes, to allow the castle evolution (for weak point) again and aganin until the castle is good enough to
                                    defend agains a kind of attackers
                                    WARNING: Be aware setting this flag to True, so it would fall on an infinite loop
        force_no_castle_evolution: Forces to avoid the castle evolution at the end of the Battles test (if repeat_until_defenders_win is True, the  battle event
                                    only finishes if the castle cannot evolve more, expanding the whole castle by default)
        flanks: List of attackers flanks (BattleEventDataFlank)
        defenders: List with defenders battalions definitions: {"Type": class_name, "Number": nSoldiers}. Used to construct the battalions. See AddBattalions method to get more information
    """
    
    def __init__(self):
        
        self.year = 0
        self.simulations = 1
        self.repeat_until_defenders_win = False
        self.force_no_castle_evolution = False
        self.__flanks = []
        self.__defenders = []
        
    

    def AddFlank(self, flank):
        self.__flanks.append(flank)

    def AddDefenderBattalions(self, battaliontype, number ):
        # Like attackers method, but without considering the placement and battalion size
        
        self.__defenders.append({"Type": battaliontype, "Number": number})



    def GetAttackersDefinition(self):
        ret = []
        for f in self.__flanks:
            ret.extend(f.attackers)
            
        return ret
          
          
    def GetFlanks(self):
        return self.__flanks  
    
    def GetDefendersDefinition(self):
        return self.__defenders


    def HaveAttackerCannons(self):
        for f in self.__flanks:
            for a in f.attackers:
                if (a["Type"] == "Cannons"):
                    return True

        return False



class BattleEvent():
    
    """ Battle event class. Defines a battle in time and its features. The features define the position, distance and troops. 
    
    Attributes:
    
        data: BattleEventData, with all battle event required data
        city: City object. Used to get current houses
        tkinter, canvas, viewport: view data from the city evolution window and given to the player board
        endControl: Object with the method EndBattle(), that should manage the ending of a battle
    """
    
    
    def __init__(self, data, tkinter, canvas, viewport, citycontrol):
        
        self.__data = data
        self.__city = citycontrol
        self.tkinter = tkinter
        self.canvas = canvas
        self.viewport = viewport
        self.endcontrol = citycontrol
        
    
    def PlayBattle(self, player, cityEvolution):
        
        if (self.GetNSimulations() <= 0):
            print "0 simulations means no simulation!!!"
            return
        
        player.PlayOnCityEvolution(self, cityEvolution)
        
        
    def GetNSimulations(self):
        return self.__data.simulations

    def IsRepeatUntilDefendersWin(self):
        return self.__data.repeat_until_defenders_win

    def AllowCastleExpansion(self):
        return not self.__data.force_no_castle_evolution

    def SetBattleFieldData(self, battlefield):
        # Construct the battlefield trenches from the city houses    
        # Be aware, this is a high-cost method
        
        Battles.Utils.Message.Log(' Configuring battlefield trenches ')

        # The trenches are defined as a list of battlefield cells.
        
        houses = self.__city.GetHouses()
        clist = []
        for h in houses:
            q = h.GetQuad()
            clist.append(battlefield.GetCellFromPoint(q.minPoint))
            clist.append(battlefield.GetCellFromPoint(q.maxPoint))
            clist.append(battlefield.GetCellFromPoint(Point2D(q.maxPoint.x, q.minPoint.y)))
            clist.append(battlefield.GetCellFromPoint(Point2D(q.minPoint.x, q.maxPoint.y)))
            clist.append(battlefield.GetCellFromPoint(h.center))


        # Check that any trench cover a moat or a river
        filterlist = []
        for c in clist:
            if ((c != None) and c.IsAvailable()):
                filterlist.append(c)
            
        battlefield.SetTrenchesCells(list(set(filterlist)), append = True)
        
        
        # Deploy random trenches 
        battlefield.DeployRandomTrenches()
        
        
        
             
    def SetDeployAttackersData(self, army, battlefield, castle):
        
        # For each flank, we define the battalions and deploy them. Note that we dont define the battalions of all flanks together, so the deploy algorithm tries to deploy
        # all avaiable battalions
        
        # Deploy the attackers army on the battlefield using the battle pattern
        
        # First calculate the main army position, at the minimum distance from the castle and at the specified direction
        # Because we do not know the castle shape, we cannot work with the castle hull, due non-convex vertices or too-long shapes could produce undesired results. 
        # We use the bounding circle to get a good distance approximation
        
        
        bound = castle.GetBounding()
        
        # Update the bounding with the city houses
        houses = self.__city.GetHouses()
        for h in houses:
            bound.InsertPoint(h.center)
        
        
        bcircle = bound.GetBoundingCircle()
        

        # Suitable cannon fire distance
        # WARNING: This is a simplification, so we are taking the default values. To be more accurate, we should use the suitable distance for each deployed cannon, so
        # each cannon can have a different shoot distance. On the other hand, the current battle event system doesnt allow specific cannon distances (too much parameters... weird) 
        suitablecannondist = Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Cannons', 'Distance') * Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Cannons', 'DefaultPlacementDistance')
        havecannons = self.__data.HaveAttackerCannons()
        
        # Place each flank
        flanks = self.__data.GetFlanks()
        for f in flanks:

            # Select a random approach vector if it is not specified
            if (not f.approachVector and not f.approachOrigin):
                apvec = Vector2D().Random()
            else:
                apvec = f.approachVector

        
            if (not f.approachOrigin):
                # If the army placement has not any origin position, we have to use only the circle radius as the attack vector (inverted) and extract the radius from the minimum distance
                vec = apvec.Copy().Invert()
                placement = Point2D().SetFrom3D(bcircle.GetCenter().Copy())
                placement.Move(vec, bcircle.GetRadius() + f.standDistance)
             
            else:
                
                # The origin and direction creates a ray that has to be intersected with the bounding circle
                # To get the minimum distance, increase the circle radius with the stand distance
                # If the ray doesnt intersect with the circle, or the stand distance is 0, the battalions are placed
                # at the specified position (no ray intersecting with the castle bounding circle)

                if (f.standDistance <= 0):
                    placement = f.approachOrigin
                else:
                    ray = Ray2D(origin = f.approachOrigin, direction = apvec.Copy())
                    bcircle.SetRadius(bcircle.GetRadius() + f.standDistance)
                    if (ray.HitCircle(bcircle)):
                        placement = ray.GetHitPoint()
                    else:
                        placement = f.approachOrigin
                        Log("WARNING: Deployment position at specified point due position + direction dont intersect with castle bound")
            
            
            # Check the cannons distance
            if (havecannons):
                cannonplacement = placement.Copy()
                # Get the nearest target from the deployment position
                wall = castle.GetClosestWall(populated = False, posfrom = placement)
                if (wall == None):
                    Log("WARNING: Cannon cannot be deployed due it cannot get the closest wall", VERBOSE_WARNING)
                else:

                    walldist = wall.DistanceFromPoint(posfrom = placement)
                    if (walldist > suitablecannondist):
                        if ((walldist - suitablecannondist) > f.standDistance):
                            # The cannon should be placed inside the castle bounding
                            # Try with the maximum cannon shoot distance.
                            # WARNING: Take the same considerations than for suitable cannon distance
                            if ((walldist - Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Cannons', 'Distance')) > f.standDistance):
                                print "WARNING: Castle bound doesnt allow to deploy cannon battalion flank enough near"
                                cannonplacement.Move(apvec, f.standDistance)
                            else:
                                cannonplacement.Move(apvec, walldist - Battles.Utils.Settings.SETTINGS.Get_F('Army', 'Cannons', 'Distance'))
                        else:
                            cannonplacement.Move(apvec, walldist - suitablecannondist)
                    
                
                
            
            
            
            # Deploy all battalions on the line created from calculated placement. This line has the same direction than the approach attack perpendicular vector
            perpvec = apvec.GetPerpendicular()
            
            for bat in f.attackers:
                
                # Define the flank battalions
                army.DefineBattalion(kind = bat["Type"], number = bat["Number"], accum = True)
                
                # The deployment is done automatically along the specified line direction and at both center point sides. If any obstacle is found along this line, the perpendicular
                # vector is used to get the parallel line and continue the deployment.
                # Note that all battalions has the same stand distance. This means that for the second and next battalions the method will try the next parallel lines. This could
                # be a wrong approach to solve the deployment problem, but this solves the problem of specifying a stand distance for each battalion: the battle field is discretized,
                # so it is not clear how specify a correct distance for the other battalions, so it changes for each battlefield cell. In addition this solves the problem about how to
                # deploy if any obstacle is found, such are previous units or construction elements
                
                deploypos = placement
                if ((bat["Type"] == "Cannons") and havecannons):
                    deploypos = cannonplacement
                
                if (bat["Type"] == "SiegeTowers"):
                    battlefield.DeploySiegeTowersOnCenteredLine(center = deploypos, 
                                                                direction = perpvec, 
                                                                alternativedirection = apvec.Copy().Invert(),
                                                                army = army, 
                                                                mindistance = bat["GroupDistance"],
                                                                command = bat["Command"], 
                                                                castle = castle)
                else:
                    battlefield.DeployOnCenteredLine(center = deploypos, 
                                                     direction = perpvec, 
                                                     alternativedirection = apvec.Copy().Invert(),
                                                     army = army, 
                                                     kind = bat["Type"], 
                                                     maxpercell = bat["BattalionsSize"], 
                                                     groupsize = bat["GroupSize"],
                                                     groupdistance = bat["GroupDistance"] ,
                                                     command = bat["Command"], 
                                                     castle = castle)
        
        
        
        
        
        
        
        
        
        
    def SetDeployDefenders(self, army, castle):
        
        
        armydef = self.__data.GetDefendersDefinition()
        
        # Define the kind of battalion into the army
        for bt in armydef:
            army.DefineBattalion(kind = bt["Type"], number = bt["Number"], accum = False)
        
        
        
        # Deploys the defender army on the castle curtain wall automatically and in sparsed mode
        
        
        # First deploy the cannon battalions
        found = False
        i = 0
        while ((i < len(armydef)) and not found):
            if (armydef[i]["Type"] == "Cannons"):
                castle.DeployBattalions(army = army, battalions = {"Cannons": -1}, placementtype = CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1, command = Command.DEFEND_CASTLE)
                found = True
            
            i += 1
                
                
        # Next, deploy the archers        
        found = False
        i = 0
        while ((i < len(armydef)) and not found):
            if (armydef[i]["Type"] == "Archers"):
                castle.DeployBattalions(army = army, battalions = {"Archers": -1}, placementtype = CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED, linespercell = 1, command = Command.DEFEND_CASTLE)
                found = True

            i += 1
        
        
        
            
    