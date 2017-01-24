#!/usr/bin/env python

from oled import ssd1306
from time import sleep
from PIL import ImageFont, ImageDraw, Image
from smbus import SMBus                  #  These are the only two variant lines !!
i2cbus = SMBus(1)                        # 1 = Raspberry Pi but NOT early REV1 board

display = ssd1306(i2cbus)
canvas = display.canvas   # "draw" onto this canvas, then call flush() to send the canvas contents to the hardware.


# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
#padding = 2
#shape_width = 20
#top = padding
#bottom = display.height - padding - 1
# Draw a rectangle of the same size of screen
#canvas.rectangle((0, 0, display.width-1, display.height-1), outline=1, fill=0)
# Move left to right keeping track of the current x position for drawing shapes.
#x = padding

# Draw an ellipse.
#canvas.ellipse((x, top, x+shape_width, bottom), outline=1, fill=0)
#x += shape_width + padding
# Draw a filled rectangle.
#canvas.rectangle((x, top, x+shape_width, bottom), outline=1, fill=1)
#x += shape_width + padding
# Draw a triangle.
#canvas.polygon([(x, bottom), (x+shape_width/2, top), (x+shape_width, bottom)], outline=1, fill=0)
#x += shape_width+padding
# Draw an X.
#canvas.line((x, bottom, x+shape_width, top), fill=1)
#canvas.line((x, top, x+shape_width, bottom), fill=1)
#x += shape_width+padding

# Load default font.
#font = ImageFont.load_default()

# Write two lines of text.
#canvas.text((x, top),    'Hello',  font=font, fill=1)
#canvas.text((x, top+40), 'World!', font=font, fill=1)
#display.flush()

#sleep(1.5)
#canvas.rectangle((0, 0, display.width-1, display.height-1), outline=255, fill=1)
#display.flush()

#sleep(1.5)
#logo = Image.open('resources/pi_logo.png')
#canvas.bitmap((32, 0), logo, fill=0)
#display.flush()

#sleep(1.5)
#canvas.rectangle((0, 0, display.width-1, display.height-1), outline=1, fill=0)
#font = ImageFont.truetype('resources/FreeSerifItalic.ttf', 57)
#canvas.text((18, 0), 'A5y', font=font, fill=1)
#display.flush()

#sleep(1.5)
#canvas.rectangle((0, 0, display.width-1, display.height-1), outline=1, fill=0)
font = ImageFont.truetype('FreeSans.ttf', 10)
canvas.text((0, 0), 'Hello me very good mateys ...', font=font, fill=1)
canvas.text((0, 10), 'Well now, what would you like', font=font, fill=1)
canvas.text((0, 20), 'to be told this sunny Sunday?', font=font, fill=1)
canvas.text((0, 30), 'Would a wild story amuse you?', font=font, fill=1)
canvas.text((0, 40), 'This is a very long statement,', font=font, fill=1)
canvas.text((0, 50), 'so believe it if you like.', font=font, fill=1)
display.flush()


#sleep(1.5)
#canvas.rectangle((0, 0, display.width-1, display.height-1), outline=20, fill=0)
#font = ImageFont.truetype('resources/FreeSans.ttf', 14)
#canvas.text((0, 0), 'Hello me good mateys', font=font, fill=1)
#canvas.text((0, 15), 'What would you like', font=font, fill=1)
#canvas.text((0, 30), 'to be told this day?', font=font, fill=1)
#canvas.text((0, 45), 'This is a long story,', font=font, fill=1)
#display.flush()

#sleep(1.5)
#display.onoff(0)   # turn off
#sleep(1.5)
#display.onoff(1)   # wake up

#sleep(1.5)
#display.clear()      # clear
