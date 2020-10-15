# RCA package
# notice from copied code
import os
import json
from itertools import compress

import pygame as pg

# Screen Constants 
# Frame rate ( in Frames / second)
FPS          = 30 
SCREENWIDTH  = 800
SCREENHEIGHT = 600
# screen size tuple
SCREENSIZE   = (SCREENWIDTH, SCREENHEIGHT)
# x and y coordinates for the center of the screen
CENTERX      = SCREENWIDTH  // 2 
CENTERY      = SCREENHEIGHT // 2 

# Animation Constants
# player speed in pixels / second
playerPEEDTIME     = 300 * 2
# Player speed in pixels/frame
playerPEED         = playerPEEDTIME // FPS
# image changes per minute
PLAYERANIMATERATE   = playerPEEDTIME 

# frames to next player animation
PLAYERANIMATEFRAMES = int(FPS * 60 / PLAYERANIMATERATE)

# pixels before camera moves instead of player
CAMERASLACK         = 100 
NSLACK              = CENTERY - CAMERASLACK
SSLACK              = CENTERY + CAMERASLACK
ESLACK              = CENTERX + CAMERASLACK
WSLACK              = CENTERX - CAMERASLACK

# direction constants North:0 East:1 South:2 West:3
DIRECTIONS      = tuple(range(4))
N,E,S,W         = DIRECTIONS
DIRECTION_DICT  = {"north": N, "east" : E, "south" : S, "west" : W}

# colors
BLACK           = (0,0,0)


class DictObj(dict):
    """
    ******NOTICE***************
    optimize.py module by Travis E. Oliphant
    
    You may copy and use this module as you see fit with no
    guarantee implied provided you keep this notice in all copies.
    *****END NOTICE************
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):
        if self.keys():
            m = max(map(len, list(self.keys()))) + 1
            return '{\n' + '\n'.join([k.rjust(m) + ': ' + repr(v)
                              for k, v in sorted(self.items())])+"\n}"
        else:
            return self.__class__.__name__ + "()"

    def __dir__(self):
        return list(self.keys())

def get_data(path):
    path_ = path.replace("\\", "/")
    path_lst = path.split("/")
    path_len = len(path_lst)
    data = DictObj()

    for root, dirs, files in os.walk(path):
        root_ = root.replace("\\", "/")
        root_lst = root_.split("/")[path_len:]
        rt = data
        for branch in root_lst:
            rt = rt[branch]

        for dir_ in dirs:
            rt[dir_] = DictObj()
        
        rt.files = files
        for file_ in files:
            if file_.endswith(".json"):
                with open(root + "/" + file_, 'r') as f:
                    rt[file_[:-5]] = DictObj(**json.load(f))
        
    return data


def init_game(data_path):
    """
    this has to get all the necessary data or at least have a reference
    to it so all the necessary data can be found.
    """        
    pg.init()
    pg.display.set_caption("RCA")
    # Set up all sprite groups
    all_sprites = pg.sprite.Group() # everything
    background  = pg.sprite.Group() # background tiles
    foreground  = pg.sprite.Group() # non-interacting block
    block       = pg.sprite.Group() # non-moving sprites that interact
    player      = pg.sprite.Group() # sprites you can control             
    friend      = pg.sprite.Group() # moving friendly sprites
    foe         = pg.sprite.Group() # enemies
    hud         = pg.sprite.Group() # HUD (health, money etc.)
    misc        = pg.sprite.Group() # other (dialog boxes etc.)
    # set up groups list (in the order in which you want them to be drawn)
    groups = [background, foreground, block, player, friend, foe, hud, misc]

    # define groups that are diegetic (i.e. groups that exist in the game
    # world and will be affected by camera movement) EXCLUDES player
    diegetic_groups = [background, foreground, block, friend, foe]

    game = DictObj(
        data_path = data_path,
        data = get_data(data_path),
        clock = pg.time.Clock(),
        screen = pg.display.set_mode(SCREENSIZE),
        accept_input = True,
        keys_pressed = [],
        running = True,
        groups = groups,
        diegetic_groups = diegetic_groups,
        all_sprites = all_sprites,
        background = background,
        foreground = foreground,
        block = block,
        player = player,         
        friend = friend,
        foe = foe,
        hud = hud,
        misc = misc,
        events = [],
        on_keys = [],
        off_keys = [],
    )

    load_zone("zone1", game)
    
    return game

    
def engine(game):
    """
    Running this function will execute the initialized game.
    """
    
    while game.running:
        events(game)
        logic(game)
        draw(game)
        
        game.clock.tick(FPS)
    pg.quit()

    
def events(game):
    """
    Captures all events input by the user and updates the event variables
    """
    game.events = []
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game.running = False
            return
        game.events.append(event)

    new_keys = pg.key.get_pressed()
    if new_keys[pg.K_BACKSPACE]:
        game.running = False
        return

    # disregard numlock key
    if pg.K_NUMLOCK in new_keys: new_keys.remove(pg.K_NUMLOCK)
    
    old_keys = game.on_keys.copy()
    game.on_keys = list(compress(range(len(new_keys)), new_keys))
    game.off_keys = list(set(old_keys).difference(game.on_keys))


def logic(game):
    game.all_sprites.update()

    
def draw(game):
    """
    Once the game logic method has run, this function updates all sprites
    based on what the logic method did and then draws the next frame in an
    order specified by the game manager.
    """
    game.screen.fill(BLACK)
    for group in game.groups:
        group.draw(game.screen)
    
    pg.display.flip()

        
def gen_sprite(path, scale=1):
    sprite = pg.sprite.Sprite()
    sprite.image = pg.image.load(path).convert_alpha()
    width, height = sprite.image.get_size()
    width *= scale
    height *= scale
    sprite.image = pg.transform.scale(
        sprite.image,(int(width), int(height))
    )
    sprite.rect = sprite.image.get_rect()
    sprite.width = sprite.image.get_width()
    sprite.height = sprite.image.get_height()
    sprite.mask = pg.mask.from_surface(sprite.image)
    
    return sprite
    

def load_zone(zone_str, game, player_init=None):
    zone = game.data.sprites.zones[zone_str]
    assert zone.type == "zone"
    env = DictObj(**zone.environment)
    bg = gen_sprite(env.background)
    fg = gen_sprite(env.foreground)
    bg.rect.x, bg.rect.y = env.xy
    fg.rect.x, fg.rect.y = env.xy
    bg.add(game.all_sprites, game.background)
    fg.add(game.all_sprites, game.foreground)

    for block in zone.blocks:
        b = DictObj(**block)
        bsprite = gen_sprite(b.image_path)
        bsprite.rect.x, bsprite.rect.y = env.xy
        bsprite.add(game.all_sprites, game.block)

    if player_init is None:
        # player = game.data.sprites.player
        player = gen_sprite(
            "./data/sprites/player/larry_st_S.png",
            scale=3
        )
        player.rect.x, player.rect.y = CENTERX, CENTERY
        player.add(game.all_sprites, game.player)
