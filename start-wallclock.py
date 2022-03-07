#!/usr/bin/env python3

import time
from mqttclient import MqttClient
import subprocess

someonehome = True

def residentsMessage(topic,msg):
    global someonehome
    if topic == None or msg == None:
        return
    v = msg.decode()
    print("Presence:",v)
    if v == "True":
        someonehome = True
    else:
        someonehome = False

def motionMessage(topic,msg):
    global someonehome
    if topic == None or msg == None:
        return
    v = msg.decode()
    print("Presence:",someonehome," Motion:",v)
    if someonehome and v == "ON":
        print("starting wall clock")
        subprocess.run(["systemctl","start","wallclock"])
        print("ending program")
        subprocess.run(["systemctl","stop","start-wallclock"])
        time.sleep(1)
        sys.exit()


if __name__ == "__main__":

    client = MqttClient("mqtt.ch5.garf.de")
    client.subscribe("Chattenweg5/Residents",residentsMessage)
    client.subscribe("Chattenweg5/2OG-Flur/sensor/binary_sensor/2og-flur_motion/state",motionMessage)

    while True:
        time.sleep(1)



