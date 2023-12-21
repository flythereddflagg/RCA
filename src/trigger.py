import pygame as pg

from .sprite import Block

class Trigger(Block):
    def __init__(self, **options):
        super().__init__(**options)


    def update(self):
        """default behavior is to set up a new scene. Override to change"""
        self.check_collision()
    
    def check_collision(self):
        collided_players = pg.sprite.spritecollide(
            # collide between self and player
            self, self.game.groups['player'], 
            # do not kill, use the masks for collision
            False, pg.sprite.collide_mask
        )
        if collided_players:
            print("loading scene")
            self.exec_trigger()
    
    def exec_trigger(self):
        self.game.load_scene(self.options['scene_path'])
