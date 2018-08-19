"""
    Name: ball.py
    Author: Aleksej Z
    Date: 2018/08/18
"""
from datetime import datetime
import pygame
import game_utils


class Ball:
    """Description: ball class defines basic behavior of the object"""

    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = game_utils.BLACK
        # get seconds
        self.started = datetime.now()
        self.dir_x = "LEFT"
        self.dir_y = "UP"
        self.changed = False

    def move(self, player_blue):
        """Description: method moves ball object with collision behavior
        :param: Player one
        """

        if self.is_colliding(player_blue):
            self.change_direction()

        if self.pos_x < game_utils.BALL_SIZE:
            self.dir_x = "RIGHT"
            self.pos_x = game_utils.BALL_SIZE
            self.changed = False
        elif (self.pos_x + game_utils.BALL_SIZE) > game_utils.B_WIDTH:
            self.dir_x = "LEFT"
            self.pos_x = game_utils.B_WIDTH - game_utils.BALL_SIZE
            self.changed = False

        if self.pos_y < game_utils.BALL_SIZE:
            self.dir_y = "DOWN"
            self.pos_y = game_utils.BALL_SIZE
            self.changed = False
        elif (self.pos_y + game_utils.BALL_SIZE) > game_utils.B_HEIGHT:
            self.dir_y = "UP"
            self.pos_y = game_utils.B_HEIGHT - game_utils.BALL_SIZE
            self.changed = False

        if self.dir_x == "LEFT" and self.dir_y == "UP":
            self.pos_x -= game_utils.BALL_SPEED_X
            self.pos_y -= game_utils.BALL_SPEED_Y
        elif self.dir_x == "RIGHT" and self.dir_y == "UP":
            self.pos_x += game_utils.BALL_SPEED_X
            self.pos_y -= game_utils.BALL_SPEED_Y
        elif self.dir_x == "LEFT" and self.dir_y == "DOWN":
            self.pos_x -= game_utils.BALL_SPEED_X
            self.pos_y += game_utils.BALL_SPEED_Y
        elif self.dir_x == "RIGHT" and self.dir_y == "DOWN":
            self.pos_x += game_utils.BALL_SPEED_X
            self.pos_y += game_utils.BALL_SPEED_Y

    def update(self, display):
        """Description: method updates ball position on display"""

        pygame.draw.circle(display, game_utils.BLACK,
                           (self.pos_x, self.pos_y), game_utils.BALL_SIZE, 0)

    def get_rect(self):
        """Description: method returns rectangle object of the ball
        :return: Rectangle object
        """

        return pygame.Rect((self.pos_x, self.pos_y),
                           (game_utils.BALL_SIZE * 2, game_utils.BALL_SIZE * 2))

    def is_colliding(self, pad):
        """Description: methods checks if ball object collides with player pad"""

        return self.get_rect().colliderect(pad.get_rect())

    def change_direction(self):
        """Description: method changes ball direction"""

        if not self.changed:
            if self.dir_x == "LEFT":
                self.dir_x = "RIGHT"
            elif self.dir_x == "RIGHT":
                self.dir_x = "LEFT"
