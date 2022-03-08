#!/usr/bin/env python3

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from widget import Widget
from PIL import Image, ImageDraw, ImageFont
import time

class AirQualityWidget(Widget):
    def __init__(self,x=0,y=0,color=(255,255,255),size=15,width=64,height=64,font=None):
        super(AirQualityWidget,self).__init__(x,y,color,size,width,height)
        if font:
            self.font = ImageFont.load("fonts/"+font)
        else:
            self.font = ImageFont.load("fonts/"+self.size2font(size))

        self.lastqual = None
        self.lastupdate = 0
        self.sensors = {}

    def update(self,sensor=None, airquality=None):
        if airquality == None:
            if (time.time() - self.lastupdate > 60*5):
                self.image = Image.new("RGBA",(self.width,self.height))
                self.lastupdate = time.time()
                self.changed = True
            else:
                self.changed = False
            return
        q = int(float(airquality.decode()))
        self.lastupdate = time.time()
        if (self.lastqual != q):
            qualStr = "{:4d}".format(q) + "ppm"
            self.image = Image.new("RGBA",(self.width,self.height))
            draw = ImageDraw.Draw(self.image)
            if q <= 1000:
                self.color = (0,255,0)
            elif q <= 2000:
                self.color = (255,255,0)
            else:
                self.color = (255,0,0)
            draw.text((self.x,self.y),qualStr,font=self.font,fill=self.color)
            self.lastqual = q
            self.changed = True
        else:
            self.changed = False

class HumidityWidget(Widget):
    def __init__(self,x=0,y=0,color=(255,255,255),size=15,width=64,height=64,font=None):
        super(HumidityWidget,self).__init__(x,y,color,size,width,height)
        if font:
            self.font = ImageFont.load("fonts/"+font)
        else:
            self.font = ImageFont.load("fonts/"+self.size2font(size))

        self.lasthum = None
        self.lastupdate = 0
        self.sensors = {}

    def update(self,sensor=None, humidity=None):
        if humidity == None:
            if (time.time() - self.lastupdate > 60*5):
                self.image = Image.new("RGBA",(self.width,self.height))
                self.lastupdate = time.time()
                self.changed = True
            else:
                self.changed = False
            return
        h = int(float(humidity.decode()))
        self.lastupdate = time.time()
        if (self.lasthum != h):
            humStr = "{:2d}".format(h) + "%"
            self.image = Image.new("RGBA",(self.width,self.height))
            self.color=(0,200-h*2,255)
            draw = ImageDraw.Draw(self.image)
            draw.text((self.x,self.y),humStr,font=self.font,fill=self.color)
            self.lasthum = h
            self.changed = True
        else:
            self.changed = False


class TemperatureWidget(Widget):
    class Sensor:
        def __init__(self,name,value):
            self.name = name
            self.value= value
            self.update=time.time()
            
    def __init__(self,x=0,y=0,color=(255,255,255),size=15,width=64,height=64,font=None):
        super(TemperatureWidget,self).__init__(x,y,color,size,width,height)
        if font:
            self.font = ImageFont.load("fonts/"+font)
        else:
            self.font = ImageFont.load("fonts/"+self.size2font(size))

        self.lasttemp = None
        self.lastupdate = 0
        self.sensors = {}

    def update(self,sensor=None, temperature=None):
        if temperature == None:
            if (time.time() - self.lastupdate > 60*5):
                self.image = Image.new("RGBA",(self.width,self.height))
                self.lastupdate = time.time()
                self.changed = True
            else:
                self.changed = False
            return
        t = float(temperature)
        self.lastupdate = time.time()
        if (self.lasttemp != t):
            tempStr = "{:2.1f}".format(t)
            self.image = Image.new("RGBA",(self.width,self.height))
            if (t< 0):
                self.color=(0,0,255)
            elif (t< 10):
                self.color=(0,128,255)
            elif (t< 15):
                self.color=(255,255,0)
            elif (t< 20):
                self.color=(255,192,0)
            elif (t< 25):
                self.color=(255,128,0)
            elif (t< 30):
                self.color=(255,64,0)
            else:
                self.color=(255,0,0)
            if (t > -20):
                draw = ImageDraw.Draw(self.image)
                draw.text((self.x,self.y),tempStr,font=self.font,fill=self.color)
                self.lasttemp = t
                self.changed = True
            else:
                self.changed = False
        else:
            self.changed = False

    def minimum(self,sensor=None,temperature=None):
        t = float(temperature)
        s = Sensor(sensor,t)
        self.sensors[sensor] = s
        # remove all too old readings and record the minimum
        minimum = s
        for x in iter(self.sensors):
            if (x.update < time.time() - 5*60):
                del self.sensors[x]
            elif x.value < minimum.value:
                minimum = x
        self.update(minimum.name,minimum.value)

        


if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64

    matrix = RGBMatrix(options = options)

    currenttemp = TemperatureWidget(size=12)
    currenttemp.update(16.9)
    while True:
        if (currenttemp.changed):
            matrix.SetImage(currenttemp.image.convert("RGB"))
        


