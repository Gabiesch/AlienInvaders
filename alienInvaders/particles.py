import pygame
import random
from settings import Settings

class Particle:
    def __init__(self, x, y, color, ai_game, lifetime=120):
        self.x = x
        self.y = y
        self.color = color
        self.radius = random.randint(2, 5)
        self.velocity_x = random.uniform(-2, 2)
        self.velocity_y = random.uniform(-2, 2)
        self.lifetime = lifetime  # 120 = 1 second at 60 FPS
        self.settings = ai_game.settings

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.lifetime -= 1

        # Bounce off screen edges
        if self.x < 0 or self.x > self.settings.screen_width:
            self.velocity_x *= -1
        if self.y < 0 or self.y > self.settings.screen_height:
            self.velocity_y *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
