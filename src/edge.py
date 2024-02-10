import pygame as pg

from .decal import Decal
from .compass import Compass

class Edge(Decal):
    """an edge is a sprite that connects two scenes in the map graph"""
    def __init__(self, **options):
        super().__init__(**options)

    def update(self):
        self.check_collision()
    

    def check_collision(self):
        if pg.sprite.spritecollideany(
            # collide between self and player
            self, self.scene.groups['player'], 
            # do not kill, use the masks for collision
            pg.sprite.collide_mask
            # psudo_collide_mask
        ):
            self.exec_trigger()
    

    def exec_trigger(self):
        # save everything we want to carry into the next scene
        game = self.scene.game
        player = self.scene.player
        new_scene = game.load_scene(self.scene, self.options['scene_path'])
        player.scene = new_scene
        new_scene.player = player
        new_scene.camera.player = player
        new_scene.layers['foreground'].add(player)
        new_scene.groups['player'].add(player)
        sprites = new_scene.layers['foreground'].sprites()
        block = list(filter(lambda x: x.id == self.id, sprites))[0]
        # print(block.id, block.scene.data['id'], block.rect.center)
        # print("cur pos", player.rect.center)
        player.rect.center = block.rect.center
        # print("mid", player.rect.center)
        dx, dy = Compass.unit_vector(block.options['exit_dir'])
        player.rect.x += dx*(player.rect.w/2 + block.rect.w/2)
        player.rect.y += dy*(player.rect.h/2 + block.rect.h/2)
        # print("after pos", player.rect.center)
        new_scene.camera.center_player()
        # print("after after pos", player.rect.center)
