#!/usr/bin/env python

import time
import pigpio
import lib.dht22 as dht
import urllib2

URL = "http://192.168.0.41"

def get_gpio_temp():
    try:
        pi = pigpio.pi()
        dht22 = dht.sensor(pi, 24)
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
    print "On-board DHT22 sensor: %sC" % get_gpio_temp()
    print "WiFi DHT22 sensor: %sC" % get_wifi_temp()
