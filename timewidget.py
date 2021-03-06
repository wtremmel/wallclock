#!/usr/bin/env python3

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from widget import Widget
from PIL import Image, ImageDraw, ImageFont
import time


class TimeWidget(Widget):
    def __init__(self,x=0,y=0,color=None,size=15,width=64,height=64,font=None):
        if color is None:
            self.dynamiccolor = True
        else:
            self.dynamiccolor = False
        super(TimeWidget,self).__init__(x,y,color,size,width,height)
        if font:
            self.font = ImageFont.load("fonts/"+font)
        else:
            self.font = ImageFont.load("fonts/"+self.size2font(size))

        self.lastminute = -1

    def update(self):
        current_time = time.localtime()

        if (self.lastminute != current_time.tm_min):
            time_string = time.strftime("%H:%M",current_time)
            self.image = Image.new("RGBA",(self.width,self.height))
            draw = ImageDraw.Draw(self.image)
            if self.dynamiccolor:
                if current_time.tm_hour < 7 or current_time.tm_hour > 22:
                    self.color = (0,0,255)
                else:
                    self.color = (0,255,0)
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

    currenttime = TimeWidget(size=7)

    while True:
        currenttime.update();
        if (currenttime.changed):
            im = Image.new("RGBA",(64,64))
            im.alpha_composite(currenttime.image)
            matrix.SetImage(im.convert("RGB"))
        time.sleep(0.5)


