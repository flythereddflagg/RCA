import pygame as pg

from .decal import Decal
from .node import node_from_dict
from .tools import mask_collision, vec


class Rosie2(Decal):
    def setup(self):
        super().setup()
        self.key_id = self.init.get("key_id")
        self.talking = False
        self.kill_after = False
        self.paused = False
        self.talking_head.animation = self.talking_head.rosie_talk
        self.seq_gen = iter([])
        self.cue_placement = (
            vec(self.scene.game.draw_surface.get_size()).elementwise()
            * vec([0.5, 1]) 
            - vec(self.button_cue.sprite.rect.size).elementwise()
            * vec([0.5, 1])
        )
        self.cue_text.set_text(self.cue_text.init.get("text", ""))
 

    def show_talk_cue(self):
        self.scene.place_node(
            self.button_cue, ["hud"], self.cue_placement
        )
        self.scene.place_node(
            self.cue_text, ["hud"],
        )
        self.cue_text.sprite.rect.midleft = (
            self.button_cue.sprite.rect.midright
        )


    def update(self):
        player = self.scene.get_player().parent
        player_rect = player.sprite.rect
        if (
            self.sprite.rect.colliderect(player_rect) 
            and not self.talking 
        ):
            # signal that talking is available
            self.show_talk_cue()
        else:
            self.button_cue.kill()
            self.cue_text.kill()
        
        if (
            self.sprite.rect.colliderect(player_rect) 
            and not self.talking 
            and self.talk_button_pressed() 
            and not self.scene.occupied
        ):
            # start the dialogue sequence
            if player.inventory.contains(self.key_id):
                assert player.inventory.remove_item(self.key_id),\
                    "gate key was possesed but did not get removed properly"
                self.talk(self.leave_text)
                self.kill_after = True
            else:
                self.talk()        

        if self.textbox:
            if not self.textbox.scrolling:
                self.talking_head.state = "silent"
            if (
                not self.textbox.scrolling
                and self.talk_button_pressed()
                and not self.paused
            ):
                self.advance_sequence()
            else:
                self.textbox.update()
                self.talking_head.animation.update()
 

    def talk_button_pressed(self):
        return "BUTTON_E" in self.scene.game.input.new_actions()


    def talk(self, alt_text:str=None):
        self.talking = True
        self.scene.paused = True
        self.scene.occupied = True
        self.scene.place_node(
            self.textbox, ["hud"], 
            self.textbox.init.get('start')
        )
        self.scene.place_node(self.talking_head,["hud"])
        self.talking_head.sprite.rect.topright = (
            self.textbox.sprite.rect.topleft
        )
        self.talking_head.state = "talking"
        if self.init.get("sequence"):
            seq = self.init.get("sequence")[
                slice(*self.init.get("seq_sets")["init"])
            ]
            self.advance_sequence(sequence=seq)
            return
        if alt_text is not None:
            self.textbox.scroll_text(alt_text)
        else:
            self.textbox.scroll_text(self.textbox.init.get("text", ""))


    def advance_sequence(self, sequence=None):
        if sequence is not None:
            self.seq_gen = iter(sequence)
        cur = next(self.seq_gen, None)
        if cur is None:
            self.stop_talk()
            return
        self.talking_head.state = "talking"
        self.talking_head.animation = getattr(
            self.talking_head, cur["talking_head"]
        )
        self.textbox.scroll_text(cur["text"])
        if cur.get("prompt") is not None:
            self.talking_head.child_by_id(cur["prompt"]).open_menu()


    def stop_talk(self):
        self.textbox.kill()
        self.talking_head.kill()
        self.scene.paused = False
        self.talking = False
        self.scene.occupied = False
        if self.kill_after:
            self.kill()
