import pygame as pg

from .decal import Decal

class Backpack(Decal):
    def __init__(self, **options):
        super().__init__(**options)

    def update(self):
        self.check_collision()
        # self.animate() # TODO add shadow and floating animation?


    def check_collision(self):

        assert isinstance(self.mask, pg.mask.Mask), \
            f"{self.id} has invlaid mask: {self.mask}"
        for sprite in self.scene.groups['player'].sprites():
            assert isinstance(sprite.mask, pg.mask.Mask), \
                f"{sprite.id} has invalid mask: {sprite.mask}"

        collided_players = pg.sprite.spritecollide(
            # collide between self and player
            self, self.scene.groups['player'], 
            # do not kill, use the masks for collision
            False, pg.sprite.collide_mask
        )
        if collided_players is not None:
            for player in collided_players:
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
                
