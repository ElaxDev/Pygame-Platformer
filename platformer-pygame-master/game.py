import pygame, sys
from pygame.locals import *

import var

class RigidBody:
    def __init__(self, coords, size, movement):
        self.rect = pygame.Rect(coords[0], coords[1], size[0], size[1])
        self.movement = movement

    def add_gravity(self, gravity):
        self.movement[1] = (gravity/var.pixel_per_meter)*var.vel

    def draw(self,color):
        pygame.draw.rect(window, color, self.rect)

class Player(RigidBody):
    def __init__(self, coords, size, movement):
        RigidBody.__init__(self, coords, size, movement)
        self.label = "Player"

    def detect_input(self, keyboard):
        self.movement[0] = (keyboard[K_RIGHT] - keyboard[K_LEFT])*10

class Block(RigidBody):
    def __init__(self, coords, size, movement):
        RigidBody.__init__(self, coords, size, movement)
        self.label = "Box"

class Wall(RigidBody):
    def __init__(self, coords, size, movement = []):
        RigidBody.__init__(self, coords, size, movement)
        self.label = "Wall"

def detect_collision(player_rect, object_list):
    collisions = []
    for object in object_list:
        if player_rect.colliderect(object):
            collisions.append(object)
    return collisions

def move(collider_object, object_list):
    collider_object.rect.centerx += round(collider_object.movement[0])
    collisions = detect_collision(collider_object.rect, object_list)
    for object in collisions:
        if collider_object.label != object.label:
            if collider_object.movement[0] > 0 and object.label != "Box":
                collider_object.rect.right = object.rect.left
            if collider_object.movement[0] < 0 and object.label != "Box":
                collider_object.rect.left = object.rect.right
            if object.label == "Box":
                if collider_object.movement[0] > 0:
                    object.rect.x = collider_object.rect.x + collider_object.rect.width
                if collider_object.movement[0] < 0:
                    object.rect.x = collider_object.rect.x - object.rect.width

    collider_object.rect.centery += round(collider_object.movement[1])
    collisions = detect_collision(collider_object.rect, object_list)
    for object in collisions:
        if collider_object.label != object.label:
            if collider_object.movement[1] > 0:
                collider_object.rect.bottom = object.rect.top
            if collider_object.movement[1] < 0:
                collider_object.rect.top = object.rect.bottom
    return collider_object.rect


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
        clock.tick(60)
        events_list = pygame.event.get()
        keys = pygame.key.get_pressed()

        for event in events_list:
            if event.type == pygame.QUIT:
                game_quit = True

        for object in solid_list:
            if object.label != "Wall":
                object.add_gravity(var.gravity)
                move(object, solid_list)
        player.detect_input(keys)
        player.add_gravity(var.gravity)
        player_rect = move(player, solid_list)
        draw_game()
    pygame.quit()

def game_initialize():

    global window, player, solid_list

    solid_list = [Wall([10,var.window_height-20], [600, 20], [0,0]), Block(var.player_coords, [50,50], [0,0])]

    pygame.init()
    window = pygame.display.set_mode((var.window_width, var.window_height))

    player = Player([200, 0], var.player_size, [0,0])


if __name__ == '__main__':
    game_initialize()
    game_loop()
