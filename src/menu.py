import pygame as pg
import yaml

from .node import node_from_dict
from .menuinterface import MenuInterface
from .decal import Decal
from .tools import vec
from .optionsmenu import OptionsMenu, OPTIONS_MENU_DICT
from .textbox import TextBox


WHITE = (255,255,255, 255)
GREY = (128,128,128, 255)
BLACK = (0, 0, 0, 255)
BLANK = (0, 0, 0, 0)
ARROW = "->"
FONTSIZE = 22

MENU_TEXT = """
    Continue 
    New Game
    Options
    Quit
"""
DEFAULT_FONT_FILE = "./assets/fonts/BoldPixels.ttf"
INDICATOR_X_OFFSET = 0
TEXT_PADDING = 10




class Menu(MenuInterface):
    def setup(self):
        super().setup()
        self.add_child(node_from_dict(self.scene, OPTIONS_MENU_DICT))
        self.textbox.set_text("Press Start")
        self.textbox.config(**self.init)
        self.textbox.sprite.image.set_alpha(0)
        self.textbox.sprite.rect.center = (
            vec([1, 1.75]).elementwise() * self.scene.game.get_center()
        )
        self.added = False
        self.started = False

        self.callbacks = { 
            text: func for text, func in zip(
                self.selection,
                [self.a_continue, self.a_new_game, self.a_options, self.a_quit]
            )
        }
        

    def a_continue(self):
        self.scene.game.load_game()
        
    
    def a_new_game(self):
        self.scene.game.saved_scenes = {}
        self.scene.deconstruct()
        self.scene.game.load_scene(
            yaml_path=self.scene.game.settings.new_game_scene,
            add_in=self.scene.game.settings.new_game_add_in
        )
    
    
    def a_options(self):
        self.close_menu()
        self.options_menu.open_menu()
    

    def a_quit(self):
        self.scene.game.running = False


    def update(self):
        if not self.added and self.parent.state == "titlescreen":
            self.fade_in_text()
        elif self.options_menu.active:
            self.options_menu.update()
            return
        
        self.process_input()
    
    
    def fade_in_text(self):
        self.textbox.sprite.add(self.scene.hud)
        if self.textbox.sprite.image.get_alpha() >= 255:
            self.added = True
            return
        # TODO -4- this effect sucks and depends on frame rate. Fix?
        self.textbox.sprite.image.set_alpha(self.textbox.sprite.image.get_alpha() + 1)


    def process_input(self):
        new_actions = self.scene.game.input.new_actions()
        select_button:bool = any([
            command in new_actions
            for command in ["START", "BUTTON_E"]
        ])
        if (
            self.parent.state != "titlescreen" and 
            select_button
        ):
            self.parent.state = "titlescreen"
            return

        if (
            not self.started and 
            select_button
        ):
            self.started = True
            self.open_menu()
            return

        if not self.started: return

        if "UP" in new_actions:
            self.go_up()
        elif "DOWN" in new_actions:
            self.go_down()
        elif select_button:
            self.select_option()
        



    def select_option(self):
        action = self.selection[self.selected]
        self.callbacks[action]()

    

    def open_menu(self):
        self.textbox.set_text(self.text)
        self.textbox.sprite.rect.center = (
            self.scene.game.get_center() *  vec([1, 1.5]).elementwise()
        )
        self.indicator = Decal(parent=self) 
        self.indicator.set_image(pg.image.load(
            "./assets/block/text_select.png"
        ))
        super().open_menu()
        self.place_indicator()
