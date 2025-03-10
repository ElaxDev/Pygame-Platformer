import pygame
import sys
import math
from pygame.locals import *
from variables import *


class RigidBody:
    def __init__(self, coords, size):
        self.rect = pygame.Rect(coords[0], coords[1], size[0], size[1])
        self.rect_color = dark_red
        self.speed = [0, 0]
        self.whitelist = []
        self.label = "RigidBody"

    def apply_gravity(self):
        self.speed[1] += round(gravity/pixel_per_metter)

    def move_and_collide(self, speed, object_list=None):
        self.rect.x += round(speed[0])
        self.rect.y += round(speed[1])

        if (speed[0] != 0 or speed[1] != 0) and (object_list != None and type(object_list) == type(list())):
            for object in object_list:
                if self.rect.colliderect(object.rect):
                    for label in self.whitelist:
                        if object.label == label:
                            if speed[0] > 0:
                                self.rect.right = object.rect.left
                            if speed[0] < 0:
                                self.rect.left = object.rect.right
                            if speed[1] > 0:
                                self.rect.bottom = object.rect.top
                                self.speed[1] = 0
                                self.can_jump = True
                                if object.speed[0] != 0:
                                    self.move_and_collide((object.speed[0], 0))
                            if speed[1] < 0:
                                self.rect.top = object.rect.bottom

    def draw_rect(self, surface):
        pygame.draw.rect(surface, self.rect_color, self.rect)


class RB_Block(RigidBody):
    def __init__(self, coords, size):
        RigidBody.__init__(self, coords, size)
        self.label = "RB_Block"
        self.rect_color = block_rect_color


class Bl_Platform(RB_Block):
    def __init__(self, coords, size, speed=1, direction=0, max_distance=100):
        RB_Block.__init__(self, coords, size)
        self.label = "Bl_Platform"
        self.direction = direction
        self.travel_speed = [
            abs(math.cos(math.radians(self.direction))*speed),
            abs(math.sin(math.radians(self.direction))*speed)
        ]
        self.rect_color = platform_rect_color
        self.initial_position = coords
        self.final_position = [
            coords[0]+int(math.cos(math.radians(self.direction))*max_distance),
            coords[1]+int(math.sin(math.radians(self.direction))*max_distance)
        ]

    def update(self):
        if self.rect.x <= self.initial_position[0]:
            self.speed[0] = self.travel_speed[0]
        if self.rect.x >= self.final_position[0]:
            self.speed[0] = -self.travel_speed[0]
        if self.rect.y <= self.initial_position[1]:
            self.speed[1] = self.travel_speed[1]
        if self.rect.y >= self.final_position[1]:
            self.speed[1] = -self.travel_speed[1]
        self.move_and_collide(self.speed)


class RB_Entity(RigidBody):
    def __init__(self, coords, size, game):
        RigidBody.__init__(self, coords, size)
        self.label = "RB_Entity"

        self.whitelist = solid_objects

        self.jump_speed = jump_speed
        self.jump_timer = [0, 6]
        self.is_jumping = False
        self.can_jump = False

    def jump(self, toggle):
        self.is_jumping = False
        if toggle and self.can_jump:
            if self.jump_timer[0] <= self.jump_timer[1]:
                self.speed[1] = -self.jump_speed
                self.jump_timer[0] += 1
            else:
                self.can_jump = False
        else:
            if self.can_jump:
                self.is_jumping = True
            self.jump_timer[0] = 0
        if self.is_jumping:
            self.can_jump = False


class Et_Player(RB_Entity):
    def __init__(self, coords, game):
        RB_Entity.__init__(self, coords, player_rect_size, game)
        self.label = "Player"
        self.keymap = {
            "Up": pygame.K_UP,
            "Down": pygame.K_DOWN,
            "Left": pygame.K_LEFT,
            "Right": pygame.K_RIGHT,
            "ButtonB": pygame.K_SPACE
        }
        self.walk_speed = player_walk_speed

    def get_input(self):
        self.keyboard = pygame.key.get_pressed()
        self.speed[0] = (self.keyboard[self.keymap["Right"]] -
                         self.keyboard[self.keymap["Left"]])*self.walk_speed
        self.toggle = bool(self.keyboard[self.keymap["ButtonB"]])

    def update(self, game):
        self.apply_gravity()
        self.get_input()
        self.jump(self.toggle)
        self.move_and_collide((0, self.speed[1]), game.object_list)
        self.move_and_collide((self.speed[0], 0), game.object_list)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.object_list = []

    def add_objects(self, *args):
        for object in args:
            self.object_list.append(object)

    def start(self):
        pj = Et_Player((100, 100), self)
        self.add_objects(RB_Block((50, 200), (200, 20)),
                         Bl_Platform((250, 200), (50, 20)))
        while True:
            self.clock.tick(max_framerate)
            self.screen.fill(background_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pj.update(self)
            pj.draw_rect(self.screen)

            for object in self.object_list:
                object.draw_rect(self.screen)
                try:
                    object.update()
                except AttributeError:
                    pass

            pygame.display.update()


game = Game()
game.start()
