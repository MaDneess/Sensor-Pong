
import Commons

from Button import Button


class MusicButton(Button):
    
    def __init__(self, pos, text, board):
        super().__init__(pos, text, board)
    
    def on_click(self):
        if self.board.music:
            self.board.music = False
            self.text = self.font.render("MUSIC OFF", True, Commons.BLACK)
        else:
            self.board.music = True
            self.text = self.font.render("MUSIC ON", True, Commons.BLACK)