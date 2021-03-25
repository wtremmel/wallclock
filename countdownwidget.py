#!/usr/bin/env python3

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from widget import Widget
from PIL import Image, ImageDraw, ImageFont
import time
import re


class CountdownWidget(Widget):
    def __init__(self,x=0,y=0,color=None,size=15,width=64,height=64):
        if color is None:
            self.dynamiccolor = True
        else:
            self.dynamiccolor = False
        super(CountdownWidget,self).__init__(x,y,color,size,width,height)
        self.font = ImageFont.truetype("Roboto-Thin.ttf",self.size)
        self.starttime = 0
        self.endtime = 0
        self.running = False
        self.lasttime= 0

    def start(self,minutes=0,seconds=0):
        if (minutes > 0 or seconds > 0):
            self.starttime = time.time()
            self.endtime   = self.starttime + (60*minutes) + seconds
            self.running   = True

    def cancel(self):
        self.running = False

    def mqttstart(self,topic=None,value=None):
        v = value.decode()
        print(topic+"::"+v)
        m1 = re.match("(\d+)\s+(\d+)",v)
        m2 = re.match("\d+",v)
        if (v == "cancel"):
            self.cancel()
        elif m1:
            minutes = int(m1.group(1))
            seconds = int(m1.group(2))
            self.start(minutes,seconds)
        elif m2:
            seconds = int(m2.group(0))
            self.start(seconds = seconds)


    def big(self):
        pass

    def update(self):
        now = time.time()
        seconds_left = self.endtime - now
        if seconds_left < 0:
            self.running = False
        if (self.running and self.lasttime != now):
            current_time = time.gmtime(seconds_left)
            time_string = time.strftime("%H:%M:%S",current_time)
            self.image = Image.new("RGBA",(self.width,self.height))
            draw = ImageDraw.Draw(self.image)
            if self.dynamiccolor:
                if seconds_left < 60:
                    self.color = (255,0,0)
                elif seconds_left < 5*60:
                    self.color = (255,255,0)
                else:
                    self.color = (64,255,64)
            draw.text((self.x,self.y),time_string,font=self.font,fill=self.color)
            self.lastminute = current_time.tm_min
            self.changed = True
        else:
            self.changed = False



if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64

    matrix = RGBMatrix(options = options)

    currenttime = CountdownWidget()
    currenttime.mqttstart("countdown",b"60")

    while True:
        currenttime.update();
        if (currenttime.changed):
            matrix.SetImage(currenttime.image.convert("RGB"))
        time.sleep(0.5)


