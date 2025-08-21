import pygame
import random
import json

with open('sim_configs.json', 'r') as file:
    sim_configs = json.load(file)

class Boid:
    def __init__(self):
        self.position = pygame.Vector2(
            random.uniform(0, sim_configs["WIDTH"]),
            random.uniform(0, sim_configs["HEIGHT"])
        )
        direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.velocity = direction.normalize() * sim_configs["MAX_SPEED"] if direction.length_squared() > 0 else pygame.Vector2(1, 0)

    def update(self, grid):
        alignment_vector = self.alignment(grid)
        cohesion_vector = self.cohesion(grid)

        steering = alignment_vector + cohesion_vector

        if steering.length_squared() > 0:
            self.velocity = steering.normalize() * sim_configs["MAX_SPEED"]

        self.position += self.velocity
        self.wrap_around_edges()

    def wrap_around_edges(self):
        w, h = sim_configs["WIDTH"], sim_configs["HEIGHT"]
        if self.position.x < 0: self.position.x = w
        elif self.position.x > w: self.position.x = 0
        if self.position.y < 0: self.position.y = h
        elif self.position.y > h: self.position.y = 0

    def draw(self, screen):
        angle = self.velocity.angle_to(pygame.Vector2(0, -1))
        size = sim_configs["BOID_SIZE"]
        shape = [
            pygame.Vector2(0, -size),
            pygame.Vector2(-size, size),
            pygame.Vector2(0, size / 3),
            pygame.Vector2(size, size)
        ]
        rotated = [point.rotate(-angle) + self.position for point in shape]

        colors = ['#f06960', '#6f7ced', '#edd651']
        pygame.draw.polygon(screen, colors[random.randint(0, 2)], rotated)

    def alignment(self, grid):
        vr = sim_configs["ALIGNMENT_VR"]
        neighbors = self.find_flock(vr, grid)

        if not neighbors:
            return self.velocity

        total_velocity = pygame.Vector2(0, 0)
        for boid in neighbors:
            total_velocity += boid.velocity

        return total_velocity / len(neighbors)

    def cohesion(self, grid):
        vr = sim_configs["COHESION_VR"]
        neighbors = self.find_flock(vr, grid)

        if not neighbors:
            return self.velocity

        total_positions = pygame.Vector2(0, 0)
        for boid in neighbors:
            total_positions += boid.position
        com = total_positions / len(neighbors)

        desired_velocity = com - self.position

        return desired_velocity

    def find_flock(self, vr, grid):
        cell_size = sim_configs["CELL_SIZE"]
        my_cell_x = int(self.position.x // cell_size)
        my_cell_y = int(self.position.y // cell_size)

        neighbors = []
        vr_sq = vr * vr

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                cell = (my_cell_x + dx, my_cell_y + dy)
                if cell in grid:
                    for other in grid[cell]:
                        if other is not self and (self.position - other.position).length_squared() <= vr_sq:
                            neighbors.append(other)
        return neighbors

def build_spatial_grid(boids, cell_size):
    grid = {}
    for b in boids:
        cell = (
            int(b.position.x // cell_size),
            int(b.position.y // cell_size)
        )
        if cell not in grid:
            grid[cell] = []
        grid[cell].append(b)
    return grid

# Initialize boids
boids = [Boid() for _ in range(sim_configs["NO_BOIDS"])]