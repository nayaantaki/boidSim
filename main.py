from boid import Boid, boids
import pygame
import json

with open('sim_configs.json', 'r') as file:
    sim_configs = json.load(file)

#<--------------------------DEPENDENCIES--------------------------->

pygame.init()

screen = pygame.display.set_mode((sim_configs["WIDTH"], sim_configs["HEIGHT"]))
pygame.display.set_caption('boid sim')

icon_image = pygame.image.load('boid.png')
pygame.display.set_icon(icon_image)

clock = pygame.time.Clock()
FPS = 60

#<---------------------------BASE SETUP------------------------------>

running = True
while running:
    screen.fill((20, 20, 20))

    fps = int(clock.tick(FPS))
    fps_text = pygame.font.SysFont("consolas", 20).render(f"FPS: {fps}", True, (255, 255, 0))
    screen.blit(fps_text, (10, 10))

    for boid in boids:
        boid.update()
        Boid.draw(boid, screen)
        # print(boid.find_flock(sim_configs["ALIGNMENT_VR"]))
        print(boid.velocity.normalize())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)