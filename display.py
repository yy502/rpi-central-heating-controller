#!/usr/bin/env python

from oled import ssd1306
import time
from PIL import ImageFont, ImageDraw, Image
from smbus import SMBus
i2cbus = SMBus(1)  # 1 = Raspberry Pi but NOT early REV1 board

display = ssd1306(i2cbus)
canvas = display.canvas   # display contents are drawn onto this canvas
                          # then call flush() to send to the display module


#canvas.rectangle((0, 0, display.width-1, display.height-1), outline=1, fill=0)
#canvas.ellipse((x, top, x+shape_width, bottom), outline=1, fill=0)
#canvas.rectangle((x, top, x+shape_width, bottom), outline=1, fill=1)
#canvas.polygon([(x, bottom), (x+shape_width/2, top), (x+shape_width, bottom)], outline=1, fill=0)
#canvas.line((x, bottom, x+shape_width, top), fill=1)

#sleep(1.5)
#logo = Image.open('resources/pi_logo.png')
#canvas.bitmap((32, 0), logo, fill=0)
#display.flush()

font = ImageFont.truetype('Roboto-Light.ttf', 12)

canvas.text((0, 0), time.strftime("%Y-%m-%d %H:%M %a",time.localtime(time.time())), font=font, fill=1)
canvas.line((0, 14, 127, 14), fill=1)
display.flush()


#display.onoff(0)   # turn off
#sleep(1.5)
#display.onoff(1)   # wake up

#sleep(1.5)
#display.clear()      # clear
