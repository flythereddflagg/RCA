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


"""
list of things that are bugging me about the game so far
none of this should be content. These are things that I
need to fix before the game is "done".
Each item may have a priority from 1 - 5
1: game breaking/driving me nuts
2: high priority
3: we do need to get to it eventually
4: nice to have but not necessary for MVP
5: we get to it when we get to it
---

TODO -1- picked up item sound
TODO -3- make cave/forest exit bigger
TODO -1- shovel noise
TODO -1- add alley way theme and mansion yard theme
TODO -1- sword swing noise
TODO -1- sword hit noise
TODO -3- weapon hit pause animation
TODO -1- meatball death animation
TODO -1- fix all the music loop issues!
TODO -1- statue animation and sound
TODO -1- rosie crash/splash sound
TODO -1- gate animation and sound
TODO -1- Music loop for FeyFrog
TODO -1- Shorten Game Over music
TODO -1- Make a proper end sequence with Neverending story reference, crack and wooshing wind sound

TODO -2- add animations and flesh out combat with fey frog
TODO -2- add final story elements
TODO -3- make glyphs and keystrokes correspond to various inputs keyboard or otherwise
TODO -3- make DPAD a valid way to move the character
TODO -4- tighten up music with loops USE TENACITY?
TODO -4- make inventory have proper labeling too!
TODO -4- make it possible to upload feedback from the menu
TODO -4- animate the river/waterfall
TODO -4- refactor the menu system to be unified
TODO -3- make meaningful TESTS
TODO -3- make scene transitions a la LTTP (polish)
TODO -4- Larry AND Holly are playable with these items but both play differently and have different exits at the end (e.g. Larry has less knockback from bludgeoning but is more susceptible to piercing while Holly is the opposite.) (exits are the Original exit to the village and the exit to the mountain or something TBD)
TODO -3- A good amount of polish so that the game is "complete"
TODO -4- add shadow and floating animation?
TODO -4- change all music formats to .ogg
TODO -4- add controller input mappings to options menu
TODO -4- add doc strings to all core files
TODO -4- make a core package in src with node and scene and stuff like that
TODO -3- add a drop item mechanic in inventory
"""
