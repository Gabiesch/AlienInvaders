import pygame.font

class EndScreen:
    '''A class to show the end game screen.'''
    
    def __init__(self, ai_game):
        '''Initialize end screen attributes.'''
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        # Set the dimensions and properties of the boxes
        self.box_width, self.box_height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 48)
        
        # Create the continue button
        self.continue_button = pygame.Rect(0, 0, self.box_width, self.box_height)
        self.continue_button.center = self.screen_rect.center
        self.continue_button.y -= 200
        
        # Create upgrade boxes
        self.upgrade_boxes = []
        self.upgrade_costs = [100, 150, 200]  # Costs for each upgrade
        self.upgrade_levels = [0, 0, 0]  # Current level of each upgrade
        self.upgrade_names = ["Ship Speed", "More Bullets", "Faster Bullets"]
        
        # Create three boxes for each upgrade (name, level, cost)
        for i in range(3):  # For each upgrade type
            boxes = []
            for j in range(3):  # For each box type (name, level, cost)
                box = pygame.Rect(0, 0, self.box_width, self.box_height)
                box.centerx = self.screen_rect.centerx + (j - 1) * (self.box_width + 10)
                box.y = self.continue_button.bottom + 20 + (i * 80)
                boxes.append(box)
            self.upgrade_boxes.append(boxes)
        
        # Prepare the initial messages
        self._prep_messages()

    def _prep_messages(self):
        '''Prepare the messages to be displayed.'''
        # Continue message
        self.continue_msg_image = self.big_font.render("Press SPACE to continue", True, 
                self.text_color, self.button_color)
        self.continue_msg_rect = self.continue_msg_image.get_rect()
        self.continue_msg_rect.center = self.continue_button.center
        
        # Upgrade messages
        self.upgrade_msg_images = []
        self.upgrade_msg_rects = []
        
        for i in range(3):  # For each upgrade type
            msgs = []
            rects = []
            
            # Name box
            name_msg = self.upgrade_names[i]
            name_image = self.font.render(name_msg, True, self.text_color, self.button_color)
            name_rect = name_image.get_rect()
            name_rect.center = self.upgrade_boxes[i][0].center
            msgs.append(name_image)
            rects.append(name_rect)
            
            # Level box
            level_msg = f"Level {self.upgrade_levels[i]}"
            level_image = self.font.render(level_msg, True, self.text_color, self.button_color)
            level_rect = level_image.get_rect()
            level_rect.center = self.upgrade_boxes[i][1].center
            msgs.append(level_image)
            rects.append(level_rect)
            
            # Cost box
            cost_msg = f"{self.upgrade_costs[i]} points"
            cost_image = self.font.render(cost_msg, True, self.text_color, self.button_color)
            cost_rect = cost_image.get_rect()
            cost_rect.center = self.upgrade_boxes[i][2].center
            msgs.append(cost_image)
            rects.append(cost_rect)
            
            self.upgrade_msg_images.append(msgs)
            self.upgrade_msg_rects.append(rects)
        
        # Points message
        self.points_msg = f"Points: {self.stats.score}"
        self.points_image = self.big_font.render(self.points_msg, True, 
                self.text_color, self.button_color)
        self.points_rect = self.points_image.get_rect()
        self.points_rect.centerx = self.screen_rect.centerx
        self.points_rect.top = 20

    def show_message(self):
        '''Show the end screen with store options.'''
        # Draw the continue button
        self.screen.fill(self.button_color, self.continue_button)
        self.screen.blit(self.continue_msg_image, self.continue_msg_rect)
        
        # Draw the upgrade boxes and messages
        for i in range(3):  # For each upgrade type
            for j in range(3):  # For each box type
                self.screen.fill(self.button_color, self.upgrade_boxes[i][j])
                self.screen.blit(self.upgrade_msg_images[i][j], self.upgrade_msg_rects[i][j])
        
        # Draw points
        self.screen.blit(self.points_image, self.points_rect)

    def check_button(self, mouse_pos):
        '''Check if any upgrade button was clicked.'''
        for i, boxes in enumerate(self.upgrade_boxes):
            if boxes[1].collidepoint(mouse_pos):  # Only the level box is clickable
                self._purchase_upgrade(i)
                return True
        return False

    def _purchase_upgrade(self, upgrade_index):
        '''Purchase an upgrade if the player has enough points.'''
        if self.stats.score >= self.upgrade_costs[upgrade_index]:
            # Deduct points
            self.stats.score -= self.upgrade_costs[upgrade_index]
            
            # Apply upgrade
            if upgrade_index == 0:  # Ship Speed
                self.settings.ship_speed += 0.5
                self.upgrade_levels[0] += 1
            elif upgrade_index == 1:  # More Bullets
                self.settings.bullets_allowed += 1
                self.upgrade_levels[1] += 1
            elif upgrade_index == 2:  # Faster Bullets
                self.settings.bullet_speed += 1.0
                self.upgrade_levels[2] += 1
            
            # Increase cost for next level
            self.upgrade_costs[upgrade_index] = int(self.upgrade_costs[upgrade_index] * 1.5)
            
            # Update messages
            self._prep_messages() 