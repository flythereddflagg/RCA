import pygame as pg

from .decal import Decal
from .compass import Compass
from .tools import mask_collision


class Edge(Decal):
    """an edge is a sprite that connects two scenes in the map graph"""
    def __init__(self, **init):
        super().__init__(**init)

    def update(self):
        if mask_collision(self, self.scene.groups['player']):
            self.exec_trigger()
        
    

    def exec_trigger(self):
        pass
        
