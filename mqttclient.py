#!/usr/bin/env python3

import time
import paho.mqtt.client as mqtt
import re
import sys
import configparser

class MqttClient():
    def on_connect(self,client, userdata, flags, rc):
        print("connected with result code "+str(rc))
        topiclist = []
        for t in list(self.handler):
            topiclist.append((t,0))
        self.client.subscribe(topiclist)

    def on_message(self,client, userdata, msg):
        found = False
        for topic,v in self.handler.items():
            if re.match(v[0],msg.topic):
                v[1](msg.topic,msg.payload)
                found = True
        if not found:
            print("not found: ",msg.topic)

    def on_subscribe(self,client,userdata,mid,granted_qos):
        pass

    def subscribe(self,topic=None,function=None):
        self.handler[topic] = (topic,function)
        self.client.subscribe(topic)

    def subscribeRegex(self,topic=None,regex=None,function=None):
        self.handler[topic] = (regex,function)
        self.client.subscribe(topic)

    def __init__(self):
        self.handler = {}
        config = configparser.ConfigParser()
        config.read('wallclock.conf')
        self.config = config['mqtt']
        self.client = mqtt.Client(clean_session=True)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.username_pw_set(self.config['user'],password=self.config['password'])
        self.client.connect(self.config['host'],int(self.config['port']),10)
        self.client.loop_start()


if __name__ == "__main__":

    def mytest(topic,msg):
        print(topic+":"+str(msg))
        
    myclient = MqttClient()
    myclient.subscribe("/Chattenweg5/2OG-Flur/temperature",mytest)
    myclient.subscribe("/Chattenweg5/2OG-Flur/humitiy",mytest)

    while True:
        time.sleep(1)
