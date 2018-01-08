import pygame as pg, random
from math import sin, cos, pi
from car import Car

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

GREEN = (20, 255, 140)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
BLUE = (100, 100, 255)


speed = 1
colorList = (RED, GREEN, PURPLE, YELLOW, CYAN, BLUE)

win_width = 700
win_height = 500
window_size = (win_width, win_height)
screen = pg.display.set_mode(window_size)
pg.display.set_caption("Car Racing")

all_sprites_list = pg.sprite.Group()

pCar = Car(RED, 60, 80, 70)
pCar.rect.x = 160
pCar.rect.y = win_height - 100


car1 = Car(PURPLE, 60, 80, random.randint(50,100))
car1.rect.x = 60
car1.rect.y = -100
 
car2 = Car(YELLOW, 60, 80, random.randint(50,100))
car2.rect.x = 160
car2.rect.y = -600
 
car3 = Car(CYAN, 60, 80, random.randint(50,100))
car3.rect.x = 260
car3.rect.y = -300
 
car4 = Car(BLUE, 60, 80, random.randint(50,100))
car4.rect.x = 360
car4.rect.y = -900


all_sprites_list.add(pCar)
all_sprites_list.add(car1)
all_sprites_list.add(car2)
all_sprites_list.add(car3)
all_sprites_list.add(car4)

all_coming_cars = pg.sprite.Group()
all_coming_cars.add(car1)
all_coming_cars.add(car2)
all_coming_cars.add(car3)
all_coming_cars.add(car4)

running = True

FPS = 60
clock = pg.time.Clock()

def draw_background(screen):
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



while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_x:
                running = False
    
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT] and pCar.rect.x > 0:
        pCar.moveLeft(5)
    if keys[pg.K_RIGHT] and pCar.rect.x < win_width - 20:
        pCar.moveRight(5)
    if keys[pg.K_UP]:
        speed += 0.05
    if keys[pg.K_DOWN]:
        speed -= 0.05
    
    
    # Game logic here
    for car in all_coming_cars:
        car.moveForward(speed)
        if car.rect.y > win_height:
            car.changeSpeed(random.randint(50,100))
            car.repaint(random.choice(colorList))
            car.rect.y = -200
    
    car_collsion_list = pg.sprite.spritecollide(pCar, all_coming_cars, False)
    for car in car_collsion_list:
        print("Car Crash!!!")
        running = False
    
    all_sprites_list.update()
    # Drawing code here
    draw_background(screen)
    # draw all the sprites
    all_sprites_list.draw(screen)
    
    # update the screen with all the new changes
    pg.display.flip()
    
    clock.tick(FPS)
    
pg.quit()
    
