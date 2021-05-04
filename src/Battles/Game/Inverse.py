# ########################################################################
#   Inverse problem computation
# ########################################################################
# ########################################################################
import csv
import math
import random

import numpy as np

import Battles.Game.Player as Player
import Battles.Game.PlayerFromXML as XMLReader
import Battles.Utils.Geometry as geom
import Battles.Utils.Message as Message
import Battles.Utils.Settings
from Battles.Game import Results
from Battles.Game.global_op import Optimizer, PInterval, Parameter

# import stackimpact

best = None;
bestPos = None;
bestBreach = None
period = None
pointsToShow = []
statisticData = []
optimumData = []
showGraphics = False  # True
battlefield = None
castle = None
initialArmy = {'attackers': None, 'defenders': None}


def isInsideCastle(point):
    from Battles.Utils.Geometry import Point2D
    global castle
    pW = gridToWorld(point)
    for c in castle.GetCastlesList():  # cannot make this more inefficient... I don't care!
        jp = c.GetJoinsPolygon()
        if jp.IsInside(Point2D(pW[0], pW[1])):
            # print "inside castle!!!"
            return True
    return False


def isOutsideBattlefield(r):
    global battlefield
    if not battlefield.GetCell(int(r[0]), int(r[1])):
        return True
    else:
        return False


def gridToWorld(gridCoords):
    from Battles.Utils.Geometry import Point2D
    # wCoords = game.GetBattlefield().GetCellSize() * gridCoords
    c = battlefield.GetCell(int(gridCoords[0]), int(gridCoords[1]))
    if c:
        wCoords = c.center
    else:
        wCoords = Point2D(0, 0)
        print  "conversion GridToW Failed:", gridCoords[0], gridCoords[1]
    # print "conversion GridToW:", gridCoords[0], gridCoords[1], '->', wCoords.x, wCoords.y
    return np.array([wCoords.x, wCoords.y])


# ====================================================
#  Show results
# ====================================================
def plotSamples(samples):
    import matplotlib.pyplot as plt

    cellSize = battlefield.GetCellSize()
    samples = np.array(samples) * cellSize
    plt.scatter(samples[:, 0], samples[:, 1], alpha=1.0, s=1)

    #     '''Plot target'''
    #     dx = 0.01
    #     x = np.arange(np.min(samples), np.max(samples), dx)
    #     y = np.arange(np.min(samples), np.max(samples), dx)
    #     X, Y = np.meshgrid(x, y)
    #     Z = q(X, Y)
    #     CS = plt.contour(X, Y, Z, 10)
    #     plt.clabel(CS, inline=1, fontsize=10)
    plt.show()


def printASCIICastle(steps=10.):
    from Battles.Utils.Geometry import Point2D

    for c in castle.GetCastlesList():
        jp = c.GetJoinsPolygon()
        bb = c.GetBounding()
        for y in np.linspace(bb.GetCenter().y - bb.GetWidth(),
                             bb.GetCenter().y + bb.GetWidth(),
                             bb.GetWidth() / steps):
            print "#",
            for x in np.linspace(bb.GetCenter().x - bb.GetLength(),
                                 bb.GetCenter().x + bb.GetLength(),
                                 bb.GetLength() / steps):
                if jp.IsInside(Point2D(x, y)):  # game.GetCastle().isInside(Point2D(x,y)):
                    print '.',
                else:
                    print ' ',
            print "#"


#         print "============================="
#         for y in np.linspace(bb.GetCenter().y-bb.GetWidth(),
#                              bb.GetCenter().y+bb.GetWidth(),
#                              bb.GetWidth()/steps):
#             #print y, ":",
#             for x in np.linspace(bb.GetCenter().x-bb.GetLength(),
#                                  bb.GetCenter().x+bb.GetLength(),
#                                  bb.GetLength()/steps):
#                 if bb.IsInside(Point2D(x,y)): #game.GetCastle().isInside(Point2D(x,y)):
#                     print '.',
#                 else:
#                     print ' ',
#             print "#"


def plotCastle(lines, ax):
    from matplotlib import collections as mc

    # lines = [[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]
    # c = np.array([(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])

    lc = mc.LineCollection(lines, linewidths=2)  # colors=c, )
    ax.add_collection(lc)
    # ax.autoscale()
    ax.set_xlim([0, 1400])
    ax.set_ylim([0, 1000])
    ax.margins(0.1)


