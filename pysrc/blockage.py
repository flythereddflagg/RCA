from .decal import Decal
from .tools import list_collided, diff_vec

class Blockage(Decal):

    def update(self):
        self.check_collision()


    def check_collision(self):
        hurt_sprites = [
            getattr(sprite, "hurtmask", sprite.sprite).sprite
            for sprite in self.scene.groups['player']
        ]
        for player in list_collided(self.sprite, hurt_sprites):
            if player.parent: player = player.parent
            damage_direction = diff_vec(
                 player.sprite.rect.center,self.sprite.rect.center
            ).normalize()
            player.signal([
                'damage', 1, damage_direction
            ])
            self.animation.set_state("squirm")