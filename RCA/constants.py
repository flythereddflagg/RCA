import pygame as pg
from rca_exception import RCAException

"""
Global constants to be used throughtout the game
"""

# screen constants
FPS          = 30 # Frame rate ( in Frames / second)
SCREENWIDTH  = 800
SCREENHEIGHT = 600
SCREENSIZE   = (SCREENWIDTH, SCREENHEIGHT) # screen size tuple
CENTERX      = SCREENWIDTH  // 2 # x coordinate for the center of the screen
CENTERY      = SCREENHEIGHT // 2 # y coordinate for the center of the screen
CAMERASLACK  = 100 # pixels before camera moves instead of player
ESLACK       = CENTERX + CAMERASLACK
WSLACK       = CENTERX - CAMERASLACK
NSLACK       = CENTERY - CAMERASLACK
SSLACK       = CENTERY + CAMERASLACK

# input constants
NOINPUTINDEX = 300 # index that registers when there is no input

# animation constants
PLRANIRT     = 10  # (PLAYER ANIMATE RATE) frames to next player animation
PLAYERSPEED  = 5   # Player speed in pixels/frame

# direction constants North:0 East:1 South:2 West:3
N,E,S,W      = tuple(range(4))

# colors
BLACK        = (0,0,0)

