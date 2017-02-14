#!/usr/bin/env python

from oled import ssd1306
from smbus import SMBus
import time
import pigpio
import DHT22
import urllib2
from PIL import ImageFont, ImageDraw, Image

i2cbus = SMBus(1)  # 1 = Raspberry Pi but NOT early REV1 board
display = ssd1306(i2cbus)
image = display.image
canvas = display.canvas
font = ImageFont.truetype('Roboto-Light.ttf', 11)

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


def get_temperature():
    """ Get room temperature from WiFi sensor or fail-over to
        the on-board sensor.
    """

    def get_gpio_temp():
        try:
            pi = pigpio.pi()
            dht22 = DHT22.sensor(pi, 24)
            dht22.trigger()
            time.sleep(0.2)
            return dht22.temperature()
        except:
            print ">> Failed to get local temperature"
            return -999

    def get_wifi_temp():
        try:
            status, temp, humid = urllib2.urlopen(URL).read().strip().split(",")
            if status == "0":
                return float(temp)
            else:
                print "Sensor error"
                return -999
        except:
            print "Network error"
            return -999

    wifi_temp = get_wifi_temp()
    if wifi_temp != -999:
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
    text(80, 12, "%fC" % temp if temp != -999 else 88.8, fill=0)

    # vertical line
    #canvas.line((63, 0, 63, 63), fill=1)

    #text(58,0,"CH",fill=0)
    #text(75,0,"HW",fill=0)

    # CH settings filler
    text_cell(col="l",row=1,txt="08:00 20C")
    text_cell(col="l",row=2,txt="11:30 18C")
    text_cell(col="l",row=3,txt="14:30 22C")
    text_cell(col="l",row=4,txt="20:30 20C")
    text_cell(col="l",row=5,txt="23:30 16C",bg=True)

    # HW settings filler
    text_cell(col="r",row=1,txt="07:30 +10m",bg=True)
    text_cell(col="r",row=2,txt="17:30 +20m")
    text_cell(col="r",row=3,txt="20:30 +30m")


def save_bmp():
    image.save('display.bmp','BMP')


if __name__ == "__main__":
    paint_canvas()
    save_bmp()
    display.flush()
