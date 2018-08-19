"""
    Name: player_pad.py
    Author: Aleksej Z
    Date: 2018/08/18
"""
import pygame
import comm_utils
import game_utils
from pad import Pad
from static_utils import StaticUtils
from pressure_device import PressureDevice


class PlayerPad(Pad):
    """Description: pad class with player actions and behavior"""

    def __init__(self, side, port, board):
        Pad.__init__(self, side)
        self.device = PressureDevice(port, board)
        self.device.start()
        # Testing
        self.key_pressed = False
        self.direction = "NONE"

    def move(self):
        """Description: method provides player pad movement action"""

        if self.device.is_open():
            pos_y = self.transform_to_pixel(self.device.reading)
            if isinstance(pos_y, int):
                self.pos_y = pos_y
                super().move()
        else:
            self.device.open()

    def transform_to_pixel(self, reading):
        """Description: method transforms device readings into player pad position
        :param: Device reading
        :return: Pad pixel position or None in exception
        """
        try:
            coord_x = int((reading - self.device.minimum_point)*100 /
                          (self.device.maximum_point - self.device.minimum_point))
            return int((game_utils.B_HEIGHT - self.height -
                        (game_utils.OFFSET_HEIGHT * 2)) * coord_x * .01)
        except TypeError:
            StaticUtils.print_message(comm_utils.CMD_ERROR, "Bad reading: " + str(reading))
            return None

    def move_key(self):
        """Description: method provides player pad movement on key press"""

        if self.key_pressed:
            if self.direction == "UP":
                coord = -game_utils.PAD_SPEED
            elif self.direction == "DOWN":
                coord = game_utils.PAD_SPEED

        self.pos_y += coord
        if self.pos_y < game_utils.OFFSET_HEIGHT:
            self.pos_y = game_utils.OFFSET_HEIGHT
        elif (self.pos_y + self.height) > \
                (game_utils.B_HEIGHT - game_utils.OFFSET_HEIGHT):
            self.pos_y = game_utils.B_HEIGHT - game_utils.OFFSET_HEIGHT - self.height

    def update(self, board):
        """Description: method updates pd position on display
        :param: Board display
        """

        pygame.draw.rect(board, game_utils.BLACK, self.get_rect(), 0)

    def calibrate_device(self):
        """Description: method calibrates middle point of the device"""

        StaticUtils.print_message(comm_utils.CMD_OK, "Calibrating Player " + self.name)
        self.device.open()
        self.device.calibrate()
        self.device.close()
        StaticUtils.print_message(comm_utils.CMD_RESPONSE,
                                  "Player middle point: " + self.device.middle_point)

    def calibrate_min(self):
        """Description: method calibrates device minimum point"""

        StaticUtils.print_message(comm_utils.CMD_OK, "Calibrating Player " + self.name)
        self.device.open()
        self.device.calibrate_min()
        self.device.close()
        StaticUtils.print_message(comm_utils.CMD_RESPONSE, "Player " + self.name +
                                  " minimum point is -- " + str(self.device.minimum_point))

    def calibrate_max(self):
        """Description: method calibrates device maximum point"""

        StaticUtils.print_message(comm_utils.CMD_OK, "Calibrating Player " + self.name)
        self.device.open()
        self.device.calibrate_max()
        self.device.close()
        StaticUtils.print_message(comm_utils.CMD_RESPONSE, "Player " + self.name +
                                  " maximum point is -- " + str(self.device.maximum_point))
