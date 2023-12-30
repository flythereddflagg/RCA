"""
File: main.py
The main() entry point for the game. 
Initializes the game from a data file and initiates the game
"""
def main():
    from src import init_game, run_game

    INIT_SETTINGS_PATH = "./assets/__init__.yaml"
    
    game_data = init_game(INIT_SETTINGS_PATH)
    run_game(game_data)


if __name__ == "__main__":
    main()


# make sure you are building out a good framework as you go!!!!

# GENERAL TO-DO LIST
# TODO rewrite UML for updated data structure SCHEME
# TODO write down character and enemy ideas
# TODO make at least three enemies (not including the dragon)
# TODO make meaningful TESTS
# TODO make a pause and save screen or whatever
# TODO make an inventory system
# TODO flesh out HUD
# TODO make a startup screen
# TODO make a load screen
# TODO make controllers work
# TODO implement the RCA W1 story
