import pygame as pg

from .tools import load_yaml, class_from_str
from .camera import Camera
from .node import Node


class Scene():  
    def __init__(self, game, yaml_path, groups):
        """
        All this must do load the data from a YAML file
        and load each sprite into a group
        """
        self.game = game
        self.data = load_yaml(yaml_path)
        self.all_sprites = pg.sprite.Group()
        self.groups = {
            group_name: pg.sprite.Group() 
            for group_name in groups
        }
        self.draw_layers = self.data.DRAW_LAYERS.copy()
        self.draw_layers.append('hud') # hud is a given
        self.layers = {
            group_name: pg.sprite.Group() 
            for group_name in self.draw_layers
        }
        
        self.load()
        self.camera = Camera(self)
        self.camera.zoom_by(self.game.SCALE * self.data.get('INIT_ZOOM'))
        # make it so non-sprite nodes get loaded as well in self.load

    @staticmethod
    def node_from_dict(self, node_init:dict):
        node_init['scene'] = self
        yaml = node_init.get("yaml")
        if yaml: node_init = {**node_init, **load_yaml(yaml)}
        class_str = node_init['type']
        node = class_from_str(class_str)(**node_init)
        return node


    def place_node(self, node:Node, layer, groups=None, start=None):
        if node.scene is not self:
            node.scene = self
        sprite_instance = (
            node 
            if isinstance(node, pg.sprite.Sprite) else 
            node.sprite
        )
        if sprite_instance.scene is not self:
            sprite_instance.scene = self
        self.all_sprites.add(sprite_instance)
        layer.add(sprite_instance)

        if groups:
            for group in groups:
                self.groups[group].add(sprite_instance)
        if start:
            sprite_instance.rect.topleft = start


    def load(self):
        for name, layer in self.layers.items():
            layer_data = self.data.get(name)
            if not layer_data: continue

            for node_init in layer_data:
                node = Scene.node_from_dict(self, node_init)
                self.place_node(
                    node, layer, 
                    node_init.get('groups'), node_init.get('start')
                )


    def update(self):        
        # update all sprites
        for group_name in self.draw_layers:
            self.layers[group_name].update()
        
        # finally, update the camera
        if self.camera: self.camera.update()


    def deconstruct(self):
        pass
        # for sprite in self.all_sprites.sprites():
        #     if sprite is self.game.player.sprite: continue
        #     sprite.kill()
        