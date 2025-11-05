import pygame as pg

from .node import Node
from .decal import Decal
from .tools import vec

WHITE = (255,255,255, 255)
GREY = (128,128,128, 255)
BLACK = (0, 0, 0, 255)
BLANK = (0, 0, 0, 0)
FONTSIZE = 15
DEFAULT_FONT_FILE = "./assets/fonts/BoldPixels.ttf"
TEXT_PADDING = 10

# TODO -1- set up text crawl and animations!
# TODO -3- bound the box and provide auto-wrapping

class TextBox(Node):
    def setup(self):
        self.font_file = self.init.get("font_file", DEFAULT_FONT_FILE)
        self.font_size = self.init.get("font_size", FONTSIZE)
        self.text_color = self.init.get("text_color", WHITE)
        self.outline = self.init.get("outline", False)
        self.outline_color = self.init.get("outline_color", BLACK)
        self.bg_color = self.init.get("bg_color", BLANK)
        self.text_padding = self.init.get("text_padding", TEXT_PADDING)
        self.text = self.init.get("text", "")
        self.scrolling = False

        self.font = pg.freetype.Font(self.font_file, self.font_size)
        self.sprite = Decal(parent=self)
        # self.set_text(self.text)
        self.scrolling_text(self.text, speed=15)

    def update(self):
        if self.scrolling:
            self.update_scroll()

    
    def scrolling_text(self, text, speed:int):
        # speed is letters per second
        self.scrolling = True
        self.scroll_speed = (1 / speed) * 1000 # ms / letter
        self.cursor = 0
        self.text = text
        self.last_time = pg.time.get_ticks()

    def update_scroll(self):
        cur_time = pg.time.get_ticks()
        if (cur_time - self.last_time) < self.scroll_speed:
            return

        self.last_time = cur_time
        text_to_render = self.text[:self.cursor]
        self.cursor += 1
        self.set_text(text_to_render)
        if self.cursor > len(self.text):
            self.scrolling = False



    def set_text(self, text:str):
        print(repr(text))
        lines = text.split("\n")
        rendered_lines = [
            self.font.render(
                line, fgcolor=self.text_color, bgcolor=BLANK
            )
            for line in lines
        ]
        size = (
            max([rect.size[0] for line, rect in rendered_lines])
                + self.text_padding * 2, 
            max([rect.size[1] for line, rect in rendered_lines])
                * len(rendered_lines) 
                + self.text_padding * (len(rendered_lines)+2), 
        )
        self.text_surface = pg.surface.Surface(size, flags=pg.SRCALPHA)
        self.text_surface.fill(self.bg_color)
        for i, (surface, rect) in enumerate(rendered_lines):
            if self.outline:
                for j in range(3):
                    for k in range(3):
                        offset = vec((j - 1, k - 1))
                        self.text_surface.blit(
                            pg.mask.from_surface(surface).to_surface(
                                setcolor=BLACK, unsetcolor=BLANK
                            ), 
                            vec((self.text_padding, size[1]/len(rendered_lines) * i + self.text_padding)) + offset
                        )
            self.text_surface.blit(
                surface, (self.text_padding, size[1]/len(rendered_lines) * i + self.text_padding)
            )
        pos = self.sprite.rect.topleft
        self.sprite.set_image(self.text_surface)
        self.sprite.rect.topleft = pos