# merge base and override settings into one settings dictionary

from logger import *
from beeper import beep
import switch
import json
import sys
import os
import time
import datetime

# DHT22 sensor BCM pin
LOCAL = 25

# WiFi sensor URL
REMOTE = "http://192.168.0.41"

# settings path including file name
SETTINGS_DIR = os.path.join(sys.path[0], "settings")
DEFAULT_FNAME = os.path.join(SETTINGS_DIR, "default.json")
TODAY_DATE = time.strftime("%y%m%d",time.localtime(time.time()))  # YYMMDD
TODAY_WEEKDAY = time.strftime("%a",time.localtime(time.time())).lower()

# settings validation
WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
MODES = ["auto", "off"]

settings = {}


def load_default_for_date(date):
    """ Load and parse default weekday settings, return a day's settings """
    weekday = datetime.datetime.strptime(date, '%y%m%d').strftime('%a').lower()
    try:
        with open(DEFAULT_FNAME, 'r') as f:
            defaults = json.load(f)
            for ctrl_type in switch.TARGETS.keys():
                for key in defaults[ctrl_type].keys():
                    if weekday in key:
                        defaults[ctrl_type] = defaults[ctrl_type][key]
                        break
                # by the end of the inner loop, today's settings for ctrl_type
                # should have been brought up by one level, directly under ctrl_type
                # now validate it as below
                first_key = next(iter(defaults[ctrl_type]))
                print type(defaults[ctrl_type][first_key])
                if type(defaults[ctrl_type][first_key]) is dict:
                    # today's weekday is not found in default weekday settings
                    logging.error("Today's (%s) setting not found in default settings.", weekday)
                    logging.warn("Turning CH and HW off for today due to lack of settings.")
                    switch.ch_off()
                    switch.hw_off()
                    beep()
                    sys.exit()
        logging.info("Loaded default settings for %s", date)
        return defaults
    except:
        logging.exception("Unable to load default settings: %s", DEFAULT_FNAME)
        raise


def save_day_settings(dict=settings, date=TODAY_DATE):
    """ Save given date's settings to a json file.

    dict:   settings dictionary
    date:   date string in YYMMDD format
    """
    with open(os.path.join(SETTINGS_DIR, "%s.json" % date), 'w') as f:
        f.write(json.dumps(dict, indent=4, sort_keys=True))
    logging.info("Settings for %s saved.", date)

def generate_day_settings(date):
    """ take defaults and generate given date's settings json file """
    global settings
    try:
        settings = load_default_for_date(date=date)
        save_day_settings(dict=settings, date=date)
        logging.info("Settings for %s generated.", date)
    except:
        logging.exception("Unable to generate settings for %s", date)
        # this is bad... kick off beeper and stop here!
        beep()
        raise


def load_by_date(date=TODAY_DATE):
    global settings
    fname = os.path.join(SETTINGS_DIR, date+".json")
    try:
        with open(fname, 'r') as f:
            settings = json.load(f)
            logging.info("Loaded %s", fname)
    except IOError:
        logging.warn("Settings for %s not found.", date)
        generate_day_settings(date)


# load today's settings by default
load_by_date()
