import pygame as pg

from .decal import Decal
from .node import node_from_dict
from .tools import mask_collision



class Rosie(Decal):
    def setup(self):
        super().setup()
        self.key_id = self.init.get("key_id")
        self.text_init = self.init.get("textbox")
        self.hitmask = Decal(mask_path=self.init.get("image"))
        self.textbox = None
        self.talking = False
        self.debounce_time = 0
        self.debounce_length = 2000 # 2 seconds

    def update(self):

        player_rect = self.scene.get_player().sprite.rect
        if self.sprite.rect.colliderect(player_rect) and not self.talking:
            self.talking = True
            self.talk()
        if self.textbox:
            if (
                not self.textbox.scrolling
                and self.debounce_time != -1
                # and pg.time.get_ticks() - self.debounce_time 
                # > self.debounce_length
            ):
                self.textbox.sprite.kill()
                self.textbox = None
                self.scene.paused = False
                self.debounce_time = pg.time.get_ticks() 
            else:
                self.textbox.update()
                if self.debounce_time == -1: # debounce time not yet set
                    self.debounce_time = pg.time.get_ticks() 
        else:
            if self.talking:
                if (
                    pg.time.get_ticks() 
                    - self.debounce_time 
                    > self.debounce_length
                ):
                    self.talking = False
                    self.debounce_time = -1
    

    def talk(self):
        self.scene.paused = True
        self.textbox = node_from_dict(self.scene, self.text_init)
        self.scene.place_node(
            self.textbox, 
            self.textbox.init.get("groups"), 
            self.textbox.init.get('start')
        )

