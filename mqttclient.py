#!/usr/bin/env python3

from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time
from temperaturewidget import TemperatureWidget
import paho.mqtt.client as mqtt

class MqttClient():
    def on_connect(self,client, userdata, flags, rc):
        print("connected with result code "+str(rc))
        topiclist = []
        for t in list(self.handler):
            topiclist.append((t,0))
        client.subscribe(topiclist)

    def on_message(self,client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        try:
            handler = self.handler[msg.topic]
            handler(msg.topic,msg.payload)
        except KeyError:
            print("handler for payload not found")

    def subscribe(self,topic,function):
        self.client.subscribe(topic)
        self.handler[topic] = function

    def __init__(self,server):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(server,1883,60)
        self.client.loop_start()
        self.handler = {}


if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.hardware_mapping = "adafruit-hat-pwm"
    options.pwm_bits = 8


    matrix = RGBMatrix(options = options)

    mytemp = TemperatureWidget(x=0,y=20)

    client = MqttClient("pi3.garf.de")
    client.subscribe("/Chattenweg5/Garten/temperature",mytemp)

    while True:
        if mytemp.changed:
            matrix.SetImage(mytemp.image.convert("RGB"))
            mytemp.changed = False
        time.sleep(0.5)


