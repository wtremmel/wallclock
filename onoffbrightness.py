#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageFont
from widget import Widget
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time


class OnOffBrightness(Widget):
    def __init__(self,x=0,y=0,color=(255,255,255),size=12,width=64,height=64):
        super(OnOffBrightness,self).__init__(x,y,color,size,width,height)
        self.somonehome = True
        self.brightness = 100
        self.changed = False

    def mqttlight(self,topic,msg):
        if topic == None or msg == None:
            self.changed = False
            return

        light = float(msg.decode())
        print(topic,":",light)

        if (ligth <= 0):
            self.brightness = 8

    def mqtthome(self,topic,msg):
        pass

    def update(self):
        self.changed = False


if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.parallel = 1
    options.chain_length = 1
    options.hardware_mapping = "adafruit-hat-pwm"

    matrix = RGBMatrix(options = options)



