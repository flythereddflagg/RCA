import pygame as pg

from .decal import Decal
from .tools import list_collided, diff_vec

class Cactus(Decal):

    def update(self):
        self.check_collision()


    def check_collision(self):
        hurt_sprites = [
            getattr(sprite, "hurtmask", sprite.sprite).sprite
            for sprite in self.scene.groups['player']
        ]
        for player in list_collided(self, hurt_sprites):
            if player.parent: player = player.parent
            if (player.animation and\
                player.state == 'damage' and\
                player.animation.active
            ): continue
            damage_direction = diff_vec(
                 player.sprite.rect.center,self.sprite.rect.center
            ).normalize()
            player.signal([
                'damage', 1, damage_direction
            ])
            
