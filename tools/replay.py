
def main():
    import sys
    sys.path.append(".")
    import pygame as pg
    from src import GameState
    input_file = sys.argv[1]
    pg.init()
    INIT_PATH = "./assets/__init__.yaml"
    game = GameState(INIT_PATH, REPLAY=input_file)
    game.run()
    
    pg.display.quit()
    pg.quit()
    print("Game ended successfully!")


if __name__ == "__main__":
    main()