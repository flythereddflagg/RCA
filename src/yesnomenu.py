import pygame as pg
import yaml

from .decal import Decal
from .tools import vec
from .menuinterface import MenuInterface


MENU_TEXT = """
Yes
No
""".strip()
INDICATOR_X_OFFSET = 0
TEXT_PADDING = 11

YES_NO_MENU_INIT = """
id: yesno
type: YesNoMenu
font_size: 22
text_padding: 3
bg_color: [0,0,0,0]
outline: true
children:
- id: indicator
  type: Decal
  image: ./assets/block/text_select.png
"""

YES_NO_MENU_DICT = yaml.load(YES_NO_MENU_INIT, Loader=yaml.Loader)

class YesNoMenu(MenuInterface):
    def setup(self):
        self.init["text"] = MENU_TEXT
        super().setup()
        self.textbox.sprite.rect.center = self.scene.game.get_center()
        self.n_choices = len(MENU_TEXT.split("\n"))
        self.selected = 0
        self.bindings = [
            self.do_yes,
            self.do_no
        ]

    def open_menu(self):
        self.parent.parent.paused = True
        super().open_menu()

    def update(self):
        if self.parent.parent.textbox.scrolling:
            return
        if self.up_pressed():
            self.go_up()
        elif self.down_pressed():
            self.go_down()
        elif self.confirm_pressed():
            self.bindings[self.selected]()


    def confirm_pressed(self):
        new_actions = self.scene.game.input.new_actions()
        return any([x in new_actions for x in [
            "BUTTON_S", "BUTTON_E", "START"
        ]])

    def do_yes(self):
        print("Doing YES")
        rosie = self.parent.parent
        seq = rosie.init.get("sequence")[
            slice(*rosie.init.get("seq_sets")["eat"])
        ]
        rosie.paused = False
        rosie.advance_sequence(seq)
        self.close_menu()


    def do_no(self):
        print("Doing NO")
        self.parent.parent.paused = False
        self.parent.parent.advance_sequence()
        self.close_menu()





