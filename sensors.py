#!/usr/bin/env python

import sys
import time
import pigpio
import lib.dht22 as dht
import urllib2
from logger import *
import app_settings

pi = pigpio.pi()
dht22 = dht.sensor(pi, app_settings.LOCAL)


def get_gpio_temp():
    """ Return a float number in string type """
    try:
        dht22.trigger()
        time.sleep(0.2)
        temp = "%.1f" % dht22.temperature()
        logging.info("On-board DHT22 sensor: %sC", temp)
        return temp
    except:
        logging.error("On-board DHT22 sensor: %s", sys.exc_info()[0])
        return "-999"


def get_wifi_temp():
    """ Return a float number in string type """
    try:
        status, temp, humid = urllib2.urlopen(app_settings.REMOTE).read().strip().split(",")
        if status == "0":
            logging.info("WiFi DHT22 sensor: %.1fC", float(temp))
            return "%.1f" % float(temp)
        else:
            logging.error("WiFi DHT22 sensor: %s,%s,%s", status, temp, humid)
            return "-999"
    except:
        logging.error("WiFi DHT22 sensor: %s", sys.exc_info()[0])
        return "-999"


def get_temperature():
    """ Get room temperature from WiFi sensor or fail-over to
        the on-board sensor.
    """
    wifi_temp = get_wifi_temp()
    if wifi_temp != "-999":
        return wifi_temp
    else:
        return get_gpio_temp()


if __name__ == "__main__":
    get_gpio_temp()
    get_wifi_temp()