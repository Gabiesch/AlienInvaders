import random
import pygame
from pygame.sprite import Sprite
import os

class PowerUp(Sprite):
    def __init__(self, ai_game, effect, image_path, size):
        '''Initialize the power-up sprite'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.effect = effect
        
        # Load the power-up image
        power_up_image_path = os.path.join(ai_game.images_path, os.path.basename(image_path))
        self.image = pygame.image.load(power_up_image_path)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        
        # Set initial position
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # Store the power-up's exact position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        '''Move the power-up down the screen.'''
        self.y += self.settings.power_up_speed
        self.rect.y = self.y

    def draw(self, screen):
        '''Draw the power-up on the screen.'''
        screen.blit(self.image, self.rect)

    def missile(self):
        '''Have the misile shoot up from the ships location and explode when colliding with an alien. 
        After colliding the missile shoots small bullets in 8 directions that each can kill an alien as well'''

def power_up_sprites(ai_game, effect, image_path, size):
    '''Create a power-up sprite with the given effect and image.'''
    return PowerUp(ai_game, effect, image_path, size)