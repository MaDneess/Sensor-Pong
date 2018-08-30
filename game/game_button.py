"""
    Name: game_button.py
    Author: Aleksej Z
    Date: 2018/08/18
"""
import game_utils
from game.button import Button


class GameButton(Button):
    """Description: start game button"""

    def __init__(self, pos, text, board):
        Button.__init__(self, pos, text, board)

    def on_click(self):
        """Description: method contains action events on button click"""
        self.board.state = game_utils.IN_GAME_CAL
