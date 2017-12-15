#!/usr/bin/env python

from os import system
import subprocess
from logger import *

BL = 26

def usage():
    print "Usage: boiler.py setup|status"

if len(sys.argv) == 1:
    usage()
elif len(sys.argv) == 2 and sys.argv[1] == "setup":
    system("/usr/local/bin/gpio mode %d input" % BL)
    logging.info("Boiler: sensor pin %d set to input mode.", BL)
elif len(sys.argv) == 2 and sys.argv[1] == "status":
    print subprocess.check_output(["/usr/local/bin/gpio", "read", str(BL)]).strip()
else:
    usage()

