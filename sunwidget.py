#!/usr/bin/env python3

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from widget import Widget
from PIL import Image, ImageDraw, ImageFont
from astral import *
import datetime
from astral.sun import *
import random
import time

class SunWidget(Widget):
    def __init__(self,x=0,y=0,color=(255,255,255),size=32,width=64,height=64):
        super(SunWidget,self).__init__(x,y,color,size,width,height)
        self.location = LocationInfo("Bad Homburg","Germany","Europe/Berlin",50.226831,8.618162)
        self.lastupdate = 0

    def drawSun(self,now = None):
        bg = Image.new("RGBA",(self.width,self.height))
        dr = ImageDraw.Draw(bg)
        rect = [self.x,self.y,self.x+self.size-1,self.y+self.size-1]
        radius = self.size/4

        sunx1 = self.x + self.size/2 - radius
        sunx2 = self.x + self.size/2 + radius
        el = [sunx1,self.y,sunx2,self.y + self.size/2]

        z= zenith(self.location.observer,now)
        height = elevation(self.location.observer,now)

        print("zenith =",z)
        print("elevation =",height)

        dr.ellipse(el,fill=(100,100,0),width=0)
        return bg

    def background(self,now = None):
        bg = Image.new("RGBA",(self.width,self.height))
        dr = ImageDraw.Draw(bg)
        rect = [self.x,self.y,self.x+self.size-1,self.y+self.size-1]
        outline = (100,100,100)

        if now == None:
            now = datetime.datetime.now(datetime.timezone.utc)

        bh1 = blue_hour(self.location.observer,direction = SunDirection.SETTING)
        bh2 = blue_hour(self.location.observer,direction = SunDirection.RISING)
        if (now >= bh1[0] and now <= bh1[1]) or (now >= bh2[0] and now <= bh2[1]):
            dr.rectangle(rect,fill=(0,0,50),outline=outline)
            return bg

        go1 = golden_hour(self.location.observer,direction = SunDirection.SETTING)
        go2 = golden_hour(self.location.observer,direction = SunDirection.RISING)
        if (now >= go1[0] and now <= go1[1]) or (now >= go2[0] and now <= go2[1]):
            dr.rectangle(rect,fill=(90,60,0),outline=outline)
            return bg

        tw1 = twilight(self.location.observer,direction = SunDirection.SETTING)
        tw2 = twilight(self.location.observer,direction = SunDirection.RISING)
        if (now >= tw1[0] and now <= tw1[1]) or (now >= tw2[0] and now <= tw2[1]):
            dr.rectangle(rect,fill=(20,10,50),outline=outline)
            return bg

        ni = night(self.location.observer)
        if (now >= ni[0] and now <= ni[1]):
            dr.rectangle(rect,fill=(0,0,5),outline=outline)
            for i in range(20):
                starx = random.randrange(self.x+1,self.x+self.size-2)
                stary = random.randrange(self.y+1,self.y+self.size-2)
                starbri= random.randrange(5,50)
                dr.point([starx,stary],fill=(starbri,starbri,starbri))
            return bg

        da = daylight(self.location.observer)
        if (now >= da[0] and now <= da[1]):
            dr.rectangle(rect,fill=(30,80,150),outline=outline)
            return bg



    def update(self):
        """Draws a sun or a moon depending on the time of day"""
        if (time.time() < self.lastupdate+60):
            self.changed = False
            return
        else:
            self.lastupdate = time.time()

        now = datetime.datetime.now(datetime.timezone.utc)
        s = sun(self.location.observer)
        # now = datetime.datetime.fromisoformat("2021-03-27 17:08+00:00")
        s["now"] = now
        (bluestart,blueend) = golden_hour(self.location.observer,direction = SunDirection.SETTING)
        # (bluestart,blueend) = daylight(self.location.observer)
        print((
            f'Dawn:    {s["dawn"]}\n'
            f'Sunrise: {s["sunrise"]}\n'
            f'Noon:    {s["noon"]}\n'
            f'Sunset:  {s["sunset"]}\n'
            f'Dusk:    {s["dusk"]}\n'
            f'Now:     {s["now"]}\n'
            f'from   {bluestart} to {blueend}\n'
        ))

        self.image = self.background(now=now)
        self.image.alpha_composite(self.drawSun(now=now))

        print("Elevation: ",elevation(self.location.observer))


        if (now > s["dawn"]):
            print("after dawn")
        if (now > s["sunrise"]):
            print("after sunrise")
        if (now > s["noon"]):
            print("after noon")
        if (now > s["sunset"]):
            print("after sunset")
        if (now > s["dusk"]):
            print("after dusk")

        if (now < s["dawn"]):
            print("before dawn")
        if (now < s["sunrise"]):
            print("before sunrise")
        if (now < s["noon"]):
            print("before noon")
        if (now < s["sunset"]):
            print("before sunset")
        if (now < s["dusk"]):
            print("before dusk")

        self.changed = True

if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.hardware_mapping = "adafruit-hat-pwm"

    matrix = RGBMatrix(options = options)

    u = SunWidget(size=16)
    u.update()
        
    while True:
        if (u.changed):
            matrix.SetImage(u.image.convert("RGB"))
            u.changed = False
