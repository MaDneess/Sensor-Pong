"""
    Name: ball.py
    Author: Aleksej Z
    Date: 2018/08/18
"""
from datetime import datetime
import pygame
import game_utils
import random


class Ball:
    """Description: ball class defines basic behavior of the object"""

    def __init__(self, pos_x=game_utils.BALL_X, pos_y=game_utils.BALL_Y):
        self.starting_pos_x, self.starting_pos_y = pos_x, pos_y
        self.pos_x, self.pos_y = pos_x, pos_y
        self.color = game_utils.BLACK
        self.sound_hit = pygame.mixer.Sound(game_utils.BALL_HIT)
        self.sound_scored = pygame.mixer.Sound(game_utils.BALL_SCORED)
        # get seconds
        self.started = datetime.now()
        self.dir_x = "LEFT"
        self.dir_y = "UP"
        self.changed = False

    def move(self, player_blue, player_red, board):
        """Description: method moves ball object with collision behavior
        :param: Player one
        """

        if self.is_colliding(player_blue, True):
            self.change_direction()
            if board.music:
                player_blue.stop_sound()
                player_blue.play_sound()
        if self.is_colliding(player_red, False):
            self.change_direction()
            if board.music:
                player_red.stop_sound()
                player_red.play_sound()

        if self.pos_x <= game_utils.BALL_SIZE:
            player_red.score += 1
            if board.music:
                board.ball_scored()
        elif (self.pos_x + game_utils.BALL_SIZE) >= game_utils.B_WIDTH:
            player_blue.score += 1
            if board.music:
                board.ball_scored()

        if self.pos_y < game_utils.BALL_SIZE:
            if board.music:
                self.play_sound_hit()
            self.dir_y = "DOWN"
            self.pos_y = game_utils.BALL_SIZE
            self.changed = False
        elif (self.pos_y + game_utils.BALL_SIZE) > game_utils.B_HEIGHT:
            if board.music:
                self.play_sound_hit()
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

        pygame.draw.circle(display, game_utils.BLACK, (self.pos_x, self.pos_y), game_utils.BALL_SIZE, 0)

    def get_rect(self):
        """Description: method returns rectangle object of the ball
        :return: Rectangle object
        """

        rect = pygame.Rect((0,0), (2*game_utils.BALL_SIZE, 2*game_utils.BALL_SIZE))
        rect.center = self.pos_x, self.pos_y
        return rect

    def is_colliding(self, pad, is_left):
        """Description: methods checks if ball object collides with player pad"""

        ball = self.get_rect()
        obj = pad.get_rect()
        collided = False
        if is_left:
            top_left = ball.topleft
            bottom_left = ball.bottomleft

            top = obj.topright
            bottom = obj.bottomright

            if top_left[0] <= top[0] and top_left[0] <= bottom[0] and \
                    bottom_left[0] <= top[0] and bottom_left[0] <= bottom[0]:
                for i in range(top[1], bottom[1], 1):
                    if top_left[1] == i or bottom_left[1] == i:
                        collided = True
                        break
        else:
            top_right = ball.topright
            bottom_right = ball.bottomright

            top = obj.topleft
            bottom = obj.bottomleft

            if top_right[0] >= top[0] and top_right[0] >= bottom[0] and \
                    bottom_right[0] >= top[0] and bottom_right[0] >= bottom[0]:
                for i in range(top[1], bottom[1], 1):
                    if top_right[1] == i or bottom_right[1] == i:
                        collided = True
                        break
        return collided

    def change_direction(self):
        """Description: method changes ball direction"""

        if not self.changed:
            if self.dir_x == "LEFT":
                self.dir_x = "RIGHT"
            elif self.dir_x == "RIGHT":
                self.dir_x = "LEFT"

    def play_sound_hit(self):
        """Description: method plays ball hit sound effect"""

        self.stop_sounds()
        self.sound_hit.play()

    def play_sound_scored(self):
        """Description: method plays ball scored sound effect"""

        self.stop_sounds()
        self.play_sound_scored()

    def stop_sounds(self):
        """Description: method stop all ball sound effects"""

        self.sound_hit.stop()
        self.sound_scored.stop()

    def reset(self):
        self.pos_x, self.pos_y = self.starting_pos_x, self.starting_pos_y
        num = random.randint(0, 80)
        if num < 20:
            self.dir_x = "LEFT"
            self.dir_y = "DOWN"
        elif num < 40:
            self.dir_x = "RIGHT"
            self.dir_y = "UP"
        elif num < 60:
            self.dir_x = "LEFT"
            self.dir_y = "UP"
        elif num < 80:
            self.dir_x = "RIGHT"
            self.dir_y = "DOWN"
