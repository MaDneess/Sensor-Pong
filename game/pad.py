"""
    Name: pad.py
    Author: Aleksej Z
    Date: 2018/08/18
"""
from abc import ABC, abstractmethod
import pygame
import game_utils
import comm_utils


class Pad(ABC):
    """Description: pad class providing general pad behavior"""

    def __init__(self, side):
        self.width = game_utils.PAD_WIDTH
        self.height = game_utils.PAD_HEIGHT
        if side == 'LEFT':
            self.name = "BLUE"
            self.pos_x = game_utils.CAGE_WIDTH
        elif side == 'RIGHT':
            self.name = "RED"
            self.pos_x = game_utils.B_WIDTH - game_utils.CAGE_WIDTH - game_utils.PAD_WIDTH
        else:
            raise Exception(comm_utils.CMD_ERROR + " Unknown side argument")
        self.pos_y = (int(game_utils.B_HEIGHT - game_utils.OFFSET_HEIGHT
                          - game_utils.PAD_HEIGHT) / 2)
        self.score = 0

    def reset(self):
        self.pos_y = (int(game_utils.B_HEIGHT - game_utils.OFFSET_HEIGHT
                          - game_utils.PAD_HEIGHT) / 2)

    @abstractmethod
    def move(self):
        """Description: method checks pad Y position"""

        if self.pos_y < game_utils.OFFSET_HEIGHT:
            self.pos_y = game_utils.OFFSET_HEIGHT
        elif (self.pos_y + self.height) > (game_utils.B_HEIGHT - game_utils.OFFSET_HEIGHT):
            self.pos_y = game_utils.B_HEIGHT - game_utils.OFFSET_HEIGHT - self.height

    @abstractmethod
    def update(self, board):
        """Description: method updates pad on display
        :param: Board display
        """

        pass

    def get_rect(self):
        """Description: method returns pad rectangle
        :return: Rectangle object
        """

        return pygame.Rect((self.pos_x, self.pos_y), (self.width, self.height))

    def add_score(self):
        """Description: method increase pads score"""

        self.score += game_utils.POINTS
