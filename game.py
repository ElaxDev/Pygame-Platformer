import pygame, sys
from pygame.locals import *

import var

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity):
        super(Player, self).__init__()
        self.x = x
        self.y = y
        self.velocity = velocity
        self.surf = pygame.Surface((25,50))
        self.surf.fill(var.red)
        self.rect = self.surf.get_rect()

    def draw(self):
        window.blit(self.surf, (self.x, self.y))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


def draw_game():
    window.fill(var.gray)
    player.draw()
    pygame.display.flip()

def game_loop():

    game_quit = False

    while not game_quit:
        events_list = pygame.event.get()

        for event in events_list:
            if event.type == pygame.QUIT:
                game_quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move(0, -player.velocity)
                elif event.key == pygame.K_DOWN:
                    player.move(0, player.velocity)
                elif event.key == pygame.K_LEFT:
                    player.move(-player.velocity, 0)
                elif event.key == pygame.K_RIGHT:
                    player.move(player.velocity, 0)
        draw_game()
    pygame.quit()

def game_initialize():

    global window, player

    pygame.init()
    window = pygame.display.set_mode((var.window_width, var.window_height))

    player = Player(0, 0, var.vel)


if __name__ == '__main__':
    game_initialize()
    game_loop()
