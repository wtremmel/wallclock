#!/usr/bin/env python3

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from widget import Widget
from PIL import Image, ImageDraw, ImageFont
import time
from pythonping import ping

class PingWidget(Widget):
    def __init__(self,x=0,y=0,color=None,size=15,width=64,height=64,target=None,every=60):
        if color is None:
            color = (0,255,0)
        super(PingWidget,self).__init__(x,y,color,size,width,height)
        self.lastping = False
        self.target = target
        self.every = every
        self.lasttime = 0

    def update(self):
        if self.target != None and time.time() > self.lasttime + self.every:
            try:
                goodPing = ping(self.target,count=1,verbose=False).success()
            except:
                goodPing = False
            if (goodPing != self.lastping):
                if (goodPing):
                    color = self.color
                else:
                    color = (255,0,0)
                self.image = Image.new("RGBA",(self.width,self.height))
                draw = ImageDraw.Draw(self.image)
                draw.point((self.x,self.y),fill=color)
                self.changed = True
            else:
                self.changed = False

            self.lastping = goodPing
            self.lasttime = time.time()
        else:
            self.changed = False



if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.drop_privileges = False

    matrix = RGBMatrix(options = options)

    myping = PingWidget(every=10, target="192.168.1.254")

    while True:
        myping.update();
        if (myping.changed):
            matrix.SetImage(myping.image.convert("RGB"))
        time.sleep(0.5)


