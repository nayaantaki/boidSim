import pygame

WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('boid sim')

icon_image = pygame.image.load('boid.png')
pygame.display.set_icon(icon_image)

MAX_SPEED = 4
BOID_SIZE = 5
