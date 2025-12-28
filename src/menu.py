import pygame as pg

from .node import Node
from .decal import Decal
from .tools import vec



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

class Menu(Node):
    def setup(self):
        self.font_file = self.init.get("font_file", DEFAULT_FONT_FILE)
        self.font_size = self.init.get("font_size", FONTSIZE)
        self.menu_text = self.init.get("menu_text", MENU_TEXT)
        self.font = pg.freetype.Font(self.font_file, self.font_size)
        # self.font.antialiased = False
        self.sprite = Decal(parent=self)
        self.text_surface = None
        self.set_text("Press Start")
        self.selection = []

        self.text_surface.set_alpha(0)
        self.sprite.rect.center = (
            vec([1, 1.75]).elementwise() * self.scene.game.get_center()
        )
        self.added = False
        self.started = False

        self.callbacks = { 
            text: func for text, func in zip(
                [
                    line.strip() 
                    for line in self.menu_text.split("\n") 
                    if line.strip()
                ],
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
        print("\n\n\t-- See './assets/init.yaml for settings' --\n\n")
    

    def a_quit(self):
        self.scene.game.running = False


    def update(self):
        if not self.added and self.parent.state == "titlescreen":
            self.fade_in_text()
        
        self.process_input()
    
    
    def fade_in_text(self):
        self.sprite.add(self.scene.hud)
        if self.text_surface.get_alpha() >= 255:
            self.added = True
            return
        # TODO -4- this effect sucks and depends on frame rate. Fix?
        self.text_surface.set_alpha(self.text_surface.get_alpha() + 1)


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
            self.start_menu()
            return

        if not self.started: return

        if "UP" in new_actions:
            self.go_up()
        elif "DOWN" in new_actions:
            self.go_down()
        elif select_button:
            self.select_option()


    def go_up(self):
        step_size = self.text_surface.get_size()[1] // len(self.selection)
        self.selected -= 1
        if self.selected < 0:
            self.selected += len(self.selection)
        self.indicator.rect.midright = (
            self.sprite.rect.topleft + 
            vec([INDICATOR_X_OFFSET, step_size * self.selected + self.font_size//3 + TEXT_PADDING])
        )


    def go_down(self):
        step_size = self.text_surface.get_size()[1] // len(self.selection)
        self.selected += 1
        if self.selected >= len(self.selection):
            self.selected -= len(self.selection)
        self.indicator.rect.midright = (
            self.sprite.rect.topleft + 
            vec([INDICATOR_X_OFFSET, step_size * self.selected + self.font_size//3 + TEXT_PADDING])
        )


    def select_option(self):
        action = self.selection[self.selected]
        self.callbacks[action]()


    def set_text(self, text:str):
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        self.selection = lines
        rendered_lines = [
            self.font.render(line, fgcolor=WHITE, bgcolor=BLANK)
            if (
                not "Continue" in line 
                or self.scene.game.save_file_path.exists()
            ) else
            self.font.render(line, fgcolor=GREY, bgcolor=BLANK)
            for line in lines
        ]
        size = (
            max([rect.size[0] for line, rect in rendered_lines])
                + TEXT_PADDING * 2, 
            max([rect.size[1] for line, rect in rendered_lines])
                * len(rendered_lines) + TEXT_PADDING * 3, 
        )
        self.text_surface = pg.surface.Surface(size, flags=pg.SRCALPHA)
        for i, (surface, rect) in enumerate(rendered_lines):
            # render text outline sprite
            for j in range(3):
                for k in range(3):
                    offset = vec((j - 1, k - 1))
                    self.text_surface.blit(
                        pg.mask.from_surface(surface).to_surface(
                            setcolor=BLACK, unsetcolor=BLANK
                        ), 
                        vec((TEXT_PADDING, size[1]/len(rendered_lines) * i + TEXT_PADDING)) + offset
                    )
            self.text_surface.blit(
                surface, (TEXT_PADDING, size[1]/len(rendered_lines) * i + TEXT_PADDING)
            )


        self.sprite.set_image(self.text_surface)
    

    def start_menu(self):

        self.set_text(self.menu_text)
        self.sprite.rect.center = (
            self.scene.game.get_center() *  vec([1, 1.5]).elementwise()
        )
        self.indicator = Decal(parent=self) 
        self.indicator.set_image(pg.image.load(
            "./assets/block/text_select.png"
        ))
        self.indicator.add(self.scene.hud)
        self.selected = 0
        self.indicator.rect.midright = (
            self.sprite.rect.topleft + 
            vec([INDICATOR_X_OFFSET, self.font_size//3 + self.font_size*self.selected + TEXT_PADDING])
        )
        