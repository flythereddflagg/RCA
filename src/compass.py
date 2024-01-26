import pygame as pg
# by convention, order is ALWAYS up, right, down, left or 0, 1, 2, 3
N_DIRECTIONS = 4

class Compass():
    indicies = [i for i in range(N_DIRECTIONS)]
    opposite = indicies[:N_DIRECTIONS//2] + indicies[N_DIRECTIONS//2:]
    strings = ["UP", "RIGHT", "DOWN", "LEFT"]
    unit_vectors = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    UP, RIGHT, DOWN, LEFT = indicies
    vec_map = {
        **{s: v for s, v in zip(strings, unit_vectors)},
        **{i: v for i, v in zip(indicies, unit_vectors)}
    }
    str_map = {
        **{v: s for s, v in zip(strings, unit_vectors)},
        **{i: s for i, s in zip(indicies, strings)}
    }
    i_map = {
        **{s: i for s, i in zip(strings, indicies)},
        **{v: i for i, v in zip(indicies, unit_vectors)}
    }
    UP, RIGHT, DOWN, LEFT = indicies

    @staticmethod
    def index(direction:int|str|tuple|pg.math.Vector2)->int:
        """returns the closest direction index of the direction"""
        if isinstance(direction, int) and direction < N_DIRECTIONS:
            return direction
        if any(map(lambda x: isinstance(direction, x), [str, tuple, int])):
            return i_map[direction]
        
        x, y = direction.normalize()
        if abs(x) < abs(y):
            return i_map[tuple(pg.math.Vector2(0, y).normalize())]
        
        return i_map[tuple(pg.math.Vector2(x, 0).normalize())]

    # TODO implement the rest of these for the other maps
