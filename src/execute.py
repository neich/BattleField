import random
from Battles.Run import Run
from Battles.Utils.Geometry import Point2D, BoundingQuad

import argparse


def parse_float(parser, message, value):
    try:
        return float(value)
    except ValueError:
        parser.error(message.format(value))


arg_parser = argparse.ArgumentParser(description='Start Battlefield run')

arg_parser.add_argument('playdata', help='XML file with the battle data')
arg_parser.add_argument("--settings", help="XML file with additional settings")
arg_parser.add_argument("--type", help="Type of run: CityExpansion, Battle, Inverse")
arg_parser.add_argument("--target", help="Target point for Inverse run")
arg_parser.add_argument("--start-area", help="Start area for army in Inverse run")
arg_parser.add_argument("--start-pos", help="Start position for army in battle statistics run")

args = arg_parser.parse_args()

params = {}

if not args.type:
    arg_parser.error('Argument --type must be defined')

if args.type not in ['CityExpansion', 'Battle', 'Inverse', 'BattleStatistics']:
    arg_parser.error('Unknown run type: {}'.format(args.type))

if args.target:
    coords = args.target.split(',')
    if len(coords) != 2:
        arg_parser.error('Wrong target: {}'.format(args.target))
    x = parse_float(arg_parser, 'Target x coordinate <{}> is not a number', coords[0])
    y = parse_float(arg_parser, 'Target y coordinate <{}> is not a number', coords[1])
    params['target'] = Point2D(x, y)

if args.start_area:
    coords = args.start_area.split(',')
    if len(coords) != 4:
        arg_parser.error('Wrong start area: {}'.format(args.start_area))
    fx = parse_float(arg_parser, 'Target from x coordinate <{}> is not a number', coords[0])
    fy = parse_float(arg_parser, 'Target from y coordinate <{}> is not a number', coords[1])
    tx = parse_float(arg_parser, 'Target to x coordinate <{}> is not a number', coords[2])
    ty = parse_float(arg_parser, 'Target to y coordinate <{}> is not a number', coords[3])
    params['start_area'] = BoundingQuad(Point2D(fx, fy), Point2D(tx, ty))

if args.start_pos:
    coords = args.start_pos.split(',')
    if len(coords) != 2:
        arg_parser.error('Wrong starting position: {}'.format(args.start_pos))
    x = parse_float(arg_parser, 'Starting position x coordinate <{}> is not a number', coords[0])
    y = parse_float(arg_parser, 'Starting position y coordinate <{}> is not a number', coords[1])
    params['start_pos'] = Point2D(x, y)


# ex1 = Run(playdataxml = basepath + "/CityExpansion1.xml", settingsxml = None)
# ex1 = Run(playdataxml = basepath + "/CityExpansion2.xml", settingsxml = None)
# ex1 = Run(playdataxml = basepath + "/CityExpansion3.xml", settingsxml = None)
# ex1 = Run(playdataxml = basepath + "/CityExpansion4.xml", settingsxml = None)
# ex1 = Run(playdataxml = basepath + "/CityExpansion5.xml", settingsxml = None)

# ex1 = Run(playdataxml = basepath + "/Battle_SimpleInfantry.xml", settingsxml = None)
# ex1 = Run(playdataxml = basepath + "/Battle_SimpleArchers.xml", settingsxml = None)
# ex1 = Run(playdataxml = basepath + "/Battle_Simple4Sides.xml", settingsxml = None)
# ex1 = Run(playdataxml = basepath + "/Battle_Simple3SiegeTowers.xml", settingsxml = None)
# ex1 = Run(playdataxml = basepath + "/Battle_SimpleCannonsBastions.xml", settingsxml = None)
# ex1 = Run(playdataxml = basepath + "/Battle_SimpleClimbHoles.xml", settingsxml = None)


# ex1 = Run(playdataxml = basepath + "/CityPuzzle.xml", settingsxml = None)

# ex1 = Run(playdataxml = rootpath + "/Examples/Girona/feudal_expansion.xml", settingsxml = rootpath + "/Examples/Girona/feudal_settings.xml")
# ex1 = Run(playdataxml = rootpath + "/Examples/Girona/feudal_expansion_war_ex1.xml", settingsxml = rootpath + "/Examples/Girona/feudal_settings_war_ex1.xml")
# ex1 = Run(playdataxml = rootpath + "/Examples/Girona/feudal_expansion_war_ex2.xml", settingsxml = rootpath + "/Examples/Girona/feudal_settings_war_ex2.xml")
# ex1 = Run(playdataxml = rootpath + "/Examples/Girona/feudal_expansion_war_ex3.xml", settingsxml = rootpath + "/Examples/Girona/feudal_settings_war_ex3.xml")


# ex1 = Run(playdataxml = basepath + "/StarFortress.xml", settingsxml = "./StarFortress_settings.xml")

# ex1 = Run(playdataxml = basepath + "/WarCastleExpansion1.xml", settingsxml = "./WarCastleExpansion1_settings.xml")

# ###########################################################################3
# Inverse problem examples
# ###########################################################################3
ex1 = Run(args.type, playdataxml=args.playdata, settingsxml=args.settings)

random.seed(42)  # Set the random number generator to a fixed sequence.
# Comment to get truly random results between different EXECUTIONS!!! (do we really need it? I doubt it...)


ex1.execute(params)

print "Done"
