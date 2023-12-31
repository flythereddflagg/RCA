import pygame as pg

for key in filter(lambda x: x.startswith("K_"), sorted(pg.__dict__.keys())):
    kid = pg.__dict__[key]
    print(f"{key:20}: {kid:20} {kid%512}")

pg.init()
print(len(pg.key.get_pressed()))
pg.quit()