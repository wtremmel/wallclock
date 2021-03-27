#!/usr/bin/env python3

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from widget import Widget
from PIL import Image, ImageDraw, ImageFont
from astral import *
import datetime
from astral.sun import *

class SunWidget(Widget):
    def __init__(self,x=0,y=0,color=(255,255,255),size=32,width=64,height=64):
        super(SunWidget,self).__init__(x,y,color,size,width,height)
        self.location = LocationInfo("Bad Homburg","Germany","Europe/Berlin",50.226831,8.618162)

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

        tw1 = twilight(self.location.observer,direction = SunDirection.SETTING)
        tw2 = twilight(self.location.observer,direction = SunDirection.RISING)
        if (now >= tw1[0] and now <= tw1[1]) or (now >= tw2[0] and now <= tw2[1]):
            dr.rectangle(rect,fill=(20,20,50),outline=outline)
            return bg

        ni = night(self.location.observer)
        if (now >= ni[0] and now <= ni[1]):
            dr.rectangle(rect,fill=(0,0,5),outline=outline)
            return bg



    def update(self):
        """Draws a sun or a moon depending on the time of day"""
        s = sun(self.location.observer)
        now = datetime.datetime.now(datetime.timezone.utc)
        now = datetime.datetime.fromisoformat("2021-03-27 17:52+00:00")
        s["now"] = now
        # (bluestart,blueend) = night(self.location.observer,direction = SunDirection.SETTING)
        (bluestart,blueend) = night(self.location.observer)
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

        u.changed = True

if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.hardware_mapping = "adafruit-hat-pwm"

    matrix = RGBMatrix(options = options)

    u = SunWidget(size=64)
    u.update()
        
    while True:
        if (u.changed):
            matrix.SetImage(u.image.convert("RGB"))
            u.changed = False