def showCastleStructure(steps=10., filename=None):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    for c in castle.GetCastlesList():
        bb = c.GetBounding()
        print "Center=", (bb.GetCenter().x, bb.GetCenter().y)
        print "length=", bb.GetLength(), "Width=", bb.GetWidth()
        # ch = c.GetCastleHull()
        jp = c.GetJoinsPolygon()
        # Draw the castle
        # for j in c.__joins)):
        #    self.__joins[i].DrawStart(self.__hierarchyLevel, canvas, viewport)
        #    i += 1
        lines = []
        for seg in jp.shape:
            if seg.p1.x != seg.p2.x or seg.p1.y != seg.p2.y:  # don't ask me, there are null-length segments!
                # print [(seg.p1.x, seg.p1.y), (seg.p2.x, seg.p2.y)]
                lines.append([(seg.p1.x, seg.p1.y), (seg.p2.x, seg.p2.y)])
        plotCastle(lines, ax)

    for opt in pointsToShow:
        if opt[2] == 'G':
            op = gridToWorld(np.array(opt[0:2]))
        else:
            op = np.array(opt[0:2])
        # print "converted:", opt[0:2], op
        if opt[3] == 'unimportant':
            plt.plot(op[0], op[1], marker='o', markersize=1, color='blue')
        elif opt[3] == 'important':
            plt.plot(op[0], op[1], marker='o', markersize=1, color='red')
        else:
            print "Important point: " + opt[3] + " =>", op[0], op[1]
            size = 4
            if opt[3] == 'green':
                size = 6
            plt.plot(op[0] + 0.1, op[1] + 0.1, marker='o', markersize=opt[4], color=opt[3])
    if not filename:
        plt.show()
    else:
        plt.savefig(filename)

    # fig2, ax2 = plt.subplots()
    # data = np.array(optimumData)
    # x, y = data.T
    # y = abs(y)
    # plt.plot(x, y, color='r', linewidth=3.0, linestyle='-')
    # alldata = np.array(statisticData)
    # xa, ya = alldata.T
    # ya = abs(ya)
    # plt.plot(xa, ya, color='grey', linewidth=1.0, linestyle='-')
    # plt.show()
    # printASCIICastle(game)
    # print "isInside? -> ", jp.IsInside(Point2D(bb.GetCenter().x,bb.GetCenter().y+100))


# ====================================================
#  (needed) utility functions
# ====================================================
def acquireInitialData(game):
    global initialAttackers
    global initialDefenders
    board = game.GetBoard()
    initialArmy['attackers'] = board.collectAttackersData()
    initialArmy['defenders'] = board.collectCastleData()
    print "attackers info:", initialArmy['attackers']
    print "castle info:", initialArmy['defenders']


#     armies = game.getArmies()
#     attackers = armies['attackers'].getBattalions()
#     defenders = armies['defenders'].getBattalions()
#     for armyType in attackers:
#         print 'attackers:', armyType, '->', attackers[armyType].number
#     for armyType in defenders:
#         print 'defenders:', armyType, '->', defenders[armyType].number
#     print

#     castle = game.GetCastle()
#     defendersDetails = {}
#     for c in self.__castle.GetCastlesList():
#         for b in c.GetAllBattalions():
#             armyType = b._label.split('_')[0]
#             #print armyType, b.GetNumber()                
#             if armyType in defendersDetails:
#                 defendersDetails[armyType] += b.GetNumber()
#             else:
#                 defendersDetails[armyType] = b.GetNumber()
#     result.addExtraInfo("defenders", defendersDetails)


def acquireStaticData(game):
    global battlefield
    battlefield = game.GetBattlefield()

    global castle
    castle = game.GetCastle()


def initGame(data, period):
    game = Player.Player(data)
    game.SetTimePeriod(period)

    # Some internal default values (dont worry know about them, there are just for historical reasons)
    game.SetLoopsForEachTest(2)
    game.SetMaxCastleEvolutions(5)
    game.SetVerboseLevel(Message.VERBOSE_RESULT)
    return game


def changeBattalionNumber(armies, faction, battalionType, newNum):
    myFaction = armies[faction].getBattalions()
    myFaction[battalionType].number = newNum
    myFaction[battalionType].freenumber = newNum


