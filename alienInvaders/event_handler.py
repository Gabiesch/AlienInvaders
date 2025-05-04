import sys
import pygame    

def _check_events(ai_game):
    '''Respond to keypresses and mouse events.'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if not ai_game.stats.game_active and not ai_game.waiting_for_space:
                # Only check play button when game is not active and not in end screen
                ai_game._check_play_button(mouse_pos)
            elif ai_game.waiting_for_space:
                if not ai_game.end_screen.check_button(mouse_pos):
                    # If no upgrade was purchased, check for space to continue
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]:
                        ai_game.waiting_for_space = False
                        ai_game._create_fleet()
                        ai_game.settings.increase_speed()
                        pygame.mouse.set_visible(False)  # Hide mouse when continuing
        elif event.type == pygame.KEYDOWN:
            _check_keydown_events(ai_game, event)
        elif event.type == pygame.KEYUP:
            _check_keyup_events(ai_game, event) 
        elif event.type == ai_game.alien_shoot_event:
            ai_game._fire_alien_bullet()
            
        # Show mouse during end screen
        if ai_game.waiting_for_space:
            pygame.mouse.set_visible(True)

def _check_keydown_events(ai_game, event):
    '''Respond to keypresses'''
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right
        ai_game.ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move the ship to the left
        ai_game.ship.moving_left = True
    elif event.key == pygame.K_UP:
        # Move the ship up
        ai_game.ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        # Move the ship down
        ai_game.ship.moving_down = True
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_SPACE:
        ai_game._fire_bullet()

def _check_keyup_events(ai_game, event):
        '''Respond to key releases.'''
        if event.key == pygame.K_RIGHT:
            ai_game.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            ai_game.ship.moving_left = False
        elif event.key == pygame.K_UP:
            ai_game.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            ai_game.ship.moving_down = False