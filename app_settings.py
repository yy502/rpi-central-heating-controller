# merge base and override settings into one settings dictionary

from logger import *
import json
import sys
import os
import time

# relay wiringPi pins
CH = 2
HW = 3

# DHT22 sensor BCM pin
LOCAL = 24

# WiFi sensor URL
REMOTE = "http://192.168.0.41"

# settings path including file name
SETTINGS_DIR = os.path.join(sys.path[0], "settings")
DEFAULT = os.path.join(SETTINGS_DIR, "default.json")
TODAY = time.strftime("%Y%m%d",time.localtime(time.time()))  # YYYYMMDD
DAILY = os.path.join(SETTINGS_DIR, "%s.json" % TODAY)

settings = {}

def load_default():
    try:
        with open(DEFAULT, 'r') as f:
            settings = json.load(f)
            logging.info("Loaded %s", DEFAULT)
    except:
        logging.exception("Unable to load default settings: %s", DEFAULT)
        raise

def load_daily():
    try:
        with open(DAILY, 'r') as f:
            settings.update(json.load(f))
            logging.info("Loaded %s", DAILY)
    except IOError:
        logging.warn("Daily settings not found: %s", DAILY)
        generate_daily_settings()

def generate_daily_settings():
    # take defaults and generate today's settings json file
    try:
        logging.info("Daily settings generated: %s", DAILY)
    except:
        logging.exception("Unable to generate daily settings: %s", DEFAULT)
        # kick off beeper!


# populate settings dictionary
load_default()
load_daily()