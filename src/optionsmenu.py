import pygame as pg
from .node import Node
from .textbox import TextBox
from .decal import Decal
from .tools import vec


MENU_TEXT = """
Music Volume: r<(){}
SFX Volume: {}
Back
""".strip()
INDICATOR_X_OFFSET = 0
TEXT_PADDING = 11

class OptionsMenu(Node):
    def setup(self):
        self.textbox.set_text(MENU_TEXT)
        self.textbox.sprite.rect.center = self.scene.game.get_center()
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
            self.kill()
            return
        if self.up_pressed():
            self.go_up()
        elif self.down_pressed():
            self.go_down()
        elif self.confirm_pressed():
            self.bindings[self.selected]()
        
        
    

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
            self.textbox.sprite.rect.topleft 
            + vec([
                INDICATOR_X_OFFSET, 
                step_size * self.selected + TEXT_PADDING
            ])
        )
