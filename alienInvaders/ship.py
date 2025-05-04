import pygame
from settings import Settings
from pygame.sprite import Sprite
import os

class Ship(Sprite):
    '''A class to manage the ship.'''

    def __init__(self, ai_game):
        '''Initialize the ship and set its starting position.'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # Load the ship image and get its rect.
        ship_image_path = os.path.join(ai_game.images_path, 'ship_def.png')
        self.image = pygame.image.load(ship_image_path)
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen. 
        self.rect.midbottom = self.screen_rect.midbottom

    def update(self):
        '''Update the ship's position based on the movement flag.'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.rect.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > self.screen_rect.top + 750:
            self.rect.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom <self.screen_rect.bottom:
            self.rect.y += self.settings.ship_speed

    def blitme(self):
        '''Draw the ship at its current location.'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        '''Center the ship on the screen.'''
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)