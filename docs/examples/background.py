import pygame as pg
from math import sin, cos, pi

"""
Challenge from:
http://www.101computing.net/getting-started-with-pygame/
"""
pg.init()

BLACK      = (0,0,0)
WHITE      = (255,255,255)
GREEN      = (0,255,0)
RED        = (255,0,0)
SKYBLUE    = (53,193,240)
TREEGREEN  = (32,143,26)
GRASSGREEN = (26,227,16)
YELLOW     = (255,255,0)
BROWN      = (143,78,26)

win_width = 700
win_height = 500
window_size = (win_width, win_height)
screen = pg.display.set_mode(window_size)
pg.display.set_caption("My first game")

running = True

FPS = 30
clock = pg.time.Clock()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    # Game logic here
    # Drawing code here
    screen.fill(SKYBLUE) # sky
    # sun and rays
    pg.draw.circle(screen, YELLOW, [75,75],20)
    pg.draw.line(screen, YELLOW, [10,75], [45,75])
    pg.draw.line(screen, YELLOW, [75,10], [75,45])
    pg.draw.line(screen, YELLOW, [105,75], [140,75])
    pg.draw.line(screen, YELLOW, [75,105], [75,140])
    pg.draw.line(screen, YELLOW, 
        [75+int(cos(pi/4.0)*30),75+int(sin(pi/4.0)*30)], 
        [75+int(cos(pi/4.0)*65),75+int(sin(pi/4.0)*65)])
    pg.draw.line(screen, YELLOW, 
        [75-int(cos(pi/4.0)*30),75-int(sin(pi/4.0)*30)], 
        [75-int(cos(pi/4.0)*65),75-int(sin(pi/4.0)*65)])
    pg.draw.line(screen, YELLOW, 
        [75+int(cos(3*pi/4.0)*30),75+int(sin(3*pi/4.0)*30)], 
        [75+int(cos(3*pi/4.0)*65),75+int(sin(3*pi/4.0)*65)])
    pg.draw.line(screen, YELLOW, 
        [75-int(cos(3*pi/4.0)*30),75-int(sin(3*pi/4.0)*30)], 
        [75-int(cos(3*pi/4.0)*65),75-int(sin(3*pi/4.0)*65)])
    
    # grass
    # rectangle area is top left posx, posy, width, height
    pg.draw.rect(screen, GRASSGREEN, 
        [0, win_height*3//4, win_width, win_height//4])
    #tree
    pg.draw.rect(screen, BROWN, 
        [win_width*3//4, 
        win_height*3//4-150, 
        20, 
        150])
    pg.draw.ellipse(screen, TREEGREEN, 
        [win_width*3//4-30, 
        win_height*3//4-int(150*1.5), 
        80, 
        150])

    # update the screen with all the new changes
    pg.display.flip()
    
    clock.tick(FPS)
    
pg.quit()
    
