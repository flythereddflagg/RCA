import random

import pygame as pg

from .decal import Decal
from .tools import list_collided

throw_dist = 32 # pixels

class SoftDirt(Decal):

    def __init__(self, treasure=None, **kwargs):
        super().__init__(**kwargs)
        self.treasure = treasure # list of treasures given by the dirt

    def update(self):
        for sprite in list_collided(self, self.scene.groups["player"]):
            state = sprite.parent.state if sprite.parent else sprite.state
            if state == "shovel":
                return self.be_dug(sprite)



    def be_dug(self, sprite):
        # I assume that any sprite that has a "shovel" state 
        # should probably have a parent. Maybe not though?
        layer = [layer for key, layer in self.scene.layers.items() if self in layer][0]
        for item in self.treasure:
            start_vector = (
                pg.math.Vector2(item["start"])
                # pg.math.Vector2([random.random(), random.random()]) * 
                # throw_dist + 
                # # throw it up and to the left 32 pixels
                # pg.math.Vector2([-throw_dist,-throw_dist]) 
            ) + sprite.rect.topleft
            node = self.scene.node_from_dict(self.scene, item)
            groups = self.options.get("groups")
            self.scene.place_node(
                node, layer, groups=groups, start=start_vector
            )
        self.kill()


            
