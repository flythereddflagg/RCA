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
    if game.LOG_INPUT:
        import datetime
        try:
            game.run()
        finally:
            with open("./VERSION") as f:
                VERSION = f.read().strip()
            with open(f"./replay_{VERSION}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.icl", 'w') as f:
                output = "\n".join([
                    "|".join(line) 
                    for line in game.input.input_record
                ])
                f.write(output)
            pg.display.quit()
            pg.quit()
            print("Game ended successfully!")
    else:
        game.run()
        pg.display.quit()
        pg.quit()
        print("Game ended successfully!")


if __name__ == "__main__":
    main()


# make sure you are building out a good framework as you go!!!!

# GENERAL TO-DO LIST
# TODO remap controller from XBOX standard?
# TODO rewrite UML for updated data structure SCHEME
# TODO make meaningful TESTS
# TODO make a pause and save screen or whatever
# TODO flesh out HUD
# TODO make a startup screen
# TODO make a load screen
# TODO make scene transitions a la LTTP (polish)
# TODO make a global zoom that scales the game to the size of the monitor
# TODO make the game dynamically adjust zoom based on window size

# TODO: Basic story and story beats from the first game
# TODO: Items: [ ✓sword, ✓shovel, pickle, gate key, statue key]
# TODO: Item mechanics completely fleshed out
# TODO: Larry AND Holly are playable with these items but both play differently and have different exits at the end (e.g. Larry has less knockback from bludgeoning but is more susceptible to piercing while Holly is the opposite.) (exits are the Original exit to the village and the exit to the mountain or something TBD)
# TODO: Enemies: [ wolf, ossifrage, goblin (club and arrows), and Rouken the dragon]
# TODO: Boss fight must have cheese in the form of the chandelier
# TODO: Basic parallax in the background or major foreground
# TODO: A good amount of polish so that the game is "complete"
# TODO: setup an autobuild system