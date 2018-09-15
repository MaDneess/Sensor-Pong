"""
    Name: ball.py
    Author: Aleksej Z
    Date: 2018/08/18
"""
import time
import pygame
import random
import game_utils


class Ball:
    """Description: ball class defines basic behavior of the object"""

    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = game_utils.BLACK
        self.sound_hit = pygame.mixer.Sound(game_utils.BALL_HIT)
        self.sound_scored = pygame.mixer.Sound(game_utils.BALL_SCORED)
        # get seconds
        self.started = time.time()
        self.speeds = [game_utils.BALL_SPEED_X, game_utils.BALL_SPEED_Y]
        self.direction = ["LEFT", "UP"]
        self.changed = False
        self.generate_direction()

    def move(self, player_blue, player_red):
        """Description: method moves ball object with collision behavior
        :param: Player one
        """

        # increase velocity based gaming time
        if int(time.time() - self.started) > 3:
            self.started = time.time()
            self.speeds[0] += game_utils.BALL_VELOCITY
            self.speeds[1] += game_utils.BALL_VELOCITY

        if self.is_colliding(player_blue):
            self.change_direction()
            player_blue.stop_sound()
            player_blue.play_sound()
        elif self.is_colliding(player_red):
            self.change_direction()
            player_red.stop_sound()
            player_red.play_sound()

        if self.pos_x < -game_utils.BALL_SIZE:
            self.reset(player_blue, player_red, "LEFT")
            # self.play_sound_hit()
            # self.dir_x = "RIGHT"
            # self.pos_x = game_utils.BALL_SIZE
            # self.changed = False
        elif (self.pos_x - game_utils.BALL_SIZE) > game_utils.B_WIDTH:
            self.reset(player_blue, player_red, "RIGHT")
            # self.play_sound_hit()
            # self.dir_x = "LEFT"
            # self.pos_x = game_utils.B_WIDTH - game_utils.BALL_SIZE
            # self.changed = False

        if self.pos_y < game_utils.BALL_SIZE:
            self.play_sound_hit()
            self.direction[1] = "DOWN"
            self.pos_y = game_utils.BALL_SIZE
            self.changed = False
        elif (self.pos_y + game_utils.BALL_SIZE) > game_utils.B_HEIGHT:
            self.play_sound_hit()
            self.direction[1] = "UP"
            self.pos_y = game_utils.B_HEIGHT - game_utils.BALL_SIZE
            self.changed = False

        if self.direction[0] == "LEFT" and self.direction[1] == "UP":
            self.pos_x -= self.speeds[0]
            self.pos_y -= self.speeds[1]
        elif self.direction[0] == "RIGHT" and self.direction[1] == "UP":
            self.pos_x += self.speeds[0]
            self.pos_y -= self.speeds[1]
        elif self.direction[0] == "LEFT" and self.direction[1] == "DOWN":
            self.pos_x -= self.speeds[0]
            self.pos_y += self.speeds[1]
        elif self.direction[0] == "RIGHT" and self.direction[1] == "DOWN":
            self.pos_x += self.speeds[0]
            self.pos_y += self.speeds[1]

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
            if self.direction[0] == "LEFT":
                self.direction[0] = "RIGHT"
            elif self.direction[0] == "RIGHT":
                self.direction[0] = "LEFT"

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

    def reset(self, player_blue, player_red, side):
        self.pos_x = game_utils.BALL_X
        self.pos_y = game_utils.BALL_Y
        self.generate_direction()
        self.speeds = [game_utils.BALL_SPEED_X, game_utils.BALL_SPEED_Y]
        player_blue.reset()
        player_red.reset()
        if side == "LEFT":
            player_red.score += 1
        elif side == "RIGHT":
            player_blue.score += 1

    def generate_direction(self):
        num_1 = 31 * random.randint(1, 9)
        if num_1 < 93:
            self.direction[0] = "RIGHT"
            num_2 = 17 * random.randint(1, 9)
            if num_2 < 51:
                self.direction[1] = "UP"
            elif num_2 > 102:
                self.direction[1] = "DOWN"
        elif num_1 > 186:
            self.direction[0] = "LEFT"
            num_2 = 17 * random.randint(1, 9)
            if num_2 < 51:
                self.direction[1] = "DOWN"
            elif num_2 > 102:
                self.direction[1] = "UP"
        else:
            self.change_direction()
