import pygame as pg
from .node import Node
from .textbox import TextBox
from .decal import Decal
from .tools import vec


MENU_TEXT = """
Music Volume: < {music_vol} >
SFX Volume: < {sfx_vol} >
Back
""".strip()
INDICATOR_X_OFFSET = 0
TEXT_PADDING = 11

class GenericMenu(Node):
    def setup(self):
        self.update_text_display()
        self.textbox.sprite.rect.center = self.scene.game.get_center()
        self.n_choices = len(MENU_TEXT.split("\n"))
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
        elif self.menu_button_pressed():
            self.do_back()
        elif self.right_pressed():
            self.bindings[self.selected](1)
        elif self.left_pressed():
            self.bindings[self.selected](-1)
        
        
    def close_menu(self):
        self.scene.paused = False
        self.scene.occupied = False
        self.active = False
        self.textbox.sprite.kill()
        self.textbox.kill()


    def update_text_display(self):
        self.textbox.set_text(MENU_TEXT.format(
            music_vol=self.scene.game.music_volume, 
            sfx_vol=self.scene.game.sfx_volume
        ))

    def do_music(self, rl_val:int=0):
        print(f"DO MUSIC CALLED WITH {rl_val}")
        self.scene.game.music_volume += rl_val
        if self.scene.game.music_volume > self.scene.game.max_volume:
            self.scene.game.music_volume = self.scene.game.max_volume
        
        if self.scene.game.music_volume < 0:
            self.scene.game.music_volume = 0
        
        self.update_text_display()


    def do_sfx(self, rl_val:int=0):
        print(f"DO MUSIC CALLED WITH {rl_val}")
        self.scene.game.sfx_volume += rl_val
        if self.scene.game.sfx_volume > self.scene.game.max_volume:
            self.scene.game.sfx_volume = self.scene.game.max_volume
        
        if self.scene.game.sfx_volume < 0:
            self.scene.game.sfx_volume = 0
        
        self.update_text_display()

    def do_back(self, rl_val:int=0):
        if rl_val: 
            return
        self.active = False
        self.close_menu()
        self.parent.open_menu()
        

    def up_pressed(self):
        return "UP" in self.scene.game.input.new_actions()
    
    def down_pressed(self):
        return "DOWN" in self.scene.game.input.new_actions()

    def confirm_pressed(self):
        new_actions = self.scene.game.input.new_actions()
        return any([x in new_actions for x in ["BUTTON_S", "START"]])
    
    def menu_button_pressed(self):
        return "SELECT" in self.scene.game.input.new_actions()

    def right_pressed(self):
        return "RIGHT" in self.scene.game.input.new_actions()

    def left_pressed(self):
        return "LEFT" in self.scene.game.input.new_actions()
    
    def go_up(self):
        step_size = (
            self.textbox.sprite.rect.size[1]
            // self.n_choices
        )
        self.selected -= 1
        if self.selected < 0:
            self.selected += self.n_choices
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
            // self.n_choices
        )
        self.selected += 1
        if self.selected >= self.n_choices:
            self.selected -= self.n_choices
        self.textbox.indicator.rect.midright = (
            self.textbox.sprite.rect.topleft 
            + vec([
                INDICATOR_X_OFFSET, 
                step_size * self.selected + TEXT_PADDING
            ])
        )
