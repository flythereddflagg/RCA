if __name__ == "__main__":
    test_controller = True
    import sys
    sys.path.append("..")
    from RCA.src.tools import load_yaml
    from RCA.src.input import Input 
    import pygame as pg

    pg.init()
    game = load_yaml("./tests/input_test.yaml")
    input_obj = Input(game)
    input_gotten = []
    # while "QUIT" not in input_gotten:
    while True:
        input_obj.update()
        input_gotten = input_obj.get()
        if test_controller:
            print(f"\r{str(input_obj.controller_state):100}", end="")
        elif input_gotten:
            print(f"\r{str(input_gotten):100}", end="")

    pg.quit()
    print()

