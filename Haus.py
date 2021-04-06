


class House:
    class Room:
        def __init__(self, name, floor):
            self.name = name
            self.floor= floor

    def __init__(self):
        self.floors = []
        self.rooms = {}

    def addFloor(self,name,index):
        self.floors[index] = name

    def addRoom(self,name,floorname):
        self.rooms[name] = Room(name, floorname)

    def getFloorIndex(self,floorname):
        return 0

    def getRoomFloor(self,roomname):
        return None


