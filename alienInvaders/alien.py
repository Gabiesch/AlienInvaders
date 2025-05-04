import pygame
from pygame.sprite import Sprite
import os


class Alien(Sprite):
    '''A class to represent a single alien in the fleet.'''
    
    def __init__(self, ai_game):
        '''Initialize the alien and set its starting position.'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute
        alien_image_path = os.path.join(ai_game.images_path, 'alien_ship.png')
        self.image = pygame.image.load(alien_image_path)
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

        # Have the aliens shoot bullets as well.
        

    def update(self):
        '''Move the alien to the right.'''
        self.x += (self.settings.alien_speed * 
                        self.settings.fleet_direction)
        self.rect.x = self.x


    def check_edges(self):
        '''Return Tru if alien is at edge of screen.'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True