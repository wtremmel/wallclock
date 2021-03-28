#!/usr/bin/env python3

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from widget import Widget
from PIL import Image, ImageDraw, ImageFont
from astral import *
from astral import moon
from astral.sun import *
import datetime
import random
import time

class SunWidget(Widget):
    def __init__(self,x=0,y=0,color=(255,255,255),size=32,width=64,height=64):
        super(SunWidget,self).__init__(x,y,color,size,width,height)
        self.location = LocationInfo("Bad Homburg","Germany","Europe/Berlin",50.226831,8.618162)
        self.lastupdate = 0
        self.elevation = 0

    def drawSun(self,now = None):
        su = Image.new("RGBA",(self.size,self.size))
        bg = Image.new("RGBA",(self.width,self.height))
        dr = ImageDraw.Draw(su)
        radius = self.size/3

        sunx1 = self.size/2 - radius
        sunx2 = self.size/2 + radius

        z= zenith(self.location.observer,now)
        height = elevation(self.location.observer,now)
        percentage = (height / z) * 100.0
        c = self.size - self.size * percentage / 100
        el = [sunx1,c-radius,sunx2,c+radius]

        self.elevation = height

        # print("zenith =",z)
        # print("elevation =",height)
        # print("percentage=",percentage)
        # print("center=",center)

        if (self.elevation >= 0):
            dr.ellipse(el,fill=(100,100,0),width=0)
            bg.paste(su,(self.x,self.y))
        return bg

    def drawMoon(self,now = None):
        bg = Image.new("RGBA",(self.width,self.height))
        dr = ImageDraw.Draw(bg)
        radius = self.size/5
        sunx1 = self.x + self.size/2 - radius
        sunx2 = self.x + self.size/2 + radius
        suny1 = self.y + self.size/2 - radius
        suny2 = self.y + self.size/2 + radius

        phase = moon.phase(now)
        # print("Moonphase = ",phase)
        el = [sunx1,suny1,sunx2,suny2]
        dr.ellipse(el,fill=(5,5,5),width=0)

        if phase < 7:
            # new moon 0
            pass 
        elif phase < 14:
            # first quarter
            pass
        elif phase < 21:
            # full moon
            pass
        elif phase < 28:
            # last quarter 360 = phase/28 * 360
            pass

        angle = phase/28*360
        start = 180 - angle/2
        end = 180 + angle/2

        dr.pieslice(el,start,end,fill=(80,80,80))

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
            print("blue hour")
            dr.rectangle(rect,fill=(0,0,70),outline=outline)
            return bg

        tw1 = twilight(self.location.observer,direction = SunDirection.SETTING)
        tw2 = twilight(self.location.observer,direction = SunDirection.RISING)
        if (now >= tw1[0] and now <= tw1[1]) or (now >= tw2[0] and now <= tw2[1]):
            print("twilight")
            dr.rectangle(rect,fill=(20,10,40),outline=outline)
            return bg

        go1 = golden_hour(self.location.observer,direction = SunDirection.SETTING)
        go2 = golden_hour(self.location.observer,direction = SunDirection.RISING)
        if (now >= go1[0] and now <= go1[1]) or (now >= go2[0] and now <= go2[1]):
            print("golden hour")
            dr.rectangle(rect,fill=(90,60,0),outline=outline)
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



    def update(self,t=None):
        """Draws a sun or a moon depending on the time of day"""
        if (t == None and time.time() < self.lastupdate+60):
            self.changed = False
            return
        else:
            self.lastupdate = time.time()

        s = sun(self.location.observer)
        if t == None:
            now = datetime.datetime.now(datetime.timezone.utc)
        else:
            now = datetime.datetime.fromisoformat("2021-03-27 "+t+"+00:00")
        s["now"] = now

        self.image = self.background(now=now)
        self.image.alpha_composite(self.drawSun(now=now))

        if self.elevation < 0:
            self.image.alpha_composite(self.drawMoon(now=now))

        self.changed = True

if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.hardware_mapping = "adafruit-hat-pwm"

    matrix = RGBMatrix(options = options)

    u = SunWidget(size=16)
        
    while True:
        t = input("HH:MM ")
        u.update(t)
        if (u.changed):
            matrix.SetImage(u.image.convert("RGB"))
            u.changed = False
