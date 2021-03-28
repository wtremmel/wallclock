#!/usr/bin/env python3

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from widget import Widget
from PIL import Image, ImageDraw, ImageFont
import re


class FensterWidget(Widget):
    def __init__(self,x=0,y=0,color=(255,255,255),size=2,width=64,height=64):
        super(FensterWidget,self).__init__(x,y,color,size,width,height)
        self.lastupdate = 0
        self.fensterliste = {}
        self.fenster = {}
        self.stockwerke = ("EG",1,2)
        self.fenster["EG"] = ("Haustuer","Kueche")
        self.fenster[1] = ("Bad1","Schlafzimmer")
        self.fenster[2] = ("Bad2","Arbeitszimmer")
        for s in self.stockwerke:
            for f in self.fenster[s]:
                self.fensterliste[f] = 0

    def update(self, topic=None, msg=None):
        if topic == None or msg == None:
            self.changed = False
            return

        isopen = msg.decode()

        fenster = re.search("/([a-zA-Z0-9]+)$",topic).group(1)
        print("fenster =",fenster)

        if self.fensterliste[fenster] != isopen:
            self.changed = True
            self.fensterliste[fenster] = isopen

        if self.changed:
            pixelcount = 0
            self.image = Image.new("RGBA",(self.width,self.height))
            draw = ImageDraw.Draw(self.image)
            for s in self.stockwerke:
                for f in self.fenster[s]:
                    if self.fensterliste[f] == 0:
                        fcolor = (0,255,0)
                    else:
                        fcolor = (255,0,0)
                    draw.rectangle([
                        self.x,self.y+(self.size)*pixelcount,
                        self.x+self.size-1,self.y+self.size+self.size*pixelcount],
                        fill=fcolor)
                    pixelcount += 1
                pixelcount += 1



if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64

    matrix = RGBMatrix(options = options)

    u = FensterWidget(size=2)
    u.update("/Chattenweg5/Fenster/Bad1",b"0")
    u.update("/Chattenweg5/Fenster/Bad2",b"1")
    while True:
        if (u.changed):
            matrix.SetImage(u.image.convert("RGB"))
        


