"""
    Name: back_button.py
    Author: Aleksej Z
    Date: 2018/08/18
"""
import game_utils
from button import Button


class BackButton(Button):
    """Description: options back button"""

    def __init__(self, pos, text, board):
        Button.__init__(self, pos, text, board)

    def on_click(self):
        """Description: method contains action events on button click"""

        if self.board.state == game_utils.IN_OPTIONS:
            self.board.state = game_utils.IN_MENU
