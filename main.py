from sim_configs import *
from boid import Boid

pygame.init()

clock = pygame.time.Clock()
FPS = 60

boids = [Boid() for _ in range(1000)]

running = True
while running:
    screen.fill((20, 20, 20))

    fps = int(clock.tick(FPS))
    fps_text = pygame.font.SysFont("consolas", 20).render(f"FPS: {fps}", True, (255, 255, 0))
    screen.blit(fps_text, (10, 10))

    for boid in boids:
        boid.update()
        Boid.draw(boid)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(FPS)