"""
file: rca/__init__.py
about:
this file is the engine and runs everything needed to keep 
the game running.
"""
import os
import random
import pathlib
import pprint

import pygame as pg

from .scene import Scene
from .tools import load_yaml, save_yaml, vec, diff_vec
from .input import Input
from .hitmask import HitMask

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RGBA_BLUE = (0,0,255,255)
RGBA_RED = (255,0,0,255)
RGBA_GREEN = (0,255,0,255)

ALLOW_DEBUG = True

SAVE_PATH = pathlib.Path(os.path.expanduser("~/.local/share/rca/saves"))
SAVE_FILE = SAVE_PATH / "save_file.yaml"

FONTSIZE = 22
DEFAULT_FONT_FILE = "./assets/fonts/BoldPixels.ttf"

class Engine():
    """
    connects the hardware to game logic and holds the game state
    including the scenes
    """
    def __init__(self, data_path, REPLAY=None):
        self.settings:'.dictobj.DictObj' = load_yaml(data_path)
        if not ALLOW_DEBUG: 
            self.settings.DEBUG = False
        self.dt = 1
        self.running = False
        self.paused = False
        self.scene = None
        self.saved_scenes:dict[str, Scene] = {}
        self.REPLAY = REPLAY
        self.max_volume = 10
        self.music_volume = 5
        self.sfx_volume = 5
        self.screen, self.draw_surface = self.init_screen()
        self.clock = pg.time.Clock()
        self.fps_counter = (
            pg.freetype.Font(DEFAULT_FONT_FILE, FONTSIZE)
            if self.settings.FPS_COUNTER or self.settings.DEBUG
            else None
        )
        self.input = Input(self, self.settings)
        self.save_file_path = pathlib.Path(
            self.settings.get("save_file", SAVE_FILE)
        )
        
        self.load_scene(
            yaml_path=self.settings.initial_scene,
            add_in=self.settings.init_add_in
        )


    def init_screen(self):
        icon_path = self.settings.get("icon")
        title = self.settings.get("title")
        if icon_path:
            pygame_icon = pg.image.load(icon_path)
            pg.display.set_icon(pygame_icon)
        if title:
            pg.display.set_caption(title)

        w, h = self.settings.ASPECT_RATIO
        float_aspect_ratio = w / h
        draw_surface_w, draw_surface_h = (
            int(self.settings.RESOLUTION * float_aspect_ratio),
            self.settings.RESOLUTION
        )        

        self.screenwidth, self.screenheight = (
            int(self.settings.RESOLUTION * float_aspect_ratio) *
            self.settings.SCALE,
            self.settings.RESOLUTION * self.settings.SCALE
        )        

        return (
            pg.display.set_mode(
                [self.screenwidth, self.screenheight], pg.RESIZABLE
            ),
            pg.Surface((draw_surface_w, draw_surface_h))
        )        

    def load_scene(self, yaml_path, add_in=None) -> Scene:
        yaml_data = self.saved_scenes.get(yaml_path)
            
        self.scene = Scene(
            game=self, 
            yaml_path=yaml_path, 
            yaml_data=yaml_data,
            add_in=add_in
        )

        return self.scene # return reference to scene if needed


    def save_game(self):
        # breakpoint()
        # ensure save_path exists
        pathlib.Path(self.save_file_path.parents[0]).mkdir(
            parents=True, exist_ok=True
        )
        filename = str(self.save_file_path)
        # get state of current scene
        self.saved_scenes[self.scene.id] = self.scene.serialize()
        # build save file
        # get player state
        player_node = self.scene.get_player().parent
        player_init = player_node.init

        player_init["start"] = [int(x) for x in diff_vec(
            player_node.sprite.rect.topleft,
            self.scene.background.sprites()[0].rect.topleft            
        )]
        # get inventory state
        inv_index = [
            item['id'] for item in player_init["children"]
        ].index("inventory")
        player_init["children"][inv_index] = (
            player_node.inventory.serialize()
        )
        save_file = {
            "add_in" : [player_init],
            "cur_scene" : self.scene.id,
            "scenes" : self.saved_scenes
        }
 
        save_yaml(save_file, filename)
        print(f"Saved game data to '{filename}'...")


    def load_game(self):
        if not self.save_file_path.exists(): return

        save_data = load_yaml(str(self.save_file_path))

        self.saved_scenes = save_data["scenes"]
        self.scene.deconstruct()
        self.load_scene(
            yaml_path=save_data["cur_scene"],
            add_in=save_data["add_in"]
        )

    def run(self):
        self.running = True

        while self.running:
            self.input.update()
            self.logic()
            self.draw_frame()
            self.dt = (
                self.clock.tick() 
                if self.settings.FPS < -1 else 
                self.clock.tick(self.settings.FPS)
            )


    def logic(self):
        # run all game logic here
        # quit overrides everything else
        new_actions = self.input.new_actions()
        if "QUIT" in new_actions:
            self.running = False
            return

        # key to refresh scene
        if (
            "REFRESH" in new_actions and
            self.settings.DEBUG and 
            self.scene
        ):
            self.scene.refresh()

        # make a breakpoint and open debugger at any time
        if (
            self.settings.DEBUG and 
            "BREAKPOINT" in new_actions
        ):
            print("\n\n---\nDEBUG: Entering the Python debugger...\n---\n\n")
            breakpoint()
        
        # update everything in the scene
        if self.scene and not self.paused:
            self.scene.update()


    def draw_frame(self):
        self.draw_surface.fill(BLACK)
        for group_name in self.scene.draw_layers:
            self.scene.groups[group_name].draw(self.draw_surface) 
        
        if self.settings.DEBUG:
            self.render_debug()
        
        scn_w, scn_h = self.screen.get_size()
        w, h = self.settings.ASPECT_RATIO
        aspect_ratio = w / h
        scn_aspect_ratio = scn_w / scn_h
        new_size = (
            (scn_w, scn_w / aspect_ratio)
            if scn_aspect_ratio < aspect_ratio else
            (scn_h * aspect_ratio, scn_h)
        )
        self.screen.fill(BLACK)
        self.screen.blit(
            pg.transform.scale(
                self.draw_surface, new_size
            ),
            (vec([scn_w, scn_h]) - new_size)/2
        )
        pg.display.flip()


    def render_debug(self):
        if self.settings.FPS_COUNTER:
            fps = str(int(self.clock.get_fps()))
            fps_sprite, rect = self.fps_counter.render(
                fps, fgcolor=WHITE, bgcolor=BLACK
            )
            self.draw_surface.blit(fps_sprite, (300,10))
            
        background = self.scene.background.sprites()[0]
        self.box_texts = []
        for group_name in self.scene.draw_layers:
            sprites = self.scene.groups[group_name].sprites()
            
            for sprite in sprites:
                if not isinstance(sprite.parent, HitMask):
                    self.render_sprite_box(sprite, background)
                if self.settings.SHOW_MASK and sprite.mask:
                    if (
                        sprite in self.scene.background and
                        not self.settings.SHOW_BG_MASK
                    ): continue

                    self.render_mask(sprite)


    def get_center(self):
        return vec(self.draw_surface.get_size()) / 2


    def render_sprite_box(self, sprite, background):
        if not vars(sprite).get('pos'):
            sprite.pos = pg.font.SysFont("Sans", 10)
        pg.draw.rect(
            self.draw_surface, (255,255,255), sprite.rect, width=2
        )
        pos1, pos2 = (
            str(vec(sprite.rect.topleft)), 
            str(diff_vec( sprite.rect.topleft, background.rect.topleft))
        )
        sprite_id = sprite.id if sprite.id != "sprite" else sprite.parent.id
        pos_sprite = sprite.pos.render(
            f"<{sprite_id}> {pos1} ; {pos2}", 
            True, (255,255,255)
        )
        pos_rect = pos_sprite.get_rect()
        screen_rect = self.draw_surface.get_rect()
        # keep it inside the screen.
        text_pos = diff_vec(sprite.rect.topleft, (0, 15))
        x, y = text_pos
        x = 0 if x < 0 else x
        x = (
            screen_rect.right - pos_rect.size[0] 
            if x > screen_rect.right - pos_rect.size[0] 
            else x
        )
        y = 0 if y < 0 else y
        y = (
            screen_rect.bottom - pos_rect.size[1] 
            if y > screen_rect.bottom - pos_rect.size[1] 
            else y
        )
        # test if it collides with another rect and move it down if it does
        text_pos = (x, y)
        test_rect = pg.Rect(x, y, pos_rect.size[0], pos_rect.size[1])

        while test_rect.collidelistall(self.box_texts):
            test_rect.top += 1
        self.box_texts.append(test_rect)

        self.draw_surface.blit(pos_sprite, test_rect.topleft)


    def render_mask(self, sprite):
        color = (
            (
                RGBA_GREEN 
                if sprite.parent.init['kind'] == "hitmask" else
                RGBA_RED
            ) 
            if isinstance(sprite.parent, HitMask)
            else RGBA_BLUE
        )
        self.draw_surface.blit(
            sprite.mask.to_surface(
                setcolor = color, unsetcolor = None
            ),
            sprite.rect.topleft
        )                  