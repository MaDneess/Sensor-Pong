import Commons, pygame

from datetime import datetime
from StaticUtils import StaticUtils


class Ball:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = Commons.BALL_SIZE
        self.color = Commons.BLACK
        # get seconds
        self.started = datetime.now()
        self.DIR_X = "LEFT"
        self.DIR_Y = "UP"
        self.changed = False

    def move(self, pBlue):

        if self.isColliding(pBlue):
            self.changeDirection()

        if self.x < Commons.BALL_SIZE:
            self.DIR_X = "RIGHT"
            self.x = Commons.BALL_SIZE
            self.changed = False
        elif (self.x + Commons.BALL_SIZE) > Commons.B_WIDTH:
            self.DIR_X = "LEFT"
            self.x = Commons.B_WIDTH - Commons.BALL_SIZE
            self.changed = False

        if self.y < Commons.BALL_SIZE:
            self.DIR_Y = "DOWN"
            self.y = Commons.BALL_SIZE
            self.changed = False
        elif (self.y + Commons.BALL_SIZE) > Commons.B_HEIGHT:
            self.DIR_Y = "UP"
            self.y = Commons.B_HEIGHT - Commons.BALL_SIZE
            self.changed = False

        if self.DIR_X == "LEFT" and self.DIR_Y == "UP":
            self.x -= Commons.BALL_SPEED_X
            self.y -= Commons.BALL_SPEED_Y
        elif self.DIR_X == "RIGHT" and self.DIR_Y == "UP":
            self.x += Commons.BALL_SPEED_X
            self.y -= Commons.BALL_SPEED_Y
        elif self.DIR_X == "LEFT" and self.DIR_Y == "DOWN":
            self.x -= Commons.BALL_SPEED_X
            self.y += Commons.BALL_SPEED_Y
        elif self.DIR_X == "RIGHT" and self.DIR_Y == "DOWN":
            self.x += Commons.BALL_SPEED_X
            self.y += Commons.BALL_SPEED_Y

    def update(self, display):
        pygame.draw.circle(display, Commons.BLACK, (self.x, self.y), self.size, 0)

    def getRect(self):
        return pygame.Rect((self.x, self.y), (self.size * 2, self.size * 2))

    def isColliding(self, pad):
        return self.getRect().colliderect(pad.getRect())

    def changeDirection(self):
        if not self.changed:
            if self.DIR_X == "LEFT":
                self.DIR_X = "RIGHT"
            elif self.DIR_X == "RIGHT":
                self.DIR_X = "LEFT"
