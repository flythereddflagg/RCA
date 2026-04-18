import itertools

import pygame as pg
import random

from .movement import Movement

from .node import Node
from .tools import vec, mask_collision, diff_vec, list_collided
from .compass import Compass

DIST_SQR_AGRO = 100**2
BASE_SPEED = 25
TRANSITION_TIME = 3.50 # sec

class MeatBall(Node):
    def setup(self):
        self.last_time = 0
        self.move = Movement(self.sprite, hitmask_sprite = self.hitmask.sprite)
        self.animation.set_state("stage1")
        self.cur_action = 4
        self.hp = 30
        self.signals = []
        self.agro = False
        self.stage3_go = False
        self.already_throwing = False
        self.thrown = True
        self.throwtime = 1120 #ms
        self.ball_direction = (1, 0)
        self.ball_speed = 500
        self.throw_timer = 0
        self.random_throw = 500
        self.chance_of_throw = 0.05
        self.vunerable = False
        self.music_node = None
        self.music_data = self.init["music"]
        self.set_meatball_music = False
        self.transition_started = False

    def signal(self, signal_):
        self.signals.append(signal_)

    
    def check_signals(self):
        for name, value, other in self.signals:
            if (
                "damage" in name 
                and self.animation.state != "damage" 
                and self.vunerable
            ):
                self.hp -= value
                self.damage_direction = other
                self.animation.set_state("damage")
                # print(f"Meatball took damage {value}")

        self.signals = [] # reset signals


    def update(self):
        if self.music_node is None:
            self.music_node = self.scene.node_by_id("music")
        if self.stage3_go:
            self.stage3()
            return
        player = self.scene.get_player().parent
        if player.inventory.contains("sword"):
            # self.music_node.stop()
            if not self.set_meatball_music:
                self.music_node.load_play(self.music_data["filename"])
                self.music_node.play_loop(0.0, self.music_data["tags"]["dim"])
                self.set_meatball_music = True

            if self.animation.state == "stage1":
                self.animation.set_state("stage2")

            self.blockage.kill()
            self.scene.place_node(
                self.blockage, 
                start=self.scene.set_bg_pos(
                    self.blockage.init['start']
                ),
                groups=["foreground"]
            )
            if (
                vec(self.sprite.rect.center).distance_squared_to(
                    player.sprite.rect.center
                ) < DIST_SQR_AGRO
                and self.animation.state == "stage2"
                and not self.transition_started
            ):
                self.music_node.goto(self.music_data['tags']['dim'])
                self.music_node.play_then_end(
                    self.music_data['tags']['terror']
                )
                self.transition_started = True
                self.transition_start_time = pg.time.get_ticks()
            elif self.transition_started:
                if (pg.time.get_ticks() - self.transition_start_time)/1000 > (
                    self.music_node.end - self.music_node.start 
                    - TRANSITION_TIME
                ):
                    self.animation.set_state("transition")
                if not pg.mixer.music.get_busy():
                    self.transition_started = False
                    self.music_node.reset()
                    pg.mixer.music.play(1)
                    self.music_node.play_loop(
                        self.music_data['tags']['terror'],
                        self.music_data['tags']['fight_loop'],
                        self.music_data['tags']['fight']
                    )
            elif self.animation.state == "wiggle":
                self.stage3_go = True
            return
        elif player.inventory.contains("shovel"): 
            self.animation.set_state("stage2")
        self.random_movement()

        
    def random_movement(self):
        cur_time = pg.time.get_ticks()
        if (cur_time - self.last_time) > 1000:
            self.last_time = cur_time
            self.cur_action = random.randint(0, 4)
        
        if self.cur_action == 4:
            return
        else:
            self.move(self.cur_action, speed=BASE_SPEED)
            # self.move(self.cur_action+random.choice([-1,1]), speed=BASE_SPEED)
            self.move(self.cur_action+1, speed=BASE_SPEED)
            # self.move(3, speed=BASE_SPEED)

    def stage3(self):
        self.check_signals()
        player_sprite = self.scene.get_player()
        self.throw_update()
        if (
            self.animation.state == "wiggle" and 
            vec(self.sprite.rect.center).distance_squared_to(
                player_sprite.rect.center
            ) < DIST_SQR_AGRO
        ):
            self.animation.set_state("throw")
            self.agro = True

        if mask_collision(self.hitmask.sprite, player_sprite):
            damage_direction = diff_vec(
                player_sprite.rect.center, 
                vec(self.hitmask.sprite.mask.centroid())
                + vec(self.sprite.rect.topleft)
            ).normalize()
            player_sprite.signal(['damage', 1, damage_direction])
        
        if self.agro and self.animation.state == "wiggle":
            self.chase_player()
            if (pg.time.get_ticks() - self.throw_timer) > self.random_throw:
                self.throw_timer = pg.time.get_ticks()
                # print("testing random throw")
                if random.random() < self.chance_of_throw:
                    # print("throwing")
                    self.animation.set_state("throw")

        self.apply_physics()
        if self.hp <= 0:
            self.kill()
            self.music_node.reset()
            self.music_node.goto(self.music_data['tags']['victory'])
            self.music_node.reload_primary = True

        
        
    def throw_update(self):
        player_sprite = self.scene.get_player()
        if self.animation.state == "throw" and not self.already_throwing:
            self.already_throwing = True
            self.starttime = pg.time.get_ticks()
            self.thrown = False
        elif self.animation.state != "throw":
            self.already_throwing = False
            self.vunerable = False

        if (
            self.already_throwing 
            and not self.thrown
            and (pg.time.get_ticks() - self.starttime) > self.throwtime
        ):
            # print("throwing the ball")
            self.scene.place_node(
                self.justball, 
                groups=["foreground"], 
                start=self.sprite.rect.midleft
            )
            self.justball.animation.set_state("rollin")
            self.ball_direction = (
                vec(player_sprite.rect.center) 
                - vec(self.justball.rect.center)
            )
            self.thrown = True
            self.vunerable = True

        
        if self.justball.sprite.alive:
            self.justball.sprite.rect.move_ip(*(vec(self.ball_direction).normalize() * (500/90)))

        if not self.justball.sprite.rect.colliderect(self.scene.game.draw_surface.get_rect()):
            self.justball.kill()
            self.vunerable = False




    def chase_player(self):
        player_sprite = self.scene.get_player()
        to_move = diff_vec(
            player_sprite.rect.center, 
            vec(self.hitmask.sprite.mask.centroid())
            + vec(self.sprite.rect.topleft)
            # self.sprite.rect.center
        )
        self.move(Compass.unit_vector(to_move), speed=35)


    def apply_physics(self):
        if self.animation.state == 'damage':
            self.move(
                Compass.unit_vector(self.damage_direction), 
                speed=2*BASE_SPEED, 
                change_direction=False
            )
        if self.justball.sprite.alive:
            for sprite in list_collided(
                self.justball.sprite, 
                self.scene.groups["player"]
            ):
                damage_direction = diff_vec(
                        sprite.rect.center, 
                        self.justball.sprite.rect.center
                ).normalize()
                sprite.signal([
                    'damage', 1, damage_direction
                ])
                self.justball.kill()


