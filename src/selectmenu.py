import pygame as py

from .node import Node, node_from_dict
from .textbox import TextBox
from .tools import vec
from .menuinterface import MenuInterface
from .optionsmenu import OptionsMenu, OPTIONS_MENU_DICT

INDICATOR_X_OFFSET = 0
TEXT_PADDING = 11

class SelectMenu(MenuInterface):
    def setup(self):
        super().setup()
        self.add_child(node_from_dict(self.scene, OPTIONS_MENU_DICT))
        self.textbox.set_text(self.text)
        self.textbox.sprite.rect.center = (
            vec(self.scene.game.get_center())
            + vec([-40, -50])
        )
        self.place_indicator()
        self.keyboard.set_text(self.keyboard.init['text'])
        self.bindings = [
            self.do_continue,
            self.do_options,
            self.do_save_quit
        ]


    def update(self):
        if self.options_menu.active and not self.active:
            self.options_menu.update()
            return
        elif self.options_menu.active and self.active:
            raise Exception("Two menus active at the same time!")
        
        select_pressed = self.menu_button_pressed() 
        if select_pressed and not self.scene.occupied:
            self.open_menu()
        elif select_pressed and self.active:
            self.close_menu()
        
        if self.active:
            if self.up_pressed():
                self.go_up()
            elif self.down_pressed():
                self.go_down()
            elif self.confirm_pressed():
                self.bindings[self.selected]()
        

    def open_menu(self):
        self.scene.paused = True
        self.scene.occupied = True
        self.active = True
        self.textbox.sprite.rect.center = (
            vec(self.scene.game.get_center())
            + vec([-60, -50])
        )# self.textbox.sprite.rect.center = self.scene.game.get_center() 
        # TODO -4- this feels uncecssary
        self.place_indicator() # TODO -4- this feels uncecssary
        super().open_menu()
        self.scene.place_node(self.controls, groups=["hud"], start=self.controls.init['start'])
        self.scene.place_node(self.keyboard, groups=["hud"], start=self.keyboard.init['start'])



    def close_menu(self):
        self.scene.paused = False
        self.scene.occupied = False
        super().close_menu()
        self.controls.kill()
        self.keyboard.kill()


    def do_continue(self):
        self.close_menu()
         

    def do_options(self):
        self.active = False
        super().close_menu()
        self.options_menu.open_menu()


    def do_save_quit(self):
        self.scene.game.save_game()
        self.scene.deconstruct()

        # effectvely soft reset the entire game
        self.scene.game.saved_scenes = {} 
                
        self.scene.game.load_scene(
            yaml_path=self.scene.game.settings.initial_scene,
            add_in=self.scene.game.settings.init_add_in
        )

