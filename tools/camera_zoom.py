import pygame as pg

BLACK = (0,0,0)
SCALE_RUN = 1.05

def gen_from_iter(iter_):
    while True:
        for thing in iter_:
            yield thing

class TestSprite(pg.sprite.Sprite):
    def __init__(self, img_path):
        super().__init__()
        self.image = pg.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (200,200)
        self.scale_gen = gen_from_iter(
            # [SCALE_RUN]*3 + [1/SCALE_RUN]*3
            [SCALE_RUN, 1/SCALE_RUN]
        )
        self.last_time = 0
        self.cur_scale = 1
        self.original_image = self.image
        self.original_size = self.original_image.get_rect().size
        self.scale_factor = 1

    def update(self):

        curtime = pg.time.get_ticks()
        if curtime - self.last_time > 1000:
            self.last_time = curtime
            self.scale_factor = next(self.scale_gen)
        self.scale(self.scale_factor)
        print(self.cur_scale)


    def scale(self, factor):
        self.cur_scale *= factor
        if self.cur_scale < 1: self.cur_scale = 1
        pos = self.rect.center
        new_size = [dim * self.cur_scale for dim in self.original_size]
        self.image = pg.transform.scale(self.original_image, new_size)
        self.rect = self.image.get_rect()
        self.rect.center = pos

def main():
    IMG_PATH = "./assets/dummy/block.png"
    pg.init()
    screen = pg.display.set_mode([400,400], pg.RESIZABLE)
    clock = pg.time.Clock()
    background = TestSprite(IMG_PATH)
    scene = pg.sprite.Group()
    scene.add(background)
    running = True
    while running:
        events = pg.event.get()
        if pg.QUIT in [event.type for event in events]:
            running = False
        scene.update()
        screen.fill(BLACK)
        scene.draw(screen)
        pg.display.flip()
        clock.tick(30)

    pg.quit()

if __name__ == '__main__':
    main()