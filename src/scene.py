import json

import pygame as pg

from .tools import load_yaml, class_from_str, filter_serializable
from .camera import Camera
from .node import Node, node_from_dict
from .decal import Decal


class Scene():  
    def __init__(self, game, yaml_path, groups):
        """
        All this must do load the data from a YAML file
        and load each sprite into a group
        """
        self.game = game
        self.id = yaml_path
        self.init = load_yaml(yaml_path)
        
        self.draw_layers = self.init.layers.copy()
        # guarentee background exists
        add_background_blank = False
        if "background" not in self.draw_layers:
            add_background_blank = True
            self.draw_layers.insert(0, "background")
        # guarentee hud exists and is drawn last
        if "hud" not in self.draw_layers:
            self.draw_layers.append('hud') 
        
        self.all_nodes = pg.sprite.Group()
        self.groups = {
            **{
                group_name: pg.sprite.Group()
                for group_name in self.draw_layers
            },
            **{
                group_name: pg.sprite.Group() 
                for group_name in groups
            },
            **{
                group_name: pg.sprite.Group() 
                for group_name, val in self.init.items()
                if isinstance(val, list) and val and isinstance(val[0], dict)
            }
        }
        # since these are guarenteed to exist, provide references to them
        self.background = self.groups["background"]
        self.hud = self.groups["hud"]

        # guarentee a blank background sprite if none exists.
        if add_background_blank:
            self.background.add(Decal(self))    
        self.load()


    def load(self):
        ### adjust scene based on game state (remembers how scenes were)
        adjust_scene = self.id in self.game.saved_scenes
        ###
        for name, group in self.groups.items():
            group_data = self.init.get(name)
            if not group_data: continue

            for node_init in group_data:
                node_id = node_init['id']
                if (
                    adjust_scene and 
                    node_id not in self.game.saved_scenes[self.id][name].keys()
                ): 
                    continue
                    
                node = node_from_dict(self, node_init)
                # TODO code here for new starting place for dropped items (further down the road?)
                self.place_node(
                    node, group, 
                    node.init.get("groups"), node_init.get('start')
                )


    def place_node(
        self, node:Node, group:pg.sprite.Group, groups=None, start=None
    ):
        if node.scene is not self:
            node.scene = self
        self.all_nodes.add(node)
        sprite_instance = node.sprite

        if sprite_instance is None: return
        
        if sprite_instance.scene is not self:
            sprite_instance.scene = self
        self.all_nodes.add(sprite_instance)
        group.add(sprite_instance)

        if groups:
            for group in groups:
                self.groups[group].add(sprite_instance)
        if start:
            sprite_instance.rect.topleft = pg.math.Vector2(start)


    def update(self):        
        self.all_nodes.update()


    def refresh(self):
        self.camera.zoom_by(0)
        current_player_position = (
            pg.math.Vector2(self.game.player.sprite.rect.topleft) - 
            pg.math.Vector2(self.background.sprites()[0].rect.topleft)
        )
        print(current_player_position)
        self.game.load_scene(
            yaml_path=self.id, 
        )
        self.game.init_player(self.game.player)
        
        self.game.player.sprite.rect.topleft = current_player_position
        self.camera.zoom_by(self.game.settings.SCALE * self.init.get('zoom'))


    def deconstruct(self):
        # save the scene as is
        scene_dict = {}
        for name, group in self.groups.items():
            scene_dict[name] = {
                sprite.id:list(sprite.rect.center) 
                for sprite in group.sprites()
            }

        self.game.saved_scenes[self.id] = scene_dict

        # TODO make a save scene and load scene. Will this work?
        # for sprite in self.all_nodes.sprites():
        #     if sprite is self.game.player.sprite: continue
        #     sprite.kill()
        