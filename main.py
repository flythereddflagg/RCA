# the main function of the game
def main():
    from src import init_game, run_game
    
    game = init_game("./assets/__init__.yaml")
    run_game(game)


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
