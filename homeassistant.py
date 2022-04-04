
from requests import get
import configparser


class HomeAssistant():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('wallclock.conf')
        self.config = config['HomeAssistant']
        self.header = { 
                "Authorization": self.config["token"],
                "content-type": "application/json"
                }


    def getState(self,statename):
        url = self.config['url'] + "states/" + statename
        print(url)
        return get(url,self.header)


if __name__ == "__main__":
    m = HomeAssistant()
    ret = m.getState("arbeitszimmer_temperatur_2")
    print(ret)
