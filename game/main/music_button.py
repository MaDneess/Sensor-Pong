"""
    Name: music_button.py
    Author: Aleksej Z
    Date: 2018/08/18
"""
import game_utils
from button import Button


class MusicButton(Button):
    """Description: music turn on/off button"""

    def __init__(self, pos, text, board):
        Button.__init__(self, pos, text, board)

    def on_click(self):
        """Description: method contains action events on button click"""

        if self.board.music:
            self.board.music = False
            self.text = self.font.render("MUSIC OFF", True, game_utils.BLACK)
        else:
            self.board.music = True
            self.text = self.font.render("MUSIC ON", True, game_utils.BLACK)
