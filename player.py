from Class import Animation
from function import *


class Player:

    def __init__(self, pos_x, pos_y, screen, scale) -> None:
        self.run_animation = None
        self.walk_animation = None
        self.jump_animation = None
        self.jump_animation2 = None
        self.run_attack_animation = None
        self.protect_animation = None
        self.hurt_animation = None
        self.defend_animation = None
        self.dead_animation = None
        self.attack1_animation = None
        self.attack2_animation = None
        self.attack3_animation = None
        self.idle_animation = None

        self.screen = screen
        self.scale = scale
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos = (self.pos_x, self.pos_y)
        self.mass = 10
        self.MaxSpeed = 30
        self.walk_speed = 20
        self.FrictionCoef = 0.9
        self.can_move = True
        self.speed_x = 0
        self.speed_y = 0
        self.speed = (0, 0)
        self.level = None

    def init_animation(self, width, height_object, sheet_location, scale):
        self.run_animation = Animation(screen=self.screen, width=width, height=height_object,
                                       sheet_location=sheet_location, scale=scale, pixel_x=128, pixel_y=128,
                                       coordinates=(self.pos_x, self.pos_y))
        self.walk_animation = Animation(screen=self.screen, width=width, height=height_object,
                                        sheet_location=sheet_location, scale=scale, pixel_x=128, pixel_y=128,
                                        coordinates=(self.pos_x, self.pos_y))

    def mouvement(self) -> None:

        # déplace le personnage en fonction des obstacles
        oldpos = self.pos
        self.speed_x = min(20, self.speed_x)
        self.speed_y = min(20, self.speed_y)
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y
        self.pos = (self.pos_x, self.pos_y)
        self.pos_x, self.pos_y, self.speed_x, self.speed_y = bloque_sur_collision(self.level, oldpos, self.pos,
                                                                                  self.speed_x, self.speed_y)

        # teste si sous le jour il y a un du sol
        if self.speed_y == 0:
            self.can_move = True

        # anime le mouvement de course si pas dans les airs
        if self.can_move:
            if self.walk_speed <= self.speed_x < 0:
                self.walk_animation.update()
                self.walk_animation.draw(orientation='left')
            if 0 > self.speed_x <= self.walk_speed:
                self.walk_animation.update()
                self.walk_animation.draw()
        else:
            if self.speed_y > 0:
                self.jump_animation.update()
                self.jump_animation.draw()
            else:
                self.jump_animation2.update()
                self.jump_animation.draw()

        self.strength(0, 2)

    def strength(self, acceleration_x, acceleration_y) -> None:
        self.speed_x += acceleration_x
        self.speed_y += acceleration_y
        self.speed = (self.speed_x, self.speed_y)

    def show(self, surface, Screen) -> None:
        Screen.blit(surface, (self.pos_x, self.pos_y))