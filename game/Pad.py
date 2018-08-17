"""
    Description:
        Abstract(parent) class Pad includes base methods and
        setup logic for all Pad childs
"""

import Commons
import pygame
from abc import ABC, abstractmethod


class Pad(ABC):
    
    def __init__(self, side):
        self.width = Commons.PAD_WIDTH
        self.height = Commons.PAD_HEIGHT
        if side == 'LEFT':
            self.name = "BLUE"
            self.x = Commons.CAGE_WIDTH
        elif side == 'RIGHT':
            self.name = "RED"
            self.x = Commons.B_WIDTH - Commons.CAGE_WIDTH - Commons.PAD_WIDTH
        else:
            raise Exception(Commons.ERROR + " Unknown side argument")
        self.y = (int(Commons.B_HEIGHT - Commons.OFFSET_HEIGHT - Commons.PAD_HEIGHT) / 2)
        self.score = 0
    
    @abstractmethod
    def move(self):
        if self.y < Commons.OFFSET_HEIGHT:
            self.y = Commons.OFFSET_HEIGHT
        elif (self.y + self.height) > (Commons.B_HEIGHT - Commons.OFFSET_HEIGHT):
            self.y = Commons.B_HEIGHT - Commons.OFFSET_HEIGHT - self.height

    @abstractmethod
    def moveKey(self, dy):
        self.y += dy
        if self.y < Commons.OFFSET_HEIGHT:
            self.y = Commons.OFFSET_HEIGHT
        elif (self.y + self.height) > (Commons.B_HEIGHT - Commons.OFFSET_HEIGHT):
            self.y = Commons.B_HEIGHT - Commons.OFFSET_HEIGHT - self.height
    
    @abstractmethod
    def update(self, board):
        pass
    
    def getRect(self):
        return pygame.Rect((self.x, self.y),(self.width, self.height))
    
    def addScore(self):
        self.score += Commons.POINTS
        