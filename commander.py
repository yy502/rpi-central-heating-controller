#!/usr/bin/env python

from logger import *
import switch
import app_settings
import display

def get_current_target_temp():
    """ Return target temperature in today's settings as a float. """
    for timestamp in app_settings.settings["ch"].keys():
        pass  # find temp setting for now
        # return

if __name__=="__main__":
    """ Get today's settings and current temperature, decide
    what to do and update display.
    """
    temp = display.get_temperature()
    target = get_current_target_temp()
    if target - app_settings.RANGE < temp and temp < target + app_settings.RANG:
        # current temperature is in desired range
        logging.info("CH: No action required (%f)", temp)
    elif temp < target - app_settings.RANGE:
        # room too cold
        
