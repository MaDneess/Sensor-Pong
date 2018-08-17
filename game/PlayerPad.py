
import pygame as pg
import Commons

from Pad import Pad
from StaticUtils import StaticUtils
from PressureDevice import PressureDevice
from CommUtils import CommUtils


class PlayerPad(Pad):
    
    def __init__(self, side, portConfig, board):
        super().__init__(side)
        self.device = PressureDevice(portConfig, board)
        self.device.start()
        # Testing
        self.keyPressed = False
        self.direction = ""
        
    def move(self):
        if self.device.isOpen():
            px = self.transformToPixel(self.device.READING)
            self.y = int(self.height/2) + px
            super().move()
        else:
            self.device.open()

    def transformToPixel(self, reading):
        x = int((reading - self.device.MINIMUM)*100/(self.device.MAXIMUM - self.device.MINIMUM))
        return int(Commons.B_HEIGHT * x * .01)

    def moveKey(self):
        if self.keyPressed:
            if self.direction == "UP":
                super().moveKey(-Commons.PAD_SPEED)
            elif self.direction == "DOWN":
                super().moveKey(Commons.PAD_SPEED)

    def update(self, board):
        pg.draw.rect(board, Commons.BLACK, self.getRect(), 0)
        
    def calibrateDevice(self):
        StaticUtils.printMessage("Calibrating Player " + self.name)
        self.device.open()
        self.device.calibrate()
        self.device.close()

    def calibrateMin(self):
        StaticUtils.printMessage(CommUtils.CMD_OK, "Calibrating Player " + self.name)
        self.device.open()
        self.device.calibrateMin()
        self.device.close()
        StaticUtils.printMessage(CommUtils.CMD_RESPONSE, "Player " + self.name + " minimum point is -- " + str(self.device.MINIMUM))

    def calibrateMax(self):
        StaticUtils.printMessage(CommUtils.CMD_OK, "Calibrating Player " + self.name)
        self.device.open()
        self.device.calibrateMax()
        self.device.close()
        StaticUtils.printMessage(CommUtils.CMD_RESPONSE, "Player " + self.name + " maximum point is -- " + str(self.device.MAXIMUM))