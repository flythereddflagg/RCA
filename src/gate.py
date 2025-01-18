import pygame as pg

from .decal import Decal

collide_dist = 50**2 # pixels

class Gate(Decal):
    def update(self):
        player = self.scene.game.player
        dist_sqr = (
            pg.math.Vector2(self.rect.center) - 
            pg.math.Vector2(player.sprite.rect.center)
        ).length_squared()
        if (
            dist_sqr//self.scene.game.SCALE**2 < collide_dist and
            player.inventory.possesed("gate key")
        ):
            assert (
                player.inventory.remove_item("gate key"), 
                "gate key was possesed but did not get removed properly"
            )
            self.kill()
