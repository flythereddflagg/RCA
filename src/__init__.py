"""
file: rca/__init__.py
about:
this file is the engine and runs everything needed to keep 
the game running.
"""

import pygame as pg

from .scene import Scene
from .tools import load_yaml
from .input import Input

BLACK = (0, 0, 0)
# TODO make a scene manager that loads a bunch of scenes here and then loads them into the game and remembers them.

class GameState():
    """
    connects the hardware to game logic and holds the game state
    including the scenes
    """
    def __init__(self, data_path, REPLAY=None):
        self.settings:'.dictobj.DictObj' = load_yaml(data_path)
        self.dt = 1
        self.running = False
        self.paused = False
        self.scene = None
        self.saved_scenes = {}
        self.REPLAY = REPLAY
        self.screen, self.draw_surface = self.init_screen()
        self.clock = pg.time.Clock()
        self.fps_counter = (
            pg.font.SysFont("Sans", 22) 
            if self.settings.FPS_COUNTER or self.settings.DEBUG
            else None
        )
        self.input = Input(self, self.settings)
        
        self.load_scene(
            yaml_path=self.settings.initial_scene,
            add_in=self.settings.init_add_in
        )


    def init_screen(self):
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


    def load_scene(self, **init) -> Scene:
        self.scene = Scene(
            game=self,  groups=self.settings.sprite_groups, **init
        )

        return self.scene # return reference to scene if needed


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
        game_input, held = self.input.get()
        if ("QUIT", 1.0) in game_input:
            self.running = False
            return

        # key to refresh scene
        if (
            self.settings.DEBUG and 
            ("REFRESH", 1.0) in game_input and 
            not "REFRESH" not in held and 
            self.scene
        ):
            self.scene.refresh()

        # make a breakpoint and open debugger at any time
        if (
            self.settings.DEBUG and
            ("BREAKPOINT", 1.0) in game_input and 
            "BREAKPOINT" not in held
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
            (pg.math.Vector2([scn_w, scn_h]) - new_size)/2
        )
        pg.display.flip()



    def render_debug(self):
        if self.settings.FPS_COUNTER:
            fps = str(int(self.clock.get_fps()))
            fps_sprite = self.fps_counter.render(fps, True, (255,255,255))
            #self.screen.blit(fps_sprite, (10,10))
            self.draw_surface.blit(fps_sprite, (10,10))
            
        background = self.scene.background.sprites()[0] 
        for group_name in self.scene.draw_layers:
            sprites = self.scene.groups[group_name].sprites()
            for sprite in sprites:
                if not vars(sprite).get('pos'):
                    sprite.pos = pg.font.SysFont("Sans", 10)
                pg.draw.rect(
                    # self.screen, (255,255,255), sprite.rect, width=2
                    self.draw_surface, (255,255,255), sprite.rect, width=2
                )
                pos1, pos2 = (
                    str(pg.math.Vector2(sprite.rect.topleft)//self.settings.SCALE), 
                    str((
                        pg.math.Vector2(sprite.rect.topleft) - 
                        pg.math.Vector2(background.rect.topleft)
                    )//self.settings.SCALE)
                )
                pos_sprite = sprite.pos.render(
                    f"<{sprite.id}> {pos1} ; {pos2}", 
                    True, (255,255,255)
                )
                pos_rect = pos_sprite.get_rect()
                # screen_rect = self.screen.get_rect()
                screen_rect = self.draw_surface.get_rect()
                # keep it inside the screen.
                text_pos = pg.math.Vector2(sprite.rect.topleft) - (0, 15)
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
                text_pos = (x, y)
                # self.screen.blit(pos_sprite, text_pos)
                self.draw_surface.blit(pos_sprite, text_pos)
                if self.settings.SHOW_MASK and sprite.mask:
                    if (
                        not self.settings.SHOW_BG_MASK and 
                        sprite in self.scene.background
                    ): continue
                    # self.screen.blit(
                    self.draw_surface.blit(
                        sprite.mask.to_surface(setcolor = (0,0,255,255), unsetcolor = None),
                        sprite.rect.topleft
                    )


    def get_center(self):
        return pg.math.Vector2(*self.draw_surface.get_size()) / 2
                    