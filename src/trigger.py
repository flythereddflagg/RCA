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
            self, self.scene.groups['player'], 
            # do not kill, use the masks for collision
            False, pg.sprite.collide_mask
        )
        if collided_players:
            print("loading scene")
            self.exec_trigger()
    
    def exec_trigger(self):
        self.scene.load_scene(self.options['scene_path'])
        if "player_start" in self.options.keys():
            startx, starty = self.options['player_start']
            background = self.scene.layers['background'].sprites()[0]
            self.scene.player.rect.x = background.rect.x + startx
            self.scene.player.rect.y = background.rect.y + starty
