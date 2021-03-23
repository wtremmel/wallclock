#!/usr/bin/env python3

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from widget import Widget
from PIL import Image, ImageDraw, ImageFont


class TemperatureWidget(Widget):
    def __init__(self,x=0,y=0,color=(255,255,255),width=64,height=64):
        super(TemperatureWidget,self).__init__(x,y,color,width,height)
        self.font = ImageFont.truetype("Roboto-Thin.ttf",15)
        self.lasttemp = -100

    def update(self,temperature):
        if (self.lasttemp != temperature):
            tempStr = "{:2.1f}".format(temperature) + "C"
            self.image = Image.new("RGBA",(self.width,self.height))
            if (temperature < 0):
                self.color=(0,0,255)
            elif (temperature < 10):
                self.color=(0,128,255)
            elif (temperature < 15):
                self.color=(255,255,0)
            elif (temperature < 20):
                self.color=(255,192,0)
            elif (temperature < 25):
                self.color=(255,128,0)
            elif (temperature < 30):
                self.color=(255,64,0)
            else:
                self.color=(255,0,0)
            draw = ImageDraw.Draw(self.image)
            draw.text((self.x,self.y),tempStr,font=self.font,fill=self.color)
            self.lasttemp = temperature
            self.changed = True
        else:
            self.changed = False



if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64

    matrix = RGBMatrix(options = options)

    currenttemp = TemperatureWidget()

    while True:
        currenttemp.update(18.8)
        if (currenttemp.changed):
            matrix.SetImage(currenttemp.image.convert("RGB"))
        


