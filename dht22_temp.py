#!/usr/bin/env python

import time
import pigpio
import DHT22

# Intervals of about 2 seconds or less will eventually hang the DHT22.
INTERVAL = 3

if __name__ == "__main__":

    pi = pigpio.pi()
    s = DHT22.sensor(pi, 24)

    try:
        while True:
            s.trigger()
            time.sleep(0.2)
            print s.temperature()
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print 'Exiting...'

