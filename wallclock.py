#!/usr/bin/env python3

from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont
import time
from timewidget import TimeWidget
from secondswidget import SecondsWidget
from datewidget import DateWidget
from mqttclient import MqttClient
from temperaturewidget import TemperatureWidget


if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.hardware_mapping = "adafruit-hat-pwm"
    options.pwm_bits = 7


    matrix = RGBMatrix(options = options)

    mytime = TimeWidget(x=0,y=0,color=(0,255,0))
    mydate= DateWidget(x=0,y=13,color=(128,128,255))
    myseconds = SecondsWidget(x=0,y=0,color=(100,100,0))
    gardentemp = TemperatureWidget(x = 30, y = 40, size = 10)

    widgetlist = []
    widgetlist.append(mytime)
    widgetlist.append(mydate)
    widgetlist.append(myseconds)
    widgetlist.append(gardentemp)


    while True:
        change = False
        for w in widgetlist:
            w.update()
            if w.changed:
                change = True
        if change:
            im = Image.new("RGBA",(64,64))
            for w in widgetlist:
                im.alpha_composite(w.image)
                w.changed = False
            matrix.SetImage(im.convert("RGB"))
        # time.sleep(0.5)


