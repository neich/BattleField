""" Message management module """
' It would be prefereable a singleton class, but in python is better to do it as variables and functions on a module '

# Verbose control. Only those messages with a verbose mode greater than Verbose variable will be displayed
VERBOSE_ALL = 0  # All messages are displayed
VERBOSE_WARNING = 1  # Warning and greater messages are displayed
VERBOSE_RESULT = 2  # Result and greater messages are displayed
VERBOSE_STATISTICS = 3  # Results statistics messages are displayed
VERBOSE_EXTRA = 4  # Extra messages and greater are displayed
VERBOSE_CASTLEEVOLUTION = 5  # Messages about the castle evolution
VERBOSE_NONE = 10  # None message is displayed

Verbose = VERBOSE_ALL  # Verbose level


def Log(msg, verboseMode=VERBOSE_ALL):
    if Verbose <= verboseMode:
        if verboseMode == VERBOSE_WARNING:
            print 'WARNING: ' + msg
        elif verboseMode == VERBOSE_CASTLEEVOLUTION:
            print 'CASTLE EVOLUTION: ' + msg
        else:
            print msg