def doOneRun(data, newPos):
    # random.seed(42)

    import Battles.Factory as Factory
    Factory.ResetCountersAndBlackboards()

    game = initGame(data, period)
    game.initData()
    game.CreateBattlefield()
    game.CreateCastle()

    game.BuildArmies()
    armies = game.getArmies()
    # changeBattalionNumber(armies, 'attackers', 'Archers', 35)
    # armies['attackers'].setBattalions(battalions)

    game.DeployArmies(newPos)
    game.SetupGameBoard(showGraphics)
    # bb = game.GetCastle().GetBounding()
    # center = bb.GetCenter()
    # print "Castle center: ", (center.x, center.y)
    # print "Castle radius: ", bb.GetLength()/2.
    if not castle or not battlefield:  # first time? Initialize!
        acquireInitialData(game)
    resultStatistics = Results.Results()
    speed = Battles.Utils.Settings.SETTINGS.Get_I(category='Game', tag='speed')
    game.StartBattle(speed, showGraphics, resultStatistics)
    if not castle or not battlefield:  # first time? Initialize!
        acquireStaticData(game)
    return resultStatistics


def getClimbingPos(result):
    return result.GetPosition()


# def getAllAttackerCasualties(result):
#     extraInfo = result.getAllExtraInfo()
#     #print "ExtraInfo:", extraInfo
#     return extraInfo['attackers']
#
# def getAttackerCasualties(result, armyType):
#     return getCasualties(result, 'attackers', armyType)
# 
# def getDefenderCasualties(result, armyType):
#     return getCasualties(result, 'defenders', armyType)

def getInitialArmyType(side, armyType):
    if armyType in initialArmy[side]:
        return initialArmy[side][armyType]
    else:
        return 0


def getRemainingArmyType(extraInfo, side, armyType):
    if armyType in extraInfo[side]:
        return extraInfo[side][armyType]
        # print "ExtraInfo:[", armyType, '] =>', remainingAttackers, "out of", initialAttackers[armyType]
    else:
        return 0
        # print "no", armyType, "in extraInfo out of", initialAttackers[armyType]


def getCasualties(result, side, armyType):
    extraInfo = result.getAllExtraInfo()
    # print "ExtraInfo:", extraInfo
    return getInitialArmyType(side, armyType) - getRemainingArmyType(extraInfo, side, armyType)


def comparePositions(a, b):
    return a.Distance(b)


def doBattle(newPos, data):
    # overwriteData = {'Archers':{'first':[5,33], 'last':[5,34]}}
    # xArchers = int(newPos[0])
    # yArchers = int(newPos[1])
    # overwriteData = {'Archers': {'first': [xArchers, yArchers],
    #                              'last': [xArchers + 1, yArchers]},
    #                  'Infantry': {'first': [xArchers - 7, yArchers - 1],
    #                               'last': [xArchers + 7, yArchers - 1]}
    #                 }

    results = doOneRun(data, newPos)
    # results.PrintResults('(round finished)')
    detailed_results = results.getRawResults()
    return detailed_results


armyWeights = {'attackers': {'Infantry': 0.5, 'Archers': 0.5},
               'defenders': {'Infantry': 0, 'Archers': 0}
               }


def reportCasualties(result):
    for side in armyWeights:
        for armyType in armyWeights[side]:
            pass
            # print side + " Casualties:", armyType, getCasualties(result, side, armyType)


def battleFunc(newPos, data, targetPos):  # This is a minimizing error function
    distWeight = 1
    detailedResults = doBattle(newPos, data)
    r = detailedResults[0]
    newDist = 0
    newBreach = None
    # for r in detailedResults:
    if r.AttackersWon():
        newDist = comparePositions(targetPos, getClimbingPos(r))
        newBreach = getClimbingPos(r)
    else:
        newDist = 1e100
        newBreach = None

    reportCasualties(r)

    # ------------------------ Compute the error value!!! ----------------------
    errorValue = distWeight * newDist
    print "Distance error=", errorValue
    casualties = 0
    for side in armyWeights:
        for armyType in armyWeights[side]:
            casualties += armyWeights[side][armyType] * getCasualties(r, side,
                                                                            armyType)  # / initialAttackers[armyType]
            # print "   " + side + " error components(", armyType, "):", armyWeights[side][armyType], "*", getCasualties(
            #     r, side, armyType), "of", getInitialArmyType(side, armyType), " =>", casualtiesForType  # * 100, "%"
            # errorValue += casualtiesForType
    # --------------------------------------------------------------------------

    print "Final error=", errorValue
    return errorValue, newBreach, casualties


