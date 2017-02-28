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
TODAY = time.strftime("%y%m%d",time.localtime(time.time()))  # YYMMDD
DAILY = os.path.join(SETTINGS_DIR, "%s.json" % TODAY)


settings = {}


def parse_default(default_settings):
    """ Converts default weekday settings to daily settings.
    Returns daily settings dictionary.
    """
    return {"place_holder": 1}


def load_default():
    global settings
    try:
        with open(DEFAULT, 'r') as f:
            settings = parse_default(json.load(f))
            logging.info("Loaded %s", DEFAULT)
    except:
        logging.exception("Unable to load default settings: %s", DEFAULT)
        raise


def save_daily(dict=None, date=TODAY):
    with open(os.path.join(SETTINGS_DIR, "%s.json" % date), 'w') as f:
        f.write(json.dumps(dict, indent=4, sort_keys=True))


def generate_daily_settings():
    # take defaults and generate today's settings json file
    try:
        load_default()
        save_daily(dict=settings)
        logging.info("Daily settings generated and loaded: %s", DAILY)
    except:
        logging.exception("Unable to generate daily settings: %s", DEFAULT)
        # this is bad... kick off beeper and stop here!
        raise


def load_daily():
    global settings
    try:
        with open(DAILY, 'r') as f:
            settings.update(json.load(f))
            logging.info("Loaded %s", DAILY)
    except IOError:
        logging.warn("Daily settings not found: %s", DAILY)
        generate_daily_settings()


load_daily()