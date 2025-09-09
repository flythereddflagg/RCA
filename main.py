"""
File: main.py
The main() entry point for the game. 
Initializes the game from a data file and initiates the game
"""
def main():
    import pygame as pg
    from src import Engine
    pg.init()
    INIT_PATH = "./assets/init.yaml"
    game = Engine(INIT_PATH)
    
    if game.settings.LOG_INPUT:
        import datetime
        try:
            game.run()
        finally:
            write_log(game)
    else:
        game.run()
    
    # game.save_game()
    pg.display.quit()
    pg.quit()
    print("Game ended successfully!")


def write_log(game):
    with open("./VERSION") as f:
        VERSION = f.read().strip()
    filename = (
        f"./replay_{VERSION}"\
        f"_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.icl"
    )
    with open(filename, 'w') as f:
        output = "\n".join([
            "|".join([str(i) for i in line]) 
            for line in game.input.input_record
        ])
        f.write(output)


if __name__ == "__main__":
    main()


# GENERAL TO-DO LIST
# TODO make meaningful TESTS
# TODO make a pause and save screen or whatever
# TODO flesh out HUD
# TODO make scene transitions a la LTTP (polish)
# TODO: Larry AND Holly are playable with these items but both play differently and have different exits at the end (e.g. Larry has less knockback from bludgeoning but is more susceptible to piercing while Holly is the opposite.) (exits are the Original exit to the village and the exit to the mountain or something TBD)
# TODO: A good amount of polish so that the game is "complete"
