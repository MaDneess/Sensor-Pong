"""
    Description:
        Commons file is used to store all constant global variables
"""

import pygame
import os

PATH = os.path.join(os.path.dirname(__file__), "resources")

IN_MENU = "MENU"
IN_OPTIONS = "MENU_OPTIONS"
IN_GAME = "GAME"
IN_GAME_WIN_P1 = "WIN_P1"
IN_GAME_WIN_P2 = "WIN_P2"
EXIT = "EXIT"
IN_GAME_CAL = "CAL_GAME"
IN_MENU_CAL = "CAL_MENU"
CAL_MIN = "CAL_MIN"
CAL_MAX = "CAL_CAL"

# SCREEN/BOARD SIZES
B_WIDTH = int(640)
B_HEIGHT = int(480)

FPS = 45

# COLORS RBG
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (26, 140, 255)
DARK_RED = (217, 16, 26)

# FONTS
ARCADE_FONT = os.path.join(PATH, "fonts", "arcade.ttf")

# SOUND EFFECTS
PAD_HIT = os.path.join(PATH, "sounds", "pad_hit.ogg")
BALL_HIT = os.path.join(PATH, "sounds", "ball_hit.ogg")
BALL_SCORED = os.path.join(PATH, "sounds", "ball_scored.ogg")

# BUTTON OPTIONS
BTN_WIDTH = int(B_WIDTH*0.2)
BTN_HEIGHT = int(B_HEIGHT*0.1)
BTN_OFFSET = 15
POS_X = int((B_WIDTH - BTN_WIDTH)/2)
POS_Y = int(B_WIDTH * 0.40)

# BALL OPTIONS
BALL_SIZE = int(B_HEIGHT*.03)
BALL_X = int(B_WIDTH/2)
BALL_Y = int(B_HEIGHT/2)
BALL_SPEED_X = 7
BALL_SPEED_Y = 3
BALL_VELOCITY = 2

# GAME OPTIONS
POINTS = 4

CAGE_WIDTH = 15
OFFSET_WIDTH = 25
OFFSET_HEIGHT = 10

PAD_WIDTH = int(B_WIDTH * 2.5 / 100)
PAD_HEIGHT = int(B_HEIGHT * 40 / 100)
PAD_SPEED = int(B_HEIGHT * 0.5 / 100)

