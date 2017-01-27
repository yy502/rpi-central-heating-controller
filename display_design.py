#!/usr/bin/env python

import time
from PIL import ImageFont, ImageDraw, Image

image = Image.new('1', (128, 64))
canvas = ImageDraw.Draw(image)
font = ImageFont.truetype('Roboto-Light.ttf', 9)

def text(x, y, txt, fill=1, bg=False):
    if bg:
        w,h = canvas.textsize(txt,font=font)
        canvas.rectangle((x, y, x+w, y+h), outline=1, fill=1)
        fill=0
    canvas.text((x, y), txt, font=font, fill=fill)

# top bar bg
canvas.rectangle((0,0,127,10), outline=1, fill=1)
text(3, 0, time.strftime("%d/%m %H:%M",time.localtime(time.time())), fill=0)
text(103, 0, "20.3C", fill=0)

# vr line
canvas.line((73, 10, 73, 63), fill=1)

text(58,0,"CH",fill=0)
text(75,0,"HW",fill=0)

# CH settings filler
text(3,13,"08:00-11:30  20c")
text(3,23,"11:30-14:30  18c")
text(3,33,"14:30-20:30  22c")
text(3,43,"20:30-23:00  20c")
text(3,53,"23:30-08:00  16c",fill=0,bg=1)

# HW settings filler
text(78,13,"07:30-08:00",fill=0,bg=1)
text(78,23,"17:30-18:00")

image.save('display_design.bmp','BMP')