import pygame
from boid import boids, build_spatial_grid, sim_configs

pygame.init()
screen = pygame.display.set_mode((sim_configs["WIDTH"], sim_configs["HEIGHT"]))
pygame.display.set_caption('boid sim')

icon_image = pygame.image.load('boid.png')
pygame.display.set_icon(icon_image)

clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    screen.fill((20, 20, 20))

    grid = build_spatial_grid(boids, sim_configs["CELL_SIZE"])

    for boid in boids:
        boid.update(grid)
        boid.draw(screen)

    fps = int(clock.tick(FPS))
    fps_text = pygame.font.SysFont("consolas", 20).render(f"FPS: {fps}", True, (255, 255, 0))
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()