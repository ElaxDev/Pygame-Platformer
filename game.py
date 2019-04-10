import pygame, sys
from pygame.locals import *

import var

class RigidBody:
    def __init__(self, coords, size, movement):
        self.rect = pygame.Rect(coords[0], coords[1], size[0], size[1])
        self.movement = movement

    def add_gravity(self, gravity):
        self.movement[1] = (gravity/var.pixel_per_meter)*var.vel

    def draw(self, color):
        pygame.draw.rect(window, color, self.rect)

    def move(self, object_list):
        self.rect.centerx += round(self.movement[0])
        collisions = [object for object in object_list if self.rect.colliderect(object)]
        for object in collisions:
            if object != self:
                if self.movement[0] > 0 and object.label != "Box":
                    self.rect.right = object.rect.left
                if self.movement[0] < 0 and object.label != "Box":
                    self.rect.left = object.rect.right
                if object.label == "Box":
                    if self.movement[0] > 0:
                        object.rect.x = self.rect.x + self.rect.width
                    if self.movement[0] < 0:
                        object.rect.x = self.rect.x - object.rect.width

        collisions = []

        self.rect.centery += round(self.movement[1])
        collisions = [object for object in object_list if self.rect.colliderect(object)]
        for object in collisions:
            if object != self:
                if self.movement[1] > 0:
                    self.rect.bottom = object.rect.top
                if self.movement[1] < 0:
                    self.rect.top = object.rect.bottom
        return self.rect


class Player(RigidBody):
    def __init__(self, coords, size, movement):
        RigidBody.__init__(self, coords, size, movement)
        self.label = "Player"
        self.keymap = {
            "Right"  :pygame.K_RIGHT,
            "Left"   :pygame.K_LEFT,
            "Up"     :pygame.K_UP,
            "Down"   :pygame.K_DOWN,
            "ButtonB":pygame.K_SPACE
        }
        self.jump_speed = 7
        self.timer = {
            "Jump" : [0, 6]
        }
        self.metadata = {
            "Jumped" : False,
            "CanJump": False
        }

    def detect_input(self):
        keyboard = pygame.key.get_pressed()
        self.movement[0] = (keyboard[self.keymap["Right"]] - keyboard[self.keymap["Left"]])*var.vel
        if bool(keyboard[self.keymap["ButtonB"]]) and self.metadata["CanJump"]:
            if self.timer["Jump"][0] <= self.timer["Jump"][1]:
                self.movement[1] = -self.jump_speed
                self.timer["Jump"][0] += 1
            else:
                if self.metadata["CanJump"]: self.metadata["Jumped"] = True
                self.timer["Jump"][0] = 0

    def jump(self, metadata):
        if metadata["CanJump"] == True:
            self.movement[1] = -50
            print(self.movement[1])

class Block(RigidBody):
    def __init__(self, coords, size, movement):
        RigidBody.__init__(self, coords, size, movement)
        self.label = "Box"

class Wall(RigidBody):
    def __init__(self, coords, size, movement = []):
        RigidBody.__init__(self, coords, size, movement)
        self.label = "Wall"


def draw_game():
    window.fill(var.gray)
    player.draw(var.red)
    for solid in solid_list:
        pygame.draw.rect(window, var.black, solid)
    pygame.display.flip()

def game_loop():

    clock = pygame.time.Clock()
    game_quit = False

    while not game_quit:
        clock.tick(var.max_fps)
        events_list = pygame.event.get()

        for event in events_list:
            if event.type == pygame.QUIT:
                game_quit = True

        for object in solid_list:
            if object.label != "Wall":
                object.add_gravity(var.gravity)
                object.move(solid_list)

        player.detect_input()
        player.add_gravity(var.gravity)
        player.move(solid_list)
        draw_game()
    pygame.quit()

def game_initialize():

    global window, player, solid_list

    solid_list = [Wall([10,var.window_height-20], [600, 20], [0,0]), Block([200, 0], [50,50], [0,0])]

    pygame.init()
    window = pygame.display.set_mode((var.window_width, var.window_height))

    player = Player(var.player_coords, [50,50], [0,0])


if __name__ == '__main__':
    game_initialize()
    game_loop()
