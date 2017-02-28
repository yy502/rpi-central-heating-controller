#!/usr/bin/env python

from lib.oled import ssd1306
from smbus import SMBus
import sys
import time
import pigpio
import lib.dht22 as dht
import urllib2
from PIL import ImageFont, ImageDraw, Image
from logger import *
import app_settings

pi = pigpio.pi()
dht22 = dht.sensor(pi, app_settings.LOCAL)

i2cbus = SMBus(1)  # 1 = Raspberry Pi but NOT early REV1 board
display = ssd1306(i2cbus)
image = display.image
canvas = display.canvas

font = ImageFont.truetype("Roboto-Light.ttf", 11)

LEFT_COLUMN_X = 3
RIGHT_COLUMN_X = 63
ROW_HEIGHT = 13


def text(x, y, txt, fill=1, bg=False):
    """ Wrapper to display texts with or without background """
    if bg:
        w,h = canvas.textsize(txt,font=font)
        canvas.rectangle((x, y, x+w, y+h), outline=1, fill=1)
        fill=0
    canvas.text((x, y-2), txt, font=font, fill=fill)


def text_cell(col=None, row=0, txt="", bg=False):
    """ Put texts in a predefined cell in left or right column
        of the OLED display.
        
        [  L1  ][ time ]
        [  L2  ][ temp ]
        [  L3  ][  R1  ]
        [  L4  ][  R2  ]
        [  L5  ][  R3  ]
    """
    if col == 'l':
        x = LEFT_COLUMN_X
    elif col == 'r':
        x = RIGHT_COLUMN_X
        row = row + 2
    else:
        raise ValueError('col must be "l" (left) or "r" (right)')
    text(x,(row-1)*ROW_HEIGHT,txt,fill=(0 if bg else 1),bg=bg)


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


def paint_canvas():
    """ Draw a new canvas with updated values, save as an image file
        and make the canvas object ready for display by OLED lib.
    """
    # top-right box
    canvas.rectangle((63,0,127,23), outline=1, fill=1)
    text(67, 0, time.strftime("%d/%m %H:%M",time.localtime(time.time())), fill=0)
    temp = get_temperature()
    text(80, 12, "%sC" % temp, fill=0)

    # vertical line
    #canvas.line((63, 0, 63, 63), fill=1)

    #text(58,0,"CH",fill=0)
    #text(75,0,"HW",fill=0)

    # CH settings filler
    text_cell(col="l",row=1,txt="08:00 20C")
    text_cell(col="l",row=2,txt="11:30 18C",bg=True)
    text_cell(col="l",row=3,txt="14:30 22C")
    text_cell(col="l",row=4,txt="20:30 20C")
    text_cell(col="l",row=5,txt="23:30 16C")

    # HW settings filler
    text_cell(col="r",row=1,txt="07:30 +10m")
    text_cell(col="r",row=2,txt="17:30 +20m",bg=True)
    text_cell(col="r",row=3,txt="20:30 +30m")


def save_bmp():
    image.save("display.bmp","BMP")


if __name__ == "__main__":
    paint_canvas()
    save_bmp()
    display.flush()
