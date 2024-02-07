import pygame
from item_shop import ItemShop  

class Player:
    def __init__(self, points):
        self.points = points

def run_shop_simulation():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Item Shop Simulation")

    player = Player(1500)  # Example starting points

    shop = ItemShop(screen, player)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                shop.handle_event(event)

        screen.fill((0, 0, 0))

        shop.draw()

        pygame.display.flip()
        pygame.time.Clock().tick(60) 

    pygame.quit()

if __name__ == "__main__":
    run_shop_simulation()