# ====================================================
#  Handle statistical information
# ====================================================
def initInteresting(p, r, breach):
    global best, bestPos, bestBreach
    best = p
    bestPos = r
    bestBreach = breach
    optimumData.append([0, p])
    statisticData.append([0, p])


def keepIfInteresting(r, p, breach, counter, maximize):
    global best, bestPos, bestBreach
    s = 10
    minimize = not maximize
    if (p < best and minimize) or \
            (p > best and maximize):
        best = p
        bestPos = r
        bestBreach = breach
        pointsToShow.append([r[0], r[1], 'G', 'important'])
        # print len(optimumData), optimumData, optimumData[len(optimumData)-1]
        if optimumData[len(optimumData) - 1][0] != counter - 1:
            optimumData.append([counter - 1, optimumData[len(optimumData) - 1][1]])
        optimumData.append([counter, p])
    else:
        if counter % s == 0:
            pointsToShow.append([r[0], r[1], 'G', 'unimportant'])
    statisticData.append([counter, p])


def finishInteresting(r, p, breach, counter):
    optimumData.append([counter - 1, optimumData[len(optimumData) - 1][1]])
    statisticData.append([counter, p])

    print "best:", bestPos[0], bestPos[1], "breach:", bestBreach.x, bestBreach.y, bestBreach.z
    # x0 = int(round(math.cos(270.* math.pi / 180) * radius + center[0]))
    # y0 = int(round(math.sin(270.* math.pi / 180) * radius + center[1]))
    pointsToShow.extend([[bestPos[0], bestPos[1], 'G', 'blue'],
                         # [x0,y0, 'G', 'black'],
                         [bestBreach.x, bestBreach.y, 'W', 'blue']
                         ])


# ====================================================
#  optimizers
# ====================================================
def SimmulatedAnnealingOptim(data, targetPos, start_area):
    def evalFunc(pos):
        d, newBreach = battleFunc([int(pos[0]), int(pos[1])], data, targetPos)
        return d, newBreach  # We are minimizing, so no changes

    def update_temperature(T, k):
        return T - 1. / N

    def propose_move(r):
        rn = r + np.random.normal(size=2)
        mcounter = 0
        while isInsideCastle(rn) or isOutsideBattlefield(rn):
            rn = r + np.random.normal(size=2)
            mcounter += 1
        print 'proposed:', mcounter, "moves around", r
        return rn

    def make_move(r, p, obreach, func, T):
        rn = propose_move(r)
        pn, nbreach = func(rn)
        delta = pn - p
        if delta < 0:  # return new point with prob = 1 if we improve the solution
            return (rn, pn, nbreach)
        else:  # Apply Metropolis-Hasting criterion.
            prob = math.exp(-delta / T)
            return (rn, pn, nbreach) if random.random() < prob else (r, p, obreach)

    #     def keepIfInteresting(r,p,breach,counter):
    #         s = 10
    #         global best, bestPos, bestBreach
    #         if p < best:
    #             best = p; bestPos = r; bestBreach = breach
    #             pointsToShow.append([r[0],r[1], 'G', 'important'])
    #         else:
    #             if counter % s == 0:
    #                 pointsToShow.append([r[0],r[1], 'G', 'unimportant'])

    global best, bestPos, bestBreach
    N = 100  # 100000

    counter = 0
    T = 1.
    k = 1.

    p = start_area.GetCenter()
    rn = (p.x, p.y)
    # rn = initCircularPoint(0)  # angle = 0 to start somewhere
    pointsToShow.append([rn[0], rn[1], 'G', 'green'])
    pn, breachn = evalFunc(rn)
    print "starting pos:", rn, "->", pn
    initInteresting(pn, rn, breachn)

    while T > 1e-3:
        print "\n\n\n\n\n T:", T, "k:", k, "counter:", counter, "/", N
        rn, pn, breachn = make_move(rn, pn, breachn, evalFunc, T)
        counter += 1
        keepIfInteresting(rn, pn, breachn, counter, maximize=False)
        T = update_temperature(T, k)
        k += 1
        # if counter % s == 0:
        #    pointsToShow.append([rn[0],rn[1], 'G', 'unimportant'])

    print "iterations:", k
    print "best:", bestPos, best
    print "counter:", counter
    finishInteresting(rn, pn, breachn, counter)
    showCastleStructure()
    return bestPos, best


