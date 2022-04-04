
from requests import get
import configparser
import json


class HomeAssistant():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('wallclock.conf')
        self.config = config['HomeAssistant']
        self.header = { 
                "Authorization": "Bearer " + self.config["token"],
                "content-type": "application/json"
                }


    def getState(self,statename):
        url = self.config['url'] + "states/" + statename
        response = get(url,headers=self.header)
        entities = response.json()
        return entities

    def getStates(self):
        response = get(self.config['url'] + "states", headers=self.header)
        print(response)
        entities = response.json()
        print(entities)


if __name__ == "__main__":
    m = HomeAssistant()
    r = m.getState("binary_sensor.fenster_bad1_state")
    print(r)
