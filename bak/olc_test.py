import numpy as np
import pygame as pg

SCRNW, SCRNH = 600, 400
SCREENSIZE = SCRNW, SCRNH 
ASPECT_RATIO = SCRNH / SCRNW
ZNEAR, ZFAR = 0.1, 1000
THETA = np.radians(90)
FOV = 1 / np.tan(THETA / 2)
Q = ZFAR / (ZFAR - ZNEAR)

V_CAMERA = 0, 0, 0 # camera position
FPS = 30
BLACK = 0, 0, 0

PROJECTION_MATRIX = np.array([
    [ASPECT_RATIO*FOV,   0,           0,         0],
    [0,                FOV,           0,         0],
    [0,                  0,           Q,         1],
    [0,                  0,    -ZNEAR*Q,         0]
])



def load_obj_file(path, offset=1):
    with open(path, 'r') as f:
        lines = f.readlines()
    vertices = []
    faces = []
    for line in lines:
        s_line = line.split(' ')
        if line.startswith("v"):
            vertices.append([float(x) for x in s_line[1:]])
        elif line.startswith('f'):
            faces.append([int(x) for x in s_line[1:]])
    
    mesh = np.zeros((len(faces), 3, 3))
    # print(np.amax(faces), len(vertices))
    # raise Exception()
    for i, face in enumerate(faces):
        mesh[i] += np.array([vertices[j-offset] for j in face])
    
    return mesh



def init():
    pg.init()
    game = {}
    game["running"] = True
    game["screen"] = pg.display.set_mode(SCREENSIZE)
    game["clock"] = pg.time.Clock()

    game["meshcube"] = load_obj_file("./weird_thing.obj")
    game["xtheta"] = np.radians(0.03)
    game["ytheta"] = np.radians(0.07)
    game["ztheta"] = np.radians(0.05)

    game['t_elapsed'] = 0
    return game


def draw_triangle(tri, display, color=(255, 255, 255), width=0):
    # tri should be of shape (3, 2)
    pg.draw.polygon(display, color, tri, width=width)

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
    
    new_mesh = game["meshcube"].copy()
    for i, tri in enumerate(game["meshcube"]):
        # rotation transform
        tri = tri @ x_rot
        tri = tri @ y_rot
        tri = tri @ z_rot
        new_mesh[i][:] = tri
    
    new_mesh = np.array(sorted(new_mesh, key=lambda x: sum(y[2] for y in x)/3, reverse=True))
    for tri in new_mesh:
        # translation transform    
        ttri = tri.copy()
        for i in range(ttri.shape[0]):
            ttri[i][2] += 10.0
        # check normal of triangle to camera to see if we should render it
        line1 = ttri[1] - ttri[0]
        line2 = ttri[2] - ttri[0]
        normal = np.cross(line1, line2)
        nnorm = normal / np.linalg.norm(normal)
        if np.dot(nnorm, (ttri[0] - V_CAMERA)) > 0:
            continue
        
        # set the lighting of the triangle
        light_direction = np.array([0.0, 0.0, -1.0])
        light_direction /= np.linalg.norm(light_direction)
        # dot the values together to get the luminace
        level = np.dot(nnorm, light_direction)
        level_mod = level*0.9 + 0.05
        if level_mod < 0: level_mod = 0 # BUG fix this
        white = np.array([255, 255, 255])
        color = tuple(level_mod*white)
        line_w = 0

        # project triangle into 2d space
        p_tri = transform_tri(ttri, PROJECTION_MATRIX)
        for i in range(p_tri.shape[0]):
            for j in range(p_tri.shape[1]):
                p_tri[i][j] += 1.0
            p_tri[i][0] *= 0.5 * SCRNW
            p_tri[i][1] *= 0.5 * SCRNH
 

        draw_triangle(p_tri, game["screen"], color=color, width=line_w)


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