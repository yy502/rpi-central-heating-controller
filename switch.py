#!/usr/bin/env python

from os import system
from logger import *

CH = 2
HW = 3
TARGETS = {"ch": CH, "hw": HW}
VALUES = {"on": 1, "off": 0}

def usage():
    print "Usage: switch.py [<ch|hw> <on|off>] | [setup]"

def setup():
    for pin in [CH, HW]:
        system("/usr/local/bin/gpio mode %d output" % pin)
    logging.info("Relay GPIOs set to out put mode.")

def switch(target, value):
    if target in TARGETS.keys() and value in VALUES.keys():
        system("/usr/local/bin/gpio write %d %d" % (TARGETS[target], VALUES[value]))
    else:
        logging.error("Unexpected switch parameters: %s, %s", str(target), str(value))
        raise Exception("Unexpected switch parameters: %s, %s" % (str(target), str(value)))

if __name__=="__main__":
    if len(sys.argv) == 1:
        usage()
    elif len(sys.argv) == 2 and sys.argv[1] == "setup":
        setup()
    elif len(sys.argv) == 3 and sys.argv[1] in TARGETS.keys() and sys.argv[2] in VALUES.keys():
        switch(sys.argv[1], sys.argv[2])
    else:
        usage()
