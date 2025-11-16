import pygame as pg

from .decal import Decal
from .node import node_from_dict
from .tools import mask_collision



class Rosie(Decal):
    def setup(self):
        super().setup()
        self.key_id = self.init.get("key_id")
        self.text_init = self.init.get("textbox")
        self.textbox = None
        self.talking = False

    def update(self):
        player_sprite = self.scene.get_player().sprite
        if mask_collision(self.sprite, player_sprite) and not self.talking:
            self.talking = True
            self.talk()
        if self.textbox:
            if not self.textbox.scrolling:
                self.textbox.sprite.kill()
                self.textbox = None
                self.scene.paused = False
            else:
                self.textbox.update()
        else:
            if self.talking:
                self.talking = False
    

    def talk(self):
        self.scene.paused = True
        self.textbox = node_from_dict(self.scene, self.text_init)
        self.scene.place_node(
            self.textbox, 
            self.textbox.init.get("groups"), 
            self.textbox.init.get('start')
        )

