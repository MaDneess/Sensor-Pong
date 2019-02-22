"""
    Name: player_pad.py
    Author: Aleksej Z
    Date: 2018/08/18
"""
import pygame
import game_utils
import comm_utils
from pad import Pad
from static_utils import StaticUtils


class PlayerPad(Pad):
    """Description: pad class with player actions and behavior"""

    def __init__(self, side, device, color=None):
        Pad.__init__(self, side, color)
        self.device = device
        self.sound = pygame.mixer.Sound(game_utils.PAD_HIT)
        # Testing
        self.key_pressed = False
        self.direction = "NONE"
        self.target_y = 0

    def move(self):
        """Description: method provides player pad movement action"""

        if not self.device.is_open():
            self.device.open()

        if self.name is "BLUE":
            self.target_y = self.transform_to_pixel(self.device.reading_1)
        else:
            self.target_y = self.transform_to_pixel(self.device.reading_2)
        if isinstance(self.target_y, int):
            if self.pos_y != self.target_y:
                if self.pos_y > self.target_y:
                    self.pos_y -= game_utils.PAD_SPEED
                elif self.pos_y < self.target_y:
                    self.pos_y += game_utils.PAD_SPEED
        super().move()

    def transform_to_pixel(self, reading):
        """Description: method transforms device readings into player pad position
        :param: Device reading
        :return: Pad pixel position or None in exception
        """
        if reading != -1:
            try:
                coord_y = int((reading - self.device.minimum_point) * 100 /
                              (self.device.maximum_point - self.device.minimum_point))

                return int((game_utils.B_HEIGHT - self.height -
                            (game_utils.OFFSET_HEIGHT * 2)) * coord_y * .01)
            except TypeError:
                StaticUtils.print_message(comm_utils.CMD_ERROR, "Bad reading: " + str(reading))
                return None
        else:
            return None

    def update(self, board):
        """Description: method updates pd position on display
        :param: Board display
        """

        pygame.draw.rect(board, self.color, self.get_rect(), 0)

    def play_sound(self):
        """Description: method plays pad sound effect"""

        self.stop_sound()
        self.sound.play()

    def stop_sound(self):
        """Description: method stops sound effect"""

        self.sound.stop()
