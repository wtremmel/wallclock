#!/usr/bin/env python3

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from widget import Widget
from PIL import Image, ImageDraw, ImageFont
import unicodedata


class TemperatureWidget(Widget):
    def __init__(self,x=0,y=0,color=(255,255,255),size=15,width=64,height=64):
        super(TemperatureWidget,self).__init__(x,y,color,size,width,height)
        self.font = ImageFont.truetype("Roboto-Thin.ttf",self.size)
        self.lasttemp = None

    def update(self,temperature=None):
        if temperature == None:
            return
        t = float(temperature)
        if (self.lasttemp != t):
            tempStr = "{:2.1f}".format(t) + "C"
            self.image = Image.new("RGBA",(self.width,self.height))
            if (t< 0):
                self.color=(0,0,255)
            elif (t< 10):
                self.color=(0,128,255)
            elif (t< 15):
                self.color=(255,255,0)
            elif (t< 20):
                self.color=(255,192,0)
            elif (t< 25):
                self.color=(255,128,0)
            elif (t< 30):
                self.color=(255,64,0)
            else:
                self.color=(255,0,0)
            draw = ImageDraw.Draw(self.image)
            draw.text((self.x,self.y),tempStr,font=self.font,fill=self.color)
            self.lasttemp = t
            self.changed = True
        else:
            self.changed = False



if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64

    matrix = RGBMatrix(options = options)

    currenttemp = TemperatureWidget(size=12)
    currenttemp.update(16.9)
    while True:
        if (currenttemp.changed):
            matrix.SetImage(currenttemp.image.convert("RGB"))
        


