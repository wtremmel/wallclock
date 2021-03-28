#!/usr/bin/env python3

from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont
import time
from timewidget import TimeWidget
from secondswidget import SecondsWidget
from datewidget import DateWidget
from sunwidget import SunWidget
from mqttclient import MqttClient
from temperaturewidget import TemperatureWidget
from countdownwidget import CountdownWidget
from pingwidget import PingWidget
from framealert import FrameAlert, ImageAlert
from fensterwidget import FensterWidget
import json

haustuerOffen = ImageAlert(y=32,howlong=30,filename="images/door-5-64.png")
esKlingelt = ImageAlert(y=32,howlong=10,filename="images/bell-64.png")

matrixBrightness = 100


def tuerklingelAlert(topic,msg):
    global esKligelt
    # /Chattenweg5/zigbee2mqtt/Tuerklingel {"battery":100,"contact":true,"linkquality":78,"voltage":3015}
    x = json.loads(msg)
    contact = x["contact"]
    if contact == False:
        esKlingelt.on()

def haustuerAlert(topic,msg):
    global haustuerOffen
    x = json.loads(msg)
    contact = x["contact"]
    if contact == False:
        haustuerOffen.on()

def setBrightness(topic,msg):
    global matrixBrightness
    matrixBrightness = int(msg)

if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.hardware_mapping = "adafruit-hat-pwm"
    options.pwm_bits = 7
    options.drop_privileges = False

    matrix = RGBMatrix(options = options)

    mytime = TimeWidget(x=0,y=0,color=(0,255,0))
    mydate= DateWidget(x=0,y=15,color=(128,128,255))
    mycountdown = CountdownWidget(x=0,y=13,size=13,bigat=10)
    myseconds = SecondsWidget(x=0,y=0,color=(100,100,0))
    gardentemp = TemperatureWidget(x = 30, y = 40, size = 12)
    pingrouter = PingWidget(x=0,y=63,target="192.168.1.254",every=30,color=(0,0,0))
    astro = SunWidget(x=48,y=1,size=16)
    allefenster = FensterWidget(x=60,y=18,size=2)

    
    widgetlist = []
    widgetlist.append(mytime)
    widgetlist.append(astro)
    widgetlist.append(mydate)
    widgetlist.append(myseconds)
    widgetlist.append(gardentemp)
    widgetlist.append(pingrouter)
    widgetlist.append(haustuerOffen)
    widgetlist.append(esKlingelt)
    widgetlist.append(allefenster)

    client = MqttClient("pi3.garf.de")
    client.subscribe("/Chattenweg5/Garten/temperature",gardentemp.update)
    client.subscribe("countdown",mycountdown.mqttstart)
    client.subscribe("/Chattenweg5/zigbee2mqtt/Tuerklingel",tuerklingelAlert)
    client.subscribe("/Chattenweg5/zigbee2mqtt/Haustuer",haustuerAlert)
    client.subscribe("/Wallclock/Brightness",setBrightness)
    client.subscribe("/Chattenweg5/Fenster/#",allefenster.update)


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
            matrix.brightness = matrixBrightness
            matrix.SetImage(im.convert("RGB"))
        time.sleep(0.5)


