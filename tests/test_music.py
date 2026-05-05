import sys
sys.path.append("..")

from yaml import load, Loader
import pygame as pg

from RCA.src.music import Music

INIT = """
id: music
type: Music
filename: ./assets/music/red_castle_valley.mp3
groups: [paused]
# start at, loop at, loop_to
primary_loop: [0.0, 107.197, 55.512]
    
"""
class Fake_Game:
    settings= {"DEBUG":False}
    music_volume = 10
class Fake_Scene:
    game = Fake_Game()
    


def main():
    pg.init()
    clock = pg.time.Clock()
    running = True
    init_dict = load(INIT, Loader=Loader)
    node = Music(scene=Fake_Scene(), parent=None, **init_dict)
    while running:
        node.update()
        clock.tick(90)
    pg.quit()


if __name__ == "__main__":
    main()