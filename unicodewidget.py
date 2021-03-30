#!/usr/bin/env python3

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from widget import Widget
from PIL import Image, ImageDraw, ImageFont
import unicodedata
import re


class UnicodeWidget(Widget):
    def __init__(self,x=0,y=0,color=(255,255,255),size=32,width=64,height=64):
        super(UnicodeWidget,self).__init__(x,y,color,size,width,height)
        self.font = ImageFont.truetype("TwitterColorEmoji-SVGinOT.ttf",self.size)
        # self.font = ImageFont.truetype("NotoColorEmoji.ttf",109,0)
        self.text = None

    def update(self,t=None,description=None):
        if description != None:
            try:
                t = unicodedata.lookup(description)
            except KeyError:
                print("symbol "+description+" not found")
                t = None

            # if re.search("[Tt]ree",description):
            #     self.color=(0,255,0)
            # elif re.search("[sS]un",description):
            #     self.color=(255,255,0)
            # elif re.search("[rR]ain",description):
            #     self.color=(64,64,255)

        if t == None:
            return
        if (self.text != t):
            self.image = Image.new("RGBA",(self.width,self.height))
            draw = ImageDraw.Draw(self.image)
            draw.text((self.x,self.y),t,font=self.font,fill=self.color)
            self.text = t
            self.changed = True
        else:
            self.changed = False



if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64

    matrix = RGBMatrix(options = options)

    while True:
        u = UnicodeWidget(size=16,color=(255,0,0))
        u.update(description=input("symbol:"))
        if (u.changed):
            im = Image.new("RGBA",(64,64))
            im.alpha_composite(u.image)
            matrix.SetImage(im.convert("RGB"))
        


