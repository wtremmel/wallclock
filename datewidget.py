#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageFont
from widget import Widget
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time


class DateWidget(Widget):
    def __init__(self,x=0,y=0,color=(255,255,255),size=12,width=64,height=64,font=None):
        super(DateWidget,self).__init__(x,y,color,size,width,height)
        if font:
            self.font = ImageFont.load("fonts/"+font)
        else:
            self.font = ImageFont.load("fonts/"+self.size2font(size))

        self.lastday = -1

    def update(self):
        current_date = time.localtime()
        if (self.lastday != current_date.tm_mday):
            date_string = time.strftime("%a %d.%m.",current_date)
            self.image = Image.new("RGBA",(self.width,self.height))
            draw = ImageDraw.Draw(self.image)
            draw.text((self.x,self.y),date_string,font=self.font,fill=self.color)
            self.lastday = current_date.tm_mday
            self.changed = True
        else:
            self.changed = False


if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.parallel = 1
    options.chain_length = 1
    options.hardware_mapping = "adafruit-hat-pwm"

    matrix = RGBMatrix(options = options)

    currentdate = DateWidget(size=9)

    while True:
        currentdate.update();
        if (currentdate.changed):
            matrix.SetImage(currentdate.image.convert("RGB"))


