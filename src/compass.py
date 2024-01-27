import pygame as pg
# by convention, order is ALWAYS up, right, down, left or 0, 1, 2, 3
N_DIRECTIONS = 4

class Compass():
    indicies = [i for i in range(N_DIRECTIONS)]
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

    @staticmethod
    def index(direction:int|str|tuple|pg.math.Vector2)->int:
        """returns the closest direction index of the direction"""
        if isinstance(direction, int) and 0 <= direction < N_DIRECTIONS:
            return direction
        if any(map(lambda x: isinstance(direction, x), [str, tuple])):
            return Compass.i_map[direction]
        
        if not isinstance(direction, pg.math.Vector2): raise ValueError(
            "Given direction must be of type: int|str|tuple|pg.math."\
            f"Vector2, got {type(direction)}"
        )
        x, y = direction
        if abs(x) < abs(y):
            return Compass.i_map[(tuple(pg.math.Vector2(0, y).normalize()))]
        
        return Compass.i_map[tuple(pg.math.Vector2(x, 0).normalize())]
    
    @staticmethod
    def string(direction:int|str|tuple|pg.math.Vector2)->str:
        """returns the closest direction string of the direction"""
        return Compass.str_map[Compass.index(direction)]

    @staticmethod
    def unit_vector(direction:int|str|tuple|pg.math.Vector2)->tuple:
        """returns the cloest unit vector direction 
        to the given the direction"""
        return Compass.vec_map[Compass.index(direction)]
    
    @staticmethod
    def vector(direction:int|str|tuple|pg.math.Vector2)->pg.math.Vector2:
        """Returns the normalized vector in the given direction"""
        if any(map(lambda x: isinstance(direction, x), [int, str, tuple])):
            return pg.math.Vector2(Compass.unit_vector(direction))
        if not isinstance(direction, pg.math.Vector2): raise ValueError(
            "Given direction must be of type: int|str|tuple|pg.math."\
            f"Vector2, got {type(direction)}"
        )
        return direction.normalize()

    @staticmethod
    def opposite(direction:int|str|tuple|pg.math.Vector2)->pg.math.Vector2:
        """
        returns a normalized vector pointing in the opposite 
        direction as a pg.math.Vector2
        """
        if any(map(lambda x: isinstance(direction, x), [int, str, tuple])):
            direction = pg.math.Vector2(Compass.unit_vector(direction))
        return direction.rotate(180).normalize()

