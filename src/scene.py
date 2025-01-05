import json

import pygame as pg

from .tools import load_yaml, class_from_str, filter_serializable
from .camera import Camera
from .node import Node


class Scene():  
    def __init__(self, game, yaml_path, groups):
        """
        All this must do load the data from a YAML file
        and load each sprite into a group
        """
        self.game = game
        self.id = yaml_path
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
            sprite_instance.rect.topleft = pg.math.Vector2(start)


    def load(self):
        ### adjust scene based on game state (remembers how scenes were)
        adjust_scene = self.id in self.game.saved_scenes
        ###
        for name, layer in self.layers.items():
            layer_data = self.data.get(name)
            if not layer_data: continue

            for node_init in layer_data:
                node_id = node_init['id']
                if (
                    adjust_scene and 
                    node_id not in self.game.saved_scenes[self.id][name].keys()
                ): 
                    continue
                node = Scene.node_from_dict(self, node_init)
                # TODO code here for new starting place for dropped items (further down the road?)
                self.place_node(
                    node, layer, 
                    node.options.get("groups"), node_init.get('start')
                )

    def refresh(self):
        self.camera.zoom_by(0)
        current_player_position = (
            pg.math.Vector2(self.game.player.sprite.rect.topleft) - 
            pg.math.Vector2(self.layers['background'].sprites()[0].rect.topleft)
        )
        print(current_player_position)
        self.game.load_scene(
            yaml_path=self.id, 
            player=self.game.player
        )
        
        self.game.player.sprite.rect.topleft = current_player_position
        self.camera.zoom_by(self.game.SCALE * self.data.get('INIT_ZOOM'))


    def update(self):        
        # update all sprites
        for group_name in self.draw_layers:
            self.layers[group_name].update()
        
        # finally, update the camera
        if self.camera: self.camera.update()


    def deconstruct(self):
        # save the scene as is
        scene_dict = {}
        for layer, group in self.layers.items():
            scene_dict[layer] = {
                sprite.id:list(sprite.rect.center) 
                for sprite in group.sprites()
            }

        self.game.saved_scenes[self.id] = scene_dict

        # TODO make a save scene and load scene. Will this work?
        # for sprite in self.all_sprites.sprites():
        #     if sprite is self.game.player.sprite: continue
        #     sprite.kill()
        