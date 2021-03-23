#!/usr/bin/env python3

from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont
import time
from timewidget import TimeWidget
from secondswidget import SecondsWidget
from datewidget import DateWidget


if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.hardware_mapping = "adafruit-hat-pwm"
    options.pwm_bits = 8


    matrix = RGBMatrix(options = options)

    mytime = TimeWidget(x=0,y=0,color=(0,255,0))
    mydate= DateWidget(x=0,y=13,color=(128,128,255))
    myseconds = SecondsWidget(x=0,y=0,color=(100,100,0))
    im = Image.new("RGBA",(64,64))

    while True:
        mytime.update();
        mydate.update()
        myseconds.update()
        if (myseconds.changed or mytime.changed):
            im.paste(mydate.image)
            im.alpha_composite(mytime.image)
            im.alpha_composite(myseconds.image)
            matrix.SetImage(im.convert("RGB"))
        time.sleep(0.5)


