from .sprite import Character

class Player(Character):
    def __init__(self, game, asset_path, **options):
        super().__init__(game, asset_path, **options)

    def update(self):
        pass
    
    def apply_action(self, action):
        # TODO fix magic numbers!
        match action:
            case "UP":
                self.rect.y -= 20
            case "DOWN":
                self.rect.y += 20
            case "LEFT":
                self.rect.x -= 20
            case "RIGHT":
                self.rect.x += 20
            case _:
                print(action + "! (no response)")
