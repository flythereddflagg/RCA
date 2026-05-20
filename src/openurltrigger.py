import pygame as pg
import webbrowser
from .textbox import TextBox

class OpenUrlTrigger(TextBox):
    def setup(self):
        super().setup()
        self.set_text(self.init.get("text", ""))

    def update(self):
        self.glyph.sprite.rect.midright = self.sprite.rect.midleft
        # for group in self.init["groups"]:
        #     self.sprite.add(self.scene.groups[group])
        if self.exec_button_pressed():
            webbrowser.open(self.init.get("url"))

    def exec_button_pressed(self):
        return "BUTTON_N" in self.scene.game.input.new_actions()