"""
    Class used to execute the simulations. It must be provided two xml settings file (global settings optional). See related descriptions.
    Call Execute() after initialization
"""

from Utils.Settings import *
from Utils.Message import *
from Utils.Geometry import *
from City.CityEvolution import CityEvolution, CityEvolutionPattern
from Game.PlayerFromXML import PlayerDataFromXML
from Game.Player import Player
from City.BattleEvent import *
import Game.Inverse as Inverse
from Army.Action import Command


# The strange thing about settings import and from usage is a little weird ....

class Run:

    # Defines the game with a playdata xml file and a settings xml file. If settings is not specified,
    # uses the standard settings file
    def __init__(self, type, playdataxml, settingsxml=None):

        # Load settings
        Settings.SETTINGS = Settings(settingsxml)

        # Load game data
        print "====> Loading XML:", playdataxml
        self._gameSettings = Settings(playdataxml)
        self.typeg = type

        # Internal data initialization
        self.__cityEvolution = CityEvolution()

    # Executes the game
    def execute(self, params={}):

        # typeg = self._gameSettings.Get_S(category='Type')

        if self.typeg == "CityExpansion":
            print "============================="
            print "=====> __ExecuteCityExpansion"
            print "============================="
            self.__ExecuteCityExpansion()
        elif self.typeg == "Battle":
            print "============================="
            print "=====> __ExecuteBattle"
            print "============================="
            self.__ExecuteBattle()
        elif self.typeg == "Inverse":
            print "============================="
            print "=====> InverseProblem"
            print "============================="
            Inverse.Execute(self, params)
        elif self.typeg == "BattleStatistics":
            print "============================="
            print "=====> Statitics for the same battle configuration"
            print "============================="
            Inverse.ExecuteStatistics(self, params)

        else:
            raise NameError('Unknown execution type (' + typeg + ')')

    # Executes a battle
    def __ExecuteBattle(self):

        # Get the century
        period = self._gameSettings.Get_I(category='Period')

        # Define the player data
        data = PlayerDataFromXML(self._gameSettings)

        # Define the game controller
        game = Player(data)
        game.SetTimePeriod(period)

        # Some internal default values (dont worry know about them, there are just for historical reasons)
        game.SetLoopsForEachTest(2)
        game.SetMaxCastleEvolutions(5)
        game.SetVerboseLevel(VERBOSE_RESULT)

        # Start the simulation
        game.Play(speed=SETTINGS.Get_I(category='Game', tag='speed'))

    # Executes a city evolution
    def __ExecuteCityExpansion(self):

        # Define the time range
        timerange = self._gameSettings.Get_A(category='TimeRange')
        if (timerange is not None) and (len(timerange) == 2):
            self.__cityEvolution.SetCenturiesRange(timerange[0], timerange[1])

        # Define the player data
        self.__cityEvolution.SetPlayerData(Player(PlayerDataFromXML(self._gameSettings)))

        # Define the city evolution patterns classified in groups
        if self._gameSettings.HasTag(category='CityEvolutions', tag='Group'):
            groups = self._gameSettings.GetCollection(category='CityEvolutions', key='Group')
            if groups is not None:
                for grp in groups:
                    groupid = self._gameSettings.Get_I(category='ID', root=grp)
                    evolutions = self._gameSettings.GetCollection(category='Evolutions', key='Evolution', root=grp)
                    if evolutions is not None:
                        for ev in evolutions:
                            timerng = self._gameSettings.Get_A(category='TimeRange', root=ev)
                            d = self._gameSettings.Get_A(category='Direction', root=ev)

                            hyear = self._gameSettings.Get_F(category='HousesPerYear', root=ev)
                            if (hyear == 0) or (hyear is None):
                                hyear = SETTINGS.Get_I('City', 'Houses', 'CreationPerYear')

                            segmentbase = None
                            if self._gameSettings.HasTag(category='SegmentBase', root=ev):
                                pp1 = self._gameSettings.Get_A(category='SegmentBase', tag='P1', root=ev)
                                if (pp1 is not None) and (len(pp1) == 2):
                                    p1 = Point2D(pp1[0], pp1[1])
                                    pp2 = self._gameSettings.Get_A(category='SegmentBase', tag='P2', root=ev)
                                    if (pp2 is not None) and (len(pp2) == 2):
                                        p2 = Point2D(pp2[0], pp2[1])

                                        segmentbase = Segment2D(p1, p2)

                            self.__cityEvolution.AddEvolutionPattern(groupID=groupid,
                                                                     pattern=CityEvolutionPattern(startyear=timerng[0],
                                                                                                  endyear=timerng[1],
                                                                                                  direction=Vector2D(
                                                                                                      d[0],
                                                                                                      d[1]).Normalize(),
                                                                                                  base=segmentbase,
                                                                                                  housesperyear=hyear))

        # Wall expansion settings
        walld = self._gameSettings.Get_A(category='CityExpansion', tag='WallDimensions', required=False)
        if (walld is not None) and (len(walld) == 2):
            self.__cityEvolution.SetWallLengths(walld[0], walld[1])

            # Define the fixed city expansion dates
        if self._gameSettings.HasTag(category='CityExpansion', tag='Expansion'):
            expansions = self._gameSettings.GetCollection(category='CityExpansion', key='Expansion')
            if expansions is not None:
                for ex in expansions:
                    y = self._gameSettings.Get_I(category='Year', root=ex)
                    gid = self._gameSettings.Get_I(category='GroupID', root=ex)
                    self.__cityEvolution.AddCastleExpansionDate(year=y, groupID=gid)

        # Set the minimum time between expansions
        if self._gameSettings.HasTag(category='CityExpansion', tag='YearsBetweenExpansions'):
            margintime = self._gameSettings.Get_I(category='CityExpansion', tag='YearsBetweenExpansions')
            self.__cityEvolution.SetTimeBetweenExpansions(margintime)

        # Define the battle events
        if self._gameSettings.HasTag(category='BattleEvents', tag='Battle'):
            battleevents = self._gameSettings.GetCollection(category='BattleEvents', key='Battle')
            if battleevents is not None:
                for battle in battleevents:

                    bat = BattleEventData()

                    bat.year = self._gameSettings.Get_I(category='Year', root=battle)
                    bat.simulations = self._gameSettings.Get_I(category='Simulations', root=battle)
                    if self._gameSettings.HasTag(category='RepeatUntilDefendersWin', root=battle):
                        bat.repeat_until_defenders_win = self._gameSettings.Get_B(category='RepeatUntilDefendersWin',
                                                                                  root=battle)
                    else:
                        # Just assuring that this flag is False if is not
                        # activated (it should produce an infinite loop)
                        bat.repeat_until_defenders_win = False
                    if self._gameSettings.HasTag(category='ForceNoCastleEvolution', root=battle):
                        bat.force_no_castle_evolution = self._gameSettings.Get_B(category='ForceNoCastleEvolution',
                                                                                 root=battle, required=False,
                                                                                 default=False)

                    # Define the defenders
                    if self._gameSettings.HasTag(category='Defenders', tag='Cannons', root=battle):
                        number = self._gameSettings.Get_I(category='Defenders', tag='Cannons', root=battle)
                        bat.AddDefenderBattalions(battaliontype="Cannons", number=number)
                    if self._gameSettings.HasTag(category='Defenders', tag='Archers', root=battle):
                        number = self._gameSettings.Get_I(category='Defenders', tag='Archers', root=battle)
                        bat.AddDefenderBattalions(battaliontype="Archers", number=number)

                    # Define the attackers flanks
                    flanks = self._gameSettings.GetCollection(category='Attackers', key='Flank', root=battle)
                    for f in flanks:

                        batflank = BattleEventDataFlank()

                        fdir = None
                        fpos = None

                        # Flank direction
                        if self._gameSettings.HasTag(category='Direction', root=f):
                            fdir = self._gameSettings.Get_A(category='Direction', root=f, required=False)
                            if (fdir is not None) and (len(fdir) == 2):
                                batflank.approachVector = Vector2D(fdir[0], fdir[1]).Normalize()
                        else:
                            batflank.approachVector = None

                        # Flank origin
                        if self._gameSettings.HasTag(category='Origin', root=f):
                            fpos = self._gameSettings.Get_A(category='Origin', root=f, required=False)
                            if (fpos is not None) and (len(fpos) == 2):
                                batflank.approachOrigin = Point2D(fpos[0], fpos[1])
                        else:
                            batflank.approachOrigin = None

                        """
                        if ((fdir == None) and (fpos == None)):
                            # Set a random approachVector
                            batflank.approachVector = Vector2D().Random()
                        """

                        # Flank distance from castle
                        batflank.standDistance = self._gameSettings.Get_F(category='StandDistance', root=f,
                                                                          required=False)

                        # Define the battalions for current flank
                        fbattalions = self._gameSettings.GetCollection(category='Battalions', key='Battalion', root=f)
                        for fbat in fbattalions:

                            typeb = self._gameSettings.Get_S(category='Type', root=fbat)
                            # Remove " chars
                            typeunit = ""
                            for ch in typeb:
                                if ch != '\"':
                                    typeunit = typeunit + ch

                            number = self._gameSettings.Get_I(category='Number', root=fbat)

                            if self._gameSettings.HasTag(category='BattalionSize', root=fbat):
                                battalionsize = self._gameSettings.Get_I(category='BattalionSize', root=fbat)
                                if (battalionsize is None) or (battalionsize == 0):
                                    battalionsize = -1
                            else:
                                battalionsize = -1

                            if self._gameSettings.HasTag(category='GroupSize', root=fbat):
                                groupsize = self._gameSettings.Get_I(category='GroupSize', root=fbat)
                                if (groupsize is None) or (groupsize == 0):
                                    groupsize = -1
                            else:
                                groupsize = -1

                            if self._gameSettings.HasTag(category='GroupDistance', root=fbat):
                                groupdistance = self._gameSettings.Get_F(category='GroupDistance', root=fbat)
                                if (groupdistance is None) or (groupdistance == 0.0):
                                    groupdistance = -1
                            else:
                                groupdistance = -1

                            if typeunit == "Infantry":
                                command = Command.GOTO_CASTLE
                            else:
                                command = Command.ATTACK_CASTLE

                            batflank.AddAttackerBattalions(battaliontype=typeunit, number=number, command=command,
                                                           battalionsize=battalionsize, groupsize=groupsize,
                                                           groupdistance=groupdistance)

                        bat.AddFlank(batflank)

                    self.__cityEvolution.AddBattleEvent(bat)

        # Define the checking expansion dates
        if self._gameSettings.HasTag(category='ExpansionCheckings', tag='Year'):
            checkings = self._gameSettings.GetCollection(category='ExpansionCheckings', key='Year')
            if checkings is not None:
                for ch in checkings:
                    y = self._gameSettings.Get_I(root=ch)
                    self.__cityEvolution.AddCastleExpansionChecking(y)

        # Define the starfortress
        if self._gameSettings.HasTag(category='StarFortress'):
            star = self._gameSettings.Get_B(category='StarFortress', tag='Activate')
            if (star is not None) and (star == True):

                stardata = StarFortressData()

                if self._gameSettings.HasTag(category='StarFortress', tag='BastionRadius'):
                    stardata.BastionRadius = self._gameSettings.Get_F(category='StarFortress', tag='BastionRadius')

                if self._gameSettings.HasTag(category='StarFortress', tag='Ravelin', subtag='Radius'):
                    stardata.RavelinRadius = self._gameSettings.Get_F(category='StarFortress', tag='Ravelin',
                                                                      subtag='Radius')

                if self._gameSettings.HasTag(category='StarFortress', tag='Ravelin', subtag='MinWidth'):
                    stardata.RavelinMinWidth = self._gameSettings.Get_F(category='StarFortress', tag='Ravelin',
                                                                        subtag='MinWidth')

                if self._gameSettings.HasTag(category='StarFortress', tag='HalfMoon'):

                    if self._gameSettings.HasTag(category='StarFortress', tag='HalfMoon', subtag='Activate'):
                        stardata.HasHalfMoons = self._gameSettings.Get_B(category='StarFortress', tag='HalfMoon',
                                                                         subtag='Activate')

                    if self._gameSettings.HasTag(category='StarFortress', tag='HalfMoon', subtag='CircleOffset'):
                        stardata.HalfMoonCircleOffset = self._gameSettings.Get_F(category='StarFortress',
                                                                                 tag='HalfMoon', subtag='CircleOffset')

                    if self._gameSettings.HasTag(category='StarFortress', tag='HalfMoon', subtag='Length'):
                        stardata.HalfMoonLength = self._gameSettings.Get_F(category='StarFortress', tag='HalfMoon',
                                                                           subtag='Length')

                if self._gameSettings.HasTag(category='StarFortress', tag='CovertWay', subtag='Thickness'):
                    stardata.CovertWayThickness = self._gameSettings.Get_F(category='StarFortress', tag='CovertWay',
                                                                           subtag='Thickness')

                if self._gameSettings.HasTag(category='StarFortress', tag='CovertWay', subtag='Offset'):
                    stardata.CovertWayOffset = self._gameSettings.Get_F(category='StarFortress', tag='CovertWay',
                                                                        subtag='Offset')

                if self._gameSettings.HasTag(category='StarFortress', tag='CovertWay', subtag='HasPlacesOfArms'):
                    stardata.CovertWayHasPlacesOfArms = self._gameSettings.Get_B(category='StarFortress',
                                                                                 tag='CovertWay',
                                                                                 subtag='HasPlacesOfArms')

                if self._gameSettings.HasTag(category='StarFortress', tag='CovertWay', subtag='PlacesOfArmsLength'):
                    stardata.CovertWayPlacesOfArmsLength = self._gameSettings.Get_F(category='StarFortress',
                                                                                    tag='CovertWay',
                                                                                    subtag='PlacesOfArmsLength')

                if self._gameSettings.HasTag(category='StarFortress', tag='GlacisThickness'):
                    stardata.GlacisThickness = self._gameSettings.Get_F(category='StarFortress', tag='GlacisThickness')

                self.__cityEvolution.SetFinalStarFortressData(stardata)

        self.__cityEvolution.Start()
