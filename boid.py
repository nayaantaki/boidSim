import pygame.draw_py
import random
from sim_configs import *

class Boid:
    def __init__(self):
        self.position = pygame.Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_SPEED

    def update(self):
        self.position += self.velocity

        if self.position.x < 0: self.position.x = WIDTH
        if self.position.x > WIDTH: self.position.x = 0
        if self.position.y < 0: self.position.y = HEIGHT
        if self.position.y > HEIGHT: self.position.y = 0

    def draw(self):
        angle = self.velocity.angle_to(pygame.Vector2(0, -1))

        pointer_shape = [
            pygame.Vector2(0, -BOID_SIZE), # tip
            pygame.Vector2(-BOID_SIZE, BOID_SIZE), # bottom left
            pygame.Vector2(0, (BOID_SIZE/3)),
            pygame.Vector2(BOID_SIZE, BOID_SIZE) #bottom right
        ]

        rotated_pointer = [point.rotate(-angle) + self.position for point in pointer_shape]

        pygame.draw.polygon(screen, (255, 255, 255), rotated_pointer)

        # end = self.position + self.velocity.normalize() * 20
        # pygame.draw.line(screen, (0, 255, 0), self.position, end, 2)