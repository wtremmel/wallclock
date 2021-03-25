#!/usr/bin/env python3

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from widget import Widget
from PIL import Image, ImageDraw
from threading import Timer
import time

class FrameAlert(Widget):
    def __init__(self,x=0,y=0,color=None,width=64,height=64):
        if color is None:
            self.color = (255,0,0)
        else:
            self.color = color
        super(FrameAlert,self).__init__(x,y,self.color,width,height)

    def blinkon(self):
        self.image = Image.new("RGBA",(self.width,self.height))
        draw = ImageDraw.Draw(self.image)
        draw.rectangle([self.x,self.y,self.width-1,self.height-1],outline=self.color)
        self.changed = True

    def blinkoff(self):
        self.image = Image.new("RGBA",(self.width,self.height))
        draw = ImageDraw.Draw(self.image)
        draw.rectangle([self.x,self.y,self.width-1,self.height-1],outline=(0,0,0))
        self.changed = True

    def update(self,count=3,duration=0.1,pause=0.1):
        if count > 0:
            self.blinkon()
            t = Timer(duration,self.blinkoff)
            t.start()
            for x in range(count):
                s = Timer(pause*x,self.blinkon)
                s.start()
                o = Timer(pause*x+duration,self.blinkoff)
                o.start()
            

if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64

    matrix = RGBMatrix(options = options)

    alertframe = FrameAlert()
    alertframe.update(count=5,duration=0.1,pause=0.2)

    while True:
        if (alertframe.changed):
            matrix.SetImage(alertframe.image.convert("RGB"))
        time.sleep(0.1)


