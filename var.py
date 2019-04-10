import pygame
pygame.init()

# Physics
gravity = 9.8
friction = 1.35
pixel_per_meter = 10

# Sizes
window_width = 800
window_height = 600
player_size = [25, 50]

# Positions
player_coords = [20, 200]

# Colors
white = (255,255,255)
gray = (200,200,200)
red = (200,0,30)
blue = (30,0,200)
black = (0,0,55)

# Game var
vel = 10
max_fps = 60
