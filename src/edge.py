import pygame as pg

from .decal import Decal
from .compass import Compass
from .tools import mask_collision


class Edge(Decal):
    """an edge is a sprite that connects two scenes in the map graph"""
    def __init__(self, **init):
        super().__init__(**init)

    def update(self):
        self.check_collision()
    

    def check_collision(self):
        if mask_collision(self, self.scene.groups['player']):
            self.exec_trigger()
    

    def exec_trigger(self):
        old_scene = self.scene
        player = old_scene.get_player()
        print(old_scene.groups["player"].sprites()[0].id)
        print("player", player)
        old_scene.deconstruct() 
        # print("loading", self.init['scene_path'])
        new_scene = old_scene.game.load_scene(
            yaml_path=self.init['scene_path']
        )
        


        new_scene.place_node(player, self.scene.groups["foreground"])

        sprites = new_scene.all_nodes.sprites()
        block = list(filter(lambda x: x.id == self.id, sprites))[0]
        player.sprite.rect.center = block.rect.center
        dx, dy = Compass.unit_vector(block.init['exit_dir'])
        player.sprite.rect.x += dx*(player.sprite.rect.w/2 + block.rect.w/2)
        player.sprite.rect.y += dy*(player.sprite.rect.h/2 + block.rect.h/2)
        # new_scene.camera.center_player()
        
