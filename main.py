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
            # game.run()
        finally:
            write_log(game)
    else:
        game.run()
        # game.run() # necessary for wasm build

    
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

async def wasm_main():
    import pygame as pg
    import yaml
    from src import Engine
    pg.init()
    INIT_PATH = "./assets/init.yaml"
    game = Engine(INIT_PATH)
    print(" --- INIT COMPLETE ---")
    
    game.running = True

    while game.running:
        game.input.update()
        game.logic()
        game.draw_frame()
        game.dt = (
            game.clock.tick() 
            if game.settings.FPS < -1 else 
            game.clock.tick(game.settings.FPS)
        )
        await asyncio.sleep(0)


    pg.display.quit()
    pg.quit()
    print("Game ended successfully!")


if __name__ == "__main__":
    import sys
    if sys.platform == "emscripten":
        asyncio.run(wasm_main())
    else: # on PC
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
TODO -2- make start or "A" be valid ways to select stuff in menus
TODO -2- add outline to menu text
TODO -2- include actual options menu with volume sliders and other settings
TODO -2- add save and quit and options menu in start menu
TODO -3- make DPAD a valid way to move the character
TODO -2- tighten up music with loops USE TENACITY?
TODO -2- add the dark overlay back into the boss room
TODO -4- make inventory have proper labeling too!
TODO -4- make it possible to upload feedback from the menu
TODO -4- animate the river/waterfall
TODO -3- fix player jitter when camera moves

TODO -3- make meaningful TESTS
TODO -3- make scene transitions a la LTTP (polish)
TODO -4- Larry AND Holly are playable with these items but both play differently and have different exits at the end (e.g. Larry has less knockback from bludgeoning but is more susceptible to piercing while Holly is the opposite.) (exits are the Original exit to the village and the exit to the mountain or something TBD)
TODO -3- A good amount of polish so that the game is "complete"
TODO -4- add shadow and floating animation?
"""
