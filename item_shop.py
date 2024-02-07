import pygame

class ItemShop:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.SysFont('Arial', 24)
        self.items = {
            'Health Potion': {'cost': 500, 'description': 'Restores health'},
            'Redo Question Card': {'cost': 800, 'description': 'Allows redoing a question'},
            'Magic Sock': {'cost': 1500, 'description': 'Ends the game with a win'}
        }
        self.health_potion_img = pygame.image.load('assets/img/hp.jpg')
        self.redo_card_img = pygame.image.load('assets/img/undo.jpg')
        self.magic_sock_img = pygame.image.load('assets/img/sock.jpg')
        self.shopkeeper_img = pygame.image.load('assets/img/shopkeeper.jpg')
        self.item_positions = {
            'Health Potion': (100, 200),
            'Redo Question Card': (300, 200),
            'Magic Sock': (500, 200)
        }
        self.shopkeeper_pos = (400, 100)

    def draw(self):
        # Draw background and items
        self.screen.fill((0, 0, 0))  # Simple background for now
        self.screen.blit(self.shopkeeper_img, self.shopkeeper_pos)
        self.screen.blit(self.health_potion_img, self.item_positions['Health Potion'])
        self.screen.blit(self.redo_card_img, self.item_positions['Redo Question Card'])
        self.screen.blit(self.magic_sock_img, self.item_positions['Magic Sock'])
        
        # Draw item costs and descriptions
        for item, details in self.items.items():
            pos = self.item_positions[item]
            text_surface = self.font.render(f"{item}: {details['cost']} points", True, (255, 255, 255))
            self.screen.blit(text_surface, (pos[0], pos[1] + 60))  
        
        # Draw player's points
        points_surface = self.font.render(f"Points: {self.player.points}", True, (255, 255, 255))
        self.screen.blit(points_surface, (10, 10))
        
        # TODO: Draw the back arrow

# Inside the ItemShop class in item_shop.py

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
            mouse_pos = pygame.mouse.get_pos()
            for item_name, position in self.item_positions.items():
                item_rect = pygame.Rect(position, (100, 100)) 
                if item_rect.collidepoint(mouse_pos):
                    self.attempt_purchase(item_name)

    def attempt_purchase(self, item_name):
        item = self.items[item_name]
        if self.player.points >= item['cost']:
            self.player.points -= item['cost']  # Deducts the points
            item['cost'] += 100 # Increases item by 100 points
            print(f"Purchased {item_name}, new cost is {item['cost']} points") 
        else:
            print("Not enough points for this item")  

