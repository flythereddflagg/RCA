"""
File     : constants.py
Author   : Mark Redd

Global constants to be used throughtout the game
"""

import pygame as pg
from rca_exception import RCAException


# screen constants
FPS          = 30 # Frame rate ( in Frames / second)
SCREENWIDTH  = 800
SCREENHEIGHT = 600
SCREENSIZE   = (SCREENWIDTH, SCREENHEIGHT) # screen size tuple
CENTERX      = SCREENWIDTH  // 2 # x coordinate for the center of the screen
CENTERY      = SCREENHEIGHT // 2 # y coordinate for the center of the screen

# input constants
NOINPUTINDEX = 300 # index that registers when there is no input

# animation constants
PLAYERSPEEDTIME   = 150 # player speed in pixels / second
PLAYERSPEED  = PLAYERSPEEDTIME // FPS  # Player speed in pixels/frame
PLAYERANIMATERATE = PLAYERSPEEDTIME # image changes per minute
PLAYERANIMATEFRAMES = int(FPS * 60 / PLAYERANIMATERATE) # frames to next player animation
CAMERASLACK  = 100 # pixels before camera moves instead of player
ESLACK       = CENTERX + CAMERASLACK
WSLACK       = CENTERX - CAMERASLACK
NSLACK       = CENTERY - CAMERASLACK
SSLACK       = CENTERY + CAMERASLACK

# direction constants North:0 East:1 South:2 West:3
N,E,S,W      = tuple(range(4))

# colors
BLACK        = (0,0,0)
