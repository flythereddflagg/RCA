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
# TODO make a weapon that the player can use (PUNCH?)
# TODO make a simple fight with complete animations
# TODO make a trigger that transfers to the next scene
# TODO rewrite UML for updated data structure SCHEME
# TODO write down character and enemy ideas
# TODO make meaningful TESTS
# TODO make a pause and save screen or whatever
# TODO make an inventory system
# TODO make a startup screen
# TODO make controllers work
# TODO implement the RCA W1 story
