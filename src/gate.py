import pygame as pg

from .decal import Decal

collide_dist = 50**2 # pixels

class Gate(Decal):
    def __init__(self, key_id=None, **kwargs):
        super().__init__(**kwargs)
        self.key_id = key_id

    def update(self):
        player = self.scene.game.player
        dist_sqr = (
            pg.math.Vector2(self.rect.center) - 
            pg.math.Vector2(player.sprite.rect.center)
        ).length_squared()
        if (
            dist_sqr//self.scene.game.SCALE**2 < collide_dist and
            player.inventory.possesed(self.key_id)
        ):
            assert (
                player.inventory.remove_item(self.key_id), 
                "gate key was possesed but did not get removed properly"
            )
            self.kill()
