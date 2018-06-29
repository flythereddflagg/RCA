"""
File          : rca_sprite.py
Author        : Mark Redd

Abstract Sprite parent to be imported by any sprite in the game.
"""
from pygame.sprite import Sprite

class SpriteRCA(Sprite):
    """
    Interface parent class for all sprites in the game.
    """
    def __init__(self):
        """
        Call the parent class (Sprite) constructor so it can be called from 
        the children.
        """
        super().__init__()
        
