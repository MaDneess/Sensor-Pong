"""
    Name: button.py
    Author: Aleksej Z
    Date: 2018/08/18
"""
from abc import ABC, abstractmethod
import pygame
import game_utils


class Button(ABC):
    """Description: button class providing general button behaviour"""

    def __init__(self, pos, text, board):
        self.font = pygame.font.Font("fonts/arcade.ttf", int(game_utils.BTN_WIDTH*0.17))
        self.text = self.font.render(text, True, game_utils.BLACK)
        self.pos_x = game_utils.POS_X
        if pos > 0:
            self.pos_y = game_utils.POS_Y + (game_utils.BTN_HEIGHT + game_utils.BTN_OFFSET)*pos
        else:
            self.pos_y = game_utils.POS_Y
        self.color = game_utils.WHITE
        self.board = board

    @abstractmethod
    def on_click(self):
        """Description: method contains action events on button click"""

        pass

    def get_rect(self):
        """Description: method return button rectangle"""

        return pygame.Rect((self.pos_x, self.pos_y), (game_utils.BTN_WIDTH, game_utils.BTN_HEIGHT))

    def get_text_rect(self):
        """Description: method return text rectangle"""

        text_rect = self.text.get_rect()
        text_rect.center = self.get_rect().center
        return text_rect
