"""
    Derived class from PlayerData ready to get the data from a XML structure
    PlayerData class is an empty class with empty methods that are called from Player class. So the class definition doesnt allow to assign data to any 
    internal member (there are not members, only calls). 
    When the game is configured by a XML file, we need to get the data from the XML loaded structure data
    See the game XML format to know more about it
    
    NOTE: Some of class methods seem to be poorly efficient. This is due the method structure and naming must be the same than PlayerData class, also following the standard
          pipeline of Player and PlayerData classes
"""

from Player import PlayerData
from Battles.Battlefield import Battlefield
from Battles.Utils.Geometry import Bounding
import Battles.Utils.Settings
from Battles.Battlefield import River
from Battles.Utils.Message import *
from Battles.Army.Battalion import *
from Battles.Castle.BattalionConstruction_XXX import *

# More python weird things: Note the two settings import. If the order of import callings are switched, there are errors ... :__(


class PlayerDataFromXML(PlayerData):

    def __init__(self, xmldata):
        PlayerData.__init__(self)
        self.__xml = xmldata

    def BattleFieldData(self):
        # # Log('################################################################# ', VERBOSE_RESULT)
        # # Log('#  Creating Battlefield Data                                    # ', VERBOSE_RESULT)
        # # Log('################################################################# ', VERBOSE_RESULT)

        b = self.__xml.Get_F(category='Battlefield', tag='Bounding')
        battle = Battlefield.BattleField(bound=Bounding(b, b),
                                         cellsize=self.__xml.Get_F(category='Battlefield', tag='CellSize'))

        if self.__xml.HasTag(category='Battlefield', tag='Trenches'):
            # Log('#  Creating Battlefield Trenches', VERBOSE_RESULT)
            trenches = self.__xml.GetCollection(category='Battlefield', tag='Trenches', key='Set')
            if trenches != None:
                tlist = []
                for t in trenches:
                    tlist.append(self.__xml.Get_A(root=t))

                battle.SetTrenchesPositions(tlist)

        if self.__xml.HasTag(category='Battlefield', tag='Rivers'):
            ## Log('#  Creating Battlefield Rivers', VERBOSE_RESULT)
            rivers = self.__xml.GetCollection(category='Battlefield', tag='Rivers', key='Trace')
            if rivers != None:
                for r in rivers:
                    width = self.__xml.Get_F(category='Width', root=r)
                    poly = self.__xml.GetCollection(category='Polyline', key='Vertex', root=r)
                    if poly != None:
                        plist = []
                        for p in poly:
                            v = self.__xml.Get_A(root=p)
                            plist.append(Point2D(v[0], v[1]))

                        river = River.River(width=width, polyline=plist)
                        battle.DeployRiver(river)

        return battle

    def CastleData(self, castle):
        # # Log('################################################################# ', VERBOSE_RESULT)
        # # Log('#  Creating Castle Data                                         # ', VERBOSE_RESULT)
        # # Log('################################################################# ', VERBOSE_RESULT)

        b = self.__xml.Get_F(category='Battlefield', tag='Bounding')

        v = self.__xml.Get_A(category='Castle', tag='Orientation')
        if (v != None) and (len(v) == 2):
            castle.SetCastleOrientation(Vector2D(v[0], v[1]))

        # Define the initial city
        city = []
        houses = self.__xml.GetCollection(category='Castle', tag='OldCity', key='House', required=False)
        if houses:
            # Log('   #  Creating Houses ', VERBOSE_RESULT)
            for h in houses:
                p = self.__xml.Get_A(root=h)
                city.append(p)

        # Check if the castle shape is defined by a polyline. If not, use the initial houses to wrap the city around them
        # Remember that the polyine can includes the towers specifications
        polylinetowers = []
        shape = self.__xml.GetCollection(category='Castle', tag='Shape', key='Vertex', required=False)
        if shape != None:
            for s in shape:
                pos = self.__xml.Get_A(category='Point', root=s)
                if len(pos) != 2:
                    continue
                if self.__xml.HasTag(category='TowerType', root=s):
                    towertype = self.__xml.Get_S(category='TowerType', root=s)
                    polylinetowers.append({'Point': Point2D(pos[0], pos[1]), 'HasTower': True, 'TowerType': towertype})
                else:
                    polylinetowers.append({'Point': Point2D(pos[0], pos[1]), 'HasTower': False, 'TowerType': None})

        if len(polylinetowers) > 0:
            castle.ConstructCurtainWallWithTowers(polylinetowers)
        elif len(city) > 0:
            castle.WrapOldCity(city=city, margin=Battles.Utils.Settings.SETTINGS.Get_F(category='Castle',
                                                                                       tag='CurtainWallOldCityMargin'),
                               battlefieldcenter=Point2D(b / 2.0, b / 2.0))
            castle.Evolve(climbings=None, attachedsiegetowers=None, battlefield=None)
        else:
            print "ERROR: No shape city data provided"

        if self.__xml.HasTag(category='Castle', tag='Moat'):
            # Log('   #  Creating Castle Moat', VERBOSE_RESULT)
            haswater = self.__xml.Get_B(category='Castle', tag='Moat', subtag='HasWater')
            castle.SetMoat(thickness=Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Moat', 'Width') * 1,
                           depth=Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Moat', 'Depth'), haswater=haswater)

    def ArmyDefenderData(self, defenders):

        if self.__xml.HasTag(category='DefendersPopulate'):
            # Log('   ###################### DefendersPopulate ########################## ', VERBOSE_RESULT)
            if self.__xml.HasTag(category='DefendersPopulate', tag='Archers'):
                number = self.__xml.Get_I(category='DefendersPopulate', tag='Archers')
                defenders.DefineBattalion("Archers", number)
                # Log('   #  Defender Archers: ' + str(number), VERBOSE_RESULT)

            if self.__xml.HasTag(category='DefendersPopulate', tag='Cannons'):
                number = self.__xml.Get_I(category='DefendersPopulate', tag='Cannons')
                defenders.DefineBattalion("Cannons", number)
                # Log('   #  Defender Cannons: ' + str(number), VERBOSE_RESULT)

    def DeployDefendersData(self, defenders, castle):
        # Log('   ################################################################# ', VERBOSE_RESULT)
        # Log('   #  Deploying Defenders                                          # ', VERBOSE_RESULT)
        # Log('   ################################################################# ', VERBOSE_RESULT)

        if defenders.HasBattalionType("Cannons"):
            # Log('   ################  Deploying Cannons  ########################### ', VERBOSE_RESULT)
            castle.DeployBattalions(army=defenders, battalions={"Cannons": -1},
                                    placementtype=CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED,
                                    linespercell=1, command=Command.DEFEND_CASTLE)
        if defenders.HasBattalionType("Archers"):
            # Log('   ################  Deploying Archers  ########################### ', VERBOSE_RESULT)
            castle.DeployBattalions(army=defenders, battalions={"Archers": -1},
                                    placementtype=CONSTRUCTION_BATTALION_DEPLOYMENT_SPARSED,
                                    linespercell=1, command=Command.DEFEND_CASTLE)
        # Log('   Defenders deployed: ' + defenders.GetString() + '\n', VERBOSE_RESULT)

    def ArmyAttackerData(self, attackers):
        # Log('   ###################### AttackersPopulate ########################## ', VERBOSE_RESULT)
        if self.__xml.HasTag(category='AttackersPopulate', tag='ArmySize'):

            sizes = self.__xml.GetCollection(category='AttackersPopulate', tag='ArmySize', key='Battalion')
            if sizes != None:

                for s in sizes:
                    bs = self.__xml.Get_A(root=s)
                    if (bs != None) and (len(bs) == 2):
                        # Remove " chars
                        typeunit = ""
                        for ch in bs[0]:
                            if ch != '\"':
                                typeunit = typeunit + ch

                        # #Lof('   #  Attackers Battalion: ' + str(typeunit) + '=' + str(bs[1]), VERBOSE_RESULT)
                        attackers.DefineBattalion(typeunit, bs[1])

            if not attackers.HasBattalionType('Infantry'):
                print "ERROR: Attacker army has not any infantry unit. The game cannot start"

    def DeployAttackersData(self, attackers, battlefield, castle, offset=None):
        # #Lof('   ################################################################# ', VERBOSE_RESULT)
        # #Lof('   #  Deploying Attackers                                          # ', VERBOSE_RESULT)
        # #Lof('   ################################################################# ', VERBOSE_RESULT)

        if self.__xml.HasTag(category='AttackersPopulate'):

            atts = self.__xml.GetCollection(category='AttackersPopulate', key='Battalion')
            if atts != None:

                for a in atts:

                    typeb = self.__xml.Get_S(category='Type', root=a)
                    typeunit = typeb.strip('\"')


                    # Get deployment type
                    if self.__xml.HasTag(category='DeploymentByRange', root=a):
                        # #Lof('   ################  Deployment by range !!! ', VERBOSE_RESULT)
                        # Standard deployment by cell range
                        first = self.__xml.Get_A(category='DeploymentByRange', tag='First', root=a)
                        last = self.__xml.Get_A(category='DeploymentByRange', tag='Last', root=a)

                        if (first == None) or (len(first) != 2) or (last == None) or (len(last) != 2):
                            continue

                        if offset:
                            first[0] += offset[0]
                            first[1] += offset[1]
                            last[0] += offset[0]
                            last[1] += offset[1]

                        # Get the battalion size
                        if self.__xml.HasTag(category='BattalionSize', root=a):
                            batsize = self.__xml.Get_I(category='BattalionSize', root=a)
                            if (batsize == None) or (batsize < 1):
                                batsize = -1
                        else:
                            batsize = -1

                        # this is a hack I (dagush) introduced for inverse problems...
                        # if overwriteData and typeunit in overwriteData:
                        #     print "Range(" + typeunit + ") (before) -> (first:", first, ", last:", last, ")"
                        #     first = overwriteData[typeunit]['first']
                        #     last = overwriteData[typeunit]['last']

                        # print "batsize:", batsize
                        # print "Range(" + typeunit + ") -> (first:", first, ", last:", last, ")"

                        battlefield.DeployBattalionRect(firstrow=first[0], firstcolumn=first[1], lastrow=last[0],
                                                        lastcolumn=last[1],
                                                        army=attackers, kind=typeunit, maxPerCell=batsize,
                                                        command=Command.ATTACK_CASTLE)

                    elif (self.__xml.HasTag(category='SiegeTowerNumber', root=a) and attackers.HasBattalionType(
                            'Infantry')):
                        # Set the number of siege towers to deploy
                        # Log('   ################  Deploying SiegeTowers ', VERBOSE_RESULT)
                        n = self.__xml.Get_I(category='SiegeTowerNumber', root=a)
                        if (n == None) or (n < 1):
                            n = -1

                        battlefield.DeploySiegeTowers(army=attackers, maxDeployed=n, castle=castle,
                                                      command=Command.ATTACK_CASTLE)

            # Log('   Attackers deployed: ' + attackers.GetString(), VERBOSE_RESULT)

    def GetConstructionHeightViews(self, castle):

        if self.__xml.Get_B(category='HasHeightViews'):
            clist = castle.GetWallsList()
            return clist
