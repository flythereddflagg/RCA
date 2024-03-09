import pygame as pg


FPS = 30

class ControllerTest():
    def __init__(self):
        self.SHOW_EVENTS = False
        self.KEY_BIND = {
            "REFRESH" : "u",
            "FORCE_QUIT" : "backspace",
            "START" : "return",
            "SELECT" : "p",
            "UP" : "up",
            "DOWN" : "down",
            "LEFT" : "left",
            "RIGHT" : "right",
            "BUTTON_1" : "c",
            "BUTTON_2" : "x",
            "BUTTON_3" : "z", # for inventory
        }
        self.INV_KEY_BIND = {v: k for k, v in self.KEY_BIND.items()}
        self.controllers = []
        
        # detect and load controllers
        for i in range(0, pg.joystick.get_count()):
            self.controllers.append(pg.joystick.Joystick(i))
            self.controllers[-1].init()
            controllers  = self.controllers
            print (f"Detected controller: {controllers[-1].get_name()}")
            print(f"{controllers[-1].get_numbuttons()} buttons detected")
            print(f"{controllers[-1].get_numhats()} joysticks detected")

        self.clock = pg.time.Clock()


    def get_input(self):
        game_input = []

        events = pg.event.get()
        if self.SHOW_EVENTS:
            for event in events:
                print(event.type, event)
        if pg.QUIT in [event.type for event in events]: return ["QUIT"]    

        # TODO make the input more sophisticated
        pressed_keys = pg.key.get_pressed()
        game_input = [
            key for key, bind in self.KEY_BIND.items()
            if pressed_keys[pg.key.key_code(bind)]
        ]
        if self.SHOW_EVENTS and game_input: print(game_input)
        if 'FORCE_QUIT' in game_input: self.running = False
        
        # PLAYER1 = 0
        # print(self.controllers[PLAYER1].get_axis(0), # left right on left stick
        #     self.controllers[PLAYER1].get_axis(1)
        # ) # up down on left stick

        return game_input


    def run(self):
        self.running = True
        while self.running:
            game_input = self.get_input()
            self.clock.tick(FPS)


if __name__ == '__main__':
    pg.init()
    controller = ControllerTest()
    controller.run()
    pg.joystick.quit()
