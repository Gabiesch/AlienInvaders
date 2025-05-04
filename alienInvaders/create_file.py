import pygame
from alien import Alien



def create_fleet(self):
    '''Create the fleet of aliens.'''
    # Create an alien and find the number of aliens in a row.
    #Spacing between each alien is equal to one alien width.
    alien = Alien(self)
    alien_width, alien_height = alien.rect.width, alien.rect.height
    available_space_x = self.settings.screen_width - (2 * alien_width)
    number_aliens_x = available_space_x // (2 * alien_width)

    # Determine the number of rows of aliens that fit on the screen.
    ship_height = self.ship.rect.height
    available_space_y = (self.settings.screen_height - 
                            (3*alien_height) - ship_height)
    number_rows = available_space_y // (2*alien_height)

    # Create the first row of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
                create_alien(self, alien_number, row_number)

def create_alien(self, alien_number, row_number):
    # Create an alien an place it in the row.
    alien = Alien(self)
    alien_width, alien_height = alien.rect.width, alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    self.aliens.add(alien)