import string
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
SCROLL_SPEED = 15
PRINTABLE_CHARS = string.printable[:-5]


class TextBox(Node):
    def setup(self):
        self.font_file = self.init.get("font_file", DEFAULT_FONT_FILE)
        self.font_size = self.init.get("font_size", FONTSIZE)
        self.text_color = self.init.get("text_color", WHITE)
        self.outline = self.init.get("outline", False)
        self.outline_color = self.init.get("outline_color", BLACK)
        self.bg_color = self.init.get("bg_color", BLANK)
        self.text_padding = self.init.get("text_padding", 0)
        self.text = self.init.get("text", "")
        self.box_size = self.init.get("box_size")
        self.scroll_speed = self.init.get("scroll_speed", SCROLL_SPEED)
        self.scrolling = False

        self.font = pg.font.Font(self.font_file, self.font_size)
        self.font_char_w, self.font_height = self.font.size(PRINTABLE_CHARS)
        self.font_char_w /= len(PRINTABLE_CHARS)
        self.add_child(Decal(id="sprite"))


    def config(self, **kwargs):
        keys = vars(self).keys()
        for key, val in kwargs.items():
            if key in keys:
                setattr(self, key, val)
        
        if (
            "font_file" in kwargs.keys()
            or "font_size" in kwargs.keys()
            or "font" in kwargs.keys()
        ):
            if "font" not in kwargs.keys():
                self.font = pg.font.Font(self.font_file, self.font_size)
            self.font_char_w, self.font_height = self.font.size(PRINTABLE_CHARS)
            self.font_char_w /= len(PRINTABLE_CHARS)


    def update(self):
        if self.scrolling:
            self.update_scroll()

    
    def scroll_text(self, text=None, speed:int=None, box_size=None):
        if text:
            self.text = text
        if speed: # speed is letters per second
            self.scroll_speed = speed
        if box_size: 
            self.box_size = box_size
        
        self.scrolling = True
        self.scroll_time = (1 / self.scroll_speed) * 1000 # ms / letter
        self.cursor = 0
        self.last_time = pg.time.get_ticks()
        self.set_text("")


    def update_scroll(self):
        cur_time = pg.time.get_ticks()
        if (cur_time - self.last_time) < self.scroll_time:
            return

        self.last_time = cur_time
        text_to_render = self.text[:self.cursor]
        self.cursor += 1
        self.set_text(text_to_render, self.box_size)
        if self.cursor > len(self.text):
            self.scrolling = False



    def set_text(self, text:str, box_size:tuple[int, int]=None):
        # print(repr(text))
        lines = text.split("\n")
        
        if box_size:
            # reformat lines to fit in box
            line_len = int(
                box_size[0] // self.font_char_w
                + self.font_char_w // 2 # add buffer for smaller chars
            )
            new_text = " ".join(lines)
            words = new_text.split(' ')
            lines = []
            line = []
            for word in words:
                line.append(word)
                if len(" ".join(line)) > line_len:
                    line.pop()
                    lines.append(" ".join(line))
                    line = [word]

            lines.append(" ".join(line))
                
        rendered_lines = [
            self.font.render(
                line, True, self.text_color, None
            )
            for line in lines
        ]

        size = (
            max([line.get_size()[0] for line in rendered_lines])
                + self.text_padding * 2, 
            self.font_height * len(rendered_lines) 
                + self.text_padding *(len(rendered_lines)+2), 
        )
        box_size = size if not box_size else box_size      

        self.text_surface = pg.surface.Surface(size, flags=pg.SRCALPHA)
        self.bounding_box_surface = pg.surface.Surface(
            box_size, flags=pg.SRCALPHA
        )
        self.bounding_box_surface.fill(self.bg_color)
        for i, surface in enumerate(rendered_lines):
            text_y_pos = (self.font_height + self.text_padding) * i + self.text_padding * 2 
            if self.outline:
                for j in range(3):
                    for k in range(3):
                        offset = vec((j - 1, k - 1))
                        self.text_surface.blit(
                            pg.mask.from_surface(surface).to_surface(
                                setcolor=BLACK, unsetcolor=BLANK
                            ), 
                            vec((self.text_padding, text_y_pos)) + offset
                        )
            self.text_surface.blit(
                surface, (self.text_padding, text_y_pos)
            )
        self.bounding_box_surface.blit(
            self.text_surface, [0,  box_size[1] - size[1]]
        )
        pos = self.sprite.rect.topleft
        self.sprite.set_image(self.bounding_box_surface)
        self.sprite.rect.topleft = pos
