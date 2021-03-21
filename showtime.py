#!/usr/bin/env python

from clockface import ClockFace
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont
import time


class TimeImage():
    def __init__(self):
        self.x = 0
        self.y = 10
        self.image = Image.new("RGB",(64,64))
        self.image.putalpha(0)
        self.font = ImageFont.truetype("LiberationMono-Regular.ttf", 15)
        self.color= (0,255,0)

    def update(self):
        current_time = time.localtime()
        time_string = time.strftime("%H:%M",current_time)
        draw = ImageDraw.Draw(self.image)
        draw.text((self.x,self.y),time_string,font=self.font,fill=self.color)


class DateImage(ClockFace):
    def __init__(self):
        self.x = 0
        self.y = 20
        self.image = Image.new("RGB",(64,64))
        self.image.putalpha(0)
        self.font = ImageFont.truetype("LiberationMono-Regular.ttf", 10)
        self.color= (0,0,255)

    def update(self):
        current_date = time.localtime()
        date_string = time.strftime("%a %d.%m.",current_date)
        draw = ImageDraw.Draw(self.image)
        draw.text((self.x,self.y),date_string,font=self.font,fill=self.color)


if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64

    matrix = RGBMatrix(options = options)

    currenttime = TimeImage()
    today = DateImage()

    while True:
        currenttime.update();
        today.update()
        im = Image.new("RGB",(64,64))
        im.paste(today.image)
        im.alpha_composite(currenttime.image)
        matrix.SetImage(im)
        time.sleep(0.1)


