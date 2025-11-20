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


    def update(self):
        player_rect = self.scene.get_player().sprite.rect
        if (
            self.sprite.rect.colliderect(player_rect) 
            and not self.talking 
            and self.talk_button_pressed()
        ):
            self.talk()
        if self.textbox:
            if (
                not self.textbox.scrolling
                and self.talk_button_pressed()
            ):
                self.stop_talk()
            else:
                # pass
                self.textbox.update()
 

    def talk_button_pressed(self):
        return "BUTTON_W" in self.scene.game.input.new_actions()


    def talk(self):
        self.talking = True
        self.scene.paused = True
        self.textbox = node_from_dict(self.scene, self.text_init)
        self.scene.place_node(
            self.textbox, 
            self.textbox.init.get("groups"), 
            self.textbox.init.get('start')
        )
    

    def stop_talk(self):
        self.textbox.sprite.kill()
        self.textbox = None
        self.scene.paused = False
        self.talking = False

