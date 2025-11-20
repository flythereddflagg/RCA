import pygame as pg

from .decal import Decal
from .node import node_from_dict
from .tools import mask_collision, vec



class Rosie(Decal):
    def setup(self):
        super().setup()
        self.key_id = self.init.get("key_id")
        self.text_init = self.init.get("textbox")
        self.hitmask = Decal(mask_path=self.init.get("image"))
        self.textbox = None
        self.talking = False
        self.button_cue = node_from_dict(self.scene, 
            {
                "id": "cue",
                "type": "Decal",
                "image": "./assets/block/glyph_B.png"
            }
        )
        self.cue_placement = (
            vec(self.scene.game.draw_surface.get_size()).elementwise()
            * vec([0.5, 1]) 
            - vec(self.button_cue.sprite.rect.size).elementwise()
            * vec([0.5, 1])
        )


    def update(self):
        
        player_rect = self.scene.get_player().sprite.rect
        if (
            self.sprite.rect.colliderect(player_rect) 
            and not self.talking 
            
        ):
            self.scene.place_node(
                self.button_cue, 
                ["hud"],
                self.cue_placement
            )
    
            if self.talk_button_pressed():
                self.talk()
        else:
            self.button_cue.kill()
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
        return "BUTTON_E" in self.scene.game.input.new_actions()


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

