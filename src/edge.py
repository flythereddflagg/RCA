import pygame as pg

from .decal import Decal
from .compass import Compass

class Edge(Decal):
    """an edge is a sprite that connects two scenes in the map graph"""
    def __init__(self, **options):
        super().__init__(**options)
# TODO set this up so that that an exit puts the player somewhere in particular

    def update(self):
        """default behavior is to set up a new scene. Override to change"""
        self.check_collision()
    
    def check_collision(self):
        if pg.sprite.spritecollideany(
            # collide between self and player
            self, self.scene.groups['player'], 
            # do not kill, use the masks for collision
            pg.sprite.collide_mask
            # psudo_collide_mask
        ):
            print("loading scene")
            self.exec_trigger()
    
    def exec_trigger(self):
        # save everything we want to carry into the next scene
        game = self.scene.game
        player = self.scene.player
        new_scene = self.scene.load_scene(self.scene, game, self.options['scene_path'])
        new_scene.player = player
        player.scene = new_scene
        new_scene.layers['characters'].add(player)
        new_scene.groups['player'].add(player)
        sprites = new_scene.layers['characters'].sprites()
        block = list(filter(lambda x: x.id == self.id, sprites))[0]
        print(block.id, block.scene.data['id'])
        print("cur pos", player.rect.center)
        player.rect.center = block.rect.center
        print("mid", player.rect.center)
        dx, dy = Compass.unit_vector(block.options['exit_dir'])
        player.rect.x += dx*(player.rect.w + block.rect.w)
        player.rect.y += dy*(player.rect.h + block.rect.h)
        ## TODO adjust player pos with background??
        print("after pos", player.rect.center)



def psudo_collide_mask(left, right):
    print('HEREs the junk')
    print('LEFT', left.mask)
    print('RIGHT', right.mask)
    return pg.sprite.collide_mask(left, right)