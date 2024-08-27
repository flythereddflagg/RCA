import pygame as pg


good_keys = {
    "REFRESH": "u",
    "FORCE_QUIT": "backspace",
    "START": "return",
    "SELECT": "p",
    "UP": "up",
    "DOWN": "down",
    "LEFT": "left",
    "RIGHT": "right",
    "BUTTON_1": "x",
    "BUTTON_2": "z",
}

# for key, kid in key_list.items():
#     print(f"{key:20}: {kid:20}")


pg.init()
key_list = {
    vars(pg)[key]:key 
    for key in filter(
        lambda x: x.startswith("K_"), 
        sorted(pg.__dict__.keys())
    )
}
screen = pg.display.set_mode([200,200], pg.RESIZABLE)
clock = pg.time.Clock()
pressed = pg.key.get_pressed()
print(len(pressed), "keys detected")
while  not pressed[pg.K_BACKSPACE]:
    events = pg.event.get()
    if pg.QUIT in [event.type for event in events]: break
    pressed = pg.key.get_pressed()
    pressed_keys = [
        name 
        for name, key in good_keys.items()
        if pressed[pg.key.key_code(key)]
    ]
    if pressed_keys: print(pressed_keys)
    clock.tick(30)
pg.display.quit()
pg.quit()