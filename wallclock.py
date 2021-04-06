#!/usr/bin/env python3

from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont
import time
from timewidget import TimeWidget
from secondswidget import SecondsWidget
from datewidget import DateWidget
from sunwidget import SunWidget
from mqttclient import MqttClient
from temperaturewidget import TemperatureWidget, HumidityWidget
from countdownwidget import CountdownWidget
from pingwidget import PingWidget
from framealert import FrameAlert, ImageAlert, UnicodeAlert
from fensterwidget import FensterWidget, MovementWidget
from onoffbrightness import OnOffBrightness
from house import House
import json

haustuerOffen = ImageAlert(y=32,howlong=30,filename="images/door-5-64.png")
esKlingelt = ImageAlert(y=32,howlong=10,filename="images/bell-64.png")
telefon = UnicodeAlert(y=22, howlong=30, size=35,description="black telephone", color=(255,0,0))
esRegnet = UnicodeAlert(y=22, howlong=600, size=24,description="CLOUD WITH RAIN", color=(0,96,255))

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
    newBrightness = int(msg)
    if newBrightness >= 0 and newBrightness <= 255:
        matrixBrightness = int(msg)

def dasTelefonKlingelt(topic,msg):
    global telefon
    telefon.on()
    
def regenAlert(topic,msg):
    global esRegnet

    v = int(msg.decode())
    if v > 15000:
        esRegnet.on()
    else:
        esRegnet.off()


if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.hardware_mapping = "adafruit-hat-pwm"
    options.pwm_bits = 7
    options.drop_privileges = False
    matrix = RGBMatrix(options = options)

    ch5 = House()
    ch5.addFloor("2.OG",2)
    ch5.addFloor("1.OG",1)
    ch5.addFloor("EG",0)
    ch5.addFloor("Keller",-1)
    ch5.addFloor("Aussen",-2)

    ch5.addRoom("Arbeitszimmer","2.OG")
    ch5.addRoom("Bad2","2.OG")
    ch5.addRoom("Loggia","2.OG")
    ch5.addRoom("RaspiBox","2.OG")
    ch5.addRoom("3DPrinter","2.OG")
    ch5.addRoom("2OG-Loggia","2.OG")
    ch5.addRoom("2OG-Flur","2.OG")
    
    ch5.addRoom("1OG-Flur","1.OG")
    ch5.addRoom("Schlafzimmer","1.OG")
    ch5.addRoom("Bad1","1.OG")
    ch5.addRoom("Ankleidezimmer","1.OG")

    ch5.addRoom("Wohnzimmer","EG")
    ch5.addRoom("Mobile","EG")
    ch5.addRoom("Kueche","EG")
    ch5.addRoom("Fenster","EG")
    ch5.addRoom("EG-Flur","EG")
    
    ch5.addRoom("Heizraum","Keller")
    ch5.addRoom("Keller","Keller")
    ch5.addRoom("Kellerabgang","Keller")
    ch5.addRoom("Fernsehzimmer","Keller")
    ch5.addRoom("Keller-Flur","Keller")
    ch5.addRoom("Hausanschlussraum","Keller")

    ch5.addRoom("Garten","Aussen")
    ch5.addRoom("Vorgarten","Aussen")

    mytime = TimeWidget(x=0,y=0,color=(0,255,0))
    mydate= DateWidget(x=0,y=11,color=(128,128,255))
    mycountdown = CountdownWidget(x=0,y=30,size=13,bigat=10)
    myseconds = SecondsWidget(x=0,y=0,color=(100,100,0))
    gardentemp = TemperatureWidget(x = 45, y = 58, size = 7)
    loggiatemp = TemperatureWidget(x = 22, y = 58, size = 7)
    vorgartentemp = TemperatureWidget(x = 0, y = 58, size = 7)
    arbeitszimmertemp = TemperatureWidget(x = 0, y = 50, size = 7)
    arbeitszimmerhum = HumidityWidget(x = 20, y = 50, size = 7)
    pingrouter = PingWidget(x=0,y=63,target="192.168.1.254",every=30,color=(0,0,0))
    astro = SunWidget(x=46,y=1,size=18)
    allefenster = FensterWidget(x=62,y=19,size=2)
    motion = MovementWidget(x=60,y=19,size=2)
    setbrightness = OnOffBrightness()

    aussentemperatur = TemperatureWidget(x=0,y=25,size=12)
    
    widgetlist = []
    widgetlist.append(mytime)
    widgetlist.append(astro)
    widgetlist.append(mydate)
    widgetlist.append(myseconds)
    widgetlist.append(gardentemp)
    widgetlist.append(vorgartentemp)
    widgetlist.append(arbeitszimmertemp)
    widgetlist.append(arbeitszimmerhum)
    widgetlist.append(loggiatemp)
    widgetlist.append(pingrouter)
    widgetlist.append(haustuerOffen)
    widgetlist.append(telefon)
    widgetlist.append(esKlingelt)
    widgetlist.append(esRegnet)
    widgetlist.append(allefenster)
    widgetlist.append(motion)
    widgetlist.append(aussentemperatur)

    client = MqttClient("pi3.garf.de")
    client.subscribe("/Chattenweg5/Garten/temperature",gardentemp.update)
    client.subscribe("/Chattenweg5/Garten/rain",regenAlert)
    client.subscribe("/Chattenweg5/Vorgarten/temperature",vorgartentemp.update)
    client.subscribe("/Chattenweg5/Arbeitszimmer/temperature",arbeitszimmertemp.update)
    client.subscribe("/Chattenweg5/Arbeitszimmer/humidity",arbeitszimmerhum.update)
    client.subscribe("/Chattenweg5/2OG-Loggia/temperature",loggiatemp.update)
    client.subscribe("/Wallclock/Countdown",mycountdown.mqttstart)
    client.subscribe("/Chattenweg5/zigbee2mqtt/Tuerklingel",tuerklingelAlert)
    client.subscribe("/Chattenweg5/zigbee2mqtt/Haustuer",haustuerAlert)
    client.subscribe("/Wallclock/Brightness",setBrightness)
    client.subscribeRegex("/Chattenweg5/Fenster/#","/Chattenweg5/Fenster/.*",allefenster.update)
    client.subscribeRegex("/Chattenweg5/+/motion","/Chattenweg5/.*/motion",motion.mqtthandler)
    client.subscribe("/Chattenweg5/Arbeitszimmer/light",setbrightness.mqttlight)
    client.subscribe("/Chattenweg5/Residents",setbrightness.mqtthome)
    client.subscribe("/Chattenweg5/Phone",dasTelefonKlingelt)
    client.subscribeRegex("/Chattenweg5/#","/Chattenweg5/.*",ch5.mqtthandler)


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

        if (setbrightness.changed):
            matrix.brightness = setbrightness.brightness
            setbrightness.changed=False
            print("brightness = ",matrix.brightness)
            change = True

        if change:
            im = Image.new("RGBA",(64,64))
            for w in widgetlist:
                im.alpha_composite(w.image)
                w.changed = False
            matrix.SetImage(im.convert("RGB"))
        time.sleep(0.5)


