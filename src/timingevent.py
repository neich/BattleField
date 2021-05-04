import time

events = []
lastFilename = None


def timing_event_start(eventname, filename=None):
    global lastFilename
    tab = ' ' * 4 * len(events)
    events.append((eventname, time.clock()))
    if filename is None:
        filename = lastFilename
    else:
        lastFilename = filename
    with open(filename, 'a+') as file:
        file.write(tab + 'START Event: {0}\n'.format(eventname))
        file.close()


def timing_event_stop(eventname, message, filename=None):
    global lastFilename
    if filename is None:
        filename = lastFilename
    else:
        lastFilename = filename

    e = events.pop()
    if e[0] != eventname:
        raise Exception("Trying to stop an eventa that is not the current one <{0} != {1}>".format(e[0], eventname))
    stop_time = time.clock()

    tab = ' ' * 4 * len(events)
    with open(filename, 'a+') as file:
        file.write(tab + 'END Event: {0}, Message: {1}, TIME: {2} secs\n'.format(eventname, message, stop_time - e[1]))
        file.flush()
        file.close()
