
import Commons, pygame, datetime

from StaticUtils import StaticUtils
from CommUtils import CommUtils

class DeviceCalibration:       
    
    @staticmethod
    def beginCalibration(display, players):
        beforeTime = datetime.datetime.now()
        sec = -1
        while sec < 4:
            display.fill(Commons.LIGHT_BLUE)
            #attention message
            size = int(Commons.B_HEIGHT * 0.09)
            font = pygame.font.Font("fonts/arcade.ttf", size)
            text = font.render("ATTENTION", True, Commons.WHITE)
            text_rect = text.get_rect()
            text_rect.center = (int(Commons.B_WIDTH/2), size)
            display.blit(text, text_rect)
            
            currTime = datetime.datetime.now()
            time = str(currTime - beforeTime)
            time = time.split(':')
            time = time[2].split('.')
            sec = int(time[0])
        
        #calibrate for all players
        for player in players:
            pass
        
        return True