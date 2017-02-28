#!/usr/bin/env python

import time
import pigpio
import lib.dht22 as dht
import urllib2
import logger
import logging

URL = "http://192.168.0.41"
pi = pigpio.pi()
dht22 = dht.sensor(pi, 24)

def get_gpio_temp():
    try:
        dht22.trigger()
        time.sleep(0.2)
        return "%.1f" % dht22.temperature()
    except:
        print "Failed to get local temperature"
        return "-999"

def get_wifi_temp():
    try:
        status, temp, humid = urllib2.urlopen(URL).read().strip().split(",")
        if status == "0":
            return "%.1f" % float(temp)
        else:
            print "Sensor error"
            return "-999"
    except:
        print "Network error"
        return "-999"

if __name__=="__main__":
    """ Get room temperature from WiFi and the on-board sensor """
    while True:
        local = get_gpio_temp()
        remote = get_wifi_temp()
        logging.info("On-board DHT22 sensor: %sC", local)
        logging.info("WiFi DHT22 sensor:     %sC", remote)
        logging.info("Diff:                   %.1fC", float(local)-float(remote))
        time.sleep(57)
