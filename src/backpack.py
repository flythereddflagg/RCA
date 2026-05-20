import pygame as pg

from .decal import Decal
from .tools import list_collided
from .node import node_from_dict


class Backpack(Decal):

    def setup(self):
        super().setup()
        self.add_child(node_from_dict(self.scene, {
            "id": "pickup_sfx",
            "type": "SFX",
            "file": "./assets/music/item_jingle.mp3"
        }))

    def update(self):
        self.check_collision()


    def check_collision(self):
        for player in list_collided(self, self.scene.groups['player']):
            if player.parent: player = player.parent
            if player.inventory:
                new_slot = player.inventory.add_slot()
                if new_slot is None: return # no more slots can be added
                self.kill()
                self.pickup_sfx.play()
            break
