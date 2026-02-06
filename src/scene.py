import traceback
import json

import pygame as pg

from .tools import load_yaml, save_yaml, vec
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
        # print("new frame")
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
        self.paused = False
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
        self.occupied = False # is the scene occupied by an entity?


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

        # groups ONLY get applied to the sprite UNLESS there is no sprite
        if sprite_instance is None: 
            if groups:
                for group in groups:
                    if group not in self.groups:
                        self.groups[group] = pg.sprite.Group()
                    self.groups[group].add(node)
            return
        
        if sprite_instance.scene is not self:
            sprite_instance.scene = self

        self.all_nodes.add(sprite_instance)

        if groups:
            for group in groups:
                if group not in self.groups:
                    self.groups[group] = pg.sprite.Group()
                self.groups[group].add(sprite_instance)
        if start:
            sprite_instance.rect.topleft = vec(start)


    def update(self):
        if self.paused:
            pause_group = self.groups.get("paused")
            if pause_group:
                pause_group.update()
            return

        self.all_nodes.update()


    def refresh(self):
        """
        Reset the scene by reloading from the yaml but keep the
        player's postion
        """
        try:
            player_sprite = self.get_player()
            if player_sprite:
                player = player_sprite.sprite.parent
                current_player_position = list(
                    vec(player.sprite.rect.topleft) - 
                    vec(self.background.sprites()[0].rect.topleft)
                )
                player.init["start"] = current_player_position
                add_in = [player.init]
            else:
                add_in = []
            self.game.saved_scenes.pop(self.id, None)
            self.game.load_scene(yaml_path=self.id, add_in=add_in)
        except Exception as e:
            print("\n\n-- ON REFRESH: EXCEPTION OCCURED -- \n\n")
            print(traceback.format_exc())
            print(type(e), e)
            print("\n\n-- DROPPING INTO DEBUG MODE -- \n--'c' to retry -- \n\n")
            breakpoint()
            self.refresh()


    def deconstruct(self, save_scene=True):
        if save_scene:
            self.game.saved_scenes[self.id] = self.serialize()

        for node in self.all_nodes:
            node.deconstruct()
            self.all_nodes.remove(node)
        
        self.all_nodes.cancel_update()
        
        for name, group in self.groups.items():
            for sprite in group:
                group.remove(sprite)
        

    def serialize(self) -> dict:
        """
        Return a serialized dict of the init info to recreate the current scene
        """
        nodes = []
        for node in self.all_nodes:
            if (
                "player" in self.groups and 
                node in [n.parent for n in self.groups["player"]]
            ):
                continue
            if node.parent is not None: continue
            init = node.init
            if not init: continue # this may caus bugs
            if init.get("start"):
                assert node.sprite, f"Node {node} is missing its sprite!"
                init["start"] = [int(i) for i in (
                    vec(node.sprite.rect.topleft) - 
                    vec(self.background.sprites()[0].rect.topleft)
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

    def node_in_groups(self, node:'.node.Node') -> list[str]:
        """
        returns the names of the groups in this scene which contain the node.
        """
        return [name for name, group in self.groups.items() if node in group]

