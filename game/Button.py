
import Commons, pygame
from abc import ABC, abstractmethod

class Button(ABC):
    
    def __init__(self, pos, text, board):
        self.font = pygame.font.Font("fonts/arcade.ttf", int(Commons.BTN_WIDTH*0.17))
        self.text = self.font.render(text, True, Commons.BLACK)
        self.x = Commons.POS_X
        self.y = Commons.POS_Y
        if pos > 0:
            for n in range(pos):
                self.y += Commons.BTN_HEIGHT + Commons.BTN_OFFSET
        self.color = Commons.WHITE
        self.board = board
        
        
    
    @abstractmethod
    def on_click(self):
        pass
    
    def getRect(self):
        return pygame.Rect((self.x, self.y), (Commons.BTN_WIDTH, Commons.BTN_HEIGHT))
    
    def getTextRect(self):
        self.textRect = self.text.get_rect()
        self.textRect.center = self.getRect().center
        return self.textRect
        