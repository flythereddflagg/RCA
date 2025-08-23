import json

import pygame as pg

from .tools import load_yaml, save_yaml
from .camera import Camera
from .node import Node, node_from_dict
from .decal import Decal


class SpriteGroup(pg.sprite.Group):

    def cancel_update(self):
        self.cancel = True

    def update(self, *args, **kwargs):
        """call the update method of every member sprite

        Group.update(*args, **kwargs): return None

        Calls the update method of every member sprite. All arguments that
        were passed to this method are passed to the Sprite update function.

        """
        self.cancel = False
        for sprite in self.sprites():
            if self.cancel:
                break
            sprite.update(*args, **kwargs)



class Scene():  
    def __init__(self, game, yaml_path, yaml_data=None, add_in:list[dict]=None):
        """
        All this must do load the data from a YAML file
        and load each sprite into a group
        """
        self.game = game
        self.id = yaml_path
        
        self.init = yaml_data if yaml_data else load_yaml(yaml_path)

        add_in = add_in if add_in else []
        self.init["nodes"].extend(add_in)
        
        self.draw_layers = self.init["layers"].copy()
        # guarentee background exists
        add_background_blank = False
        if "background" not in self.draw_layers:
            add_background_blank = True
            self.draw_layers.insert(0, "background")
        # guarentee hud exists and is drawn last
        if "hud" not in self.draw_layers:
            self.draw_layers.append('hud') 
        
        self.all_nodes = SpriteGroup()
        self.groups = {
            group_name: pg.sprite.Group()
            for group_name in self.draw_layers
        }
        # since these are guarenteed to exist, provide references to them
        self.background = self.groups["background"]
        self.hud = self.groups["hud"]
        
        # guarentee a blank background sprite if none exists.
        if add_background_blank:
            self.place_node(Decal(self), ["background"])

        for node_init in self.init.get("nodes"):
            node = node_from_dict(self, node_init)
            self.place_node(
                node, 
                node.init.get("groups"), 
                node_init.get('start')
            )


    def place_node(self, node:Node, groups=None, start=None):
        if node.scene is not self:
            node.scene = self
        self.all_nodes.add(node)
        for child in node.children:
            self.place_node(
                child, 
                groups=child.init.get("groups"), 
                start=child.init.get("start")
            )

        sprite_instance:'.decal.Decal' = node.sprite

        if sprite_instance is None: return
        
        if sprite_instance.scene is not self:
            sprite_instance.scene = self

        self.all_nodes.add(sprite_instance)

        if groups:
            for group in groups:
                if group not in self.groups:
                    self.groups[group] = pg.sprite.Group()
                self.groups[group].add(sprite_instance)
        if start:
            sprite_instance.rect.topleft = pg.math.Vector2(start)


    def update(self):        
        self.all_nodes.update()


    def refresh(self):
        # TODO this is all garbage since our last refactor. REWRITE!
        self.camera.zoom_by(0)
        current_player_position = (
            pg.math.Vector2(self.game.player.sprite.rect.topleft) - 
            pg.math.Vector2(self.background.sprites()[0].rect.topleft)
        )
        self.game.load_scene(
            yaml_path=self.id, 
        )
        self.game.init_player(self.game.player)
        
        self.game.player.sprite.rect.topleft = current_player_position
        self.camera.zoom_by(self.game.settings.SCALE * self.init.get('zoom'))


    def deconstruct(self):
        # TODO profile memory usage and destroy scenes?
        serial = self.serialize()
        self.game.saved_scenes[self.id] = serial


    def serialize(self) -> dict:
        """
        Return a serialized dict of the init info to recreate the current scene
        """
        nodes = []
        for node in self.all_nodes:
            if node in [n.parent for n in self.groups["player"]]:
                continue
            if node.parent is not None: continue
            init = node.init
            if init.get("start"):
                assert node.sprite, f"Node {node} is missing its sprite!"
                init["start"] = [int(i) for i in (
                    pg.math.Vector2(node.sprite.rect.topleft) - 
                    pg.math.Vector2(self.background.sprites()[0].rect.topleft)
                )]
            nodes.append(init)
            draw_layers = self.draw_layers.copy()
            draw_layers.remove("hud")

        return {"layers":draw_layers, "nodes": nodes}

        
    
    def get_player(self, player_number:int=0) -> Node:
        """
        Gets a reference to the player number specified.
        Defaults to first player.
        Returns None if specified player does not exist
        in the player group or player group does not exist.
        """
        player_group = self.groups.get("player")
        if not player_group: return None
        player_sprites = player_group.sprites()
        player = (
            player_sprites[player_number]
            if len(player_sprites) > player_number
            else None
        )
        return player
    

    def node_by_id(self, id_str:str) -> '.node.Node':
        return [
            node 
            for node in self.all_nodes.sprites() 
            if node.id == id_str
        ]
    

    def node_ids(self) -> list['.node.Node']:
        return [node.id for node in self.all_nodes.sprites()]
