#!/usr/bin/env python

from sensors import get_gpio_temp, get_wifi_temp
from display import text
from logger import *
from lib.oled import ssd1306
from smbus import SMBus

display = ssd1306(SMBus(1))


if __name__=="__main__":
    """ Get room temperature from WiFi and the on-board sensor """
    while True:
        display.clear()
        
        image = display.image
        canvas = display.canvas
        
        local = get_gpio_temp()
        remote = get_wifi_temp()
        diff = float(local)-float(remote)
        
        logging.info("Diff: %.1fC", diff)
        
        text(0,0,"Local: %s" % local)
        text(0,20,"Remote: %s" % remote)
        text(0,40,"Diff: %.1f" % diff)
        
        display.flush()
        
        time.sleep(57)
