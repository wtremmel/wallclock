#!/usr/bin/env python3

import time
from mqttclient import MqttClient
import subprocess

someonehome = True

def residentsMessage(topic,msg):
    global someonehome
    if topic == None or msg == None:
        return
    v = int(msg.decode())
    if v == 1:
        someonehome = True
    if v == 0:
        someonehome = False

def motionMessage(topic,msg):
    global someonehome
    if topic == None or msg == None:
        return
    v = int(msg.decode())
    print("Presence:",someonehome," Motion:",v)
    if someonehome and v == 1:
        print("starting wall clock")
        subprocess.run(["systemctl","start","wallclock"])
        print("ending program")
        subprocess.run(["systemctl","stop","start-wallclock"])
        time.sleep(1)
        sys.exit()


if __name__ == "__main__":

    client = MqttClient("pi3.garf.de")
    client.subscribe("/Chattenweg5/Residents",residentsMessage)
    client.subscribe("/Chattenweg5/2OG-Flur/motion",motionMessage)

    while True:
        time.sleep(1)



