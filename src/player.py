import pygame as pg
from .sprite import Character



class Player(Character):
    def __init__(self, game, asset_path, startx, starty, **options):
        super().__init__(game, asset_path, startx, starty, **options)

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

        if pg.sprite.spritecollide(
                self, foreground,
                False,
                pg.sprite.collide_mask
        ):
            jump_dist = int(self.game.dist_per_frame)
            while jump_dist:
                if pg.sprite.spritecollide(
                    self, foreground,
                    False,
                    pg.sprite.collide_mask
                ): 
                    self.move(direction, -jump_dist)
                else:
                    self.move(direction, jump_dist)
                
                jump_dist = jump_dist // 2
            
            while pg.sprite.spritecollide(
                self, foreground,
                False,
                pg.sprite.collide_mask
            ):
                self.move(direction, -1)


