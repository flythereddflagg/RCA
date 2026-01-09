import pygame as pg
from .node import Node
from .textbox import TextBox
from .decal import Decal


MENU_TEXT = """
Music Volume: r<(){}
SFX Volume: {}
Back
""".strip()

class OptionsMenu(Node):
    def setup(self): #TODO -1- WORK HERE NEXT
        self.add_child_node(TextBox(id = "textbox", children=[id= indicator
            type: Decal
            image: ./assets/block/text_select.png]))
        self.textbox.set_text(MENU_TEXT)
        self.choices = MENU_TEXT.split("\n")
        self.active = False
        self.selected = 0
        self.bindings = [
            self.do_music,
            self.do_sfx,
            self.do_back
        ]

    def update(self):
        if not self.active:
            return
    
    def do_music(self):
        pass

    def do_sfx(self):
        pass

    def do_back(self):
        pass

        

    def up_pressed(self):
        return "UP" in self.scene.game.input.new_actions()
    
    def down_pressed(self):
        return "DOWN" in self.scene.game.input.new_actions()

    def confirm_pressed(self):
        new_actions = self.scene.game.input.new_actions()
        return any([x in new_actions for x in ["BUTTON_S", "START"]])
    
    def menu_button_pressed(self):
        return "SELECT" in self.scene.game.input.new_actions()
        
    
    def go_up(self):
        step_size = (
            self.textbox.sprite.rect.size[1]
            // len(self.choices)
        )
        self.selected -= 1
        if self.selected < 0:
            self.selected += len(self.choices)
        self.textbox.indicator.rect.midright = (
            self.textbox.sprite.rect.topleft 
            + vec([
                INDICATOR_X_OFFSET, 
                step_size * self.selected + TEXT_PADDING
            ])
        )


    def go_down(self):
        step_size = (
            self.textbox.sprite.rect.size[1]
            // len(self.choices)
        )
        self.selected += 1
        if self.selected >= len(self.choices):
            self.selected -= len(self.choices)
        self.textbox.indicator.rect.midright = (
            self.textboxf.sprite.rect.topleft 
            + vec([
                INDICATOR_X_OFFSET, 
                step_size * self.selected + TEXT_PADDING
            ])
        )
