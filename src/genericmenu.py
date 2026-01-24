import pygame as pg
from .node import Node
from .textbox import TextBox
from .decal import Decal
from .tools import vec


class GenericMenu(Node):
    def setup(self):
        self.add_child(TextBox(id="textbox"))
        self.add_child(Decal(id="indicator"))
        self.indicator_x_offset = self.init.get("indicator_x_offset", 0)
        self.v_text_padding = self.init.get("v_text_padding", 0)

        self.active = False
        self.selection = self.init.text
        self.selected = 0
        
        
        
    def close_menu(self):
        self.scene.paused = False
        self.scene.occupied = False
        self.active = False
        self.textbox.kill()


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
        self.place_indicator()


    def go_down(self):
        step_size = (
            self.textbox.sprite.rect.size[1]
            // self.n_choices
        )
        self.selected += 1
        if self.selected >= self.n_choices:
            self.selected -= self.n_choices
        self.place_indicator()


    def place_indicator(self):
        self.indicator.rect.midright = (
            self.textbox.sprite.rect.topleft 
            + vec([
                self.indicator_x_offset, 
                step_size * self.selected + self.v_text_padding
            ])
        )