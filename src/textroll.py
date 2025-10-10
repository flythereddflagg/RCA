import pygame as pg

from .node import Node
from .decal import Decal
from .tools import vec
from .movement import Movement



WHITE = (255,255,255)
FONTSIZE = 22
DEFAULT_FONT_FILE = "./assets/fonts/BoldPixels.ttf"
CREDITS = """
              To be continued...


Thank you so much for playing this demo!
If you would like to leave feedback 
please follow the link in the README.

                                         
                 CREDITS

             -- Powered by -- 
                 pygame
          
            -- Produced by --
            FlyTheReddFlagg Games
            
             -- Tech Stack --
            Python      VSCodium
            pygame      Aseprite
            PyYAML      MuseScore
            
       -- Creation and Direction -- 
                Mark Redd

          -- Software Design --
                Mark Redd

            -- Concept Art --
                Emma Redd
                Mark Redd
             Elizabeth Floyd

             -- Line Art --
             Elizabeth Floyd
                Emma Redd
                
       -- Pixel art and animation --
                Mark Redd
            
           -- Art Consulting --
             Elizabeth Floyd

               -- Music --
                Mark Redd
                Emma Redd
             Elizabeth Floyd

               -- Story --
                Mark Redd








Press BACKSPACE on your keyboard to exit.
"""

class TextRoll(Node):
    def setup(self):
        self.font_file = self.init.get("font_file", DEFAULT_FONT_FILE)
        self.font_size = self.init.get("font_size", FONTSIZE)
        self.text = self.init.get("text", CREDITS)
        self.scroll_speed = self.init.get("scroll_speed", 20)
        self.font = pg.font.Font(self.font_file, self.font_size)
        self.sprite = Decal(parent=self)
        self.text_surface = None
        self.set_text(self.text)
        self.sprite.rect.midtop = ( 
            self.scene.game.draw_surface.get_rect().midbottom
        )
        self.move = Movement(self.sprite)


    def update(self):
        draw_surface = self.scene.game.draw_surface
        if self.sprite.rect.bottom > draw_surface.get_rect().size[1] * 0.55:
            self.move("UP", speed = self.scroll_speed)


    def set_text(self, text:str):
        lines = text.split("\n")
        self.selection = lines
        rendered_lines = [self.font.render(line, True, WHITE) for line in lines]
        size = (
            max([line.get_size()[0] for line in rendered_lines]), 
            max([line.get_size()[1] for line in rendered_lines]) *\
            len(rendered_lines), 
        )
        self.text_surface = pg.surface.Surface(size, flags=pg.SRCALPHA)
        for i, surface in enumerate(rendered_lines):
            self.text_surface.blit(
                surface, (0, size[1]/len(rendered_lines) * i)
            )
        self.sprite.set_image(self.text_surface)
    


