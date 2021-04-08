#!/usr/bin/env python3

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from widget import Widget
from PIL import Image, ImageDraw, ImageFont
from house import House
import re

class MovementWidget(Widget):
    class Sensor:
        def __init__(self,sensor=None,floor=None):
            self.lastmovement = 0
            self.sensor = sensor
            self.floor  = floor
            
    def __init__(self,x=0,y=0,color=(255,255,255),size=2,width=64,height=64):
        super(MovementWidget,self).__init__(x,y,color,size,width,height)
        self.sensors={}

    def mqtthandler(self,topic=None, msg=None):
        if topic == None or msg == None:
            self.changed = False
            return

        hasmovement = int(msg.decode())
        if hasmovement == 0:
            self.changed = False
            return

        found = re.search("/Chattenweg5/([^/]+/",topic)
        if found:
            print("Movement at "+found.group(1))


    def update(self):
        pass


class FensterWidget(Widget):
    def __init__(self,x=0,y=0,color=(255,255,255),size=2,width=64,height=64):
        super(FensterWidget,self).__init__(x,y,color,size,width,height)
        self.lastupdate = 0
        self.fensterliste = {}
        self.fenster = {}
        self.stockwerke = (2,1,"EG")
        self.fenster["EG"] = ("EG_Haustuer","Kueche_Fenster","WZ_Fenster","WZ_Fenster_R")
        self.fenster[1] = ("Bad1_Fenster","Schlafzimmer_Balkontuer")
        self.fenster[2] = ("Arbeitszimmer_Balkontuer","Arbeitszimmer_Dachfenster","Bad2_Fenster")
        for s in self.stockwerke:
            for f in self.fenster[s]:
                self.fensterliste[f] = 9

    def update(self, topic=None, msg=None):
        if topic == None or msg == None:
            self.changed = False
            return

        isopen = int(msg.decode())

        found = re.search("/([a-zA-Z0-9_]+)$",topic)
        if found:
            fenster = found.group(1)
        else:
            self.changed = False
            print("window not found:",topic)
            return

        try:
            if self.fensterliste[fenster] != isopen:
                self.changed = True
                self.fensterliste[fenster] = isopen
        except KeyError:
            print("Unknown window: ",fenster)

        if self.changed:
            thisy = self.y 
            self.image = Image.new("RGBA",(self.width,self.height))
            draw = ImageDraw.Draw(self.image)
            for s in self.stockwerke:
                for f in self.fenster[s]:
                    if self.fensterliste[f] == 0:
                        fcolor = (0,255,0)
                    else:
                        fcolor = (255,0,0)
                    draw.rectangle([
                        self.x,
                        thisy,
                        self.x+self.size-1,
                        thisy+self.size-1],
                        fill=fcolor)
                    thisy += self.size+1
                thisy += self.size+1



if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64

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

    matrix = RGBMatrix(options = options)

    u = FensterWidget(x=60,y=18,size=2)
    u.update("/Chattenweg5/Fenster/Arbeitszimmer_Balkontuer",b'0')
    u.update("/Chattenweg5/Fenster/Arbeitszimmer_Dachfenster",b'0')
    u.update("/Chattenweg5/Fenster/Bad1_Fenster",b'0')
    u.update("/Chattenweg5/Fenster/Bad2_Fenster",b'0')
    u.update("/Chattenweg5/Fenster/EG_Haustuer",b'0')
    u.update("/Chattenweg5/Fenster/Kueche_Fenster",b'0')
    u.update("/Chattenweg5/Fenster/Schlafzimmer_Balkontuer",b'0')
    u.update("/Chattenweg5/Fenster/WZ_Fenster",b'0')
    u.update("/Chattenweg5/Fenster/WZ_Fenster_R",b'0')
    u.update("/Chattenweg5/Fenster/rg_Fenster",b'0')

    m = MovementWidget(x=58,y=18,size=2)
    # m.mqtthandler("/Chattenweg5/EG-Flur/Movement",b"1")
    while True:
        if (m.changed):
            matrix.SetImage(m.image.convert("RGB"))
        


