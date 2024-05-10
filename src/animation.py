import operator
import itertools

import pygame as pg

class Animation():
    """
    A system for setting the parent sprite object's image.
    """
    def __init__(self, sprite:pg.sprite.Sprite, ):
        self.sprite = sprite
        self.current = None
        self.previous = None
        self.data = None
        self.active = False
        self.load_animations()


    def load_animations(self) -> None:
        pass
    

    def update(self) -> None:
        pass


    def set_action(self, action:str) -> None:
        """Sets the current animation action and direction"""
        pass


    def cancel(self) -> None:
        """Force cancels the animation back to the previous one"""
        pass