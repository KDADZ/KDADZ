import pygame
import sys

pygame.init()

screen_width, screen_height = 1000, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Trivia Trek')

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

font = pygame.font.Font(None, 36)

def game_scene():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(white)

        portal_size = 100
        portal_spacing = 100
        portal_start_x = (screen_width - (3 * portal_size + 2 * portal_spacing)) // 2
        portal_y = (screen_height - portal_size) // 2

        for i in range(3):
            pygame.draw.rect(screen, red, (portal_start_x + i * (portal_size + portal_spacing), portal_y, portal_size, portal_size))

        shop_portal_size = 50
        shop_portal_x = screen_width - shop_portal_size - 20
        shop_portal_y =  screen_height - shop_portal_size - 20
        pygame.draw.rect(screen, red, (shop_portal_x, shop_portal_y, shop_portal_size, shop_portal_size))

        level_difficulty = "Easy/Medium/Hard"
        footer_text = font.render(f"Level Difficulty: {level_difficulty}", True, black)
        screen.blit(footer_text, (10, screen_height - 40))

        pygame.display.flip()

game_scene()
