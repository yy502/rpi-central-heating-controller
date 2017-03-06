#!/usr/bin/env python

from logger import *
import switch
import app_settings
from sensors import get_temperature
from switch import ch_on, ch_off, hw_on, hw_off


def get_current_target_temp():
    """ Return target temperature in today's settings as a float. """
    for timestamp in app_settings.settings["ch"].keys():
        pass  # find temp setting for now
        # return


def control_ch():
    target = get_current_target_temp()
    low = target - app_settings.RANGE
    high = target + app_settings.RANG
    temp = float(get_temperature())

    if low <= temp and temp <= high:
        # current temperature is in desired range
        logging.info("CH: No action required (%f < %f < %f)", low, temp, high)
    elif temp < low:
        # room too cold
        ch_on()
        logging.info("CH: on (%f < %f)", temp, low)
    elif temp > high:
        # room too hot
        ch_off()
        logging.info("CH: off (%f > %f)", temp, high)


def control_hw():
    pass

if __name__=="__main__":
    """ Get today's settings and current temperature, decide
    what to do. This script is called once 2 or more minutes.
    Display is updated once a minute in a separate script.
    """
    control_ch()
    control_hw()

