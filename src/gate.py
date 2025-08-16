import pygame as pg

from .decal import Decal

collide_dist = 50**2 # pixels

class Gate(Decal):
    def __init__(self, key_id=None, **kwargs):
        super().__init__(**kwargs)
        self.key_id = key_id

    def update(self):
        player = self.scene.get_player()
        if not player:
            return
        dist_sqr = (
            pg.math.Vector2(self.rect.center) - 
            pg.math.Vector2(player.sprite.rect.center)
        ).length_squared()
        print(self.key_id, player.id, player.inventory.contains(self.key_id), player.inventory.left_item, f"id: {type(player), id(player)}", f"id: {type(player.inventory), id(player.inventory)}")
        if (
            dist_sqr < collide_dist and
            player.inventory.contains(self.key_id)
        ):
            assert player.inventory.remove_item(self.key_id),\
                "gate key was contains but did not get removed properly"
            self.kill()
