import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
import random
from explosion import Explosion
from ship_explosion import ShipExplosion
from particles import Particle
from alien_bullet import AlienBullet
from event_handler import _check_events
from bullet_actions import _fire_alien_bullet, _fire_bullet, _update_alien_bullets, _update_bullets
from create_file import create_fleet
from power_ups import PowerUp
from end_screen import EndScreen
import math
import os

class AlienInvasion:
    '''Overall class to manage game assets and behavior.'''

    def __init__(self):  
        '''Initialize the game, and create game resources.'''
        pygame.init()   
        self.settings = Settings()

        # Get the directory where the executable is located
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle (exe)
            self.base_path = os.path.dirname(os.path.dirname(sys.executable))
        else:
            # If the application is run as a script
            self.base_path = os.path.dirname(os.path.abspath(__file__))

        # Set the images directory path
        self.images_path = os.path.join(self.base_path, 'images')

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
        # Create an instance to store game statistics,
        #   and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.end_screen = EndScreen(self)  # Create end screen
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()  # Initialize power-ups group
        self.active_power_ups = {}  # Dictionary to track active power-ups and their timers
        self.explosions = []
        self.ship_explosions = []
        self.ship_exploding = False
        self.explosion_start_time = None
        self.waiting_for_space = False  # New state for waiting for spacebar
        
        # Rocket tracking
        self.rocket_active = False
        self.active_rocket = None

        self.alien_shoot_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.alien_shoot_event, 1000)

        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, 'Play')

        # Set background color.
        self.bg_color = (230, 230, 230)

    def run_game(self):
        '''Start the mail loop for the game.'''
        while True:
            self._check_events()

            if self.stats.game_active:
                if self.ship_exploding:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.explosion_start_time >= 1500: # 5 second explosion
                        self.ship_exploding = False
                        self.ship.center_ship()
                else:
                    self.ship.update()
                    _update_bullets(self)
                    _update_alien_bullets(self)
                    self._update_aliens()
                    self.power_ups.update()
                    self._check_power_up_collision()
                    self._check_power_up_timers()  # Check for expired power-ups
                    self._check_rocket_collision()  # Check for rocket collisions

            self._update_screen()

    def _check_events(self):
        _check_events(self)  

    def _fire_bullet(self):
        _fire_bullet(self)

    def _fire_alien_bullet(self):
        _fire_alien_bullet(self)

    def _update_screen(self):
        '''Update images on the screen, and flip to the new screen'''
        self.screen.fill(self.settings.bg_color)
       
        if not self.ship_exploding:
            self.ship.blitme()
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for bullet in self.alien_bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Update and draw explosions
        for explosion in self.explosions:
            explosion.update()
            explosion.draw(self.screen)

        for shipexplosion in self.ship_explosions:
            shipexplosion.update()
            shipexplosion.draw(self.screen)

        # Draw the power-ups
        for power_up in self.power_ups.sprites():
            power_up.draw(self.screen)

        # Remove finished explosions
        self.explosions = [e for e in self.explosions if not e.is_finished()]
        self.ship_explosions = [e for e in self.ship_explosions if not e.is_finished()]

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        # Show end screen if all aliens are destroyed and game is still active
        elif self.waiting_for_space:
            self.end_screen.show_message()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.waiting_for_space = False
                self._create_fleet()
                self.settings.increase_speed()

        # Draw the starry background:
        for star in self.settings.stars:
            x, y, brightness = star
            brightness += random.randint(-15, 15)
            brightness = max(0, min(brightness, 255))
            star[2] = brightness
            pygame.draw.circle(self.screen, (brightness, brightness, brightness), (x, y), 1)
        
        pygame.display.flip()

    def _create_fleet(self):
        create_fleet(self)


    def _update_aliens(self):
        '''
        Check if the fleet is at an edge,
            then update the positions of all aliens in the fleet.
        '''
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

        # check for destroyed aliens
        for alien in self.aliens.copy():
            if not alien:
                self.aliens.remove(alien)

    def _check_fleet_edges(self):
        '''Respond appropriately if any aliens have reached an edge.'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        '''Drop the entire fleet and change the fleet's direction.'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self): #BY Alien
        '''Respond to the ship being hit by an alien.'''
        if self.stats.ships_left > 0:
            self.ship_explosions.append(ShipExplosion(self.ship.rect.centerx, self.ship.rect.centery, self))
            self.ship_exploding = True
            self.explosion_start_time = pygame.time.get_ticks()
            
            # Decrement ships left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Clear bullets
            self.bullets.empty()
            self.alien_bullets.empty()

            # Store the positions of remaining aliens
            alien_positions = [(alien.rect.x, alien.rect.y) for alien in self.aliens.sprites()]
            # Clear and recreate fleet
            self.aliens.empty()
            self._create_fleet()
            # Remove excess aliens and position remaining ones
            new_aliens = self.aliens.sprites()
            for i, pos in enumerate(alien_positions):
                if i < len(new_aliens):
                    new_aliens[i].rect.x = pos[0]
                    new_aliens[i].rect.y = pos[1]
                    new_aliens[i].x = float(new_aliens[i].rect.x)
            # Remove any excess aliens
            while len(self.aliens) > len(alien_positions):
                self.aliens.sprites()[-1].kill()

            # Center the ship
            self.ship.center_ship()

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_power_up_collision(self):
        '''Check if the ship collects a power-up.'''
        collisions = pygame.sprite.spritecollide(self.ship, self.power_ups, True)
        for power_up in collisions:
            current_time = pygame.time.get_ticks()
            
            if power_up.effect == 'rocket':
                # Create a rocket that moves up and explodes on contact
                self._fire_rocket()
            elif power_up.effect == 'boost':
                self.settings.ship_speed += 2
                self.active_power_ups['boost'] = current_time + 5000  # 5 seconds
            elif power_up.effect == 'bigger_bullets':
                self.settings.bullet_width += 5
                self.active_power_ups['bigger_bullets'] = current_time + 5000  # 5 seconds
            elif power_up.effect == 'faster_aliens':
                self.settings.alien_speed *= 1.2
                self.active_power_ups['faster_aliens'] = current_time + 5000  # 5 seconds
            elif power_up.effect == 'more_alien_bullets':
                self.settings.alien_bullets_allowed += 1
                self.active_power_ups['more_alien_bullets'] = current_time + 5000  # 5 seconds

    def _check_power_up_timers(self):
        '''Check and remove expired power-up effects.'''
        current_time = pygame.time.get_ticks()
        expired_effects = []
        
        for effect, end_time in self.active_power_ups.items():
            if current_time >= end_time:
                expired_effects.append(effect)
                
        for effect in expired_effects:
            if effect == 'boost':
                self.settings.ship_speed -= 2
            elif effect == 'bigger_bullets':
                self.settings.bullet_width -= 5
            elif effect == 'faster_aliens':
                self.settings.alien_speed /= 1.2
            elif effect == 'more_alien_bullets':
                self.settings.alien_bullets_allowed -= 1
            del self.active_power_ups[effect]

    def _fire_rocket(self):
        '''Create a rocket that moves up and explodes on contact with aliens.'''
        rocket = Bullet(self)
        rocket.rect.width = 20  # Make rocket wider
        rocket.rect.height = 30  # Make rocket taller
        rocket.color = (255, 165, 0)  # Orange color for rocket
        self.bullets.add(rocket)
        print("Rocket created and added to bullets group")  # Debug print
        
        # Wait for collision in the update loop
        self.rocket_active = True
        self.active_rocket = rocket

    def _check_rocket_collision(self):
        '''Check for rocket collision with aliens.'''
        if self.rocket_active and self.active_rocket:
            collisions = pygame.sprite.spritecollide(self.active_rocket, self.aliens, True)
            if collisions:
                print("Rocket collision detected!")  # Debug print
                alien = collisions[0]  # Get the first alien hit
                print(f"Alien hit at position: {alien.rect.centerx}, {alien.rect.centery}")  # Debug print
                
                # Create explosion effect
                self.explosions.append(Explosion(alien.rect.centerx, alien.rect.centery, self))
                
                # Create 5 bullets that spread out in different directions
                angles = [0, 72, 144, 216, 288]  # 5 directions at 72-degree intervals
                for angle in angles:
                    # Convert angle to radians
                    angle_rad = angle * (3.14159 / 180)
                    # Create a new bullet
                    explosion_bullet = Bullet(self)
                    # Set position at alien's center
                    explosion_bullet.rect.centerx = alien.rect.centerx
                    explosion_bullet.rect.centery = alien.rect.centery
                    explosion_bullet.color = (255, 165, 0)  # Orange color
                    # Set initial position
                    explosion_bullet.x = float(explosion_bullet.rect.x)
                    explosion_bullet.y = float(explosion_bullet.rect.y)
                    # Set velocity based on angle
                    explosion_bullet.speed_x = self.settings.bullet_speed * 2 * math.cos(angle_rad)
                    explosion_bullet.speed_y = self.settings.bullet_speed * 2 * math.sin(angle_rad)
                    # Add to bullets group
                    self.bullets.add(explosion_bullet)
                    print(f"Created explosion bullet at angle {angle}")  # Debug print
                
                self.stats.score += self.settings.alien_points
                self.sb.prep_score()
                self.sb.check_high_score()
                
                # Remove the rocket and reset the active rocket
                self.active_rocket.kill()
                self.rocket_active = False
                self.active_rocket = None

    def _check_aliens_bottom(self):
        '''Check if any aliens have reached the bottom of the screen.'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit
                self._ship_hit()
            break

    def _check_play_button(self, mouse_pos):
        '''Start a new game when the player clicks Play.'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.aliens.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

 
if __name__ == '__main__': 
        # Make a game instance, and run the game.
        ai = AlienInvasion() 
        ai.run_game()
