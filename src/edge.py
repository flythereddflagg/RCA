import pygame as pg

from .decal import Decal
from .compass import Compass
from .tools import list_collided, vec


class Edge(Decal):
    """an edge is a sprite that connects two scenes in the map graph"""

    def update(self):
        if list_collided(self, self.scene.groups['player']):
            self.exec_trigger()
        

    def exec_trigger(self):
        player_sprite = self.scene.get_player()
        player = player_sprite.parent
        game = self.scene.game
        self.scene.deconstruct()
        new_scene = game.load_scene(
            yaml_path=self.init["scene_path"]
        )
        out_block = new_scene.node_by_id(self.id)[0]
        half_size = (
            vec(player.sprite.rect.size) / 2 +
            vec(out_block.sprite.rect.size) / 2
        )
        start_pos = (
            vec(out_block.sprite.rect.topleft) + 
            half_size.elementwise() * 
            Compass.unit_vector(out_block.init["exit_dir"])
        )
        bg_pos = vec(
            new_scene.background.sprites()[0].sprite.rect.topleft
        )
        new_scene.place_node(
            player, 
            player.init.get("groups"), start=start_pos
        )