def MetropolisHastingsOptim(data, targetPos, start_area):
    def evalFunc(pos):
        d, newBreach = battleFunc([int(pos[0]), int(pos[1])], data, targetPos)
        return -d, newBreach  # invert sign to convert it into a maximization problem

    def propose_move(r):
        d = np.random.normal(size=2)
        rn = r + d
        # print 'proposing move:',
        counter = 0
        # print "debug propose move:", isInsideCastle(rn), isOutsideBattlefield(rn)
        while isInsideCastle(rn) or isOutsideBattlefield(rn) or not start_area.IsInside(geom.Point2D(rn[0], rn[1])):
            rn = r + 2.0*np.random.normal(size=2)
            counter += 1
            # print '.',
        print 'proposed:', counter, "moves around", r
        return rn

    #     def keepIfInteresting2(r,p,breach,counter,maximize):
    #         s = 10
    #         global best, bestPos, bestBreach
    #         if p >= best and maximize:
    #             best = p; bestPos = r; bestBreach = breach
    #             pointsToShow.append([r[0],r[1], 'G', 'important'])
    #         else:
    #             if counter % s == 0:
    #                 pointsToShow.append([r[0],r[1], 'G', 'unimportant'])

    '''Metropolis Hastings'''
    global best, bestPos, bestBreach
    N = 100  # 50000
    p = start_area.GetCenter()
    r = (p.x, p.y)
    pointsToShow.append([r[0], r[1], 'G', 'green'])
    # we need to execute at least once, to initialize the optimization, but also to have a castle built!
    p, breach = evalFunc(r)
    print "starting pos:", r, "->", p
    initInteresting(p, r, breach)

    # showCastleStructure(game)
    for i in xrange(N):
        print "\n\n\n\n\n"
        rn = propose_move(r)
        print i, "-> new sample", rn, "(", i, ")"
        pn, breach = evalFunc(rn)
        print "(", i, ") eval:", pn,
        if pn >= p:  # Probability of 1 if we improve the solution
            p = pn
            r = rn
        else:  # otherwise, use Metropolis-Hasting criterion
            u = np.random.rand()
            if p != 0 and u < pn / p:
                p = pn
                r = rn
        print "-> new position =", r, p
        keepIfInteresting(r, p, breach, i, maximize=True)
    # print "samples", samples
    # print "values", values
    finishInteresting(r, p, breach, N)
    showCastleStructure()
    # return r,p
    return bestPos, best


# A simple (full) brute optimization to compute the maximum/minimum.
def fullBruteForceOptim(data, targetPos):
    def check_move(r):
        return not isInsideCastle(r) and not isOutsideBattlefield(r)

    step = 1
    startX = 0;
    startY = 0
    endX = 50;
    endY = 50

    posOfMinX = 0;
    posOfMinY = 0
    minDist = 2000000  # a very large number
    breachOfMin = None

    for y in range(startY, endY, step):
        for x in range(startX, endX, step):
            print "\n\n\n\n\n"
            pos = np.array([x, y])
            if check_move(pos):
                newDist, newBreach = battleFunc([pos[0], pos[1]], data, targetPos)
                if newDist < minDist:
                    minDist = newDist
                    posOfMinX = x;
                    posOfMinY = y
                    breachOfMin = newBreach
                    pointsToShow.extend([[pos[0], pos[1], 'G', 'important']])
                else:
                    pointsToShow.extend([[pos[0], pos[1], 'G', 'unimportant']])

    bestPoint = np.array([posOfMinX, posOfMinY])
    print "best:", bestPoint[0], bestPoint[1], "breach:", breachOfMin.x, breachOfMin.y, breachOfMin.z
    # x0 = int(round(math.cos(270.* math.pi / 180) * radius + center[0]))
    # y0 = int(round(math.sin(270.* math.pi / 180) * radius + center[1]))
    pointsToShow.extend([[bestPoint[0], bestPoint[1], 'G', 'blue'],
                         # [x0,y0, 'G', 'black'],
                         [breachOfMin.x, breachOfMin.y, 'W', 'blue']
                         ])
    showCastleStructure()
    return bestPoint, minDist


