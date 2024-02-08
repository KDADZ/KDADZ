import pygame

class ItemShop:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.SysFont('Arial', 24)
        self.background_img = pygame.image.load('assets/img/shopbackground.jpg').convert_alpha()
        self.items = {
            'Health Potion': {'cost': 500, 'description': 'Restores health', 'rect': pygame.Rect(100, 200, 100, 100)},
            'Magic Sock': {'cost': 1500, 'description': 'Ends the game with a win', 'rect': pygame.Rect(300, 200, 100, 100)},
            'Redo Potion': {'cost': 800, 'description': 'Allows redoing a question', 'rect': pygame.Rect(500, 200, 100, 100)}
        }

    def draw(self):
        self.screen.blit(self.background_img, (0, 0))
        
        points_surface = self.font.render(f"Points: {self.player.points}", True, (255, 255, 255))
        self.screen.blit(points_surface, (10, 10))

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
            item['cost'] += 100  # Increases item by 100 points
            print(f"Purchased {item_name}, new cost is {item['cost']} points") 
        else:
            print("Not enough points for this item")

