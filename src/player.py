import pygame as pg
from .sprite import Character



class Player(Character):
    def __init__(self, game, asset_path, **options):
        super().__init__(game, asset_path, **options)

    def update(self):
        pass
    
    def apply_action(self, action):
        if action in self.game.UNIT_VECTORS.keys():
            direction = self.game.UNIT_VECTORS[action]
            self.move(direction, self.game.dist_per_frame)
        else:
            print(action + "! (no response)")
            return
        
        # move rejection for foreground
        foreground = self.game.groups[
            self.game.group_enum['foreground']
        ]

        for _ in range(sum(self.image.get_rect().size)):
            if not pg.sprite.spritecollide(
                self, foreground,
                False,
                pg.sprite.collide_mask
            ): break
            self.move(direction, -1)

