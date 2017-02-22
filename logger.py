import logging
import sys

LOGNAME = "%s/control.log" % sys.path[0]

logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler(LOGNAME)
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)