import pygame as pg

from .decal import Decal
from .node import node_from_dict
from .tools import mask_collision, vec



class Rosie(Decal):
    def setup(self):
        super().setup()
        self.key_id = self.init.get("key_id")
        self.hitmask = Decal(mask_path=self.init.get("image"))
        self.talking = False
        self.kill_after = False
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
        self.leave_text = """
I Just LOVE Pickles! I can snack on them before bed time
and then I can use the pickle juice to make a soup!
...In Fact, I am going to do that right now!
NOW! You listen to me Robbie Hart, you're going to be 
a fine husband!
"""
        self.stop_talk()


    def update(self):
        
        player = self.scene.get_player().parent
        player_rect = player.sprite.rect
        if (
            self.sprite.rect.colliderect(player_rect) 
            and not self.talking 
            
        ):
            self.scene.place_node(self.button_cue, ["hud"], self.cue_placement)
    
            if self.talk_button_pressed():
                if player.inventory.contains(self.key_id):
                    assert player.inventory.remove_item(self.key_id),\
                        "gate key was contains but did not get removed properly"
                    self.talk(self.leave_text)
                    self.kill_after = True
                else:
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
                # self.children.update()
                print("updating 1")
                self.textbox.update()
                self.talking_head.animation.update()
 

    def talk_button_pressed(self):
        return "BUTTON_E" in self.scene.game.input.new_actions()


    def talk(self, alt_text:str=None):
        self.talking = True
        self.scene.paused = True
        self.scene.place_node(
            self.textbox, 
            self.textbox.init.get("groups"), 
            self.textbox.init.get('start')
        )
        self.scene.place_node(
            self.talking_head,
            self.talking_head.init.get("groups")
        )
        self.talking_head.sprite.rect.topright = (
            self.textbox.sprite.rect.topleft
        )
        if alt_text is not None:
            self.textbox.scroll_text(alt_text)
        else:
            self.textbox.scroll_text(self.textbox.init.get("text", ""))

    

    def stop_talk(self):
        self.textbox.sprite.kill()
        self.textbox.kill()
        self.talking_head.sprite.kill()
        self.talking_head.kill()
        self.scene.paused = False
        self.talking = False
        if self.kill_after:
            self.sprite.kill()
            self.kill()
