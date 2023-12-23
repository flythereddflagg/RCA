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
