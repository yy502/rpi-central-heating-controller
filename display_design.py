#!/usr/bin/env python

import time
from PIL import ImageFont, ImageDraw, Image

image = Image.new('1', (128, 64))
canvas = ImageDraw.Draw(image)
font = ImageFont.truetype('Roboto-Light.ttf', 11)

LEFT_COLUMN_X = 3
RIGHT_COLUMN_X = 63
LINE_HEIGHT = 13

def text(x, y, txt, fill=1, bg=False):
    if bg:
        w,h = canvas.textsize(txt,font=font)
        canvas.rectangle((x, y, x+w, y+h), outline=1, fill=1)
        fill=0
    canvas.text((x, y-2), txt, font=font, fill=fill)

def text_cell(col=None, row=0, txt="", bg=False):
    if col == 'l':
        x = LEFT_COLUMN_X
    elif col == 'r':
        x = RIGHT_COLUMN_X
        row = row + 2
    else:
        raise ValueError('col must be "l" (left) or "r" (right)')
    text(x,(row-1)*13,txt,fill=(0 if bg else 1),bg=bg)


# top-right box
canvas.rectangle((63,0,127,23), outline=1, fill=1)
text(67, 0, time.strftime("%d/%m %H:%M",time.localtime(time.time())), fill=0)
text(80, 12, "20.3C", fill=0)

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

image.save('display_design.bmp','BMP')