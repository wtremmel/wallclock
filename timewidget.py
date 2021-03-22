#!/usr/bin/env python

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont
import time


class TimeWidget():
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



if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64

    matrix = RGBMatrix(options = options)

    currenttime = TimeWidget()

    while True:
        currenttime.update();
        if (currenttime.changed):
            matrix.SetImage(currenttime.image.convert("RGB"))


