import pygame, sys
from pygame.locals import *

import var

class Dynamic_Body:
    def __init__(self, coords, size):
        self.rect = pygame.Rect(coords[0], coords[1], size[0], size[1])
        self.rect_color = (60, 60, 60)
        self.speed = [0,0]
        self.type = "Dynamic_Body"



class Player(pygame.sprite.Sprite):
    def __init__(self, coords, velocity, color):
        super(Player, self).__init__()
        self.coords = coords
        self.velocity = velocity
        self.rect = pygame.Rect(self.coords[0], self.coords[1], var.player_width, var.player_heigth)

    def draw(self):
        pygame.draw.rect(window, var.red, self.rect)

def detect_collision(player_rect, object_list):
    collisions = []
    for object in object_list:
        if player_rect.colliderect(object):
            collisions.append(object)
    return collisions

def move(player_rect, movement, object_list):
    player_rect.x += movement[0]
    collisions = detect_collision(player_rect, object_list)
    for object in collisions:
        if movement[0] > 0:
            player_rect.right = object.left
        if movement[0] < 0:
            player_rect.left = object.right
    player_rect.y += movement[1]
    collisions = detect_collision(player_rect, object_list)
    for object in collisions:
        if movement[1] > 0:
            player_rect.bottom = object.top
        if movement[1] < 0:
            player_rect.top = object.bottom
    return player_rect


def draw_game():
    window.fill(var.gray)
    player.draw()
    for solid in solid_list:
        pygame.draw.rect(window, var.black, solid)
    pygame.display.flip()

def game_loop():

    clock = pygame.time.Clock()
    clock.tick(60)
    game_quit = False

    while not game_quit:
        events_list = pygame.event.get()
        keys = pygame.key.get_pressed()
        movement = [0,0]

        for event in events_list:
            if event.type == pygame.QUIT:
                game_quit = True

        if keys[K_UP] and player.rect.y > 0:
            movement[1] -= player.velocity
        if keys[K_DOWN] and player.coords[1] < var.window_height - var.player_heigth:
            movement[1] += player.velocity
        if keys[K_LEFT] and player.rect.x > 0:
            movement[0] -= player.velocity
        if keys[K_RIGHT] and player.coords[0] < var.window_width - var.player_width:
            movement[0] += player.velocity

        player_rect = move(player.rect, movement, solid_list)
        draw_game()
    pygame.quit()

def game_initialize():

    global window, player, solid_list

    solid_list = [pygame.Rect(0,var.window_height-20, var.window_width, 20), pygame.Rect(200, 200, 50, 50)]

    pygame.init()
    window = pygame.display.set_mode((var.window_width, var.window_height))

    player = Player(var.player_coords, var.vel, var.red)


if __name__ == '__main__':
    game_initialize()
    game_loop()