def initCircularPoint(angle):
    center = (24.869040781902532, 25.069766855791138)
    radius = 10.5806485321 * 1.5  # they start at 1.5 times the diagonal of the boundingBox
    angRad = angle * math.pi / 180
    xStart = int(round(math.cos(angRad) * radius + center[0]))
    yStart = int(round(math.sin(angRad) * radius + center[1]))
    newPos = [xStart, yStart]
    print angle, newPos
    return np.array(newPos)


# A simple brute circular optimization to find an obvious result.
# Just for text and debug.
def circularBruteForceOptim(data, targetPos):
    def check_move(r):
        return not isInsideCastle(r) and not isOutsideBattlefield(r)

    posOfMin = 0
    minDist = 2000000  # a very large number
    breachOfMin = None
    for angle in range(0, 359, 20):
        print str(angle) + "==============================================="
        print "==================================================="
        print "==================================================="
        print "==================================================="
        print "==================================================="

        nPos = initCircularPoint(angle)
        if check_move(nPos):  # We don't need this, only for debug purposes
            pointsToShow.extend([[nPos[0], nPos[1], 'G', 'unimportant']])
            newDist, newBreach = battleFunc([nPos[0], nPos[1]], data, targetPos)
            if newDist < minDist:
                minDist = newDist
                posOfMin = angle
                breachOfMin = newBreach
    bestPoint = initCircularPoint(posOfMin)
    showCastleStructure()
    return posOfMin, minDist


def defineTarget(data):
    # Start the simulation
    angle = 270.
    newPos = initCircularPoint(angle)
    global showGraphics
    showGraphics = True
    detailedResults = doBattle(newPos, data)
    showGraphics = False
    newDist = 0
    newBreach = None
    for r in detailedResults:
        # newDist = comparePositions(targetPos, getClimbingPos(r))
        newBreach = getClimbingPos(r)
    # targetPos = geom.Point2D(153, 234) #this is the result from angle 270
    targetPos = geom.Point2D(newBreach.x, newBreach.y)
    print "Objective:", newBreach.x, newBreach.y, newBreach.z
    print "From:", angle, "=>", [newPos[0], newPos[1]]
    pointsToShow.extend([[newPos[0], newPos[1], 'G', 'red'],
                         [newBreach.x, newBreach.y, 'W', 'red']
                         ])
    return targetPos


# Executes a battle
def Execute(runData, params):
    # agent = stackimpact.start(
    #    agent_key = '85be06439e62edb9a97c493eebc8af91c3c134a0',
    #    app_name = 'Battlefield',
    #    debug = True)
    # span = agent.profile('span1');

    # Get the century
    global period
    period = runData._gameSettings.Get_I(category='Period')
    # Define the player data
    data = XMLReader.PlayerDataFromXML(runData._gameSettings)

    # Define the game controller
    # game = initGame(data, period)

    targetPos = params['target'] if 'target' in params is not None else defineTarget(data)
    start_area = params['start_area'] if 'start_area' in params is not None else None
    # posOfMin, minDist = circularBruteForceOptim(data, targetPos)
    # posOfMin, minDist = fullBruteForceOptim(data, targetPos)
    # posOfMin, minDist = MetropolisHastingsOptim(data, targetPos, start_area)
    # posOfMin, minDist = SimmulatedAnnealingOptim(data, targetPos, start_area)

    param_interval = PInterval()
    param_interval.add_parameter(Parameter("TARGET_X", 0, 140, 1))
    param_interval.add_parameter(Parameter("TARGET_Y", 0, 20, 1))
    # param_interval.add_parameter(Parameter("ANGLE_OFFSET", -30, 30, 5))

    def function(pstate, extra_data):
        f, breach, casualties = battleFunc((pstate.get_value("TARGET_Y"), pstate.get_value("TARGET_X")), extra_data['data'], extra_data['target_pos'])
        return f, {'breach': breach, 'casualties': casualties}

    op = Optimizer(param_interval, function, {'data': data, 'target_pos': targetPos}, initial_subdivison_d=15, n_iterations=50)
    op.run()

    for ne in op.best_nodes:
        print("F = {}, pos = ({}, {}), casualties = {}".format(ne.f,
                                                               ne.pstate.get_value('TARGET_X'),
                                                               ne.pstate.get_value('TARGET_Y'),
                                                               ne.extra['casualties']))

    for i in xrange(len(op.best_nodes)):
        eval = op.best_nodes[i]
        if eval.extra['breach'] is not None:
            pointsToShow.append([eval.pstate.get_value('TARGET_Y'), eval.pstate.get_value('TARGET_X'), 'G', 'blue', 10 - i])
            pointsToShow.append([eval.extra['breach'].x, eval.extra['breach'].y, 'W', 'red', 10 - i])

    showCastleStructure()

    print "optimumData:", optimumData
    print "statisticData:", statisticData

    # span.stop();


