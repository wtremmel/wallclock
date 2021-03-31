#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageFont
from widget import Widget
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time
import subprocess


class OnOffBrightness(Widget):
    def __init__(self,x=0,y=0,color=(255,255,255),size=12,width=64,height=64):
        super(OnOffBrightness,self).__init__(x,y,color,size,width,height)
        self.somonehome = True
        self.brightness = 100
        self.changed = False

    def mqttlight(self,topic,msg):
        if topic == None or msg == None or self.somonehome == False:
            return

        light = int(round(float(msg.decode())))

        oldbrightness = self.brightness
        self.brightness = light*4

        if (self.brightness < 8):
            self.brightness = 8
        elif self.brightness > 100:
            self.brightness = 100

        self.changed = (oldbrightness != self.brightness)
        print ("light = ",light," brightness = ",self.brightness)

    def mqtthome(self,topic,msg):
        if topic == None or msg == None:
            return

        residents = int(msg.decode())
        if residents == 0:
            self.someonehome = False
            self.brightness = 0
            self.changed = True
            print("nobody home, turn off")
            subprocess.run(["systemctl","stop","wallclock"])
            time.sleep(5)
            sys.exit()
        elif residents >= 1:
            print("somebody home, turn on")
            self.someonehome = True
        else:
            print("Unknown value for "+topic+": "+residents)

    def update(self):
        pass


if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.parallel = 1
    options.chain_length = 1
    options.hardware_mapping = "adafruit-hat-pwm"

    matrix = RGBMatrix(options = options)



