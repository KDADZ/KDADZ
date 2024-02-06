from inventory import Inventory
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, hp, money):
        super().__init__()
        self.hp = hp
        self.money = money
        self.inventory = Inventory()
        self.points = 0
        
        # self.original_image = pygame.image.load()
        # self.image = self.original_image
        # self.rect = self.image.get_rect()
        # self.rect.topleft = (100, screen_height - self.rect.height)


    def add_money(self, amount):
        self.money += amount
        
    def add_points(self, points):
        self.points += points
        
    def lose_points(self, points):
        points = points / 2
        self.points -= points

    def take_damage(self, damage):
        self.hp -= damage
        self.hp = max(self.hp, 0)

    def heal(self, amount):
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
    
            