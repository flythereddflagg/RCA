import pygame as pg

from .decal import Decal
from .tools import list_collided

class Cactus(Decal):
    def __init__(self, **init):
        super().__init__(**init)

    def update(self):
        self.check_collision()


    def check_collision(self):
        for player in list_collided(self, self.scene.groups['player']):
            if player.parent: player = player.parent
            if (player.animation and\
                player.state == 'damage' and\
                player.animation.active
            ): continue

            damage_direction = (
                pg.math.Vector2(player.sprite.rect.center) -
                pg.math.Vector2(self.rect.center)
            ).normalize()
            player.signal([
                'damage', 10, damage_direction
            ])
            
