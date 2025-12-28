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
        self.cue_placement = (
            vec(self.scene.game.draw_surface.get_size()).elementwise()
            * vec([0.5, 1]) 
            - vec(self.button_cue.sprite.rect.size).elementwise()
            * vec([0.5, 1])
        )
        self.cue_text.set_text(self.cue_text.init.get("text", ""))
        self.leave_text = """
Pickles? For me? I Just LOVE Pickles! I can snack on 
them before bed time and then I can use the pickle 
juice to make a soup!
...In Fact, I am going to do that right now!
NOW! You listen to me Robbie Hart, you're going to be 
a fine husband!
"""     

        


    def update(self):
        
        player = self.scene.get_player().parent
        player_rect = player.sprite.rect
        if (
            self.sprite.rect.colliderect(player_rect) 
            and not self.talking 
        ):
            # signal that talking is available
            self.scene.place_node(
                self.button_cue, ["hud"], self.cue_placement
            )
            self.scene.place_node(
                self.cue_text, ["hud"],
            )
            self.cue_text.sprite.rect.midleft = (
                self.button_cue.sprite.rect.midright
            )

            # start the talking
            if self.talk_button_pressed():
                if player.inventory.contains(self.key_id):
                    assert player.inventory.remove_item(self.key_id),\
                        "gate key was possesed but did not get removed properly"
                    self.talk(self.leave_text)
                    self.kill_after = True
                else:
                    self.talk()
        else:
            self.button_cue.kill()
            self.cue_text.sprite.kill()

        if self.textbox:
            if not self.textbox.scrolling:
                self.talking_head.state = "Silent"
            if (
                not self.textbox.scrolling
                and self.talk_button_pressed()
            ):
                self.stop_talk()
            else:
                self.textbox.update()
                self.talking_head.animation.update()
 

    def talk_button_pressed(self):
        return "BUTTON_E" in self.scene.game.input.new_actions()


    def talk(self, alt_text:str=None):
        self.talking = True
        self.scene.paused = True
        self.scene.place_node(
            self.textbox, ["hud"], 
            self.textbox.init.get('start')
        )
        self.scene.place_node(self.talking_head,["hud"])
        self.talking_head.sprite.rect.topright = (
            self.textbox.sprite.rect.topleft
        )
        self.talking_head.sprite.state = "Talking"
        if alt_text is not None:
            self.textbox.scroll_text(alt_text)
        else:
            self.textbox.scroll_text(self.textbox.init.get("text", ""))

    

    def stop_talk(self):
        self.textbox.sprite.kill()
        self.textbox.kill()
        self.talking_head.kill()
        self.scene.paused = False
        self.talking = False
        if self.kill_after:
            self.sprite.kill()
            self.kill()
