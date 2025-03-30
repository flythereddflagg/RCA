import time
import pygame as pg

import src

def init_dummy_game():
    pg.init()
    screen = pg.display.set_mode([100, 100])
    return screen


def end_game():
    pg.display.quit()
    pg.quit()

def alt_move(self, direction, distance):
        xunit, yunit = direction
        addx, addy = distance * xunit, distance * yunit
        self.rect.x += addx 
        self.rect.y += addy

def test_Character():
    screen = init_dummy_game()
    char = src.sprite.Character(None, "./assets/dummy/character.png")
    n_times = 1000
    ptime = []
    alt_ptime = []
    for i in range(n_times):
        t1 = time.perf_counter_ns()
        char.move([0,1], 10.0)
        t2 = time.perf_counter_ns()
        ptime.append(t2-t1)
        t1 = time.perf_counter_ns()
        alt_move(char, [0,1], 10.0)
        t2 = time.perf_counter_ns()
        alt_ptime.append(t2-t1)
    avg, alt_avg = sum(ptime)/n_times, sum(alt_ptime)/n_times
    print(avg, alt_avg, abs(avg - alt_avg)/avg*100)
    end_game()
    assert abs(avg - alt_avg)/avg*100 > 30.0 and alt_avg < avg
