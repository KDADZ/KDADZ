from inventory import Inventory
import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, hp, money, position=(100, 100)):
        super().__init__()
        self.hp = hp
        self.max_hp = hp
        self.money = money
        self.inventory = Inventory()
        self.points = 0
        
        self.image = pygame.image.load("assets\img\Stickman4.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        
        self.base_y = position[1]  # Base Y position for hover effect
        self.hover_amplitude = 5  # How much the sprite moves up and down
        self.hover_frequency = 2  # Speed of the hover effect
        self.t = 0  # Time variable for the hover effect
        self.hover_enabled = False


    def add_money(self, amount):
        self.money += amount
        
    def add_points(self, points):
        self.points += points
        
    def lose_points(self, points):
        points = points / 2
        self.points -= points

    def take_damage(self, damage=1):
        self.hp -= damage
        self.hp = max(self.hp, 0)

    def heal(self, amount=1):
        self.hp += amount
        self.hp = min(self.hp, 5)

    def add_item(self, item, quantity=1):
        self.inventory.add_item(item, quantity)

    def use_item(self, item_name, game):
        self.inventory.use_item(item_name, self, game)

    def user_movement(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.velocity[0] = -5
            elif event.key == pygame.K_RIGHT:
                self.velocity[0] = 5
            if event.key == pygame.K_UP:
                self.velocity[1] = -5
            elif event.key == pygame.K_DOWN:
                self.velocity[1] = 5

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.velocity[0] = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                self.velocity[1] = 0
    
    def update(self, *args):
        
            if self.hover_enabled:
                self.t += 0.05
                self.rect.y = self.base_y + self.hover_amplitude * math.sin(self.hover_frequency * self.t)
            else:
                self.rect.y = self.base_y
                self.t = 0
            
    def toggle_hover(self):
        self.hover_enabled = not self.hover_enabled