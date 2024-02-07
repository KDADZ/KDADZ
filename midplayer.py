import pygame

class MidLevel:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.portal_categories = ['a) history', 'b) video games', 'c) sports', 'd) food']
        self.background_image = pygame.transform.scale(pygame.image.load('assets/img/background.png').convert(), (1000, 800))
        self.portal_image = pygame.transform.scale(pygame.image.load('assets/img/portal1.png').convert_alpha(), (100, 100))
        self.shop_portal_image = pygame.transform.scale(pygame.image.load('assets/img/portal2.png').convert_alpha(), (50, 50))
        self.stick_figure_image = pygame.transform.scale(pygame.image.load('assets/img/cropstickman.png').convert_alpha(), (50, 100))
        self.stickman_position = (self.screen.get_width() - self.stick_figure_image.get_width()) // 2
        self.stickman_speed = 1
        self.fast_speed = 1
        self.is_left_held = False
        self.is_right_held = False
        self.font = pygame.font.Font(None, 36)

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

    def update(self):
        # Adjust speed of stickman based on key holds
        current_speed = self.fast_speed if (self.is_left_held or self.is_right_held) else self.stickman_speed
        if self.is_left_held:
            self.stickman_position = max(0, self.stickman_position - current_speed)  # Prevent going off-screen
        elif self.is_right_held:
            self.stickman_position = min(self.screen.get_width() - self.stick_figure_image.get_width(), self.stickman_position + current_speed)  # Prevent going off-screen

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        num_portals = len(self.portal_categories)
        portal_size = self.portal_image.get_size()[0]
        portal_spacing = (self.screen.get_width() - (num_portals * portal_size)) // (num_portals + 1)
        portal_start_x = portal_spacing

        # Draw portals and stick figure
        for i in range(num_portals):
            portal_x = portal_start_x + i * (portal_size + portal_spacing)
            portal_y = (self.screen.get_height() - portal_size) // 2
            self.screen.blit(self.portal_image, (portal_x, portal_y))

            # Check for collisions (optional logic here)

            # Draw category text below each portal
            category_text = self.font.render(self.portal_categories[i], True, (255, 255, 255))
            category_x = portal_x + (portal_size - category_text.get_width()) // 2
            category_y = portal_y + portal_size + 5
            self.screen.blit(category_text, (category_x, category_y))

        # Draw the stick figure
        stick_figure_y = portal_y - self.stick_figure_image.get_height() - 10
        self.screen.blit(self.stick_figure_image, (self.stickman_position, stick_figure_y))

        # Draw shop portal and footer text
        # (shop portal and footer text drawing code here)

    # Additional methods for check_collisions, etc., can be added here
