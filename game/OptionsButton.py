
import Commons

from Button import Button

class OptionsButton(Button):
    
    def __init__(self, pos, text, board):
        super().__init__(pos, text, board)
        
    def on_click(self):
        self.board.state = Commons.IN_OPTIONS
        