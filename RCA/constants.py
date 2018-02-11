import pygame as pg

FPS          = 30 # Frame rate ( in Frames / second)
SCREENWIDTH  = 800
SCREENHEIGHT = 600
CAMERASLACK  = 100 # pixels before background moves
PLRANIRT     = 10  # (PLAYER ANIMATE RATE) frames to next player animation
CENTERX      = SCREENWIDTH  // 2 # x coordinate for the center of the screen
CENTERY      = SCREENHEIGHT // 2 # y coordinate for the center of the screen
SCRNSIZE     = (SCREENWIDTH, SCREENHEIGHT) # screen size tuple

# direction constants North:0 East:1 South:2 West:3
N,E,S,W      = tuple(range(4))
# colors
BLACK = (0,0,0)