"""
File     : constants.py
Author   : Mark Redd

Global constants to be used throughout the game
"""
import pygame as pg
# Screen Constants
#   Frame rate ( in Frames / second)
FPS          = 30 
SCREENWIDTH  = 800
SCREENHEIGHT = 600
#   screen size tuple
SCREENSIZE   = (SCREENWIDTH, SCREENHEIGHT)
#   x and y coordinates for the center of the screen
CENTERX      = SCREENWIDTH  // 2 
CENTERY      = SCREENHEIGHT // 2 

# Animation Constants
#   player speed in pixels / second
PLAYERSPEEDTIME     = 300 * 2
#    Player speed in pixels/frame
PLAYERSPEED         = PLAYERSPEEDTIME // FPS
#    image changes per minute
PLAYERANIMATERATE   = PLAYERSPEEDTIME 

#   frames to next player animation
PLAYERANIMATEFRAMES = int(FPS * 60 / PLAYERANIMATERATE)

# pixels before camera moves instead of player
CAMERASLACK         = 100 
NSLACK              = CENTERY - CAMERASLACK
SSLACK              = CENTERY + CAMERASLACK
ESLACK              = CENTERX + CAMERASLACK
WSLACK              = CENTERX - CAMERASLACK

# direction constants North:0 East:1 South:2 West:3
DIRECTIONS      = tuple(range(4))
N,E,S,W         = DIRECTIONS
DIRECTION_DICT  = {"north": N, "east" : E, "south" : S, "west" : W}

# colors
BLACK           = (0,0,0)

DATAPATH        = "./data/{}.json"
