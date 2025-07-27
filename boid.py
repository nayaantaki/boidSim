import pygame.draw_py
import random
import json

with open('sim_configs.json', 'r') as file:
    sim_configs = json.load(file)

class Boid:
    def __init__(self):
        self.position = pygame.Vector2(random.uniform(0, sim_configs["WIDTH"]), random.uniform(0, sim_configs["HEIGHT"]))
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * sim_configs["MAX_SPEED"]

    def update(self):
        self.position += self.velocity
        self.velocity = self.alignment().normalize() * sim_configs["MAX_SPEED"]

        if self.position.x < 0: self.position.x = sim_configs["WIDTH"]
        if self.position.x > sim_configs["WIDTH"]: self.position.x = 0
        if self.position.y < 0: self.position.y = sim_configs["HEIGHT"]
        if self.position.y > sim_configs["HEIGHT"]: self.position.y = 0

    def draw(self, screen):
        angle = self.velocity.angle_to(pygame.Vector2(0, -1))

        pointer_shape = [
            pygame.Vector2(0, -sim_configs["BOID_SIZE"]), # tip
            pygame.Vector2(-sim_configs["BOID_SIZE"], sim_configs["BOID_SIZE"]), # bottom left
            pygame.Vector2(0, (sim_configs["BOID_SIZE"]/3)), # centroid
            pygame.Vector2(sim_configs["BOID_SIZE"], sim_configs["BOID_SIZE"]) #bottom right
        ]

        rotated_pointer = [point.rotate(-angle) + self.position for point in pointer_shape]

        pygame.draw.polygon(screen, (255, 255, 255), rotated_pointer)

        # end = self.position + self.velocity.normalize() * 20
        # pygame.draw.line(screen, (0, 255, 0), self.position, end, 2)

    def alignment(self):
        flock = self.find_flock(sim_configs["ALIGNMENT_VR"])

        total_velocity = pygame.Vector2(0, 0)
        for boid in flock:
            total_velocity += boid.velocity
        # total_velocity = total_velocity.normalize() * sim_configs["MAX_SPEED"]
        flock_velocity = (total_velocity/len(flock))

        return flock_velocity

    def find_flock(self, vr):
        flock = []
        for boid in boids:
            if self.position.distance_to(boid.position) <= vr:
                flock.append(boid)
        return flock


boids = [Boid() for _ in range(sim_configs["NO_BOIDS"])]