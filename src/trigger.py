import pygame as pg

from .sprite import Block
from .compass import Compass

class Trigger(Block):
    def __init__(self, **options):
        super().__init__(**options)
# TODO set this up so that that an exit puts the player somewhere in particular

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
        self.scene.game.load_scene(self.options['scene_path'])
        new_scene = self.scene.game.scene
        print(new_scene.data.id)
        background = new_scene.layers['background'].sprites()[0]
        sprites = new_scene.layers['characters'].sprites()
        print([s.id for s in sprites])
        block = list(filter(lambda x: x.id == self.id, sprites))[0]
        startx, starty = block.rect.x, block.rect.y
        player = new_scene.player
        player.rect.x = background.rect.x + startx
        player.rect.y = background.rect.y + starty
        dx, dy = Compass.vec_map[block.options['exit_dir']]
        player.rect.x += dx*(player.rect.w + block.rect.w)
        player.rect.y += dy*(player.rect.h + block.rect.w)
        print(player.rect.center)
