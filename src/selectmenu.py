import pygame as py

from .node import Node
from .textbox import TextBox
from .tools import vec
from .optionsmenu import OptionsMenu

INDICATOR_X_OFFSET = 0
TEXT_PADDING = 11

class SelectMenu(Node):
    def setup(self):
        self.add_child_node(OptionsMenu(id="options_menu"))
        self.active = False
        self.selecttext.set_text(self.selecttext.text)
        self.selecttext.sprite.rect.center = self.scene.game.get_center()
        self.choices = self.selecttext.text.split("\n")
        self.selected = 0
        self.bindings = [
            self.do_continue,
            self.do_options,
            self.do_save_quit
        ]

    def update(self):
        if self.options_menu.active:
            self.options_menu.update()
            return
        select_pressed = self.menu_button_pressed() 
        if select_pressed and not self.scene.occupied:
            self.scene.paused = True
            self.scene.occupied = True
            self.active = True
            self.scene.place_node(self.selecttext, groups=["hud"])
            self.scene.place_node(self.selecttext.indicator, groups=["hud"])
            self.selecttext.indicator.sprite.rect.topright = (
                self.selecttext.sprite.rect.topleft
            )
            self.selected = 0
            
        
        elif select_pressed and self.active:
            self.scene.paused = False
            self.scene.occupied = False
            self.active = False
            self.selecttext.sprite.kill()
            self.selecttext.kill()
        
        if self.active:
            if self.up_pressed():
                self.go_up()
            elif self.down_pressed():
                self.go_down()
            elif self.confirm_pressed():
                self.bindings[self.selected]()


    def do_continue(self):
        self.scene.paused = False
        self.scene.occupied = False
        self.active = False
        self.selecttext.kill()
         

    def do_options(self):
        self.options_menu.active = True
        self.active = False
        self.selecttext.sprite.kill()
        self.selecttext.kill()
        self.scene.place_node(self.options_menu)

    def do_save_quit(self):
        self.scene.game.save_game()
        self.scene.game.running = False


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
            self.selecttext.sprite.rect.size[1]
            // len(self.choices)
        )
        self.selected -= 1
        if self.selected < 0:
            self.selected += len(self.choices)
        self.selecttext.indicator.rect.midright = (
            self.selecttext.sprite.rect.topleft 
            + vec([
                INDICATOR_X_OFFSET, 
                step_size * self.selected + TEXT_PADDING
            ])
        )


    def go_down(self):
        step_size = (
            self.selecttext.sprite.rect.size[1]
            // len(self.choices)
        )
        self.selected += 1
        if self.selected >= len(self.choices):
            self.selected -= len(self.choices)
        self.selecttext.indicator.rect.midright = (
            self.selecttext.sprite.rect.topleft 
            + vec([
                INDICATOR_X_OFFSET, 
                step_size * self.selected + TEXT_PADDING
            ])
        )
