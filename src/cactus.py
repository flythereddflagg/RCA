import pygame as pg

from .decal import Decal
from .tools import list_collided

class Cactus(Decal):
    def __init__(self, **options):
        super().__init__(**options)

    def update(self):
        self.check_collision()
        # self.animate() # TODO add shadow and floating animation?


    def check_collision(self):
        for player in list_collided(self, self.scene.groups['player']):
            if (player.animation and\
                player.animation.current['id'] == 'damage' and\
                player.animation.active
            ): continue

            damage_direction = (
                pg.math.Vector2(player.rect.center) -
                pg.math.Vector2(self.rect.center)
            ).normalize()
            player.signal([
                'damage', 10, damage_direction
            ])
            
