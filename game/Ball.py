
import Commons, pygame

from datetime import datetime
from StaticUtils import StaticUtils

class Ball:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = Commons.BALL_SIZE
        self.color = Commons.BLACK
        #get seconds
        self.started = datetime.now()
        self.DIR_X = "LEFT"
        self.DIR_Y = "UP"
    
    def move(self):            
        if self.x <= Commons.CAGE_WIDTH:
            self.DIR_X = "RIGHT"
        elif (self.x + Commons.BALL_SIZE) >= (Commons.B_WIDTH - Commons.CAGE_WIDTH):
            self.DIR_X = "LEFT"
        
        if self.y <= Commons.CAGE_WIDTH:
            self.DIR_Y = "DOWN"
        elif (self.y + Commons.BALL_SIZE) >= (Commons.B_HEIGHT - Commons.CAGE_WIDTH):
            self.DIR_Y = "UP"
        
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
        pygame.draw.rect(display, Commons.BLACK, self.getRect(), 0)
    
    def getRect(self):
        return pygame.Rect((self.x, self.y),(self.size, self.size))

    