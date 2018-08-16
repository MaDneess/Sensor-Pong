
import pygame as pg
import Commons, time

from Pad import Pad
from StaticUtils import StaticUtils
from datetime import datetime

class PlayerPad(Pad):
    
    def __init__(self, side, device):
        super().__init__(side)
        self.device = device
        self.started = datetime.now()
        # Testing
        self.keyPressed = False
        self.direction = ""
        
    def move(self):
        if self.device.isOpen():
            #get reading from sensor
            if StaticUtils.getSeconds(datetime.now() - self.started) >= 1:
                self.device.READING = self.device.getReadings()
                self.started = datetime.now()
            
            reading = self.device.READING - Commons.DATA_OFFSET
            pxReading = int(reading*100/(Commons.MAX_DATA - Commons.DATA_OFFSET))
            px = int((Commons.B_HEIGHT - self.height)/100*pxReading)
            #if (self.y + int(self.height/2)) < px:
            #    super().move(-Commons.PAD_SPEED)
            #elif (self.y + int(self.height/2)) > px:
            #   px = px
            #    super().move(Commons.PAD_SPEED)
            self.y = int(self.height/2) + px
            super().move(self.y)
            
        else:
            self.device.open()

    def moveKey(self):
        if self.keyPressed:
            if self.direction == "UP":
                super().moveKey(-Commons.PAD_SPEED)
            elif self.direction == "DOWN":
                super().moveKey(Commons.PAD_SPEED)

    def update(self, board):
        pg.draw.rect(board, Commons.BLACK, self.getRect(), 0)
        
    def calibrateDevice(self):
        self.device.open()
        self.device.calibrate()
        self.device.close()