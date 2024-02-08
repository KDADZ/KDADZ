import pygame

class MidLevel:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.portal_category_mapping = {
            0: 'history',
            1: 'video games',
            2: 'sports',
            3: 'food',
        }
        self.background_image = pygame.transform.scale(pygame.image.load('assets/img/background.png').convert(), (1000, 800))
        self.portal_image = pygame.transform.scale(pygame.image.load('assets\img\portalcrop.png').convert_alpha(), (150, 150))
        self.portal_rotation_angle = 0  # New attribute for rotation animation
        self.portal_rect = self.portal_image.get_rect(center=(400, 300))
        self.shop_portal_image = pygame.transform.scale(pygame.image.load('assets/img/portal2.png').convert_alpha(), (50, 50))
        self.stick_figure_image = pygame.transform.scale(pygame.image.load('assets/img/cropstickman.png').convert_alpha(), (50, 100))
        self.stickman_position = (self.screen.get_width() - self.stick_figure_image.get_width()) // 2
        self.stickman_speed = 2
        self.fast_speed = 4
        self.is_left_held = False
        self.is_right_held = False
        self.font = pygame.font.Font(None, 36)
        self.portal_size = 100  # Set the portal size (adjust as needed)
        self.portal_spacing = 20  # Set the portal spacing (adjust as needed)
        self.portal_start_x = self.portal_spacing  # Initialize portal start x position
        self.current_category_index = 0  # Initialize the category index


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.is_left_held = True
                elif event.key == pygame.K_RIGHT:
                    self.is_right_held = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.is_left_held = False
                elif event.key == pygame.K_RIGHT:
                    self.is_right_held = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                
                # Calculate the single portal rectangle
                portal_size = self.portal_image.get_size()[0]
                portal_spacing = (self.screen.get_width() - portal_size) // 2
                portal_rect = pygame.Rect(portal_spacing, (self.screen.get_height() - portal_size) // 2, portal_size, portal_size)

                if portal_rect.collidepoint(mouse_x, mouse_y):
                    # Rotate to the next category
                    self.rotate_category()
                    selected_category = self.portal_category_mapping[self.current_category_index]
                    print(f"Selected category: {selected_category}")
                    self.game.trivia_room(selected_category)
                    return


    def rotate_category(self):
        # Increment the category index, and loop back to the beginning if it exceeds the number of categories
        self.current_category_index = (self.current_category_index + 1) % len(self.portal_category_mapping)  
        
    
    def update(self):
        # Adjust speed of stickman based on key holds
        current_speed = self.fast_speed if (self.is_left_held or self.is_right_held) else self.stickman_speed
        if self.is_left_held:
            self.stickman_position = max(0, self.stickman_position - current_speed)  # Prevent going off-screen
        elif self.is_right_held:
            self.stickman_position = min(self.screen.get_width() - self.stick_figure_image.get_width(), self.stickman_position + current_speed)  # Prevent going off-screen

        # Update the rotation angle for animation
        self.portal_rotation_angle = (self.portal_rotation_angle + 2) % 360  # Adjust the rotation speed as needed


    def draw(self):
        self.screen.blit(self.background_image, (0, 0))

        # Draw the single portal with rotation
        rotated_portal = pygame.transform.rotate(self.portal_image, self.portal_rotation_angle)
        portal_size = rotated_portal.get_size()[0]
        portal_spacing = (self.screen.get_width() - portal_size) // 2
        portal_x = portal_spacing
        portal_y = (self.screen.get_height() - portal_size) // 2
        portal_rect = rotated_portal.get_rect(center=(portal_x + portal_size // 2, portal_y + portal_size // 2))
        self.screen.blit(rotated_portal, portal_rect.topleft)

        # Check for collisions (optional logic here)

        # Draw category text below the portal
        category_text = self.font.render("Enter Portal Here", True, (255, 255, 255))
        category_x = portal_x + (portal_size - category_text.get_width()) // 2
        category_y = portal_y + portal_size + 5
        self.screen.blit(category_text, (category_x, category_y))

        # Draw the stick figure
        stick_figure_y = portal_y - self.stick_figure_image.get_height() - 10
        self.screen.blit(self.stick_figure_image, (self.stickman_position, stick_figure_y))
        # self.screen.blit(self.portal_image, self.portal_rect.topleft)

