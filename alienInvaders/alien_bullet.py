import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    '''A class to manage bullets fired from the ship'''

    def __init__(self, ai_game, alien):
        '''Create a bullet object at the ship's current position'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = (255, 0, 0) # Red color for alien bullets

        # Create a bullet rect at (0,0) and then at the aliens position.
        self.rect = pygame.Rect(0, 0, self.settings.alien_bullet_width, 
                                self.settings.alien_bullet_height)
        # At random alien location

        self.rect.midtop = alien.rect.midbottom

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

    def update(self):
        '''Move the bullet up the screen.'''
        self.y += self.settings.alien_bullet_speed
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        '''Draw the bullet to the screen.'''
        pygame.draw.rect(self.screen, self.color, self.rect)