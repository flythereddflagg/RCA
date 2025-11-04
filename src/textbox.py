import pygame as pg

from .node import Node
from .decal import Decal
from .tools import vec

WHITE = (255,255,255, 255)
GREY = (128,128,128, 255)
BLACK = (0, 0, 0, 255)
BLANK = (0, 0, 0, 0)
FONTSIZE = 22
DEFAULT_FONT_FILE = "./assets/fonts/BoldPixels.ttf"
TEXT_PADDING = 10

# TODO -1- set up text crawl and animations!

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

        self.font = pg.freetype.Font(self.font_file, self.font_size)
        self.sprite = Decal(parent=self)
        self.set_text(self.text)

    def update(self):
        pass

    def set_text(self, text:str):
        print(repr(text))
        lines = text.split("\n")
        rendered_lines = [
            self.font.render(
                line, fgcolor=self.text_color, bgcolor=self.bg_color
            )
            for line in lines
        ]
        size = (
            max([rect.size[0] for line, rect in rendered_lines])
                + self.text_padding * 2, 
            max([rect.size[1] for line, rect in rendered_lines])
                * len(rendered_lines) 
                + self.text_padding * len(rendered_lines), 
        )
        self.text_surface = pg.surface.Surface(size, flags=pg.SRCALPHA)
        for i, (surface, rect) in enumerate(rendered_lines):
            if self.outline:
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