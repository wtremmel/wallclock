#!/usr/bin/env python

import time
from widget import Widget
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont


class SecondsWidget(Widget):
    def __init__(self,x=0,y=0,color=(255,255,255),width=64,height=64):
        super(SecondsWidget,self).__init__(x,y,color,width,height)
        self.lastsec = -1

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

    seconds = SecondsWidget()

    while True:
        seconds.update();
        if (seconds.changed):
             matrix.SetImage(seconds.image.convert("RGB"))


