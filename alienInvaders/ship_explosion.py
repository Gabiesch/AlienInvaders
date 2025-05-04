import random
import pygame
from particles import Particle

class ShipExplosion:
    def __init__(self, x, y, ai_game):
        self.particles = []
        colors = [(239, 184, 18), (141, 141, 141), (204, 204, 204)]
        for _ in range(50):  # Create 50 particles
            color = random.choice(colors)
            lifetime = 300 # 5 seconds at 60 fps
            self.particles.append(Particle(x, y, color, ai_game))

    def update(self):
        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if p.lifetime > 0]

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

    def is_finished(self):
        return len(self.particles) == 0
    
