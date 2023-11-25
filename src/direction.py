# by convention, order is ALWAYS up, right, down, left or 0, 1, 2, 3

class Compass():
    indicies = [i for i in range(4)]
    strings = ["UP", "RIGHT", "DOWN", "LEFT"]
    unit_vectors = [( 0, -1), ( 1,  0), ( 0, -1), (-1,  0),]
    vec_map = {
        **{s: v for s, v in zip(strings, unit_vectors)},
        **{i: v for i, v in zip(indicies, unit_vectors)}
    }
    d_key = {
        **{v: s for s, v in zip(strings, unit_vectors)},
        **{i: s for i, s in zip(indicies, strings)}
    }
    index = {
        **{s: i for s, i in zip(strings, indicies)},
        **{v: i for i, v in zip(indicies, unit_vectors)}
    }
    UP, RIGHT, DOWN, LEFT = indicies
    # FIXME add the compass functionality to all code (refactor needed)