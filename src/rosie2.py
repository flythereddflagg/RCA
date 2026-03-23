import pygame as pg

from .decal import Decal
from .node import node_from_dict
from .tools import mask_collision, vec
from .movement import Movement

EDGE_OF_CLIFF = 970

class Rosie2(Decal):
    def setup(self):
        super().setup()
        self.key_id = self.init.get("key_id")
        self.state = "standing"
        self.talking = False
        self.kill_after = False
        self.paused = False
        self.exiting = False
        self.shaken = False
        self.talk_state = "init"
        self.talking_head.animation = self.talking_head.rosie_talk
        self.seq_gen = iter([])
        self.move = Movement(self.sprite)
        self.cue_placement = (
            vec(self.scene.game.draw_surface.get_size()).elementwise()
            * vec([0.5, 1]) 
            - vec(self.button_cue.sprite.rect.size).elementwise()
            * vec([0.5, 1])
        )
        self.cue_text.set_text(self.cue_text.init.get("text", ""))
        self.rotation = 0
        self.original_image = self.sprite.image
        self.start_time = -1


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
            and not self.exiting
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
                self.talk_state = "tupperware"
                self.exiting = True
                self.talk()
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

        if (
                not self.talking 
                and self.exiting 
                and self.talk_state == "tupperware"
        ):          
            self.scene.paused = True
            self.scene.occupied = True
            self.state = "walking"
            
            if self.scene.node_by_id("meatball") not in self.scene.active_nodes:
                self.scene.place_node(
                    self.scene.node_by_id("meatball"), 
                    groups=["foreground", "paused"],
                    start=vec([-50, 50]) + self.sprite.rect.topleft
                )
                self.scene.node_by_id("meatball").state = "stage1"
            self.move(direction="RIGHT", speed=25, reject_foreground=False)
            bg_x = (
                vec(self.sprite.rect.topleft)
                - vec(self.scene.background.sprites()[0].rect.topleft)
            )[0]

            if bg_x > EDGE_OF_CLIFF and self.rotation < 90:

                self.sprite.set_image(
                    pg.transform.rotate(self.original_image, -self.rotation)
                )
                self.rotation += 1
            elif self.rotation >= 90:
                self.move(direction="DOWN", speed=300, reject_foreground=False)
            
            if not self.sprite.rect.colliderect(
                    self.scene.game.draw_surface.get_rect()
            ):

                # TODO -1- make a walking animation
                
                camera = self.scene.node_by_id("camera")
                if not camera.shaking:
                    if not self.shaken:
                        camera.screenshake()
                        self.shaken = True
                        self.crash_sound.play()
                    elif not camera.shaking: #shaking is done
                        # timing delay for comedic effect.
                        if self.start_time == -1:
                            self.start_time = pg.time.get_ticks()
                        if (pg.time.get_ticks() - self.start_time) > 1000:
                            self.talk_state = "fine"
                            self.kill_after = True
                            self.talk()


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
            self.advance_sequence(sequence=self.talk_state)
            return
        if alt_text is not None:
            self.textbox.scroll_text(alt_text)
        else:
            self.textbox.scroll_text(self.textbox.init.get("text", ""))


    def advance_sequence(self, sequence:str=None):
        # TODO -2- This does not accomodate single values
        if sequence is not None:
            seq_list = self.init.get("sequence")
            self.talk_state = sequence
            seq_slice = self.init.get("seq_sets")[sequence]
            if len(seq_slice) == 1:
                begin = seq_slice[0]
                end = len(seq_list)-1
            else:
                begin, end = seq_slice
            iter_seq = seq_list[slice(begin, end + 1)]
            self.seq_gen = iter(iter_seq)
        cur = next(self.seq_gen, None)
        if cur is None:
            if "after_" + self.talk_state in self.init.get("seq_sets"):
                self.talk_state = "after_" + self.talk_state
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
        if self.kill_after == True:
            self.kill()
