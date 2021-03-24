#!/usr/bin/env python

from PIL import Image

class Widget():
    def __init__(self,x=0,y=0,color=(255,255,255),width=64,height=64):
        self.x = x
        self.y = y
        self.image = Image.new("RGBA",(width,height))
        self.color= color
        self.changed = False
        self.width = width
        self.height = height



