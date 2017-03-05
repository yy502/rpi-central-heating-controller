#!/usr/bin/env python

from os import system
import subprocess
from logger import *

CH = 2
HW = 3
TARGETS = {"ch": CH, "hw": HW}
VALUES = {"on": 1, "off": 0}

def usage():
    print "Usage: switch.py [<ch|hw> <on|off>]|setup|status"

def setup():
    for pin in [CH, HW]:
        system("/usr/local/bin/gpio mode %d output" % pin)
        logging.info("Switch: relay control pin %d set to output mode.", pin)

def status():
    status = []
    for pin in [CH, HW]:
        status.append(subprocess.check_output(["/usr/local/bin/gpio", "read", str(pin)]).strip())
    return status

def switch(target, value):
    if target in TARGETS.keys() and value in VALUES.keys():
        system("/usr/local/bin/gpio write %d %d" % (TARGETS[target], VALUES[value]))
        logging.info("Switch: %s %s", target, value)
    else:
        logging.error("Switch: unexpected parameters: %s, %s", str(target), str(value))
        raise Exception("Switch: unexpected parameters: %s, %s" % (str(target), str(value)))

def ch_on():
    switch("ch", "on")

def ch_off():
    switch("ch", "off")

def hw_on():
    switch("hw", "on")

def hw_off():
    switch("hw", "off")

if __name__=="__main__":
    if len(sys.argv) == 1:
        usage()
    elif len(sys.argv) == 2 and sys.argv[1] == "setup":
        setup()
    elif len(sys.argv) == 2 and sys.argv[1] == "status":
        print status()
    elif len(sys.argv) == 3 and sys.argv[1] in TARGETS.keys() and sys.argv[2] in VALUES.keys():
        switch(sys.argv[1], sys.argv[2])
    else:
        usage()
