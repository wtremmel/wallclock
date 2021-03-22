#!/usr/bin/env python

from clockface import ClockFace
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont
import time


class TimeImage():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = Image.new("RGBA",(64,64))
        self.font = ImageFont.truetype("Roboto-Thin.ttf",15)
        self.color= (0,255,0)
        self.lasttimestring = ""
        self.changed = True

    def update(self):
        current_time = time.localtime()
        time_string = time.strftime("%H:%M",current_time)
        if (self.lasttimestring != time_string):
            self.image = Image.new("RGBA",(64,64))
            draw = ImageDraw.Draw(self.image)
            draw.text((self.x,self.y),time_string,font=self.font,fill=self.color)
            self.lasttimestring = time_string
            self.changed = True
        else:
            self.changed = False


class DateImage():
    def __init__(self):
        self.x = 0
        self.y = 15
        self.image = Image.new("RGBA",(64,64))
        self.font = ImageFont.truetype("Roboto-Thin.ttf",12)
        self.color= (0,0,255)
        self.laststring = ""
        self.changed = True

    def update(self):
        current_date = time.localtime()
        date_string = time.strftime("%a %d.%m.",current_date)
        if (date_string != self.laststring):
            self.image = Image.new("RGBA",(64,64))
            draw = ImageDraw.Draw(self.image)
            draw.text((self.x,self.y),date_string,font=self.font,fill=self.color)
            self.laststring = date_string
            self.changed = True
        else:
            self.changed = False

class Seconds():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = Image.new("RGBA",(64,64))
        self.color= (128,128,128)
        self.lastsec = 0
        self.changed = True

    def update(self):
        sec = time.localtime().tm_sec
        if (sec != self.lastsec):
            draw = ImageDraw.Draw(self.image)
            if (sec == 0):
                draw.line([(self.x,self.y),(self.x+61,self.y)],(0,0,0),1)
            else:
                draw.line([(self.x,self.y),(self.x+sec-1,self.y)],self.color,1)
            self.lastsec = sec
            self.changed = True
        else:
            self.changed = False



if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64

    matrix = RGBMatrix(options = options)

    currenttime = TimeImage()
    today = DateImage()
    seconds = Seconds()

    while True:
        currenttime.update();
        today.update()
        seconds.update()
        if (seconds.changed or today.changed or currenttime.changed):
            im = Image.new("RGBA",(64,64))
            im.paste(today.image)
            im.alpha_composite(currenttime.image)
            im.alpha_composite(seconds.image)
            matrix.SetImage(im.convert("RGB"))


