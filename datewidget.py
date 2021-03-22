#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageFont
from widget import Widget
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time


class DateWidget(Widget):
    def __init__(self,x=0,y=0,color=(255,255,255),width=64,height=64):
        super(DateWidget,self).__init__(x,y,color,width,height)
        self.font = ImageFont.truetype("Roboto-Thin.ttf",12)
        self.laststring = ""

    def update(self):
        current_date = time.localtime()
        date_string = time.strftime("%a %d.%m.",current_date)
        if (date_string != self.laststring):
            self.image = Image.new("RGBA",(self.width,self.height))
            draw = ImageDraw.Draw(self.image)
            draw.text((self.x,self.y),date_string,font=self.font,fill=self.color)
            self.laststring = date_string
            self.changed = True
        else:
            self.changed = False


if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64

    matrix = RGBMatrix(options = options)

    currentdate = DateWidget()

    while True:
        currentdate.update();
        if (currentdate.changed):
            matrix.SetImage(currentdate.image.convert("RGB"))


