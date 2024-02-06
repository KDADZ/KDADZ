import pygame
import sys

pygame.init()

screen_width, screen_height = 1000, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Trivia Trek')

# Load the background image and scale it to fit the screen
background_image = pygame.image.load('assets/img/background.png').convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Load images for portals
portal_image = pygame.image.load('assets/img/portal1.png').convert_alpha()
portal_image = pygame.transform.scale(portal_image, (100, 100))

shop_portal_image = pygame.image.load('assets/img/portal2.png').convert_alpha()
shop_portal_image = pygame.transform.scale(shop_portal_image, (50, 50))

# Load each stick figure image
stick_figure_images = [
    pygame.image.load('assets/img/stickman1.png').convert_alpha(),
    pygame.image.load('assets/img/stickman2.png').convert_alpha(),
    pygame.image.load('assets/img/stickman3.png').convert_alpha(),
    pygame.image.load('assets/img/stickman4.png').convert_alpha(),
]

# Ensure all stick figures are scaled to fit above the portals
for i in range(len(stick_figure_images)):
    stick_figure_images[i] = pygame.transform.scale(stick_figure_images[i], (50, 100))

num_portals = len(stick_figure_images)  # Now you have 4 stick figures and 4 portals

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Font
font = pygame.font.Font(None, 36)

def game_scene():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the background
        screen.blit(background_image, (0, 0))

        portal_size = portal_image.get_size()[0]
        portal_spacing = (screen_width - (num_portals * portal_size)) // (num_portals + 1)
        portal_start_x = portal_spacing
        portal_y = (screen_height - portal_size) // 2

        # Draw portals and stick figures
        for i in range(num_portals):
            portal_x = portal_start_x + i * (portal_size + portal_spacing)
            screen.blit(portal_image, (portal_x, portal_y))

            # Get the current stick figure image
            stick_figure_image = stick_figure_images[i]
            stick_figure_x = portal_x + (portal_size - stick_figure_image.get_size()[0]) // 2
            stick_figure_y = portal_y - stick_figure_image.get_size()[1] - 10  # 10 pixels above the portal

            # Draw the stick figure above the portal
            screen.blit(stick_figure_image, (stick_figure_x, stick_figure_y))

        # Draw shop portal
        shop_portal_x = screen_width - shop_portal_image.get_size()[0] - 20
        shop_portal_y = screen_height - shop_portal_image.get_size()[1] - 20
        screen.blit(shop_portal_image, (shop_portal_x, shop_portal_y))

        # Footer text
        level_difficulty = "Easy/Medium/Hard"
        footer_text = font.render(f"Level Difficulty: {level_difficulty}", True, black)
        screen.blit(footer_text, (10, screen_height - 40))

        pygame.display.flip()

game_scene()
