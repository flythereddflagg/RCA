import pygame as pg

from .decal import Decal
from .tools import diff_vec, mask_collision

collide_dist = 50**2 # pixels

class Gate(Decal):
    def setup(self):
        super().setup()
        self.key_id = self.init.get("key_id")

    def update(self):
        # tack all sprite to self
        # for child in self.children:
        #     if not child.sprite:
        #         continue
        #     child.sprite.rect.topleft = self.rect.topleft
        player_sprite = self.scene.get_player()
        if not player_sprite:
            return
        player = (
            player_sprite 
            if not player_sprite.parent 
            else player_sprite.parent
        )
        if self.child_by_id("hitmask"):
            if (
                mask_collision(self.hitmask, player_sprite) and
                player.inventory.contains(self.key_id)
            ):
                assert player.inventory.remove_item(self.key_id),\
                    "gate key was contains but did not get removed properly"
                self.gate_fx.play()
                self.kill()
            return

        dist_sqr = diff_vec(
            player.sprite.rect.center, self.rect.center
        ).length_squared()

        if (
            dist_sqr < collide_dist and
            player.inventory.contains(self.key_id)
        ):
            assert player.inventory.remove_item(self.key_id),\
                "gate key was contains but did not get removed properly"
            self.gate_fx.play()
            self.kill()

