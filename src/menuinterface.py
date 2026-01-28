import pygame as pg
from .node import Node
from .textbox import TextBox
from .decal import Decal
from .tools import vec

PLACHOLDER = """
    placeholder
"""

class MenuInterface(Node):
    def setup(self):
        self.add_child(TextBox(id="textbox"))
        self.textbox.config(**self.init)
        if self.child_by_id("indicator") is None:
            self.add_child(Decal(id="indicator"))
            self.indicator.set_image(self.textbox.font.render(
                "-->", True, self.textbox.text_color, None 
            ))
        for group in self.init.get("groups", []):
            self.scene.groups[group].add(self.indicator)
        self.indicator_x_offset = self.init.get("indicator_x_offset", 0)
        self.v_text_padding = self.init.get("v_text_padding", 0)
        self.active = False
        self.selected = 0
        self.sprite = self.textbox.sprite
        self.text = self.init.get("text", PLACHOLDER)
        self.textbox.set_text(self.text)
        self.selection = [a.strip() for a in self.text.split("\n")]
        self.n_choices = len(self.selection)


    # def update(self):
    #     if self.up_pressed():
    #         self.go_up()
    #     elif self.down_pressed():
    #         self.go_down()
    #     elif self.confirm_pressed():
    #         self.close_menu()


    def open_menu(self):
        self.scene.place_node(self.textbox, groups=["hud"])
        self.scene.place_node(self.indicator, groups=["hud"])
        self.indicator.sprite.rect.topright = (
            self.textbox.sprite.rect.topleft
        )
        self.selected = 0


    def close_menu(self):
        self.scene.paused = False
        self.scene.occupied = False
        self.active = False
        self.kill()


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
        self.selected -= 1
        if self.selected < 0:
            self.selected += self.n_choices
        self.place_indicator()


    def go_down(self):
        self.selected += 1
        if self.selected >= self.n_choices:
            self.selected -= self.n_choices
        self.place_indicator()


    def place_indicator(self):
        step_size = (
            self.textbox.sprite.rect.size[1]
            // self.n_choices
        )
        self.indicator.rect.topright = (
            self.textbox.sprite.rect.topleft
            + vec([
                self.indicator_x_offset, 
                step_size * self.selected + self.v_text_padding
            ])
        )