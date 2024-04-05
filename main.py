"""
File: main.py
The main() entry point for the game. 
Initializes the game from a data file and initiates the game
"""
def main():
    import pygame as pg
    from src import GameState

    pg.init()
    INIT_PATH = "./assets/__init__.yaml"
    game = GameState(INIT_PATH)
    game.run()
    
    pg.display.quit()
    pg.quit()
    print("Game ended successfully!")


if __name__ == "__main__":
    main()


# make sure you are building out a good framework as you go!!!!

# GENERAL TO-DO LIST
# TODO rewrite UML for updated data structure SCHEME
# TODO write down character and enemy ideas
# TODO make at least three enemies (not including the dragon)
# TODO make meaningful TESTS
# TODO make a pause and save screen or whatever
# TODO flesh out HUD
# TODO make a startup screen
# TODO make a load screen
# TODO implement the RCA W1 story
# TODO make scene transitions a la LTTP (polish)
# TODO make a global zoom that scales the game to the size of the monitor
# TODO implement Emma's character
