#!/usr/bin/env python

import time
import pigpio
import lib.dht22 as dht
import urllib2
from logger import *
import app_settings
from lib.oled import ssd1306
from smbus import SMBus
from PIL import ImageFont

i2cbus = SMBus(1)  # 1 = Raspberry Pi but NOT early REV1 board
display = ssd1306(i2cbus)

font = ImageFont.truetype("Roboto-Light.ttf", 18)

pi = pigpio.pi()
dht22 = dht.sensor(pi, app_settings.LOCAL)

def text(x, y, txt, fill=1, bg=False):
    """ Wrapper to display texts with or without background """
    if bg:
        w,h = canvas.textsize(txt,font=font)
        canvas.rectangle((x, y, x+w, y+h), outline=1, fill=1)
        fill=0
    canvas.text((x, y-2), txt, font=font, fill=fill)

def get_gpio_temp():
    """ Return a float number in string type """
    try:
        dht22.trigger()
        time.sleep(0.2)
        temp = "%.1f" % dht22.temperature()
        logging.info("On-board DHT22 sensor: %sC", temp)
        return temp
    except:
        logging.exception("On-board DHT22 sensor error")
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
        logging.exception("WiFi DHT22 sensor error")
        return "-999"

if __name__=="__main__":
    """ Get room temperature from WiFi and the on-board sensor """
    while True:
        local = get_gpio_temp()
        remote = get_wifi_temp()
        diff = float(local)-float(remote)
        logging.info("Diff: %.1fC", diff)
        image = display.image
        canvas = display.canvas
        display.clear()
        text(0,0,"Local: %s" % local)
        text(0,20,"Remote: %s" % remote)
        text(0,40,"Diff: %.1f" % diff)
        display.flush()
        time.sleep(57)
