
import Commons

from Button import Button

class BackButton(Button):
    
    def __init__(self, pos, text, board):
        super().__init__(pos, text, board)
        
    def on_click(self):
        if self.board.state == Commons.IN_OPTIONS:
            self.board.state = Commons.IN_MENU