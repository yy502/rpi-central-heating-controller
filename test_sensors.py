#!/usr/bin/env python

from sensors import get_gpio_temp, get_wifi_temp
from logger import *
import time

if __name__=="__main__":
    """ Get room temperature from WiFi and the on-board sensor """
    while True:
        
        local = get_gpio_temp()
        remote = get_wifi_temp()
        diff = float(local)-float(remote)
        
        logging.info("Diff: %.1fC", diff)
        
        time.sleep(57)
