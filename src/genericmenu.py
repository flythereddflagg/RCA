import pygame as pg
from .node import Node
from .textbox import TextBox
from .decal import Decal
from .tools import vec

PLACHOLDER = """
    placeholder
"""

class GenericMenu(Node):
    def setup(self):
        self.add_child(TextBox(id="textbox"))
        if self.child_by_id("indicator") is None:
            self.add_child(Decal(id="indicator"))
            self.indicator.set_image(self.textbox.font.render(
                "->", True, self.textbox.text_color, None 
            ))
        for group in self.init.get("groups", []):
            self.scene.groups[group].add(self.indicator)
        self.indicator_x_offset = self.init.get("indicator_x_offset", 0)
        self.v_text_padding = self.init.get("v_text_padding", 0)

        self.active = False
        self.selected = 0
        self.sprite = self.textbox.sprite
        self.textbox.set_text(self.init.get("text", PLACHOLDER))
        self.selection = self.textbox.text.split("\n")
        self.n_choices = len(self.selection)
        self.place_indicator()
        self.last_time = 0

    def update(self):
        time = pg.time.get_ticks()
        if time - self.last_time > 1000:
            self.go_down()
            self.last_time = time

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
        self.place_indicator(step_size)


    def go_down(self):
        step_size = (
            self.textbox.sprite.rect.size[1]
            // self.n_choices
        )
        self.selected += 1
        if self.selected >= self.n_choices:
            self.selected -= self.n_choices
        self.place_indicator(step_size)


    def place_indicator(self, step_size=0):
        self.indicator.rect.midright = (
            self.textbox.sprite.rect.topleft 
            + vec([
                self.indicator_x_offset, 
                step_size * self.selected + self.v_text_padding
            ])
        )