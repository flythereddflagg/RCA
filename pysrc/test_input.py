if __name__ == "__main__":
    test_controller = True
    import sys
    sys.path.append("..")
    from RCA.src.tools import load_yaml
    from RCA.src.input import Input 
    import pygame as pg

    pg.init()
    clock = pg.time.Clock()
    game = load_yaml("./assets/init.yaml")
    display = pg.display.set_mode((300, 300))
    input_obj = Input(game)
    input_gotten = []
    # while "QUIT" not in input_gotten:
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False  # Flag that we are done so we exit this loop.
        input_obj.update()
        input_gotten = input_obj.get()
        print(input_gotten)
        clock.tick(30)


    pg.quit()
    print()

