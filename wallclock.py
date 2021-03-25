#!/usr/bin/env python3

from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont
import time
from timewidget import TimeWidget
from secondswidget import SecondsWidget
from datewidget import DateWidget
from mqttclient import MqttClient
from temperaturewidget import TemperatureWidget
from countdownwidget import CountdownWidget
from pingwidget import PingWidget
from framealert import FrameAlert


if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.hardware_mapping = "adafruit-hat-pwm"
    options.pwm_bits = 7
    options.drop_privileges = False


    matrix = RGBMatrix(options = options)

    mytime = TimeWidget(x=0,y=0,color=(0,255,0))
    mydate= DateWidget(x=0,y=13,color=(128,128,255))
    mycountdown = CountdownWidget(x=0,y=13)
    myseconds = SecondsWidget(x=0,y=0,color=(100,100,0))
    gardentemp = TemperatureWidget(x = 30, y = 40, size = 12)
    pingrouter = PingWidget(x=0,y=63,target="192.168.1.254",every=30,color=(0,0,0))
    
    widgetlist = []
    widgetlist.append(mytime)
    widgetlist.append(mydate)
    widgetlist.append(myseconds)
    widgetlist.append(gardentemp)
    widgetlist.append(pingrouter)

    client = MqttClient("pi3.garf.de")
    client.subscribe("/Chattenweg5/Garten/temperature",gardentemp.update)
    client.subscribe("countdown",mycountdown.mqttstart)

    while True:
        change = False
        for w in widgetlist:
            w.update()
            if w.changed:
                change = True

        # countdown timer disables date
        if mycountdown.started:
            mycountdown.started = False
            try:
                widgetlist.remove(mydate)
                widgetlist.append(mycountdown)
            except ValueError:
                pass
        elif mycountdown.cancelled:
            mycountdown.cancelled = False
            widgetlist.append(mydate)
            widgetlist.remove(mycountdown)
        elif mycountdown.ended:
            mycountdown.ended = False
            widgetlist.append(mydate)
            widgetlist.remove(mycountdown)
            flasher = FrameAlert()
            for i in range(5):
                flasher.blinkon()
                im.alpha_composite(flasher.image)
                matrix.SetImage(im.convert("RGB"))
                time.sleep(0.1)
                flasher.blinkoff()
                im.alpha_composite(flasher.image)
                matrix.SetImage(im.convert("RGB"))
                time.sleep(0.1)

        if change:
            im = Image.new("RGBA",(64,64))
            for w in widgetlist:
                im.alpha_composite(w.image)
                w.changed = False
            matrix.SetImage(im.convert("RGB"))
        time.sleep(0.5)


