import pygame as pg

from .decal import Decal
from .compass import Compass

class Edge(Decal):
    """an edge is a sprite that connects two scenes in the map graph"""
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
        # save everything we want to carry into the next scene
        player = self.scene.player
        game = self.scene.game
        new_scene = self.scene.load_scene(game, self.options['scene_path'])
        new_scene.player = player
        player.scene = new_scene
        new_scene.layers['characters'].add(player)
        new_scene.groups['player'].add(player)
        sprites = new_scene.layers['characters'].sprites()
        block = list(filter(lambda x: x.id == self.id, sprites))[0]
        print(block.id, block.scene.data['id'])
        print(player.rect.center)
        player.rect.center = block.rect.center
        dx, dy = Compass.vec_map[block.options['exit_dir']]
        player.rect.x += dx*(player.rect.w/2 + block.rect.w/2)
        player.rect.y += dy*(player.rect.h/2 + block.rect.h/2)
        print(player.rect.center)
