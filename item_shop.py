import pygame

class ItemShop:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.SysFont('Arial', 24)
        self.background_img = pygame.image.load('assets/img/shopbackground.jpg').convert_alpha()
        self.items = {
            'Health Potion': {'cost': 500, 'description': 'Restores health', 'rect': pygame.Rect(116, 159, 176, 197)},
            'Magic Sock': {'cost': 1500, 'description': 'Ends the game with a win', 'rect': pygame.Rect(300, 168, 170, 207)},
            'Redo Potion': {'cost': 800, 'description': 'Allows redoing a question', 'rect': pygame.Rect(503, 168, 173, 185)}
        }
        self.notification_msg = ""
        self.notification_time = 0
        self.notification_duration = 3  # seconds

    def draw(self):
        self.screen.blit(self.background_img, (0, 0))
        
        points_surface = self.font.render(f"Points: {self.player.points}", True, (255, 255, 255))
        self.screen.blit(points_surface, (10, 10))

        # Draw notification message if it exists and is within the display time
        current_time = pygame.time.get_ticks() / 1000  # Get current time in seconds
        if self.notification_msg and current_time - self.notification_time < self.notification_duration:
            # Calculate the position for the notification
            notification_x = 10  # For example, 10 pixels from the left
            notification_y = 50  # Change to where you want the notification

            # Render the notification text
            notification_surface = self.font.render(self.notification_msg, True, (255, 255, 255))
            notification_rect = notification_surface.get_rect(x=notification_x, y=notification_y)
        
            # Create a semi-transparent background for the text
            background_surface = pygame.Surface((notification_rect.width, notification_rect.height))
            background_surface.set_alpha(128)  # Semi-transparent
            background_surface.fill((0, 0, 0))  # Black background or any other color
        
            # Blit the background and text to the screen
            self.screen.blit(background_surface, notification_rect.topleft)
            self.screen.blit(notification_surface, notification_rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
            mouse_pos = pygame.mouse.get_pos()
            for item_name, item_details in self.items.items():
                if item_details['rect'].collidepoint(mouse_pos):
                    self.attempt_purchase(item_name)

    def attempt_purchase(self, item_name):
        item = self.items[item_name]
        if self.player.points >= item['cost']:
            self.player.points -= item['cost']  # Deducts the points
            item['cost'] += 100  # Increases item cost by 100 points
            self.player.inventory.add_item(item_name, 1)  # Add the purchased item to the inventory
            self.set_notification(f"Purchased {item_name}.")  # Notify purchase
        else:
            # Now the message includes the item's cost and description
            self.set_notification(f"You need {item['cost']} points for a {item_name}: {item['description']}")


    
    def set_notification(self, message):
        self.notification_msg = message
        self.notification_time = pygame.time.get_ticks() / 1000  # Store the current time in seconds

