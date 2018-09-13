"""
    Name: board.py
    Author: Aleksej Z
    Date: 2018/08/18
"""
import sys
import pygame as pg
from pygame.constants import *
import game_utils
from player_pad import PlayerPad
from game_button import GameButton
from options_button import OptionsButton
from exit_button import ExitButton
from calibrate_button import CalibrateButton
from music_button import MusicButton
from back_button import BackButton
from ball import Ball


class Board:
    """Description: game board contains main gui and game widgets"""

    def __init__(self, port1, port2):
        pg.init()
        self.state = game_utils.IN_MENU
        # INIT BUTTONS
        self.game_btn = GameButton(0, "START GAME", self)
        self.opt_btn = OptionsButton(1, "OPTIONS", self)
        self.exit_btn = ExitButton(2, "EXIT", self)
        self.cal_btn = CalibrateButton(0, "CALIBRATE", self)
        self.music_btn = MusicButton(1, "MUSIC ON", self)
        self.back_btn = BackButton(2, "BACK", self)
        # self.player_blue = PlayerPad('LEFT', None, self)
        self.player_blue = PlayerPad('LEFT', port1, self)
        # self.player_red = PlayerPad('RIGHT', port2, self)
        self.ball = Ball(game_utils.BALL_X, game_utils.BALL_Y)
        self.music = True
        self.clock = pg.time.Clock()
        self.display = pg.display.set_mode((game_utils.B_WIDTH, game_utils.B_HEIGHT))
        pg.display.set_caption('Pressure Project v1.0')

    def run(self):
        """Description: method contains board logic running in a loop"""

        while self.state != game_utils.EXIT:
            for event in pg.event.get():
                self.check_for_events(event)
            if self.state != game_utils.EXIT:
                # BEGIN CAL
                self.draw_calibration_messages()
                # MENU
                self.menu_loop()
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

            def check_key_testing():
                """Description: function check events for testing purposes"""
                if (event.key == K_w) and (self.state == game_utils.IN_GAME):
                    self.player_blue.keyPressed = True
                    self.player_blue.direction = "UP"
                elif (event.key == K_s) and (self.state == game_utils.IN_GAME):
                    self.player_blue.keyPressed = True
                    self.player_blue.direction = "DOWN"

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if self.state != game_utils.IN_MENU:
                        self.state = game_utils.IN_MENU
                elif (event.key == K_RETURN) or (event.key == K_KP_ENTER):
                    if (self.state == game_utils.IN_GAME_CAL) or\
                            (self.state == game_utils.IN_MENU_CAL):
                        # self.player_blue.calibrate_device()
                        if self.state == game_utils.IN_GAME_CAL:
                            self.state = game_utils.CAL_MIN
                        elif self.state == game_utils.IN_MENU_CAL:
                            self.state = game_utils.IN_OPTIONS
                    elif self.state == game_utils.CAL_MIN:
                        self.begin_calibration_cycle()
                        self.state = game_utils.CAL_MAX
                    elif self.state == game_utils.CAL_MAX:
                        self.begin_calibration_cycle()
                        self.state = game_utils.IN_GAME
                else:
                    check_key_testing()
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

    def game_loop(self):
        """Description: method contains game logic sequence"""

        # GAME LOOP
        if self.state == game_utils.IN_GAME:
            # game logic
            self.display.fill(game_utils.WHITE)
            self.draw_board()
            self.draw_scores()
            # new by state movement
            self.player_blue.move_by_state()
            # min - max movement
            # self.player_blue.move()
            # self.pRed.move()
            # -- For testing --
            # self.player_blue.move_key()
            # -----------------
            self.ball.move(self.player_blue)
            self.player_blue.update(self.display)
            # self.pRed.update(self.display)
            self.ball.update(self.display)

    def menu_loop(self):
        """Description: method contains menu logic sequence"""

        if (self.state == game_utils.IN_MENU) or (self.state == game_utils.IN_OPTIONS):
            self.display.fill(game_utils.LIGHT_BLUE)
            self.draw_authors()
            self.draw_header()
            self.draw_images()
        if self.state == game_utils.IN_MENU:
            self.draw_menu_buttons()
        elif self.state == game_utils.IN_OPTIONS:
            self.draw_options_buttons()

    def begin_calibration_cycle(self):
        """Description: method start player device calibration"""

        if self.state == game_utils.CAL_MIN:
            self.player_blue.calibrate_min()
            # self.pRed.calibrate_min()
        elif self.state == game_utils.CAL_MAX:
            self.player_blue.calibrate_max()
            # self.pRed.calibrate_max()

    def draw_board(self):
        """Description: method draws basic game board structure"""

        pg.draw.rect(self.display, game_utils.BLACK,
                     (0, 0, game_utils.B_WIDTH, game_utils.B_HEIGHT), game_utils.CAGE_WIDTH)
        pg.draw.line(self.display, game_utils.BLACK, (int(game_utils.B_WIDTH / 2 - 2), 0),
                     (int(game_utils.B_WIDTH / 2 - 2), game_utils.B_HEIGHT), 4)

    def draw_images(self):
        """Description: method draws images on the board"""

        logo_rect = game_utils.LOGO.get_rect()
        logo_rect.center = (game_utils.B_WIDTH - 45, game_utils.B_HEIGHT - 45)
        self.display.blit(game_utils.LOGO, logo_rect)

    def draw_scores(self):
        """Description: method draws player scores on the board"""

        size = int(game_utils.B_HEIGHT * .1)
        font = pg.font.Font(game_utils.ARCADE_FONT, size)
        score1 = font.render(str(self.player_blue.score), True, game_utils.BLACK)
        # score2 = font.render(str(self.pRed.score), True, game_utils.BLACK)
        rect1 = score1.get_rect()
        # rect2 = score2.get_rect()
        rect1.topright = (int(game_utils.B_WIDTH / 2) - 10, game_utils.OFFSET_HEIGHT)
        # rect2.topleft = (int(game_utils.B_WIDTH/2)-10, game_utils.OFFSET_HEIGHT)
        self.display.blit(score1, rect1)
        # self.display.blit(score2, rect2)

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

        pg.draw.rect(self.display, self.cal_btn.color, self.cal_btn.get_rect(), 0)
        self.display.blit(self.cal_btn.text, self.cal_btn.get_text_rect())

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

        if self.cal_btn.get_rect().collidepoint(pos) == 1:
            self.cal_btn.on_click()
        elif self.music_btn.get_rect().collidepoint(pos) == 1:
            self.music_btn.on_click()
        elif self.back_btn.get_rect().collidepoint(pos) == 1:
            self.back_btn.on_click()

    def draw_header(self):
        """Description: method draws board header"""

        font = pg.font.Font(game_utils.ARCADE_FONT, int(game_utils.B_HEIGHT * 0.22))
        text = font.render("SENSOR  PONG", True, game_utils.WHITE)
        text_rect = text.get_rect()
        text_rect.center = (int(game_utils.B_WIDTH / 2), int(game_utils.B_HEIGHT * 0.2))
        self.display.blit(text, text_rect)

    def draw_authors(self):
        """Description: method draws authors"""

        size = int(game_utils.B_HEIGHT * .045)
        font = pg.font.Font(game_utils.ARCADE_FONT, size)
        text = "BHGE  PiCoding  Club"
        text = font.render(text, True, game_utils.WHITE)
        text_rect = text.get_rect()
        text_rect.bottomleft = (25, int(game_utils.B_HEIGHT * 0.92))
        self.display.blit(text, text_rect)

    def draw_calibration_messages(self):
        """Description: method draws calibration messages"""

        def display_print(text_size, msg, pos):
            """Description: function prints messages on display
            :param: Text size
            :param: Message to print
            :param: Text position
            """

            text = font.render(msg, True, game_utils.WHITE)
            text_rect = text.get_rect()
            text_rect.center = (int(game_utils.B_WIDTH / 2),
                                int(game_utils.B_HEIGHT / 2) - text_size * pos)
            self.display.blit(text, text_rect)

        if (self.state == game_utils.IN_GAME_CAL) or (self.state == game_utils.IN_MENU_CAL):
            self.display.fill(game_utils.LIGHT_BLUE)
            size = int(game_utils.B_HEIGHT * .09)
            font = pg.font.Font(game_utils.ARCADE_FONT, size)
            display_print(size, "ATTENTION", 2)
            display_print(size, "HOLD   THE   SENSOR   IN", 1)
            display_print(size, "PLAYABLE   POSITION", 0)
            display_print(size, "CALIBRATION   WILL   BE", -1)
            display_print(size, "DONE  FOR  ALL  PLAYERS", -2)
            font = pg.font.Font("fonts/arcade.ttf", int(size * 0.5))
            display_print(int(size * 0.5), "Press   ENTER   to continue", -10)

        elif self.state == game_utils.CAL_MIN or self.state == game_utils.CAL_MAX:
            self.display.fill(game_utils.LIGHT_BLUE)
            size = int(game_utils.B_HEIGHT * .09)
            font = pg.font.Font(game_utils.ARCADE_FONT, size)
            display_print(int(size * 0.5), "Press   ENTER   to continue", -10)
            if self.state == game_utils.CAL_MIN:
                display_print(size, "HOLD SENSOR AT UPPER POINT", 0)
            elif self.state == game_utils.CAL_MAX:
                display_print(size, "HOLD SENSOR AT LOWER POINT", 0)