def ExecuteStatistics(runData, params):
    global pointsToShow

    # agent = stackimpact.start(
    #    agent_key = '85be06439e62edb9a97c493eebc8af91c3c134a0',
    #    app_name = 'Battlefield',
    #    debug = True)
    # span = agent.profile('span1');

    # Get the century
    global period
    period = runData._gameSettings.Get_I(category='Period')
    # Define the player data
    data = XMLReader.PlayerDataFromXML(runData._gameSettings)

    # Define the game controller
    # game = initGame(data, period)

    targetPos = params['target'] if 'target' in params is not None else defineTarget(data)

    def function(x, y, extra_data):
        f, breach, casualties = battleFunc((x, y), extra_data['data'], extra_data['target_pos'])
        return f, {'breach': breach, 'casualties': casualties}

    with open('search_selected.csv', 'rb') as search_file:
        points_reader = csv.reader(search_file, delimiter=',')
        n_points = 0
        points_reader.next()

        for point in points_reader:
            results = []
            niter = 200
            x = int(point[1])
            y = int(point[2])
            for n in range(niter):
                f, data = function(x, y, {'data': XMLReader.PlayerDataFromXML(runData._gameSettings), 'target_pos': targetPos})
                results.append((f, (x, y), data))
                # pointsToShow = [[targetPos.x, targetPos.y, 'W', 'green', 5]]
                # if data['breach'] is not None:
                #     pointsToShow.append([data['breach'].x, data['breach'].y, 'W', 'red', 3])
                #     showCastleStructure(filename='tmp' + '_castle.png')
                #
                # pointsToShow = [[targetPos.x, targetPos.y, 'W', 'green', 5]]
                # for r in results:
                #     if r[2]['breach'] is not None:
                #         pointsToShow.append([r[2]['breach'].x, r[2]['breach'].y, 'W', 'red', 3])
                #         showCastleStructure(filename='tmp_accum' + '_castle.png')

            filename = 'battleStats_{0}_{1}'.format(x, y)
            n_breaches = 0
            with open(filename + '_points.csv', 'wb') as csvfile:
                node_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                node_writer.writerow(['Distance'])
                for r in results:
                    if r[2]['breach'] is not None:
                        node_writer.writerow([r[0]])
                        n_breaches += 1
                csvfile.close()

            print('Percentage of breaches: {:10.1f}%'.format(100.0*n_breaches/niter))

            pointsToShow = [[targetPos.x, targetPos.y, 'W', 'green', 5], [x, y, 'G', 'blue', 5]]
            for r in results:
                if r[2]['breach'] is not None:
                    pointsToShow.append([r[2]['breach'].x, r[2]['breach'].y, 'W', 'red', 3])

            showCastleStructure(filename=filename + '_castle.png')
            saveHistogram(filename, results)

            n_points += 1


def saveHistogram(filename, results):
    import matplotlib.pyplot as plt

    a = []
    for r in results:
        if r[2]['breach'] is not None:
            a.append(r[0])

    np_hist = np.array(a)

    plt.figure(figsize=[10, 8])

    n, bins, patches = plt.hist(x=np_hist, bins=20, range=(0, 100), color='#0504aa', alpha=0.7, rwidth=0.95)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value (distance to target)', fontsize=15)
    plt.ylabel('Frequency', fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.ylabel('Frequency', fontsize=15)
    plt.title('Distance Distribution Histogram', fontsize=15)
    plt.savefig(filename + '_histogram.png')

# EOF
