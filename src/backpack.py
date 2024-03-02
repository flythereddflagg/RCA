import pygame as pg

from .decal import Decal
from .tools import list_collided

class Backpack(Decal):
    def __init__(self, **options):
        super().__init__(**options)

    def update(self):
        self.check_collision()
        # self.animate() # TODO add shadow and floating animation?


    def check_collision(self):
        for player in list_collided(self, self.scene.groups['player']):
            if player.inventory:
                new_slot = player.inventory.add_slot()
                if new_slot is None: return # no more slots can be added
                self.kill()
            break
