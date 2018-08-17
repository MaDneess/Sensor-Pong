import pygame as pg
import Commons, sys, time

from pygame.locals import *
from PlayerPad import PlayerPad
from GameButton import GameButton
from OptionsButton import OptionsButton
from ExitButton import ExitButton
from CalibrateButton import CalibrateButton
from MusicButton import MusicButton
from BackButton import BackButton
from Ball import Ball


class Board:

    def __init__(self, port1, port2):
        pg.init()

        self.state = Commons.IN_MENU
        # INIT BUTTONS
        self.gameBtn = GameButton(0, "START GAME", self)
        self.optBtn = OptionsButton(1, "OPTIONS", self)
        self.extBtn = ExitButton(2, "EXIT", self)
        self.calBtn = CalibrateButton(0, "CALIBRATE", self)
        self.musicBtn = MusicButton(1, "MUSIC ON", self)
        self.backBtn = BackButton(2, "BACK", self)

        # self.pBlue = PlayerPad('LEFT', None, self)
        self.pBlue = PlayerPad('LEFT', port1, self)
        # self.pRed = PlayerPad('RIGHT', PressureDevice(port2))

        self.ball = Ball(Commons.BALL_X, Commons.BALL_Y)

        self.music = True

        self.clock = pg.time.Clock()
        self.display = pg.display.set_mode((Commons.B_WIDTH, Commons.B_HEIGHT))
        pg.display.set_caption('Pressure Project v1.0')

    def run(self):
        while self.state != Commons.EXIT:
            for event in pg.event.get():
                self.checkForGameEvent(event)
            if self.state != Commons.EXIT:
                # BEGIN CAL
                self.beginCal()
                # MENU
                self.menuLoop()
                # GAME
                self.gameLoop()

            pg.display.flip()
            self.clock.tick(Commons.FPS)

        # clean exit
        pg.quit()
        sys.exit(0)

    def checkForGameEvent(self, event):
        if event.type == QUIT:
            self.state = Commons.EXIT
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if self.state != Commons.IN_MENU: self.state = Commons.IN_MENU
            elif (event.key == K_RETURN) or (event.key == K_KP_ENTER):
                if (self.state == Commons.IN_GAME_CAL) or (self.state == Commons.IN_MENU_CAL):
                    # self.pBlue.calibrateDevice()
                    if self.state == Commons.IN_GAME_CAL:
                        self.state = Commons.CAL_MIN
                    elif self.state == Commons.IN_MENU_CAL:
                        self.state = Commons.IN_OPTIONS
                elif self.state == Commons.CAL_MIN:
                    self.beginCalibrationCycle()
                    self.state = Commons.CAL_MAX
                elif self.state == Commons.CAL_MAX:
                    self.beginCalibrationCycle()
                    self.state = Commons.IN_GAME
            # FOR TESTING
            elif (event.key == K_w) and (self.state == Commons.IN_GAME):
                self.pBlue.keyPressed = True
                self.pBlue.direction = "UP"
            elif (event.key == K_s) and (self.state == Commons.IN_GAME):
                self.pBlue.keyPressed = True
                self.pBlue.direction = "DOWN"
        # -----------
        elif event.type == KEYUP:
            if (event.key == K_w) and (self.state == Commons.IN_GAME):
                self.pBlue.keyPressed = False
            elif (event.key == K_s) and (self.state == Commons.IN_GAME):
                self.pBlue.keyPressed = False
        elif event.type == MOUSEBUTTONUP:
            if self.state == Commons.IN_MENU:
                self.checkMenuButtonEvent(pg.mouse.get_pos())
            elif self.state == Commons.IN_OPTIONS:
                self.checkOptionsButtonEvent(pg.mouse.get_pos())

    def getDisplay(self):
        return self.display

    def getPlayers(self):
        return self.pBlue, None

    def drawBoard(self):
        pg.draw.rect(self.display, Commons.BLACK, (0, 0, Commons.B_WIDTH, Commons.B_HEIGHT), Commons.CAGE_WIDTH)
        pg.draw.line(self.display, Commons.BLACK, (int(Commons.B_WIDTH / 2 - 2), 0),
                     (int(Commons.B_WIDTH / 2 - 2), Commons.B_HEIGHT), 4)

    def gameLoop(self):
        # GAME LOOP
        if self.state == Commons.IN_GAME:
            # game logic
            self.display.fill(Commons.WHITE)
            self.drawBoard()
            self.drawScores()
            self.pBlue.move()
            # self.pRed.move()

            # For testing
            # self.pBlue.moveKey()
            # -----------

            self.ball.move(self.pBlue)
            self.pBlue.update(self.display)
            # self.pRed.update(self.display)
            self.ball.update(self.display)

    def menuLoop(self):
        if (self.state == Commons.IN_MENU) or (self.state == Commons.IN_OPTIONS):
            self.display.fill(Commons.LIGHT_BLUE)
            self.drawAuthors()
            self.drawHeader()
            self.drawImages()
        if self.state == Commons.IN_MENU:
            self.drawMenuButtons()
        elif self.state == Commons.IN_OPTIONS:
            self.drawOptionsButtons()

    def beginCalibrationCycle(self):
        if self.state == Commons.CAL_MIN:
            self.pBlue.calibrateMin()
            # self.pRed.calibrateMin()
        elif self.state == Commons.CAL_MAX:
            self.pBlue.calibrateMax()
            # self.pRed.calibrateMax()

    def drawImages(self):
        logoRect = Commons.LOGO.get_rect()
        logoRect.center = (Commons.B_WIDTH - 45, Commons.B_HEIGHT - 45)
        self.display.blit(Commons.LOGO, logoRect)

    def drawScores(self):
        size = int(Commons.B_HEIGHT * .1)
        font = pg.font.Font(Commons.ARCADE_FONT, size)
        score1 = font.render(str(self.pBlue.score), True, Commons.BLACK)
        # score2 = font.render(str(self.pRed.score), True, Commons.BLACK)
        rect1 = score1.get_rect()
        # rect2 = score2.get_rect()
        rect1.topright = (int(Commons.B_WIDTH / 2) - 10, Commons.OFFSET_HEIGHT)
        # rect2.topleft = (int(Commons.B_WIDTH/2)-10, Commons.OFFSET_HEIGHT)
        self.display.blit(score1, rect1)
        # self.display.blit(score2, rect2)

    def drawMenuButtons(self):
        pg.draw.rect(self.display, self.gameBtn.color, self.gameBtn.getRect(), 0)
        self.display.blit(self.gameBtn.text, self.gameBtn.getTextRect())

        pg.draw.rect(self.display, self.optBtn.color, self.optBtn.getRect(), 0)
        self.display.blit(self.optBtn.text, self.optBtn.getTextRect())

        pg.draw.rect(self.display, self.extBtn.color, self.extBtn.getRect(), 0)
        self.display.blit(self.extBtn.text, self.extBtn.getTextRect())

    def drawOptionsButtons(self):
        pg.draw.rect(self.display, self.calBtn.color, self.calBtn.getRect(), 0)
        self.display.blit(self.calBtn.text, self.calBtn.getTextRect())

        pg.draw.rect(self.display, self.musicBtn.color, self.musicBtn.getRect(), 0)
        self.display.blit(self.musicBtn.text, self.musicBtn.getTextRect())

        pg.draw.rect(self.display, self.backBtn.color, self.backBtn.getRect(), 0)
        self.display.blit(self.backBtn.text, self.backBtn.getTextRect())

    def checkMenuButtonEvent(self, pos):
        if self.gameBtn.getRect().collidepoint(pos) == 1:
            self.gameBtn.on_click()
        elif self.optBtn.getRect().collidepoint(pos) == 1:
            self.optBtn.on_click()
        elif self.extBtn.getRect().collidepoint(pos) == 1:
            self.extBtn.on_click()

    def checkOptionsButtonEvent(self, pos):
        if self.calBtn.getRect().collidepoint(pos) == 1:
            self.calBtn.on_click()
        elif self.musicBtn.getRect().collidepoint(pos) == 1:
            self.musicBtn.on_click()
        elif self.backBtn.getRect().collidepoint(pos) == 1:
            self.backBtn.on_click()

    def drawHeader(self):
        font = pg.font.Font(Commons.ARCADE_FONT, int(Commons.B_HEIGHT * 0.22))
        text = font.render("SENSOR  PONG", True, Commons.WHITE)
        text_rect = text.get_rect()
        text_rect.center = (int(Commons.B_WIDTH / 2), int(Commons.B_HEIGHT * 0.2))
        self.display.blit(text, text_rect)

    def drawAuthors(self):
        size = int(Commons.B_HEIGHT * .045)
        font = pg.font.Font(Commons.ARCADE_FONT, size)
        text = "BHGE  PiCoding  Club"
        text = font.render(text, True, Commons.WHITE)
        text_rect = text.get_rect()
        text_rect.bottomleft = (25, int(Commons.B_HEIGHT * 0.92))
        self.display.blit(text, text_rect)

    def beginCal(self):
        def displayPrint(size, msg, pos):
            text = font.render(msg, True, Commons.WHITE)
            text_rect = text.get_rect()
            text_rect.center = (int(Commons.B_WIDTH / 2), int(Commons.B_HEIGHT / 2) - size * pos)
            self.display.blit(text, text_rect)

        if (self.state == Commons.IN_GAME_CAL) or (self.state == Commons.IN_MENU_CAL):
            self.display.fill(Commons.LIGHT_BLUE)
            size = int(Commons.B_HEIGHT * .09)
            font = pg.font.Font(Commons.ARCADE_FONT, size)
            displayPrint(size, "ATTENTION", 2)
            displayPrint(size, "HOLD   THE   SENSOR   IN", 1)
            displayPrint(size, "PLAYABLE   POSITION", 0)
            displayPrint(size, "CALIBRATION   WILL   BE", -1)
            displayPrint(size, "DONE  FOR  ALL  PLAYERS", -2)
            font = pg.font.Font("fonts/arcade.ttf", int(size * 0.5))
            displayPrint(int(size * 0.5), "Press   ENTER   to continue", -10)

        elif self.state == Commons.CAL_MIN or self.state == Commons.CAL_MAX:
            self.display.fill(Commons.LIGHT_BLUE)
            size = int(Commons.B_HEIGHT * .09)
            font = pg.font.Font(Commons.ARCADE_FONT, size)
            displayPrint(int(size * 0.5), "Press   ENTER   to continue", -10)
            if self.state == Commons.CAL_MIN:
                displayPrint(size, "HOLD SENSOR AT UPPER POINT", 0)
            elif self.state == Commons.CAL_MAX:
                displayPrint(size, "HOLD SENSOR AT UPPER POINT", 0)
