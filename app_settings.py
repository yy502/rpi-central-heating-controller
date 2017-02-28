# merge base and override settings into one settings dictionary

from logger import *
import json

BASE = "settings_base.json"
OVERRIDES = "settings_overrides.json"

base = {}
overrides = {}

try:
    with open(BASE, 'r') as f:
        base = json.load(f)
        logging.info("Loaded %s", BASE)
except:
    logging.error("Unable to load base config file: %s", BASE)
    raise Exception("Unable to load base config file: %s" % BASE)

try:
    with open(OVERRIDES, 'r') as f:
        overrides = json.load(f)
        logging.info("Loaded %s", OVERRIDES)
except:
    logging.error("Unable to load overrides config file: %s", OVERRIDES)
    raise Exception("Unable to load overrides config file: %s" % OVERRIDES)

settings = base.copy()
for k in settings.keys():
settings.update(overrides)