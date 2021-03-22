#!/usr/bin/env python

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from widget import Widget
from PIL import Image, ImageDraw, ImageFont
import time


class TimeWidget(Widget):
    def __init__(self,x=0,y=0,color=(255,255,255),width=64,height=64):
        super(TimeWidget,self).__init__(x,y,color,width,height)
        self.font = ImageFont.truetype("Roboto-Thin.ttf",15)
        self.lasttimestring = ""

    def update(self):
        current_time = time.localtime()
        time_string = time.strftime("%H:%M",current_time)
        if (self.lasttimestring != time_string):
            self.image = Image.new("RGBA",(self.width,self.height))
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


