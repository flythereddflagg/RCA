import json

import pygame as pg

from .tools import load_yaml, class_from_str, filter_serializable
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
    def __init__(
            self, 
            game, 
            yaml_path, 
            groups, 
            add_in:dict=None
        ):
        """
        All this must do load the data from a YAML file
        and load each sprite into a group
        """
        self.game = game
        self.id = yaml_path
        
        self.init = load_yaml(yaml_path)
        add_in = add_in if add_in else {}
        for key, val in add_in.items():
            self.init[key].extend(val)
        
        self.draw_layers = self.init.layers.copy()
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
        for name, group in self.groups.items():
            group_data = self.init.get(name)
            if not group_data: continue

            for node_init in group_data:
                node = node_from_dict(self, node_init)
                self.place_node(
                    node, group, 
                    node.init.get("groups"), node_init.get('start')
                )


    def place_node(
        self, node:Node, draw_layer:pg.sprite.Group=None, 
        groups=None, start=None
    ):
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
       
        # decal to be in ONLY one draw_layer or otherwise not be drawn
        if draw_layer is not None:
            draw_layer.add(sprite_instance)

        # node can exist in other groups though
        if groups:
            for group in groups:
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
        print(current_player_position)
        self.game.load_scene(
            yaml_path=self.id, 
        )
        self.game.init_player(self.game.player)
        
        self.game.player.sprite.rect.topleft = current_player_position
        self.camera.zoom_by(self.game.settings.SCALE * self.init.get('zoom'))


    def deconstruct(self):
        # TODO serialize scene as YAML and save then delete
        # save the scene as is
        serial = self.serialize()


    def serialize(self) -> dict:
        pass
        # TODO CONTINUE HERE ON THE SERIAL STUFF!
        
    
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
