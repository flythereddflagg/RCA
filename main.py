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
    import datetime
    with open("./VERSION") as f:
        VERSION = f.read().strip()
    filename = (
        f"./replay_{VERSION}"\
        f"_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.icl"
    )
    with open(filename, 'w') as f:
        output = "\n".join([
            "|".join([str(i) for i in line]) 
            for line in game.input.input_log
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

maybe do -1- picked up item sound
maybe do -3- make cave/forest exit bigger
maybe do -1- shovel noise
maybe do -1- add alley way theme and mansion yard theme
maybe do -1- sword swing noise
maybe do -1- sword hit noise
maybe do -3- weapon hit pause animation
maybe do -1- meatball death animation
maybe do -1- statue animation and sound
maybe do -1- rosie crash/splash sound
maybe do -1- gate animation and sound
maybe do -1- Music loop for FeyFrog
maybe do -1- Shorten Game Over music
maybe do -1- Make a proper end sequence with Neverending story reference, crack and wooshing wind sound

maybe do -2- add animations and flesh out combat with fey frog
maybe do -2- add final story elements
maybe do -3- make glyphs and keystrokes correspond to various inputs keyboard or otherwise
maybe do -3- make DPAD a valid way to move the character
maybe do -4- tighten up music with loops USE TENACITY?
maybe do -4- make inventory have proper labeling too!
maybe do -4- make it possible to upload feedback from the menu
maybe do -4- animate the river/waterfall
maybe do -4- refactor the menu system to be unified
maybe do -3- make meaningful TESTS
maybe do -3- make scene transitions a la LTTP (polish)
maybe do -4- Larry AND Holly are playable with these items but both play differently and have different exits at the end (e.g. Larry has less knockback from bludgeoning but is more susceptible to piercing while Holly is the opposite.) (exits are the Original exit to the village and the exit to the mountain or something TBD)
maybe do -3- A good amount of polish so that the game is "complete"
maybe do -4- add shadow and floating animation?
maybe do -4- change all music formats to .ogg
maybe do -4- add controller input mappings to options menu
maybe do -4- add doc strings to all core files
maybe do -4- make a core package in src with node and scene and stuff like that
maybe do -3- add a drop item mechanic in inventory
"""
