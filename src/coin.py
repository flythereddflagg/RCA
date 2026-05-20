import pygame as pg
from .decal import Decal

from .tools import list_collided

class Coin(Decal):
    def setup(self):
        super().setup()
        self.value = self.init.get("value", 1)

    def update(self):
        for player in list_collided(self, self.scene.groups['player']):
            if player.parent: player = player.parent
            if player.inventory:
                new_amount = player.inventory.change_money(self.value)
                if new_amount is None: return # money cannot be added
                self.kill()
            break
