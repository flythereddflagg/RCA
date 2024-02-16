import pygame as pg

from .decal import Decal
from .compass import Compass
from .tools import mask_collision


class Edge(Decal):
    """an edge is a sprite that connects two scenes in the map graph"""
    def __init__(self, **options):
        super().__init__(**options)

    def update(self):
        self.check_collision()
    

    def check_collision(self):
        if mask_collision(self, self.scene.groups['player']):
            self.exec_trigger()
    

    def exec_trigger(self):
        old_scene = self.scene
        game = self.scene.game
        player = self.scene.player
        player.set_scale(0) # reset player scale
        # FIXME player zoom stays in the previous scene's zoom
        
        new_scene = game.load_scene(self.scene, self.options['scene_path'])
        player.scene = new_scene
        player.set_scale(new_scene.data.INIT_ZOOM)
        player.animation.previous = '' # force player to update image
        new_scene.player = player
        new_scene.camera.player = player
        new_scene.layers['foreground'].add(player)
        new_scene.groups['player'].add(player)
        sprites = new_scene.layers['foreground'].sprites()
        block = list(filter(lambda x: x.id == self.id, sprites))[0]
        player.rect.center = block.rect.center
        dx, dy = Compass.unit_vector(block.options['exit_dir'])
        player.rect.x += dx*(player.rect.w/2 + block.rect.w/2)
        player.rect.y += dy*(player.rect.h/2 + block.rect.h/2)
        new_scene.camera.center_player()
        old_scene.kill() 
