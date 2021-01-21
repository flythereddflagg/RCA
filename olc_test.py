import numpy as np
import pygame as pg

SCRNW, SCRNH = 600, 400
SCREENSIZE = SCRNW, SCRNH 
ASPECT_RATIO = SCRNH / SCRNW
ZNEAR, ZFAR = 0.1, 1000
THETA = np.radians(90)
FOV = 1 / np.tan(THETA / 2)
Q = ZFAR / (ZFAR - ZNEAR)

FPS = 30
BLACK = 0, 0, 0

PROJECTION_MATRIX = np.array([
    [ASPECT_RATIO*FOV,   0,           0,         0],
    [0,                FOV,           0,         0],
    [0,                  0,           Q,         1],
    [0,                  0,    -ZNEAR*Q,         0]
])


def init():
    pg.init()
    game = {}
    game["running"] = True
    game["screen"] = pg.display.set_mode(SCREENSIZE)
    game["clock"] = pg.time.Clock()

    game["meshcube"] = np.array([
        [[0,0,0], [0,1,0], [1,1,0]], # S
        [[0,0,0], [1,1,0], [1,0,0]],

        [[1,0,0], [1,1,0], [1,1,1]], # E
        [[1,0,0], [1,1,1], [1,0,1]],
        
        [[1,0,1], [1,1,1], [0,1,1]], # N
        [[1,0,1], [0,1,1], [0,0,1]],
        
        [[0,0,1], [0,1,1], [0,1,0]], # W
        [[0,0,1], [0,1,0], [0,0,0]],
        
        [[0,1,0], [0,1,1], [1,1,1]], # TOP
        [[0,1,0], [1,1,1], [1,1,0]],
        
        [[0,0,0], [1,0,0], [0,0,1]], # BOTTOM
        [[0,0,0], [0,0,1], [1,0,0]],
    ], dtype=np.float64)
    game["xtheta"] = np.radians(0.03)
    game["ytheta"] = np.radians(0.07)
    game["ztheta"] = np.radians(0.05)

    game['t_elapsed'] = 0
    return game


def draw_triangle(tri, display, color=(255, 255, 255), width=1):
    # tri should be of shape (3, 2)
    for i in range(len(tri)):
        pg.draw.line(display, color, tri[i-1], tri[i])

def transform_tri(tri, transform_matrix):

    ext_tri = np.hstack([tri, np.ones(3).reshape([3,1])])
    p_tri = ext_tri @ transform_matrix
    return p_tri[:,:2] / p_tri[:, 2].reshape([3,1])


def events(game):
    # capture input here
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game["running"] = False
            return


def logic(game):
    # execute logic here
    pass


def draw(game):
    # draw everything here
    game["screen"].fill(BLACK)
    game['t_elapsed'] += game["clock"].get_time()
    xtheta = game["xtheta"] * game['t_elapsed']
    ytheta = game["ytheta"] * game['t_elapsed']
    ztheta = game["ztheta"] * game['t_elapsed']

    x_rot = np.array([
        [1,             0,                0],
        [0, np.cos(xtheta), -np.sin(xtheta)],
        [0, np.sin(xtheta),  np.cos(xtheta)]
    ])
    y_rot = np.array([
        [ np.cos(ytheta), 0, np.sin(ytheta)],
        [             0,  1,              0],
        [-np.sin(ytheta), 0, np.cos(ytheta)]
    ])
    z_rot = np.array([
        [np.cos(ztheta), -np.sin(ztheta), 0],
        [np.sin(ztheta),  np.cos(ztheta), 0],
        [            0,                0, 1],
    ])

    for tri in game["meshcube"]:
        # rotation transform

        tri = tri @ x_rot
        tri = tri @ y_rot
        tri = tri @ z_rot

        ttri = tri.copy()
        for i in range(ttri.shape[0]):
            ttri[i][2] += 3.0

        p_tri = transform_tri(ttri, PROJECTION_MATRIX)
        for i in range(p_tri.shape[0]):
            for j in range(p_tri.shape[1]):
                p_tri[i][j] += 1.0
            p_tri[i][0] *= 0.5 * SCRNW
            p_tri[i][1] *= 0.5 * SCRNH
 

        draw_triangle(p_tri, game["screen"])


    pg.display.flip()


def engine(game):
    
    while game["running"]:
        events(game)
        logic(game)
        draw(game)

        game["clock"].tick(FPS)
    
    pg.quit()


if __name__ == "__main__":
    init_data = init()
    engine(init_data)