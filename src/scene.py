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
        self.layers = {
            group_name: pg.sprite.Group() 
            for group_name in self.data.DRAW_LAYERS
        }
        self.layers['hud'] = pg.sprite.Group() # hud is a given
        
        self.load()
        self.camera = Camera(self)
        self.camera.zoom_by(self.game.SCALE * self.data.get('INIT_ZOOM'))
        # make it so non-sprite nodes get loaded as well in self.load


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
        self.all_sprites.add(sprite_instance)
        layer.add(sprite_instance)

        if groups:
            for group in groups:
                self.groups[group].add(sprite_instance)
        if start:
            sprite_instance.rect.center = start


    def load(self):
        for name, layer in self.layers.items():
            layer_data = self.data.get(name)
            if not layer_data: continue

            for node_init in layer_data:
                node = self.node_from_dict(node_init)
                self.place_node(
                    node, layer, 
                    node_init.get('groups'), node_init.get('start')
                )


    def update(self):        
        # update all sprites
        for group_name in self.data.DRAW_LAYERS:
            self.layers[group_name].update()
        
        # finally, update the camera
        if self.camera: self.camera.update()


    def load_player(self, player_init) -> Node:
        if not player_init: return None

        if isinstance(player_init, str) and player_init.endswith(".yaml"):
            player_data = load_yaml(player_init)
            player_data['scene'] = self
            player = (
                class_from_str(player_data['type'])(**player_data)
            )
            sprite_instance = (
                player 
                if isinstance(player, pg.sprite.Sprite) else 
                player.sprite
            )
            # groups = player_data.get('groups')
            # if groups:
            #     for group in groups:
            #         self.groups[group].add(sprite_instance)
            
            start = player_data.get('start')
            if start:
                sprite_instance.rect.center = start
            self.layers['foreground'].add(player.sprite)
            self.groups['player'].add(player.sprite)

        # elif isinstance(player_init, Node):
        #     player = player_init
        #     player.sprite.scale_by(0) # FIXME should this work?
        #     player.scene = self
        #     self.layers['foreground'].add(player.sprite)
        #     self.groups['player'].add(player.sprite)
        else:
            raise TypeError(
                f"Player {player_init} is of Type {type(player_init)}! Should be str or Node"
            )

        player.sprite.add(self.all_sprites)
        return player

    def deconstruct(self):
        pass
        # for sprite in self.all_sprites.sprites():
        #     if sprite is self.game.player.sprite: continue
        #     sprite.kill()
        