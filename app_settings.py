# merge base and override settings into one settings dictionary

from logger import *
import json
import sys
import os

# relay wiringPi pins
CH = 2
HW = 3

# DHT22 sensor BCM pin
LOCAL = 24

# WiFi sensor URL
REMOTE = "http://192.168.0.41"

# settings path including file name
SETTINGS_DIR = "settings"
DEFAULT = os.path.join(sys.path[0], SETTINGS_DIR, "default.json")
DAILY = os.path.join(sys.path[0], SETTINGS_DIR, "20170301.json")  # file name will be today's date

settings = {}

try:
    with open(DEFAULT, 'r') as f:
        settings = json.load(f)
        logging.info("Loaded %s", DEFAULT)
except:
    logging.exception("Unable to load default settings: %s", DEFAULT)
    raise

try:
    with open(DAILY, 'r') as f:
        settings.update(json.load(f))
        logging.info("Loaded %s", DAILY)
except:
    logging.exception("Daily settings not found: %s", DAILY)
    logging.info("Using default settings only.")
