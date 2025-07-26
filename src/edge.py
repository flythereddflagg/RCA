import pygame as pg

from .decal import Decal
from .compass import Compass
from .tools import mask_collision


class Edge(Decal):
    """an edge is a sprite that connects two scenes in the map graph"""
    def __init__(self, **init):
        super().__init__(**init)

    def update(self):
        if mask_collision(self, self.scene.groups['player']):
            self.exec_trigger()
        
    

    def exec_trigger(self):
        player_sprite = self.scene.get_player()
        player = player_sprite.parent
        game = self.scene.game
        player_layer = [
            grp
            for grp in self.scene.draw_layers 
            if player_sprite in self.scene.groups[grp]
        ][0]
        # self.scene.deconstruct()
        # for sprite in self.scene.all_nodes:
        #     sprite.kill()
        new_scene = game.load_scene(
            yaml_path=self.init["scene_path"]
        )

        out_block = new_scene.node_by_id(self.id)[0]
        half_size = (
            pg.math.Vector2(player.sprite.rect.size) / 2 +
            pg.math.Vector2(out_block.sprite.rect.size) / 2
        )
        start_pos = (
            pg.math.Vector2(out_block.sprite.rect.topleft) + 
            half_size.elementwise() * 
            Compass.unit_vector(out_block.init["exit_dir"])
        )
        bg_pos = pg.math.Vector2(
            new_scene.background.sprites()[0].sprite.rect.topleft
        )
        print(start_pos - bg_pos, out_block.sprite.rect.topleft - bg_pos, Compass.unit_vector(out_block.init["exit_dir"]), half_size)
        new_scene.place_node(
            player, new_scene.groups[player_layer], 
            player.init.get("groups"), start=start_pos
        )
        self.scene.all_nodes.cancel_update()
        print("Completed edge loading")