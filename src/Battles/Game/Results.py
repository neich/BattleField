from Battles.Utils import Message
from Battles.Utils.Geometry import ClusteringKMeans
from Battles.Utils.Geometry import Point3D

# Types of victory
RESULT_ATTACKERS_VICTORY_CLIMBING = 1                   # When an attacker soldier has climbed on a wall
RESULT_ATTACKERS_VICTORY_WALLFALLEN = 2                  # When the attacker cannons destroy completely a wall
RESULT_ATTACKERS_VICTORY_ALLDEAD = 3                    # When the attackers have killed all defenders
RESULT_DEFENDERS_VICTORY_ALLDEAD = 4                 # When defenders kill all attacker battalions
RESULT_ATTACKERS_VICTORY_SIEGETOWER = 5                 # When a siege tower is attached to a wall


class ResultData():
    """ Results auxiliar class that stores the results of one game
    Attributes:
        reason: Type of victory (see previous defines)
        rounds: Number of played rounds
    """
    
    def __init__(self, reason = RESULT_DEFENDERS_VICTORY_ALLDEAD):
        self._reason = reason
        self._rounds = 0
        self._extraInfo = {}
        
    def SetRounds(self, n):
        self._rounds = n    
     
    def GetRounds(self):
        return self._rounds   

    # ====================== 
    # Added by dagush to store whatever I need for inverse optim
    # ====================== 
    def addExtraInfo(self, key, n):
        self._extraInfo[key] = n    
     
    def getExtraInfo(self, key):
        return self._extraInfo[key]   

    def getAllExtraInfo(self):
        return self._extraInfo   
    # ====================== 

    def GetPosition(self):
        return Point3D();

    def IsWallDefeated(self):
        if ((self._reason == RESULT_ATTACKERS_VICTORY_CLIMBING) or 
            (self._reason == RESULT_ATTACKERS_VICTORY_WALLFALLEN) or
            (self._reason == RESULT_ATTACKERS_VICTORY_SIEGETOWER)):
            return True
        else:
            return False
        
    def IsWallDefeatedByClimbing(self):
        if (self._reason == RESULT_ATTACKERS_VICTORY_CLIMBING):
            return True
        else:
            return False
        
        
    def IsWallDefeatedByFall(self):
        if (self._reason == RESULT_ATTACKERS_VICTORY_WALLFALLEN):
            return True
        else:
            return False        
        
    def IsWallDefeatedBySiegeTower(self):
        if (self._reason == RESULT_ATTACKERS_VICTORY_SIEGETOWER):
            return True
        else:
            return False
        
    def AttackersWon(self):
        if ((self._reason == RESULT_ATTACKERS_VICTORY_CLIMBING) or 
            (self._reason == RESULT_ATTACKERS_VICTORY_WALLFALLEN) or
            (self._reason == RESULT_ATTACKERS_VICTORY_ALLDEAD) or
            (self._reason == RESULT_ATTACKERS_VICTORY_SIEGETOWER)):
            return True
        else:
            return False
        
    def GetStringReason(self):
        if (self._reason == RESULT_DEFENDERS_VICTORY_ALLDEAD):
            return 'The army have been fallen. Eternal glory for the fallen heroes!'
        elif (self._reason == RESULT_ATTACKERS_VICTORY_ALLDEAD):
            return 'The army have been fallen. Eternal glory for the fallen heroes!'
        elif (self._reason == RESULT_ATTACKERS_VICTORY_CLIMBING):
            return 'Climbed construction'
        elif (self._reason == RESULT_ATTACKERS_VICTORY_WALLFALLEN):
            return 'Hole in construction'
        elif (self._reason == RESULT_ATTACKERS_VICTORY_SIEGETOWER):
            return 'Siege Tower attached to wall'
        else:
            return 'Unknown'
        
     
