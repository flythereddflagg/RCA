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
# primary_loop: [0.0, 10, 5]
    
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
    start_time = 0
    while running:
        try:
            node.update()
            if pg.time.get_ticks() - start_time > 250:
                print(node.current_loop_time())
                start_time = pg.time.get_ticks()
            clock.tick(90)
        except KeyboardInterrupt:
            running = False
    pg.quit()


if __name__ == "__main__":
    main()