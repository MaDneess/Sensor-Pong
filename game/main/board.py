"""
    Name: board.py
    Author: Aleksej Z
    Date: 2018/08/18
"""
import sys

import pygame as pg
from pygame.constants import *

import game_utils
from back_button import BackButton
from ball import Ball
from exit_button import ExitButton
from game_button import GameButton
from music_button import MusicButton
from options_button import OptionsButton
from player_pad import PlayerPad
from sensor_device import SensorDevice
from time import time


class Board:
    """Description: game board contains main gui and game widgets"""

    def __init__(self, port):
        pg.init()
        self.state = game_utils.IN_MENU
        # INIT BUTTONS
        self.game_btn = GameButton(0, "START GAME", self)
        self.opt_btn = OptionsButton(1, "OPTIONS", self)
        self.exit_btn = ExitButton(2, "EXIT", self)
        self.music_btn = MusicButton(1, "MUSIC ON", self)
        self.back_btn = BackButton(2, "BACK", self)
        self.game_started = False
        sensor = SensorDevice(port, self)
        sensor.start()
        self.player_blue = PlayerPad('LEFT', sensor, game_utils.LIGHT_BLUE)
        self.player_red = PlayerPad('RIGHT', sensor, game_utils.DARK_RED)
        self.ball = Ball()
        self.music = True
        self.clock = pg.time.Clock()
        self.display = pg.display.set_mode((game_utils.B_WIDTH, game_utils.B_HEIGHT))
        pg.display.set_caption('Ping-Pong Distance Sensor v1.1')
        self.timer = 0
        self.started_time = None

    def run(self):
        """Description: method contains board logic running in a loop"""

        while self.state != game_utils.EXIT:
            for event in pg.event.get():
                self.check_for_events(event)
            if self.state != game_utils.EXIT:
                # MENU
                self.menu_loop()
                # WINS
                self.win_loop()
                # GAME
                self.game_loop()
            pg.display.flip()
            self.clock.tick(game_utils.FPS)
        # clean exit
        pg.quit()
        sys.exit(0)

    def check_for_events(self, event):
        """Description: method check for event happened on the board
        :param: Pygame event
        """

        def check_key_event():
            """Description: function checks event for key press"""

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if self.state != game_utils.IN_MENU:
                        self.state = game_utils.IN_MENU
                elif (event.key == K_RETURN) or (event.key == K_KP_ENTER):
                    if (self.state == game_utils.IN_GAME_WIN_P1) or (self.state == game_utils.IN_GAME_WIN_P2):
                        self.restart_game()
            elif event.type == KEYUP:
                if (event.key == K_w) and (self.state == game_utils.IN_GAME):
                    self.player_blue.keyPressed = False
                elif (event.key == K_s) and (self.state == game_utils.IN_GAME):
                    self.player_blue.keyPressed = False

        # --------------------
        if event.type == QUIT:
            self.state = game_utils.EXIT
        elif event.type == MOUSEBUTTONUP:
            if self.state == game_utils.IN_MENU:
                self.check_menu_events(pg.mouse.get_pos())
            elif self.state == game_utils.IN_OPTIONS:
                self.check_options_events(pg.mouse.get_pos())
        else:
            check_key_event()

    def restart_game(self):
        self.player_blue.reset()
        self.player_red.reset()
        self.ball.reset()
        self.game_started = False
        self.timer = 0
        self.started_time = None
        self.state = game_utils.IN_GAME

    def draw_timer(self):
        if self.started_time is None:
            self.started_time = time()
        self.timer = int(time() - self.started_time)
        if self.timer < 1:
            self.draw_countdown(3)
        elif self.timer < 2:
            self.draw_countdown(2)
        elif self.timer < 3:
            self.draw_countdown(1)
        elif self.timer < 4:
            self.draw_countdown("G  O")
        elif self.timer > 4:
            self.game_started = True

    def draw_countdown(self, value=None):
        size = int(game_utils.B_HEIGHT * .6)
        font = pg.font.Font(game_utils.ARCADE_FONT, size)
        text = font.render(str(value), True, game_utils.BLACK)
        rect = text.get_rect()
        rect.center = (int(game_utils.B_WIDTH / 2), int(game_utils.B_HEIGHT / 2))
        self.display.blit(text, rect)

    def game_loop(self):
        """Description: method contains game logic sequence"""

        # GAME LOOP
        if self.state == game_utils.IN_GAME:
            # game logic
            self.display.fill(game_utils.WHITE)
            self.draw_board()
            self.draw_scores()

            if not self.game_started:
                self.draw_timer()

            self.player_blue.move()
            self.player_red.move()

            if self.game_started:
                self.ball.move(self.player_blue, self.player_red, self)

            self.player_blue.update(self.display)
            self.player_red.update(self.display)

            self.ball.update(self.display)

    def win_loop(self):
        """Description: """
        if (self.state == game_utils.IN_GAME_WIN_P1) or (self.state == game_utils.IN_GAME_WIN_P2):
            size = int(game_utils.B_HEIGHT * .13)
            font = pg.font.Font(game_utils.ARCADE_FONT, size)
            if self.state == game_utils.IN_GAME_WIN_P1:
                self.display.fill(game_utils.LIGHT_BLUE)
                text = "Blue   Player   Wins"
            else:
                self.display.fill(game_utils.DARK_RED)
                text = "Red   Player   Wins"
            text = font.render(text, True, game_utils.WHITE)
            text_rect = text.get_rect()
            text_rect.center = (int(game_utils.B_WIDTH / 2), int(game_utils.B_HEIGHT / 2))
            self.display.blit(text, text_rect)

            size = int(game_utils.B_HEIGHT * .07)
            font = pg.font.Font(game_utils.ARCADE_FONT, size)
            text = "Press  ENTER  to continue"
            text = font.render(text, True, game_utils.WHITE)
            text_rect = text.get_rect()
            text_rect.center = (int(game_utils.B_WIDTH / 2), int(game_utils.B_HEIGHT * .9))
            self.display.blit(text, text_rect)

    def menu_loop(self):
        """Description: method contains menu logic sequence"""

        if (self.state == game_utils.IN_MENU) or (self.state == game_utils.IN_OPTIONS):
            self.display.fill(game_utils.LIGHT_BLUE)
            self.draw_header()
        if self.state == game_utils.IN_MENU:
            self.draw_menu_buttons()
        elif self.state == game_utils.IN_OPTIONS:
            self.draw_options_buttons()

    def draw_board(self):
        """Description: method draws basic game board structure"""

        pg.draw.rect(self.display, game_utils.BLACK,
                     (0, 0, game_utils.B_WIDTH, game_utils.B_HEIGHT), game_utils.CAGE_WIDTH)
        pg.draw.line(self.display, game_utils.BLACK, (int(game_utils.B_WIDTH / 2 - 2), 0),
                     (int(game_utils.B_WIDTH / 2 - 2), game_utils.B_HEIGHT), 4)

    def draw_scores(self):
        """Description: method draws player scores on the board"""

        size = int(game_utils.B_HEIGHT * .1)
        font = pg.font.Font(game_utils.ARCADE_FONT, size)
        score1 = font.render(str(self.player_blue.score), True, game_utils.BLACK)
        score2 = font.render(str(self.player_red.score), True, game_utils.BLACK)
        rect1 = score1.get_rect()
        rect2 = score2.get_rect()
        rect1.topright = (int(game_utils.B_WIDTH / 2) - 10, game_utils.OFFSET_HEIGHT)
        rect2.topleft = (int(game_utils.B_WIDTH / 2) + 10, game_utils.OFFSET_HEIGHT)
        self.display.blit(score1, rect1)
        self.display.blit(score2, rect2)

    def draw_menu_buttons(self):
        """Description: method draws main menu buttons"""

        pg.draw.rect(self.display, self.game_btn.color, self.game_btn.get_rect(), 0)
        self.display.blit(self.game_btn.text, self.game_btn.get_text_rect())

        pg.draw.rect(self.display, self.opt_btn.color, self.opt_btn.get_rect(), 0)
        self.display.blit(self.opt_btn.text, self.opt_btn.get_text_rect())

        pg.draw.rect(self.display, self.exit_btn.color, self.exit_btn.get_rect(), 0)
        self.display.blit(self.exit_btn.text, self.exit_btn.get_text_rect())

    def draw_options_buttons(self):
        """Description: method draws options menu buttons"""

        pg.draw.rect(self.display, self.music_btn.color, self.music_btn.get_rect(), 0)
        self.display.blit(self.music_btn.text, self.music_btn.get_text_rect())

        pg.draw.rect(self.display, self.back_btn.color, self.back_btn.get_rect(), 0)
        self.display.blit(self.back_btn.text, self.back_btn.get_text_rect())

    def check_menu_events(self, pos):
        """Description: method checks menu buttons events
        :param: Mouse position
        """

        if self.game_btn.get_rect().collidepoint(pos) == 1:
            self.game_btn.on_click()
        elif self.opt_btn.get_rect().collidepoint(pos) == 1:
            self.opt_btn.on_click()
        elif self.exit_btn.get_rect().collidepoint(pos) == 1:
            self.exit_btn.on_click()

    def check_options_events(self, pos):
        """Description: method checks options menu events
        :param: Mouse position
        """

        if self.music_btn.get_rect().collidepoint(pos) == 1:
            self.music_btn.on_click()
        elif self.back_btn.get_rect().collidepoint(pos) == 1:
            self.back_btn.on_click()

    def draw_header(self):
        """Description: method draws board header"""

        font = pg.font.Font(game_utils.ARCADE_FONT, int(game_utils.B_HEIGHT * 0.22))
        text = font.render("SENSOR  PONG", True, game_utils.WHITE)
        text_rect1 = text.get_rect()
        text_rect1.center = (int(game_utils.B_WIDTH / 2), int(game_utils.B_HEIGHT * 0.2))
        self.display.blit(text, text_rect1)

        font = pg.font.Font(game_utils.ARCADE_FONT, int(game_utils.B_HEIGHT * 0.1))
        text = font.render("Coding   Club", True, game_utils.WHITE)
        text_rect = text.get_rect()
        text_rect.top = text_rect1.bottom
        text_rect.centerx = text_rect1.centerx
        self.display.blit(text, text_rect)

    def ball_scored(self):
        if self.player_blue.score == 1:
            self.state = game_utils.IN_GAME_WIN_P1
        elif self.player_red.score == 1:
            self.state = game_utils.IN_GAME_WIN_P2
        else:
            self.game_started = False
            self.timer = 0
            self.started_time = None
            self.ball.reset()