class ResultDataAttClimb(ResultData):
    """ Results data for attackers victory climbing
    Attributes:
        climbPos: 3D Position of winning climbing soldier
        construction: Climbed construction (usually a wall) label/ID
    """
    
    def __init__(self, construction, climbpos):
        ResultData.__init__(self, RESULT_ATTACKERS_VICTORY_CLIMBING)
        self.__climbPos = climbpos
        self.__construction = construction
        
    def GetConstruction(self):
        return self.__construction
    
    def GetPosition(self):
        return self.__climbPos
    
    def GetStringReason(self):
        return 'The ' + self.__construction + ' has been climbed at ' + self.__climbPos.GetString()
  
      
       
class ResultDataWallFallen(ResultData):
    """ Simple results data for a fallen wall       
    Attributes:    
        construction: Broken construction label/ID
    """    
        
    def __init__(self, construction):   
        ResultData.__init__(self, RESULT_ATTACKERS_VICTORY_WALLFALLEN)
        self.__construction = construction
        
    def GetConstruction(self):
        return self.__construction
            
    def GetStringReason(self):
        return 'The ' + self.__construction + ' has been fallen!!'
       
     
     
class ResultDataSiegeTower(ResultData):
    """ Results data for attackers victory on attachment of a siege tower on a wall
    Attributes:
        position: 3D Position of final siege tower position
        wall: Wall label/ID
    """
    
    def __init__(self, wall, position):
        ResultData.__init__(self, RESULT_ATTACKERS_VICTORY_SIEGETOWER)
        self.__position = position
        self.__wall = wall
        
    def GetConstruction(self):
        return self.__wall
    
    def GetPosition(self):
        return self.__position
    
    def GetStringReason(self):
        return 'The ' + self.__wall + ' has been defeated by a siege tower at ' + self.__position.GetString()
       
     
       
          
        
