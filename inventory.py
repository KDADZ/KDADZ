import pygame

class Inventory:
    def __init__(self):
        self.items = {}
        
    def add_item(self, item_name, quantity):
        
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity
            
    def remove_item(self, item_name, quantity=1):
        
        if item_name in self.items and self.items[item_name] >= quantity:
            self.items[item_name] -= quantity
            if self.items[item_name] <= 0:
                del self.items[item_name]
            return True
        return False

    def use_item(self, item_name, player, game):
        if item_name in self.items and self.items[item_name][1] > 0:
            item, quantity = self.items[item_name]
            item.effect(player, game)
            self.items[item_name][1] -= 1
            if self.items[item_name][1] == 0:
                del self.items[item_name]

    def draw(self, screen):
        # You can customize the inventory display here
        font = pygame.font.SysFont('Arial', 24)
        item_x = 50  # Starting x position of the first item
        item_y = 100  # Starting y position of the first item
        item_height = 50  # Height of each item slot

        for item_name, quantity in self.items.items():
            text_surface = font.render(f"{item_name}: {quantity}", True, (255, 255, 255))
            screen.blit(text_surface, (item_x, item_y))
            item_y += item_height  # Move down to draw the next item