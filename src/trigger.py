import pygame as pg

from .decal import Decal


class Trigger(Decal):
    def setup(self):
        super().setup()
    
    def update(self):
        textbox = self.scene.node_by_id("intro_text")
        if not textbox.text:
            textbox.scroll_text(textbox.init['text'])
        if not textbox.scrolling:
            if self.sprite not in self.scene.groups["foreground"]:
                self.scene.place_node(
                    self,
                    ["foreground"],
                    self.init["start"]
                )
            if self.button_pressed():
                self.a_new_game()

    def a_new_game(self):
        self.scene.game.saved_scenes = {}
        self.scene.deconstruct()
        self.scene.game.load_scene(
            yaml_path=self.scene.game.settings.new_game_scene,
            add_in=self.scene.game.settings.new_game_add_in
        )

    def button_pressed(self):
        return "BUTTON_E" in self.scene.game.input.new_actions()