#!/usr/bin/env python3

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from widget import Widget
from PIL import Image, ImageDraw, ImageFont
import time


class FensterWidget(Widget):
    def __init__(self,x=0,y=0,color=(255,255,255),size=15,width=64,height=64):
        super(FensterWidget,self).__init__(x,y,color,size,width,height)
        self.lastupdate = 0
        self.fensterliste = {}

    def update(self,fenster=None, openclose=None):
        pass




if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64

    matrix = RGBMatrix(options = options)

    u = FensterWidget(size=32)
    u.update("/Chattenweg5/Fenster/Bad1","0")
    u.update("/Chattenweg5/Fenster/Bad2","1")
    while True:
        if (u.changed):
            matrix.SetImage(u.image.convert("RGB"))
        


