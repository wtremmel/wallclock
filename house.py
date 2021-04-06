import re

class House:
    def __init__(self):
        self.floors = {}
        self.floorname = {}
        self.rooms = {}

    def addFloor(self,name,index):
        self.floors[index] = name
        self.floorname[name] = index

    def getFloor(self,name):
        try:
            f = self.floorname[name]
            return f
        except KeyError:
            return None

    def addRoom(self,name,floorname):
        self.rooms[name] = self.getFloor(floorname)

    def getRoomFloor(self,roomname):
        try:
            r = self.rooms[roomname]
            return r
        except KeyError:
            return None

    def mqtthandler(self,topic=None, msg=None):
        if topic == None:
            return
        r = re.search("/[^/]+/([^/]+)",topic)
        if not r:
            print("No room found in ",topic)
            return
        rr = r.group(1)

        f = self.getRoomFloor(rr)
        if f == None:
            print("No floor know for room ",rr)
            return

        return f

