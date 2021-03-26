#!/usr/bin/env python

from PIL import Image

class Widget():
    def __init__(self,x=0,y=0,color=(255,255,255),size=15,width=64,height=64):
        self.x = x
        self.y = y
        self.size = size
        self.image = Image.new("RGBA",(width,height))
        self.color= color
        self.changed = False
        self.width = width
        self.height = height

    def size2font(self,size=15):
        if size == 6:
            return "4x6.pil"
        elif size == 7:
            return "5x7.pil"
        elif size == 8:
            return "5x8.pil"
        elif size == 9:
            return "6x9.pil"
        elif size == 10 or size == 11:
            return "6x10.pil"
        elif size == 12:
            return "6x12.pil"
        elif size == 13:
            return "7x13.pil"
        elif size == 14:
            return "7x14.pil"
        elif size == 15 or size == 16 or size == 17:
            return "9x15.pil"
        elif size == 18:
            return "9x18.pil"
        elif size == 19:
            return "9x18B.pil"
        elif size >= 20:
            return "10x20.pil"





