import sys
import pygame
import random
from explosion import Explosion
from bullet import Bullet
from alien_bullet import AlienBullet
from power_ups import power_up_sprites

def _fire_bullet(self):
    '''Create a new bullet and add it to the bulllets group.'''
    if len(self.bullets) < self.settings.bullets_allowed:
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

def _update_bullets(self):
    '''Update position of bullets and get rid of old bullets.'''
    self.bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in self.bullets.copy():
        if bullet.rect.bottom <= 0:
            self.bullets.remove(bullet)
    _check_bullet_alien_collisions(self)

def _check_bullet_alien_collisions(self):
    # Check for any bullets that have hit aliens.
    #   If so, get rid of the bullet and the alien.
    collisions = pygame.sprite.groupcollide(
        self.bullets, self.aliens, True, True)

    if collisions:
        for aliens_hit in collisions.values():
            self.stats.score += self.settings.alien_points * len(aliens_hit)
            for alien in aliens_hit:
                # Only generate power-up if it's not the last alien
                if len(self.aliens) > 1 and random.randint(0,100) < self.settings.power_up_drop_chance:
                    power_up_effect = random.choice([
                        ('rocket', 'missile.png', (self.settings.screen_width//20, self.settings.screen_height//20)),
                        ('boost', 'boost.png', (self.settings.screen_width//20, self.settings.screen_height//20)), 
                        ('bigger_bullets', 'bigger.png', (self.settings.screen_width//20, self.settings.screen_height//20)),
                        ('faster_aliens', 'faster_aliens.png', (self.settings.screen_width//20, self.settings.screen_height//20)),
                        ('more_alien_bullets', 'more_alien_bullets.png', (self.settings.screen_width//20, self.settings.screen_height//20))
                    ])
                    new_power_up = power_up_sprites(self, *power_up_effect)
                    new_power_up.rect.center = alien.rect.center # Spawn at alien's location
                    self.power_ups.add(new_power_up)
                
                # Create an explosion at the aliens position
                self.explosions.append(Explosion(alien.rect.centerx, alien.rect.centery, self))

        self.sb.prep_score()
        self.sb.check_high_score()
        
    if not self.aliens and not self.waiting_for_space:
        # Destroy existing bullets
        self.bullets.empty()
        # Set waiting_for_space to True to show end screen
        self.waiting_for_space = True
        # Increase level and update display
        self.stats.level += 1
        self.sb.prep_level()

def _fire_alien_bullet(self):
    '''Randomly select an alien to fire a bullet.'''
    if self.aliens and len(self.alien_bullets) < self.settings.alien_bullets_allowed and self.stats.game_active:
        alien = random.choice(self.aliens.sprites())
        new_bullet = AlienBullet(self, alien)
        self.alien_bullets.add(new_bullet)

def _update_alien_bullets(self):
    '''Update position of alien_bullets and get rid of old bullets'''
    self.alien_bullets.update()

    # Get rid of alien_bullets
    for bullet in self.alien_bullets.copy():
        if bullet.rect.top >= self.settings.screen_height:
            self.alien_bullets.remove(bullet)

    _ship_alien_bullet_collisions(self)

def _ship_alien_bullet_collisions(self):
    '''Check if alien bullets hit the ship'''
    if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
        self._ship_hit()

def _ship_hit(self):
    if self.stats.ships_left > 0:
        self.ship_explosions.append(ShipExplosion(self.ship.rect.centerx, self.ship.rect.centery, self))
        self.ship_exploding = True
        self.explosion_start_time = pygame.time.get_ticks()

        # Decrement ships left, and update scoreboard.
        self.stats.ships_left -= 1
        self.sb.prep_ships()

        # Clear bullets and reset alien positions
        self.bullets.empty()
        self.alien_bullets.empty()

        # Reset remaining aliens to starting positions
        for alien in self.aliens.sprites():
            alien.rect.x = alien.rect.width
            alien.rect.y = alien.rect.height
            alien.x = float(alien.rect.x)

        # Center the ship
        self.ship.center_ship()
    else:
        self.stats.game_active = False
        pygame.mouse.set_visible(True)