import random
import pygame

class Settings:
    '''A class to store all settings for Alien Invasion.'''

    def __init__(self):
        '''Initialize the game's settings.'''

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 255, 255)
        self.bullets_allowed = 5
        

        # Alien bullet settings
        self.alien_bullet_width = 6
        self.alien_bullet_height = 20


        # Ship settings
        self.ship_limit = 3

        # Screen settings
        self.screen_width = 0  # Will be set by display.Info()
        self.screen_height = 0  # Will be set by display.Info()
        display_info = pygame.display.Info()
        self.screen_width = display_info.current_w
        self.screen_height = display_info.current_h
        self.bg_color = (0,0,0)

        WIDTH, HEIGHT = self.screen_width, self.screen_height
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()

        self.stars = []
        for _ in range(100):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            brightness = random.randint(0, 255)
            self.stars.append([x, y, brightness])

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        # Power-up settings
        self.power_up_speed = 1
        self.power_up_drop_chance = 5  # 10% chance to drop when alien is destroyed
        self.power_up_duration = 5000  # 5 seconds in milliseconds

        self.initialize_dynamic_settings()

        # Scoring
        self.alien_points = 50



    def initialize_dynamic_settings(self):
        '''Initialize settings that change throughout the game.'''
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        self.alien_bullet_speed = 2
        self.alien_bullets_allowed = 2

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        '''Increase speed settings and alien point values.'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_bullet_speed *= self.speedup_scale
        self.alien_bullets_allowed *= 1.01

        self.alien_points = int(self.alien_points * self.score_scale)