class Results():
    """ Results class used to store and get statistics on each played game
    
    Attributes:
        ngames : Number of played games
        resultsList: List with all game results
    
        meanRounds: mean number of rounds for each game
        attackersVictories: Number of times that attackers have win
        defendersVictories: Number of times that defenders have win
        attackersKilled: Number of times that attackers have been killed
        defendersKilled: Number of times that defenders have been killed
        constructionsDefeated: List of constructions that have been defeated. It's a dictionary that groups by kind of defeat. Each element is a list of constructions, where
                                each one is composed by the construction label, number of defeats and weakest point. By example:
                                
                                constructionsDefeated["Climbed"][i]["label"] = "Wall_3"
                                constructionsDefeated["Climbed"][i]["defeats"] = 4
                                constructionsDefeated["Climbed"][i]["weakPoint"] = Point3D(1,2,3)
                                constructionsDefeated["Fall"][i] = {"label": Wall_3, "defeats": 2, "weakPoint": Point3D(4,5,6)}
                                constructionsDefeated["SiegeTower"][i]["label"] = "Wall_3"
                                constructionsDefeated["SiegeTower"][i]["defeats"] = 4
                                constructionsDefeated["SiegeTower"][i]["weakPoint"] = Point3D(1,2,3)
        
        weakestConstructionList: List of weak points, one for each construction, and sorted by number of defeats
        
    """
    
    def __init__(self):
        
        self.__ngames = 0
        self.__resultsList = []    
        
        self.__meanRounds = 0
        self.__attackersVictories = 0
        self.__defendersVictories = 0
        self.__attackersKilled = 0
        self.__defendersKilled = 0
        self.__constructionsDefeated = {"Climbed": [], "Fall": [], "SiegeTower": []}
        self.__weakestConstructionList = []
        
    def AddResult(self, result):
        self.__ngames += 1
        self.__resultsList.append(result)    
        
        
    def CalculateResults(self):
        # Performs results calculations to extract useful data
        self.__meanRounds = 0
        self.__attackersVictories = 0
        self.__defendersVictories = 0
        self.__attackersKilled = 0
        self.__defendersKilled = 0
        del self.__constructionsDefeated["Climbed"][0:len(self.__constructionsDefeated["Climbed"])]
        del self.__constructionsDefeated["Fall"][0:len(self.__constructionsDefeated["Fall"])]
        del self.__constructionsDefeated["SiegeTower"][0:len(self.__constructionsDefeated["SiegeTower"])]
        del self.__weakestConstructionList[0:len(self.__weakestConstructionList)]
        
        if (len(self.__resultsList) == 0):
            Message.Log('No statistics for 0 games', Message.VERBOSE_STATISTICS)
            return        
        
        # Gather results
        constr = {}
        for r in self.__resultsList:
            self.__meanRounds += r.GetRounds()
            
            if (r.IsWallDefeated()):
                w = constr.get(r.GetConstruction())
                if (w == None):
                    constr[r.GetConstruction()] = {"number":1, "climbs": [], "falls": [], "siegetowers": []}
                else: 
                    constr[r.GetConstruction()]["number"] += 1
                    
                if (r.IsWallDefeatedByClimbing()):
                    constr[r.GetConstruction()]["climbs"].append(r.GetPosition())
                elif (r.IsWallDefeatedByFall()):
                    constr[r.GetConstruction()]["falls"].append(Point3D())
                elif (r.IsWallDefeatedBySiegeTower()):
                    constr[r.GetConstruction()]["siegetowers"].append(r.GetPosition())
            else:
                if (r.AttackersWon()):
                    self.__defendersKilled += 1
                else:
                    self.__attackersKilled += 1
            
            if (r.AttackersWon()):
                self.__attackersVictories += 1

        self.__meanRounds /= len(self.__resultsList)
        
        self.__defendersVictories = len(self.__resultsList) - self.__attackersVictories
        
        # Calculate constructions weak points clustering all succeed climbings
        tmplist = []
        for k, v in constr.iteritems():

            cclimb = ClusteringKMeans(points = v["climbs"], initialMeans = 3)
            cclimb.execute()
            weakclimb = cclimb.GetLargestCluster()
        
            sclimb = ClusteringKMeans(points = v["siegetowers"], initialMeans = 3)
            sclimb.execute()
            weaksiegetower = sclimb.GetLargestCluster()
        
            if (len(v["climbs"]) > 0):
                self.__constructionsDefeated["Climbed"].append({"label": k, "defeats": len(v["climbs"]), "weakPoint": weakclimb})
            if (len(v["falls"]) > 0):
                self.__constructionsDefeated["Fall"].append({"label": k, "defeats": len(v["falls"]), "weakPoint": Point3D()})
            if (len(v["siegetowers"]) > 0):
                self.__constructionsDefeated["SiegeTower"].append({"label": k, "defeats": len(v["siegetowers"]), "weakPoint": weaksiegetower})    
            
            # Calculate the weakest point in construction
            wc = {"label": None, "defeats": 0, "weakPoint" : Point3D()}

            wc["label"] = k
            wc["defeats"] = v["number"]

            wlst = v["climbs"]
            wlst.extend(v["siegetowers"])
            wclust = ClusteringKMeans(points = wlst, initialMeans = 3)
            wclust.execute()
            wc["weakPoint"] = wclust.GetLargestCluster()

            tmplist.append(wc)

        # Finally, sort the weakest construction list by number of defeats
        self.__weakestConstructionList = sorted(tmplist, key=lambda k: k['defeats'], reverse=True)


                
        
    def PrintResults(self, optionalText=''):        
        if (len(self.__resultsList) == 0):
            Message.Log('No statistics for 0 games', Message.VERBOSE_STATISTICS)
            return
        
        Message.Log(' ', Message.VERBOSE_STATISTICS)
        Message.Log('+++++++++++++++++++++++++++++++++++++++++', Message.VERBOSE_STATISTICS)
        Message.Log('+ STATISTICS', Message.VERBOSE_STATISTICS)
        Message.Log('+ ' + optionalText, Message.VERBOSE_STATISTICS)
        Message.Log('+', Message.VERBOSE_STATISTICS)
        
        Message.Log('+ Number of games: ' + str(self.__ngames), Message.VERBOSE_STATISTICS)
        Message.Log('+ Mean rounds per game: ' + str(self.__meanRounds), Message.VERBOSE_STATISTICS)
        
        Message.Log('+ Attackers victories: ' + str(self.__attackersVictories) + '(' + str(self.__attackersVictories * 100.0 / len(self.__resultsList)) + '%)', Message.VERBOSE_STATISTICS)
        Message.Log('+ Defenders victories: ' + str(self.__defendersVictories) + '(' + str(self.__defendersVictories * 100.0 / len(self.__resultsList)) + '%)', Message.VERBOSE_STATISTICS)
       
        if (self.__attackersVictories > 0):       
            Message.Log('+ Construction defeats: ', Message.VERBOSE_STATISTICS)
            Message.Log('+     Climbed:', Message.VERBOSE_STATISTICS)
            for c in self.__constructionsDefeated["Climbed"]:
                Message.Log('+         ' + c["label"] + ' climbed ' + str(c["defeats"]) + ' times. Weakest point: ' + c["weakPoint"].GetString(), Message.VERBOSE_STATISTICS)
            Message.Log('+     Fall:', Message.VERBOSE_STATISTICS)
            for c in self.__constructionsDefeated["Fall"]:
                Message.Log('+         ' + c["label"] + ' broken ' + str(c["defeats"]) + ' times. Weakest point: ' + c["weakPoint"].GetString(), Message.VERBOSE_STATISTICS)
            Message.Log('+     Siege Tower attached:', Message.VERBOSE_STATISTICS)
            for c in self.__constructionsDefeated["SiegeTower"]:
                Message.Log('+         ' + c["label"] + ' broken ' + str(c["defeats"]) + ' times. Weakest point: ' + c["weakPoint"].GetString(), Message.VERBOSE_STATISTICS)
            Message.Log('+ Weakest construction: ' + self.GetWeakestConstruction() + ' at ' + self.GetWeakestPoint().GetString() + ',  defeated ' + str(self.GetWeakestDefeats()) + ' times', Message.VERBOSE_STATISTICS)
        Message.Log('+ Defenders defeats (by killing): ' + str(self.__defendersKilled), Message.VERBOSE_STATISTICS)
        Message.Log('+ Attackers defeats (by killing): ' + str(self.__attackersKilled), Message.VERBOSE_STATISTICS)
        Message.Log('+ __resultsList: ' + str(self.__resultsList), Message.VERBOSE_STATISTICS)
        Message.Log('+++++++++++++++++++++++++++++++++++++++++', Message.VERBOSE_STATISTICS)
        Message.Log(' ', Message.VERBOSE_STATISTICS)


    def DefendersInvictus(self):
        # Return true if defenders have won each time
        return (self.__defendersVictories == self.__ngames)
    
    def MeanDefendersWin(self):
        # Return true if defenders have won in mean
        return (self.__defendersVictories >= (self.__ngames / 2.0))
    
    def GetWeakestConstruction(self):
        if (len(self.__weakestConstructionList) > 0):
            return self.__weakestConstructionList[0]["label"]
        else:
            return "None"
    
    def GetWeakestPoint(self):
        if (len(self.__weakestConstructionList) > 0):
            return self.__weakestConstructionList[0]["weakPoint"]
        else:
            return Point3D()

    def GetWeakestDefeats(self):
        if (len(self.__weakestConstructionList) > 0):
            return self.__weakestConstructionList[0]["defeats"]
        else:
            return 0

    def GetSortedWeakPointList(self):

        return self.__weakestConstructionList



    def GetClimbedConstructions(self, castle):
        # Return a list with climbed constructions and weak points: {"Construction": ..., "WeakPoint": Point3D(...)}
        
        lst = []
        for c in self.__constructionsDefeated["Climbed"]:
            lst.append({"Construction": castle.GetConstructionByLabel(c["label"]), "WeakPoint": c["weakPoint"]})
            
        return lst
    
    
    
    def GetSiegeTowersAttachments(self, castle):
        lst = []
        for c in self.__constructionsDefeated["SiegeTower"]:
            lst.append({"Construction": castle.GetConstructionByLabel(c["label"]), "WeakPoint": c["weakPoint"]})
            
        return lst
    
    def getRawResults(self):
        return self.__resultsList       
        